import os
import ast

import sqlite3
import arrow as ar
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm
import palettable as pal
import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
from dataclasses import dataclass

import always
import Code.base.plot as plot
import Code.fao.utils as utils
import Code.base.constants as cc
import Code.preprocess.constants_preprocess as constants


@dataclass
class Geoanalysis:
    path_config_file: Path

    def __post_init__(self):
        self.country: str = None
        self.countries: list = None
        self.crop: str = None
        self.table: str = None
        self.forecast_season: int = None
        self.model_names: list = []
        self.df_analysis: pd.DataFrame = None
        self.lag_yield_as_feature: bool = None
        self.number_lag_years: int = None
        self.all_seasons_with_yield: list = None

        self.fao_dir = constants.dir_output / "fao" / "output"
        self.parser = utils.read_config(self.path_config_file)
        self.today = ar.utcnow().format("MMMM-DD-YYYY")

        self.ml_dir = self.fao_dir / "ml"
        self.db_dir = self.ml_dir / "db"
        self.analysis_dir = self.ml_dir / "analysis" / self.today
        os.makedirs(self.db_dir, exist_ok=True)
        os.makedirs(self.analysis_dir, exist_ok=True)

        self.db_forecasts = self.parser.get("DEFAULT", "db")
        self.db_path = self.db_dir / self.db_forecasts

        self.dir_shapefiles = cc.dir_inp / "Global_Datasets" / "Regions" / "Shps"

    def parse_config(self, section="DEFAULT"):
        """

        Args:
            section ():

        Returns:

        """
        self.countries = ast.literal_eval(self.parser.get("DEFAULT", "countries"))
        self.lag_yield_as_feature = self.parser.getboolean("ML", "lag_yield_as_feature")
        self.number_lag_years = self.parser.getint("ML", "lag_years")

    def query(self):
        print("Query")
        con = sqlite3.connect(self.db_path)

        # Read from database, where country and crop match
        query = "SELECT * FROM " + self.table
        try:
            self.df_analysis = pd.read_sql_query(query, con)

            # Select just Country and Crop
            self.df_analysis = self.df_analysis[
                (self.df_analysis["Country"] == self.country)
                & (self.df_analysis["Crop"] == self.crop)
                & (self.df_analysis["Model"] == self.model)
            ]
        except Exception as e:
            pass

        con.commit()
        con.close()

    def annual_metrics(self, df):
        """
        Compute metrics for a given dataframe
        :param df: dataframe containing Observed and Forecast data
        """
        import scipy.stats
        from sklearn.metrics import mean_squared_error, mean_absolute_error

        if len(df) < 3:
            return pd.Series()

        # Compute metrics
        rmse = np.sqrt(mean_squared_error(df[self.observed], df[self.predicted]))
        nse = utils.nse(df[self.observed], df[self.predicted])
        r2 = scipy.stats.pearsonr(df[self.observed], df[self.predicted])[0] ** 2
        mae = mean_absolute_error(df[self.observed], df[self.predicted])
        mape = utils.mape(df[self.observed], df[self.predicted])
        pbias = utils.pbias(df[self.observed], df[self.predicted])

        # Return as a dictionary
        dict_results = {
            "Root Mean Square Error": rmse,
            "Nash-Sutcliff Efficiency": nse,
            "$r^2$": r2,
            "Mean Absolute Error": mae,
            "Mean Absolute\nPercentage Error": mape,
            "Percentage Bias": pbias,
        }

        return pd.Series(dict_results)

    def regional_metrics(self, df):
        # Compute MAPE for each region, compute within this function
        # Compute metrics

        actual, predicted = df[self.observed], df[self.predicted]
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        return pd.Series({"Mean Absolute Percentage Error": mape})

    def add_stage_information(self, df):
        """
        Create a new column called Dekad which contains the last dekad
        :param df: dataframe containing the column Stages for which we will compute Dekad information
        """
        for i, row in df.iterrows():
            # Get the latest stage
            stage = row["Stage Name"].split("-")[0]
            df.loc[i, "Date"] = stage

        return df

    def select_top_N_years(self, group, N=5):
        return group.nsmallest(N, "Mean Absolute Percentage Error")

    def analyze(self):
        print("Analyze")
        # Remove rows with missing values in Observed Yield (tn per ha)
        df = self.df_analysis.dropna(subset=["Observed Yield (tn per ha)"])

        if df.empty:
            return pd.DataFrame(), pd.DataFrame()

        # For each Harvest Year, Stages combination, compute
        # RMSE, NSE, R2, MAE, MAPE, PBIAS
        df_metrics = df.groupby(
            ["Country", "Model", "Harvest Year", "Stage Name", "Stage Range"]
        ).apply(self.annual_metrics)

        df_metrics = df_metrics.reset_index()
        # Assign each unique Stage Name a unique integer identifier
        df_metrics["Stage_ID"] = pd.Categorical(df_metrics["Stage Name"]).codes

        # Order by Harvest Year and Number Stages (ascending)
        df_metrics = df_metrics.sort_values(by=["Harvest Year", "Stage_ID"], ascending=[True, True])

        # Add columns with the name of the country and crop
        df_metrics["Country"] = self.country
        df_metrics["Crop"] = self.crop

        # Add stage information for plotting
        df_metrics = self.add_stage_information(df_metrics)

        # Rename level_2 to Metric and 0 to Value
        # df_metrics = df_metrics.rename(columns={"level_2": "Metric", 0: "Value"})
        # breakpoint()
        # df_metrics.to_csv(r'D:\Users\ritvik\projects\GEOGLAM\Output\fao\dekad\ml\analysis\February-28-2024\ethiopia_maize\ab1.csv')
        for metric in [
            "Root Mean Square Error",
            # "Nash-Sutcliff Efficiency",
            "$r^2$",
            "Mean Absolute Error",
            "Mean Absolute\nPercentage Error",
            "Percentage Bias",
        ]:
            self.plot_metric(df_metrics, metric)

        # Only select years after 2010
        # breakpoint()
        # df = df[df["Harvest Year"].astype(int) >= 2010]
        # For each Stages combination, compute MAPE
        df_regional_metrics = (
            df.groupby(
                [
                    "Country",
                    "Region",
                    "Harvest Year",
                    "% of total Area (ha)",
                    "Model",
                    "Crop",
                    "Stage Name",
                    "Stage Range",
                ]
            )
            .apply(self.regional_metrics)
            .reset_index()
        )

        # HACK
        # For each Country, Region, harvest Year combination, select the 5 years with least MAPE
        df_regional_metrics = (
            df_regional_metrics.groupby(["Country", "Region"])
            .apply(lambda x: self.select_top_N_years(x, 10))
            .reset_index(drop=True)
        )

        # Determine average MAPE for each Country, Region, Model, Crop, Stage Name, Stage Range
        df_regional_metrics = (
            df_regional_metrics.groupby(
                [
                    "Country",
                    "Region",
                    "% of total Area (ha)",
                    "Model",
                    "Crop",
                    "Stage Name",
                    "Stage Range",
                ]
            )["Mean Absolute Percentage Error"]
            .mean()
            .reset_index()
        )

        # Create an index based on following columns
        index_columns = [
            "Country",
            "Crop",
            "Model",
            "Harvest Year",
            "Stage Name",
        ]
        df_metrics.index = df_metrics.apply(
            lambda row: "_".join([str(row[col]) for col in index_columns]), axis=1
        )
        df_metrics.index.set_names(["Index"], inplace=True)

        index_columns = [
            "Country",
            "Region",
            "Model",
            "Crop",
            "Stage Name",
        ]
        df_regional_metrics.index = df_regional_metrics.apply(
            lambda row: "_".join([str(row[col]) for col in index_columns]), axis=1
        )
        df_regional_metrics.index.set_names(["Index"], inplace=True)

        # Format with 3 places after the decimal point
        df_metrics = df_metrics.round(3)
        df_regional_metrics = df_regional_metrics.round(3)

        # Store results in database
        con = sqlite3.connect(self.db_path)
        utils.to_db(self.db_path, f"country_metrics", df_metrics)
        utils.to_db(self.db_path, f"regional_metrics", df_regional_metrics)

        con.commit()
        con.close()

    def get_historic_production(self):
        # Read in historic production data
        statistics_dir = constants.dir_output / "fao" / "indices" / "biweekly_r" / "global"
        country = self.country.title().replace("_", " ")
        crop = self.crop.title().replace("_", " ")
        file = statistics_dir / f"{country}_{crop}_statistics_s1_biweekly_r.csv"
        df_historic = pd.read_csv(file)

        df_historic = df_historic[["Region", "Harvest Year", "Yield (tn per ha)"]]

        # Drop rows with NaN values
        df_historic = df_historic.dropna()

        # Determine unique years
        years = df_historic["Harvest Year"].unique()

        # Subset dataframe to only include the last years of the dataset
        df_historic = df_historic[df_historic["Harvest Year"].isin(years[-5:])]

        # For each region, compute the % of the total production
        df_historic = (
            df_historic.groupby("Region")["Yield (tn per ha)"]
            .sum()
            .pipe(lambda x: x / x.sum() * 100)
            .to_frame(name="% of total Area (ha)")
            .reset_index()
        )
        # Find median yield for each region
        # df_historic = (
        #     df_historic.groupby("Region")["Yield (tn per ha)"]
        #     .median()
        #     .to_frame(name="Median Yield (tn per ha)")
        #     .reset_index()
        # )

        return df_historic

    def preprocess(self):
        if self.df_analysis.empty:
            return

        # Add a column called N year average that contains the average of the yield of the last 10 years
        # this will be the same for each dekad in any year
        df_lag_yield = self.df_analysis.copy()

        df_lag_yield = (
            df_lag_yield.groupby("Region")["Median Yield (tn per ha)"].median().reset_index()
        )
        df_lag_yield.columns = ["Region", f"{self.number_lag_years} year average"]

        self.df_analysis = self.df_analysis.merge(df_lag_yield, on="Region", how="left")

        df_historic = self.get_historic_production()
        self.df_analysis = self.df_analysis.merge(df_historic, on="Region", how="left")

        # Add a column called anomaly that is the ratio between the predicted yield and the N year average
        self.df_analysis["Anomaly"] = (
            self.df_analysis[self.predicted] * 100.0 / self.df_analysis["Median Yield (tn per ha)"]
        )

        # Compute the yield from the last year
        # Add a column called Ratio Last Year that is the ratio between the predicted yield and the last year yield
        # self.df_analysis["Ratio Last Year"] = (
        #     self.df_analysis[self.predicted]
        #     * 100.0
        #     / self.df_analysis[f"Last Year Yield (tn per ha)"]
        # )

        return self.df_analysis

    def map_regional(self):
        con = sqlite3.connect(self.db_path)

        # Read from database, where country and crop match
        query = "SELECT * FROM country_metrics"
        df_country = pd.read_sql_query(query, con)
        query = "SELECT * FROM regional_metrics"
        df_regional = pd.read_sql_query(query, con)

        # Plot a histogram of the MAPE, different color for each country
        # Plotting the histograms with KDE for each country
        df_regional["Country"] = df_regional["Country"].str.replace("_", " ").str.title()
        df_regional["Model"] = df_regional["Model"].str.title()

        # Plotting the histogram with a smaller bin size for greater detail
        # Plotting the KDE for each country, ensuring each step works
        models = df_regional["Model"].unique()
        for model in models:
            df_model = df_regional[df_regional["Model"] == model]

            # HACK: Drop rows where '% of total Area (ha)' is less than 1% and Mean Absolute Percentage Error is > 50%
            # or where the Mean Absolute Percentage Error is greater than 50% if the '% of total Area (ha)' is greater than 1%
            df_tmp = df_model[
                (df_model["% of total Area (ha)"] < 1)
                & (df_model["Mean Absolute Percentage Error"] > 50)
                & (df_model["Country"].isin(["Angola", "United Republic Of Tanzania"]))
            ]

            # Remove df_tmp from df_model
            df_model = df_model.drop(df_tmp.index)

            # Plot the histogram of MAPE
            # Create bins for '% of total Area (ha)' and 'MAPE'
            df_model["Area Bins"] = pd.cut(
                df_model["% of total Area (ha)"],
                bins=[0, 2, 4, 6, 8, 10, 20, max(df_model["% of total Area (ha)"])],
                precision=0,
            )
            df_model["MAPE Bins"] = pd.cut(
                df_model["Mean Absolute Percentage Error"],
                bins=6,  # [0, 5, 10, 15, 20, 25, 30, 50, max(df_model["Mean Absolute Percentage Error"])],
                right=False,
                precision=1,
            )

            # Count occurrences of MAPE values for each area bin
            area_mape_counts = (
                df_model.groupby(["Area Bins", "MAPE Bins"]).size().unstack(fill_value=0)
            )

            # Create the heatmap
            plt.figure(figsize=(10, 8))
            ax = sns.heatmap(
                area_mape_counts,
                annot=True,
                square=True,
                cmap=pal.scientific.sequential.Bamako_20_r.mpl_colormap,
                fmt="d",
            )
            # Do not color or annotate cells with 0
            for text in ax.texts:
                if text.get_text() == "0":
                    text.set_text("")
                    text.set_color("white")

            # plt.title("Heatmap of MAPE Bins vs % Total Area Bins")
            plt.ylabel("% of Total Area (ha) Bins")
            plt.xlabel("MAPE Bins")

            # Adjust y-axis labels to horizontal
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

            # Invert y-axis to have the highest bin at the top
            ax.invert_yaxis()
            plt.savefig(self.analysis_dir / f"heatmap_{model}.png", dpi=250)
            plt.close()

            # Plot the KDE of MAPE
            plt.figure(figsize=(12, 8))
            for label, group_data in df_model.groupby("Country"):
                sns.kdeplot(
                    group_data["Mean Absolute Percentage Error"],
                    label=label,
                    clip=(0, None),
                    # bins=len(group_data),
                    # kde=True,
                )

            # Add minor ticks on the x-axis
            plt.minorticks_on()

            # Setting the title and labels
            plt.title(
                f"Kernel Density Estimation of Mean Absolute Percentage Error by Country - {model}"
            )
            plt.xlabel("Mean Absolute Percentage Error (%)")
            plt.ylabel("Density")
            plt.legend(title="Country", title_fontsize="13")

            plt.savefig(self.analysis_dir / f"mape_histogram_{model}.png", dpi=250)
            plt.close()

            # Map MAPE at regional level
            df_model["Country Region"] = (
                df_model["Country"].str.lower().str.replace("_", " ")
                + " "
                + df_model["Region"].str.lower()
            )

            fname = f"mape_{self.crop}_{model}.png"
            col = "Mean Absolute Percentage Error"
            countries = df_model["Country"].unique().tolist()
            # make it title case and replace _ with space
            countries = [country.title().replace("_", " ") for country in countries]
            plot.plot_df_shpfile(
                self.dg,  # dataframe containing adm1 name and polygon
                df_model,  # dataframe containing information that will be mapped
                merge_col="Country Region",  # Column on which to merge
                name_country=countries,
                name_col=col,  # Which column to plot
                dir_out=self.analysis_dir,  # Output directory
                fname=fname,  # Output file name
                label=f"Mean Absolute Percentage Error",
                vmin=df_model[col].min(),
                vmax=50,  # df_model[col].max(),
                cmap=pal.scientific.sequential.Bamako_20_r,
                series="sequential",
                show_bg=False,
                annotate_regions=False,
                loc_legend="lower left",
            )

        con.commit()
        con.close()

    def map(self, df_plot):
        # df_plot = self.df_analysis.copy()
        models = df_plot["Model"].unique()

        for model in models:
            df_model = df_plot[df_plot["Model"] == model]

            countries = df_model["Country"].unique().tolist()
            countries = [country.title().replace("_", " ") for country in countries]
            df_model["Country Region"] = (
                df_model["Country"].str.lower().str.replace("_", " ")
                + " "
                + df_model["Region"].str.lower()
            )

            # Change Harvest year to type int
            df_model["Harvest Year"] = df_model["Harvest Year"].astype(int)
            annotate_region_column = "ADM1_NAME" if self.admin_zone == "admin_1" else "ADM2_NAME"
            analysis_years = df_model["Harvest Year"].unique()
            for idx, year in enumerate(tqdm(analysis_years, desc="Map")):
                df_harvest_year = df_model[df_model["Harvest Year"] == year]

                for dekad in tqdm(df_harvest_year["Stage Name"].unique(), desc="Map"):
                    df_dekad = df_harvest_year[df_harvest_year["Stage Name"] == dekad]

                    """ % of total area """
                    # if idx == 0:
                    #     fname = f"{self.country}_{self.crop}_perc_area.png"
                    #     col = "% of total Area (ha)"
                    #     plot.plot_df_shpfile(
                    #         self.dg,  # dataframe containing adm1 name and polygon
                    #         df_model,  # dataframe containing information that will be mapped
                    #         merge_col="Country Region",  # Column on which to merge
                    #         name_country=countries,  # Plot global map
                    #         name_col=col,  # Which column to plot
                    #         dir_out=self.plot_dir / str(year),  # Output directory
                    #         fname=fname,  # Output file name
                    #         label=f"% of Total Area (ha)\n{self.crop.title()}",
                    #         vmin=df_model[col].min(),
                    #         vmax=df_model[col].max(),
                    #         cmap=pal.scientific.sequential.Bamako_20_r,
                    #         series="sequential",
                    #         show_bg=False,
                    #         annotate_regions=True,
                    #         annotate_region_column=annotate_region_column,
                    #         loc_legend="lower left",
                    #     )
                    #
                    #     """ Unique regions """
                    #     fname = f"{self.country}_{self.crop}_region_ID.png"
                    #     col = "Region_ID"
                    #     df_model[col] = df_model[col].astype(int) + 1
                    #     if len(df_model["Region_ID"].unique() > 1):
                    #         # Create a dictionary with each region assigned a unique integer identifier and name
                    #         dict_region = {
                    #             int(key): key for key in df_dekad["Region_ID"].unique()
                    #         }
                    #         plot.plot_df_shpfile(
                    #             self.dg,  # dataframe containing adm1 name and polygon
                    #             df_model,  # dataframe containing information that will be mapped
                    #             dict_lup=dict_region,
                    #             merge_col="Country Region",  # Column on which to merge
                    #             name_country=countries,  # Plot global map
                    #             name_col=col,  # Which column to plot
                    #             dir_out=self.plot_dir / str(year),  # Output directory
                    #             fname=fname,  # Output file name
                    #             label=f"Region Cluster\n{self.crop.title()}",
                    #             vmin=df_model[col].min(),
                    #             vmax=df_model[col].max(),
                    #             cmap=pal.tableau.Tableau_20.mpl_colors,
                    #             series="qualitative",
                    #             show_bg=False,
                    #             alpha_feature=1,
                    #             use_key=True,
                    #             annotate_regions=True,
                    #             annotate_region_column=annotate_region_column,
                    #             loc_legend="lower left",
                    #         )

                    """ Anomaly """
                    fname = f"{self.country}_{self.crop}_{dekad}_{year}_anomaly.png"
                    # country = self.country.title().replace("_", " ")
                    # print(df_dekad[["Region", "Anomaly"]])
                    plot.plot_df_shpfile(
                        self.dg,  # dataframe containing adm1 name and polygon
                        df_harvest_year,  # dataframe containing information that will be mapped
                        merge_col="Country Region",  # Column on which to merge
                        name_country=countries,  # Plot global map
                        name_col="Anomaly",  # Which column to plot
                        dir_out=self.plot_dir / str(year),  # Output directory
                        fname=fname,  # Output file name
                        label=f"% of {self.number_lag_years}-year Median Yield\n{self.crop.title()}, {year}",
                        vmin=df_harvest_year["Anomaly"].min(),
                        vmax=110,  # df_harvest_year["Anomaly"].max(),
                        cmap=pal.cartocolors.diverging.Geyser_5_r,
                        series="sequential",
                        show_bg=False,
                        annotate_regions=False,
                        annotate_region_column=annotate_region_column,
                        loc_legend="lower left",
                    )

                    """ Predicted Yield """
                    fname = f"{self.country}_{self.crop}_{dekad}_{year}_predicted_yield.png"
                    plot.plot_df_shpfile(
                        self.dg,  # dataframe containing adm1 name and polygon
                        df_harvest_year,  # dataframe containing information that will be mapped
                        merge_col="Country Region",  # Column on which to merge
                        name_country=countries,  # Plot global map
                        name_col="Predicted Yield (tn per ha)",  # Which column to plot
                        dir_out=self.plot_dir / str(year),  # Output directory
                        fname=fname,  # Output file name
                        label=f"{self.predicted}\n{self.crop.title()}, {year}",
                        vmin=df_harvest_year[self.predicted].min(),
                        vmax=df_harvest_year[self.predicted].max(),
                        cmap=pal.scientific.sequential.Bamako_20_r,
                        series="sequential",
                        show_bg=False,
                        annotate_regions=False,
                        annotate_region_column=annotate_region_column,
                        loc_legend="lower left",
                    )

                    """ Ratio of Predicted to last Year Yield """
                    fname = f"{self.country}_{self.crop}_{dekad}_{year}_ratio_last_year_yield.png"
                    plot.plot_df_shpfile(
                        self.dg,  # dataframe containing adm1 name and polygon
                        df_dekad,  # dataframe containing information that will be mapped
                        merge_col="Country Region",  # Column on which to merge
                        name_country=countries,  # Plot global map
                        name_col="Ratio Last Year",  # Which column to plot
                        dir_out=self.plot_dir / str(year),  # Output directory
                        fname=fname,  # Output file name
                        label=f"Ratio Last Year to {self.predicted}\n{self.crop.title()}, {dekad} {year}",
                        vmin=df_dekad["Ratio Last Year"].min(),
                        vmax=df_dekad["Ratio Last Year"].max(),
                        cmap=pal.scientific.sequential.Bamako_20_r,
                        series="sequential",
                        show_bg=False,
                        annotate_regions=False,
                        annotate_region_column=annotate_region_column,
                        loc_legend="lower left",
                    )
                    break

                    # Area
                    # breakpoint()
                    # if df_dekad["Area (ha)"].notna().all():
                    #     fname = f"{self.country}_{self.crop}_{year}_area.png"
                    #     plot.plot_df_shpfile(
                    #         self.dg,  # dataframe containing adm1 name and polygon
                    #         df_dekad,  # dataframe containing information that will be mapped
                    #         merge_col="Country Region",  # Column on which to merge
                    #         name_country=country,  # Plot global map
                    #         name_col="Area (ha)",  # Which column to plot
                    #         dir_out=self.plot_dir / str(year),  # Output directory
                    #         fname=fname,  # Output file name
                    #         label=f"{self.predicted}\n{self.crop.title()}, {dekad}",
                    #         vmin=df_dekad[self.predicted].min(),
                    #         vmax=df_dekad[self.predicted].max(),
                    #         cmap=pal.scientific.sequential.Bamako_20_r,
                    #         series="sequential",
                    #         show_bg=False,
                    #         annotate_regions=True,
                    #         loc_legend="lower left",
                    #     )

    def plot_metric(self, df, metric="$r^2$"):
        with plt.style.context("science"):
            fig, ax = plt.subplots(figsize=(10, 5))
            ax = sns.lineplot(data=df, x="Date", y=metric, ax=ax)  # "$r^2$"
            ax.set_xlabel("")
            ax.set_ylabel(metric)
            plt.xticks(rotation=0)
            plt.tight_layout()

            # If metric is $r^2$ or NSE, do not plot values below 0
            if metric in ["$r^2$", "Nash-Sutcliff Efficiency"]:
                plt.ylim(0, 1)

            # Replace \n in metric
            metric = metric.replace("\n", " ")
            fname = f"{self.country}_{self.crop}_{metric}.png"

            plt.savefig(self.plot_dir / fname, dpi=250)
            plt.close()

    def run(self):
        self.query()
        aa = self.preprocess()
        self.analyze()

        return aa

    def setup(self, country, crop, model):
        """

        Args:
            country:
            crop:
            model:

        Returns:

        """
        print(f"Setup {country}")
        self.country = country
        self.crop = crop
        self.model = model
        self.table = f"{self.country}_{self.crop}"
        self.observed = "Observed Yield (tn per ha)"
        self.predicted = "Predicted Yield (tn per ha)"

        self.name_shapefile = self.parser.get(self.country, "boundary_file")
        self.admin_zone = self.parser.get(self.country, "admin_zone")

        # Plot directory
        self.plot_dir = self.analysis_dir / self.country / self.crop
        os.makedirs(self.plot_dir, exist_ok=True)


