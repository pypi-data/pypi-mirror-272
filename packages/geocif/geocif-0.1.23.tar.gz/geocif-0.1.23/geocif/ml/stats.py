import os
import numpy as np
import pandas as pd
from tqdm import tqdm


def add_GEOGLAM_statistics(df, stats, method, admin_zone):
    """

    Args:
        df:
        stats:
        method:
        admin_zone:

    Returns:

    """
    # Create empty columns for all the ag statistics
    for stat in stats:
        df.loc[:, stat] = np.NaN

    # Fill in the ag statistics columns with data when available
    # Compute national scale statistics
    crop = df["Crop"].unique()[0]
    # Change crop to lower case and replace space by _
    crop = crop.lower().replace(" ", "_")
    season = df["Season"].unique()[0]

    # Read in the area stats for the crop and season
    stat_file = cc.dir_yld / f"{crop}_{season}.xlsx"

    for stat in stats:
        if os.path.isfile(stat_file):
            df_stat = pd.read_excel(stat_file, sheet_name=stat)
        else:
            continue

        # Loop over each Country, Region, harvest year combination and add the area
        grp = df.groupby(["Country", "Region", "Harvest Year"], dropna=False)
        for key, group in tqdm(grp, desc=f"Adding {stat} {method}", leave=False):
            country, region, year = key

            df_adm0 = pd.DataFrame()
            if not df_stat.empty:
                tmp = df_stat["ADM0_NAME"].str.lower()
                if country != "vietnam":  # Hack alert
                    mask_country = tmp == country.replace("_", " ").lower()
                else:
                    mask_country = tmp == "viet nam"
                df_adm0 = df_stat.loc[mask_country]

            if df_adm0.empty:
                continue

            # Get the statistic for the country and year
            region_column = "ADM2_NAME" if admin_zone == "admin_2" else "ADM1_NAME"
            val = inp.get_yld_prd(
                df_adm0,
                crop,  # maize
                cntr=country,  # Brazil
                region=region,  # Mato Grasso
                calendar_year=year,
                region_column=region_column,
            )

            # Add the statistic to the dataframe
            df.loc[group.index, stat] = val

    return df


def add_statistics(df, country, crop, admin_zone, stats, method, target_col="Yield (tn per ha)"):
    """

    Args:
        df:
        country:
        crop:
        admin_zone:
        stats:
        method:
        target_col:

    Returns:

    """
    # First check if country and crop are in the admin_crop_production.csv file
    df_fewsnet = pd.read_csv(
        cc.dir_yld / "adm_crop_production.csv",
    )
    # Check if country and crop exist in the fewsnet database
    mask = (df_fewsnet["country"] == country) & (df_fewsnet["product"] == crop)

    if mask.sum() == 0 or country == "Malawi" or country == "Zambia":
        df = add_GEOGLAM_statistics(df, stats, method, admin_zone)
    else:
        group_by = ["Region", "Harvest Year"]
        groups = df.groupby(group_by)

        # Define processing for each group
        def process_group(group, region, harvest_year):
            mask = (df["Region"] == region) & (df["Harvest Year"] == harvest_year)

            mask_region = df_fewsnet[admin_zone] == region
            mask_yield = (
                df_fewsnet["crop_production_system"].isin(
                    ["none", "Small-scale (PS)", "Commercial (PS)", "All (PS)"]
                )
                & (df_fewsnet["harvest_year"] == harvest_year)
                & (df_fewsnet["product"] == crop)
                & df_fewsnet["season_name"].isin(
                    ["Main", "Meher", "Main harvest", "Annual", "Summer"]
                )
                & (df_fewsnet["indicator"].isin(["yield", "area", "production"]))
            )

            # Fetching values for each indicator
            yield_value = df_fewsnet.loc[
                mask_yield & mask_region & (df_fewsnet["indicator"] == "yield"), "value"
            ]
            area_value = df_fewsnet.loc[
                mask_yield & mask_region & (df_fewsnet["indicator"] == "area"), "value"
            ]
            prod_value = df_fewsnet.loc[
                mask_yield & mask_region & (df_fewsnet["indicator"] == "production"),
                "value",
            ]

            if not yield_value.empty:
                group.loc[:, target_col] = yield_value.values[0]
                group.loc[:, "Area (ha)"] = area_value.values[0]
                group.loc[:, "Production (tn)"] = prod_value.values[0]

            return group

        # Process each group with a progress bar
        results = []
        for (region, harvest_year), group in tqdm(
            groups, total=len(groups), desc="Processing statistics", leave=False
        ):
            processed_group = process_group(group.copy(), region, harvest_year)
            results.append(processed_group)

        df = pd.concat(results)

    # Add columns for obj.stats_cols
    for col in ["Area"]:
        df.loc[:, col] = np.nan

    return df
