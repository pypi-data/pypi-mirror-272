import numpy as np
from sklearn.ensemble import RandomForestRegressor


def select_features(X, y, method="RFE", min_features_to_select=3):
    """

    Args:
        X:
        y:
        method:
        min_features_to_select:
        num_cpus:

    Returns:

    """

    # df = X.copy()
    #
    # # Initialize and apply StandardScaler
    # scaler = StandardScaler()
    # scaled_data = scaler.fit_transform(df)
    #
    # # Initialize and apply VarianceThreshold
    # # Note: Since data is standardized, all features now have variance of 1 before applying VarianceThreshold.
    # # You would adjust the threshold based on new criteria since variances have been normalized.
    # selector = VarianceThreshold(threshold=scaled_data.var().mean())
    # X = selector.fit_transform(scaled_data)

    # Fill in columns with median of that column
    X = X.fillna(X.median())

    # Define the RandomForestRegressor
    forest = RandomForestRegressor(
        n_estimators=500,
        n_jobs=8,
        max_depth=5,
        random_state=1,
    )

    # Adjusting numpy types due to deprecation warnings or errors
    np.int = np.int32
    np.float = np.float64
    np.bool = np.bool_

    if method == "SelectKBest":
        from sklearn.feature_selection import SelectKBest, f_regression

        k = 10  # Number of features to select
        selector = SelectKBest(score_func=f_regression, k=10)

        # Fit the selector to the data and transform the data to select the best features
        X_new = selector.fit_transform(X, y)

        # Get the selected feature indices
        selected_features = selector.get_support(indices=True)

        # Get the selected feature names
        selected_features = X.columns[selected_features].tolist()
    elif method == "RFECV":
        from sklearn.feature_selection import RFECV
        from sklearn.model_selection import KFold

        # Initialize a k-fold cross-validation strategy
        cv = KFold(n_splits=5)

        # Patch the scoring function to add a progress bar
        class RFECVWithProgress(RFECV):
            def _fit(self, X, y):
                from tqdm import tqdm

                n_features = X.shape[1]
                with tqdm(total=n_features) as pbar:

                    def patched_scorer(*args, **kwargs):
                        pbar.update(1)
                        return self.scorer_(*args, **kwargs)

                    self.scorer_ = patched_scorer
                    super()._fit(X, y)

        # Initialize RFECV with the estimator and cross-validation strategy
        selector = RFECVWithProgress(
            estimator=forest, step=1, n_jobs=-1, cv=cv, scoring="neg_mean_squared_error"
        )
        selector.fit(X, y)
        # Get the selected feature indices
        selected_features = selector.get_support(indices=True)

        # Get the selected feature names
        selected_features = X.columns[selected_features].tolist()
    elif method == "BorutaPy":
        from boruta import BorutaPy

        selector = BorutaPy(forest, n_estimators="auto", random_state=42)
        selector.fit(X.values, y.values)
        selected_features_mask = selector.support_
        selected_features = X.columns[selected_features_mask].tolist()
    elif method == "Leshy":
        import arfs.feature_selection.allrelevant as arfsgroot
        from catboost import CatBoostRegressor

        model = CatBoostRegressor(n_estimators=350, verbose=0, use_best_model=False)
        selector = arfsgroot.Leshy(
            model,
            n_estimators="auto",
            verbose=1,
            max_iter=10,
            random_state=42,
            importance="fastshap",
        )
        selector.fit(X, y, sample_weight=None)

        selected_features = selector.get_feature_names_out()
        # feat_selector.plot_importance(n_feat_per_inch=5)
    elif method == "PowerShap":
        from powershap import PowerShap
        from catboost import CatBoostRegressor

        selector = PowerShap(
            model=CatBoostRegressor(n_estimators=500, verbose=0, use_best_model=True),
            power_alpha=0.05,
        )

        selector.fit(X, y)  # Fit the PowerShap feature selector
        selector.transform(X)  # Reduce the dataset to the selected features
    elif method == "BorutaShap":
        from BorutaShap import BorutaShap
        from catboost import CatBoostRegressor

        hyperparams = {
            "depth": 6,
            "learning_rate": 0.05,
            "iterations": 500,
            "subsample": 1.0,
            "random_strength": 0.5,
            "reg_lambda": 0.001,
            "loss_function": "RMSE",
            "early_stopping_rounds": 25,
            "random_seed": 42,
            "verbose": False,
        }
        model = CatBoostRegressor(**hyperparams)

        selector = BorutaShap(model=model, importance_measure="shap", classification=False)
        selector.fit(
            X=X,
            y=y,
            n_trials=100,
            sample=False,
            train_or_test="test",
            normalize=True,
            verbose=False,
        )
        selected_features_mask = selector.Subset().columns
        selected_features = X[selected_features_mask].columns.tolist()
    elif method == "Genetic":
        from sklearn_genetic import GAFeatureSelectionCV

        selector = GAFeatureSelectionCV(
            estimator=forest,
            cv=5,
            verbose=1,
            scoring="neg_mean_squared_error",
            max_features=max(len(X.columns) // 3, min_features_to_select),
            population_size=100,
            generations=40,
            crossover_probability=0.9,
            mutation_probability=0.1,
            keep_top_k=2,
            elitism=True,
            n_jobs=-1,
        )
        selector.fit(X, y)
        selected_features_mask = selector.support_
        selected_features = X.columns[selected_features_mask].tolist()
    elif method == "RFE":
        from sklearn.feature_selection import RFE

        selector = RFE(forest, n_features_to_select=min_features_to_select, step=1, verbose=1)
        selector = selector.fit(X, y)
        selected_features_mask = selector.support_
        selected_features = X.columns[selected_features_mask].tolist()
    else:
        raise ValueError("Method not recognized. Use BorutaPy, Genetic, or RFE")
    # tentative_features = X.columns[selector.support_weak_].tolist()

    # Filter the dataset for selected features
    X_filtered = X.loc[:, selected_features]

    return selector, X_filtered, selected_features