def main():
    obj = Geoanalysis(path_config_file=Path("../config/geocif.txt"))
    obj.parse_config()

    obj.dg = gpd.read_file(
        obj.dir_shapefiles / "adm_shapefile.shp",
        engine="pyogrio",
    )

    # Hack rename Tanzania to United Republic of Tanzania
    obj.dg["ADMIN0"] = obj.dg["ADMIN0"].replace("Tanzania", "United Republic of Tanzania")

    # Rename ADMIN0 to ADM0_NAME and ADMIN1 to ADM1_NAME and ADMIN2 to ADM2_NAME
    obj.dg = obj.dg.rename(
        columns={
            "ADMIN0": "ADM0_NAME",
            "ADMIN1": "ADM1_NAME",
            "ADMIN2": "ADM2_NAME",
        }
    )

    # Create a new column called Country Region that is the concatenation of ADM0_NAME and ADM1_NAME
    # however if ADM2_NAME is not null, then it is the concatenation of ADM0_NAME and ADM2_NAME
    obj.dg["Country Region"] = obj.dg["ADM0_NAME"]
    obj.dg["Country Region"] = obj.dg["Country Region"].str.cat(obj.dg["ADM1_NAME"], sep=" ")
    obj.dg.loc[obj.dg["ADM2_NAME"].notna(), "Country Region"] = (
        obj.dg["ADM0_NAME"] + " " + obj.dg["ADM2_NAME"]
    )
    # Make it lower case
    obj.dg["Country Region"] = obj.dg["Country Region"].str.lower()
    frames = []
    for country in obj.countries:
        crops = ast.literal_eval(obj.parser.get(country, "crops"))

        for crop in crops:
            models = ast.literal_eval(obj.parser.get(country, "models"))

            for model in models:
                obj.setup(country, crop, model)
                gg = obj.run()
                frames.append(gg)

    dk = pd.concat(frames)

    # Map the metrics
    # obj.map_regional()
    obj.map(dk)


if __name__ == "__main__":
    main()
