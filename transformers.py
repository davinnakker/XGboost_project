"""
--------------------------------------------------------------------------------------
Imports 
--------------------------------------------------------------------------------------
"""

from abc import ABC, abstractmethod
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error, r2_score, rmse
import polars as pl

"""
-----------------------------------------------------------------------------------------
Abstract Transformation Class. Please Inherit from this class for any new transformations
-----------------------------------------------------------------------------------------
"""
class Transformation(ABC):

    @abstractmethod
    def fit(self, df: pl.DataFrame):
        return self
    
    @abstractmethod
    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        pass

    def fit_transform(self, df: pl.DataFrame) -> pl.DataFrame:
        return self.fit(df).transform(df)
    
"""
--------------------------------------------------------------------------------------
Please Code any new Transformation Child Classes directly below this comment.  
--------------------------------------------------------------------------------------
"""


class ZipCodeTransformer(Transformation):

    def __init__(self):
        self.zipcode_data = None

    def fit(self, df):
        self.zipcode_data = (
            df
            .group_by("zipcode")
            .agg(
                median_price = pl.col("price").median(),
                median_grade = pl.col("grade").median()
            )
        )
        return self

    def transform(self, df):
        return df.join(self.zipcode_data, how="left", on="zipcode")


class PCATransformer(Transformation):

    def __init__(self):
        self.num_of_pcs = 3
        self.pca = PCA(self.num_of_pcs)
        self.scaler = StandardScaler()
        self.pca_cols = ["bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "sqft_above", "sqft_basement"]

    def fit(self, df):
        df = self.scaler.fit_transform(df.select(self.pca_cols).to_numpy())
        self.pca.fit(df)
        return self
    
    def transform(self, df):
        df_numpy = df.select(self.pca_cols).to_numpy()
        df_scaled = self.scaler.transform(df_numpy)
        components = self.pca.transform(df_scaled)
        components = pl.DataFrame(data=components, schema=[f"PC {i + 1}" for i in range(self.num_of_pcs)])
        df = df.drop(self.pca_cols).hstack(components)
        
        return df


class DropColumnTransformer(Transformation):

    def __init__(self):
        self.columns = ["date", "id", "yr_renovated", "zipcode"]

    def fit(self, df):
        return super().fit(df)
        
    def transform(self, df):
        return df.drop(self.columns)
    
"""
--------------------------------------------------------------------------------------
Preprocessing Pipeline
--------------------------------------------------------------------------------------
"""

class PreprocessingPipeline():

    def __init__(self, transformations: list[Transformation]):
        self.transformations = transformations

    def run_train(self, df: pl.DataFrame):
        for step in self.transformations:
            df = step.fit_transform(df)
        return df

    def run_inference(self, df: pl.DataFrame):
        for step in self.transformations:
            df = step.transform(df)
        return df
    
"""
--------------------------------------------------------------------------------------
Experimentation Functions
--------------------------------------------------------------------------------------
"""
    
def features_target_split(df: pl.DataFrame, target_col: str):
    y = df.select(target_col)
    X = df.drop(target_col)
    return X, y


def regression_report(y_test, y_pred):
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Regression Report")
    print("-" * 30)
    print(f"MAE  : {mae:.4f}")
    print(f"MSE  : {mse:.4f}")
    print(f"R²   : {r2:.4f}")
    print(f"Average Error: {mae / y_test.to_numpy().mean():.2f}%")


def get_feature_importance(model: BaseEstimator, X_train: pl.DataFrame):
    importance_df = pl.DataFrame({
        "Features": X_train.columns,
        "Importance": model.feature_importances_})
    
    return importance_df.sort("Importance", descending=True)


def test_model(
        pipeline: PreprocessingPipeline,
        model: BaseEstimator,
        train: pl.DataFrame,
        test: pl.DataFrame,
        target_col: str,
        regression: bool = False,
        show_training: bool = False
        ):
    
    train_preprocessed = pipeline.run_train(train)
    X_train, y_train = features_target_split(train_preprocessed, target_col)
    model.fit(X_train, y_train)

    if show_training:
        train_predictions = model.predict(X_train)
        if regression:
            regression_report(y_train, train_predictions)
        else:
            print(classification_report(y_train, train_predictions))

    test_preprocessed = pipeline.run_inference(test)
    X_test, y_test = features_target_split(test_preprocessed, target_col)
    predictions = model.predict(X_test)

    if regression:
        regression_report(y_test, predictions)
    else:
        print(classification_report(y_test, predictions))
    
    print(get_feature_importance(model, X_train))



    


        

    
    
