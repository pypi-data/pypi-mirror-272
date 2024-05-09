# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

from .modules import *
from .config import Config
from .logger import Logger


class Inputs(Modules, Config, Logger):
    def __init__(
        self,
        df: pd.DataFrame,
        X: pd.DataFrame,
        Y: pd.Series,
        model: any,
        target: str,
        X_features: list = None,
    ):
        """Class for Input Data and Model."""

        self.X_features = X_features
        self.validate_inputs(df, X, Y, model, target)

        if(df is not None):
            self.df = df
            self.X = df.drop(target, axis=1)
            self.Y = df[target]
        else:
            self.df = pd.concat([X, pd.Series(Y, name=target)], axis=1)
            self.X = X
            self.Y = Y
        self.model = model
        self.target = target


        self.check_columns()

        self.model = model
        self.feature_names = self.df.columns.to_list()
        self.feature_types = [str(self.df[col].dtype) for col in self.df.columns]

        self.clean()

    def validate_inputs(self, df, X, Y, model, target):
        """ 
        if df is there, target should be there in df and target should be given as string
        if df is given then X_features should be given as list
        if X and Y is given then no target no X_features needed
        """
        if df is not None:
            if not target:
                raise ValueError("Target should be given if df is given")
            if target not in df.columns:
                print("TARGET", target, df.columns)
                raise ValueError(f"Target column {target} not found in DataFrame")
            if not isinstance(target, str):
                raise ValueError("Target should be given as string")
            if self.X_features is None:
                raise ValueError("X_features should be given as list")
        else:
            if target is not None:
                raise ValueError("Target should not be given if X and Y is given")
            if self.X_features is not None:
                raise ValueError("X_features should not be given if X and Y is given")


    def clean(self):
        self.log("CLEANING DATA", hash_print=True)

        self.df = pd.concat([self.X, self.Y], axis=1)

        try:
            self.cat_columns = self.modules_instance.get_categorical_features(self.df)
        except:
            self.cat_columns = self.df.select_dtypes(include=object).columns

        self.log("REPLACING POSSIBLE NANS")
        for feature in self.df.columns:
            self.df[feature] = self.df[feature].apply(
                lambda x: self.replace_possible_nans(x)
            )

        self.log("REMOVING SPECIAL CHARACTERS")
        for feature in self.df.columns:
            if feature not in self.cat_columns:
                self.df[feature] = self.df[feature].apply(
                    lambda x: self.remove_special_characters(x)
                )

        self.log("INFO", hash_print=True)
        self.log(f"SHAPE: {self.X.shape}")
        self.log(f"TARGET: {self.target}")
        self.log("MODEL", hash_print=True)
        self.log(f"{self.model}")

    def check_columns(self):
        """Check if DataFrame contains all columns used in the model."""
        try:    
            self.required_columns = set(self.model.feature_names_in_)
            print("REQUIRED COLUMNS", self.required_columns)
        except:
            raise ValueError("Model does not have feature_names_in_ attribute")
        current_columns = set(self.X.columns)

        missing_columns = self.required_columns - current_columns

        if missing_columns:
            self.log(
                f"Warning: Extra columns found that were not in training data: {missing_columns} hence X will be modified"
            )
            self.X = pd.get_dummies(self.X, prefix_sep=".").astype(
                float
            )  # One hot encode
            if (
                self.required_columns - set(self.X.columns)
            ):
                raise ValueError(
                    f"Missing columns in the input data: {missing_columns}"
                )

        current_columns = set(self.X.columns)
        missing_columns = self.required_columns - current_columns

        if missing_columns:
            raise ValueError(f"Missing columns in the input data: {missing_columns}")
        
        # reset required columns order
        if(hasattr(self, "X")): 
                self.required_columns = self.X.columns.to_list()
        elif(hasattr(self, "df")):
            if(hasattr(self, "X_features")):
                self.required_columns = self.X_features
            else:
                raise ValueError("Required columns not found and cannot calculate as X is not found")
