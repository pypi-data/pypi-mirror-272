import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from viewai.xai import *  # Make sure this import is correct based on your package structure
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import os

class TestViewAI:
    @classmethod
    def setup_class(cls):
        """Setup for the entire module"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This will navigate to the project root from tests/
        train_file = os.path.join(base_dir, 'datasets/train.csv')
        cls.df = pd.read_csv(train_file)
        cls.df.dropna(inplace=True)
        cls.df = cls.df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1)
        cls.X = cls.df.drop(["Survived"], axis=1)
        cls.Y = cls.df["Survived"]

        # We have to transform categorical variables to use sklearn models
        cls.X = pd.get_dummies(cls.X, prefix_sep='.').astype(float)
        X_train, X_test, y_train, y_test = train_test_split(cls.X, cls.Y, test_size=0.20, random_state=RANDOM_SEED)

        #Blackbox system can include preprocessing, not just a classifier!
        pca = PCA()
        rf = RandomForestClassifier(random_state=RANDOM_SEED)

        cls.blackbox_model = Pipeline([('pca', pca), ('rf', rf)])
        cls.blackbox_model.fit(X_train, y_train)

        cls.xai = XAI()
        cls.xai.run(
            X=X_train,
            Y=y_train,
            model=cls.blackbox_model,
        )

    def test_shap_values(self):
        """Test the calculation of SHAP values"""
        assert hasattr(self.xai, 'shap_values') and self.xai.shap_values is not None

    def test_explanations(self):
        """Test the global explanations generation"""
        assert hasattr(self.xai, 'feature_attributions_figs') and len(self.xai.feature_attributions_figs) > 0

    def test_feature_importance(self):
        """Test the feature importance export functionality"""
        assert hasattr(self.xai, 'feature_importance_fig') and self.xai.feature_importance_fig is not None
