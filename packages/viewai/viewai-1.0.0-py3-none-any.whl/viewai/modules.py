# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

from .config import *


class Modules(Config):
    """Helper functions for XAI"""

    def get_encoding(self, file_path):
        """Detects file encoding using cchardet
        Args:
            file_path: str

        Returns dict
        """
        with open(file_path, "rb") as f:
            return chardet.detect(f.read())

    def remove_special_characters(self, x):
        """Remove potential characters from numerical features
        Args:
            x: string or float/int

        Returns string back or numeric
        """
        temp = str(x).lower()
        characters = [
            "!",
            "@",
            "#",
            "$",
            "€",
            "%",
            "£",
            "¥",
            "ˆ",
            "&",
            "*",
            ",",
            ";",
            "[",
            "]",
        ]
        for char in characters:
            flag = 0
            if char in str(x):
                flag = 1
            if flag == 1:
                try:
                    temp = temp.replace(char, "")
                except Exception as e:
                    # log("EXCEPTION HANDLED {}".format(e), is_error=True)
                    pass

        try:
            return pd.to_numeric(float(temp))
        except Exception as e:
            # log("EXCEPTION HANDLED {}".format(e), is_error=True)
            return temp

    def replace_possible_nans(self, x):
        """Remove potential nans from features
        Args:
            x: string

        Returns nan or itself
        """
        possible_empties = ["-", "n/a", "na", "nan", "nil", np.inf, -np.inf, ""]
        if x in possible_empties:
            return np.nan
        else:
            return x

    def replace_acronyms_to_zeros(self, x):
        """Remove potential anronyms from numerical features
        Args:
            x: string

        Returns string
        """
        try:
            x = x.replace("k", "000")
        except Exception as e:
            pass
        try:
            x = x.replace("m", "000000")
        except Exception as e:
            pass
        try:
            x = x.replace("b", "000000000")
        except Exception as e:
            pass
        return x

    def get_irrelevant_feature(self, df):
        """Remove potential ids from dataframes
        Args:
            df: Dataframe to remove potential id's from

        Searches for 'id' in the name else look for nunique == df.rows and alpha numeric or skewness == 0

        Returns list of features which are irrelevant
        """

        def is_alpha_numeric(value):
            """Check for alpha-numeric value similar to pd.Series.isalnum
            Args:
                value: value to check for alpha numeric value

            Returns boolean
            """
            value = str(value).lower()
            numeric_flag = False
            alpha_flag = False
            for char in list("1234567890"):
                if char in value:
                    numeric_flag = True
                    break
            for char in list("abcdefghijklmnopqrstuvwxyz"):
                if char in value:
                    alpha_flag = True
                    break
            if numeric_flag and alpha_flag:
                return True
            else:
                return False

        irrelevant_features = []
        for feature in df.columns:
            if (
                df[feature].isnull().sum() / len(df) * 100
                > self.get_missing_value_threshold()
            ):
                continue
            if re.findall(feature.lower(), "id"):
                irrelevant_features.append(feature)
                continue

            if df[feature].nunique() == len(df):
                value = df[feature].iloc[0]
                if is_alpha_numeric(value):
                    irrelevant_features.append(feature)
                    continue
                try:
                    temp_feature = pd.to_numeric(df[feature])
                    if temp_feature.skew() == 0:
                        irrelevant_features.append(feature)
                        continue
                except Exception as e:
                    pass

        return irrelevant_features

    def get_supervised_type(self, y):
        """Check between Regression and Classification on the target feature
            Args:
                y: target feature; pd.Series

            Looks for nunique and dtype of the target feature

        Returns tring
        """
        is_class = False
        type_of_target = type(y)
        if type_of_target in ["int", "float"]:
            if y.nunique() < self.get_supervised_type_threshold():
                is_class = True
                # return self.get_classification_type()
            else:
                is_class = False
                # return self.get_regression_type()
        else:
            y = pd.Series(y)
            if y.nunique() < self.get_supervised_type_threshold():
                is_class = True
                # return self.get_classification_type()
            else:
                try:
                    y = y.astype(float)
                    is_class = False
                    # return self.get_regression_type()
                except:
                    raise Exception("NOT SUPPORTED: TARGET")

        if is_class:
            if(y.nunique() == 2):
                return self.get_classification_type(binary=True)
            else:
                return self.get_classification_type(binary=False)
        else:
            return self.get_regression_type()

    def get_numerical_features(self, df):
        """Getter function to get a list of numerical features of a dataframe
            Args:
                df: dataframe to check for numerical features

        Returns list
        """
        num_columns = []
        for feature in df.columns:
            if (
                df[feature].isnull().sum() / len(df) * 100
                > self.get_missing_value_threshold()
            ):
                continue
            if df[feature].nunique() >= self.get_categorical_feature_threshold():
                if df[feature].dtype in (int, float):
                    num_columns.append(feature)
                else:
                    try:
                        temp_feature = pd.to_numeric(df[feature], errors="coerce")
                        if temp_feature.isnull().sum() / len(df) * 100 > 50:
                            continue
                        num_columns.append(feature)
                    except:
                        pass
        return num_columns

    def get_categorical_features(self, df):
        """Getter function to get a list of categorical features of a dataframe
            Args:
                df: dataframe to check for categorical features

        Returns list
        """
        cat_columns = []
        for feature in df.columns:
            if (
                df[feature].isnull().sum() / len(df) * 100
                > self.get_missing_value_threshold()
            ):
                continue
            if (
                df[feature].dtype == object
                and df[feature].nunique() < self.get_categorical_feature_threshold()
            ):
                cat_columns.append(feature)
                continue
            if df[feature].nunique() < self.get_categorical_feature_threshold():
                try:
                    df[feature] = df[feature].astype(float)
                except:
                    df[feature] = df[feature].astype(str)
                cat_columns.append(feature)
        return cat_columns