# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

from .config import *
from .inputs import Inputs
from .modules import Modules
from .logger import Logger
from .plots import Plots
from .explanations import Explanations

class XAI(Modules, Plots, Logger):

    def __init__(self, cli=False):
        self.cli = cli

    def configure(self):
        self.config = Config()

    def run(
        self,
        df: pd.DataFrame = None,
        X: pd.DataFrame = None,
        Y: pd.Series = None,
        model: any = None,
        target: str = None,
        X_features: list = None,
    ):
        process_start_time = time()

        if not hasattr(self, "config"):
            self.configure()

        if not (self.cli or hasattr(self, "inputs")):
            self.inputs = Inputs(
                df=df,
                X=X,
                Y=Y,
                model=model,
                target=target,
                X_features=X_features,
            )

        if hasattr(self, "inputs") and all(
            hasattr(self.inputs, attr) for attr in ["X", "Y", "df", "target", "model"]
        ):
            self._describe()
            self._calculate_metrics()
            self._calculate_shap_values()
            self._export_global_explanation()
            self._export_feature_importance()
        else:
            self.log("TERMINATING PROCESS DUE TO INVALID USER INPUTS", is_error=True)
            raise Exception("Invalid Inputs")
        process_end_time = time()
        self.log("TOTAL TIME TAKEN {}(s)".format(process_end_time - process_start_time))

    def _describe(self):
        """Logs and drops features
        Returns:
            None
        """
        self.log("DATA DESCRIPTION", hash_print=True)
        self.cat_columns = self.get_categorical_features(self.inputs.X)
        self.rows, self.cols = self.inputs.X.shape[0], self.inputs.X.shape[1]
        self.duplicate_rows = self.inputs.X.duplicated().sum()
        self.high_cardinality_features = [
            feature
            for feature in self.cat_columns
            if self.inputs.X[feature].nunique()
            >= self.high_cardinality_features_threshold()
        ]
        self.missing_features = [
            feature
            for feature in self.inputs.X.columns
            if self.inputs.X[feature].isnull().sum() / self.rows * 100
            > self.get_missing_value_threshold()
        ]
        self.missing_values = self.inputs.X.isnull().sum().sum()

        self.supervised_type = self.get_supervised_type(self.inputs.Y)
        self.log("SUPERVISED TYPE: {}".format(self.supervised_type))

        if self.supervised_type == ClassificationType.BINARY:
            try:
                self.inputs.Y = self.inputs.Y.astype(int)
            except:
                #lable encode the target
                self.inputs.Y = self.inputs.Y.astype("category").cat.codes
        elif self.supervised_type == ClassificationType.MULTICLASS:
            raise Exception("Multiclass Classification is not supported")
        else:
            self.inputs.Y = self.inputs.Y.astype(float)

        self.log("NUMBER OF ROWS: {}\nNUMBER OF COLS: {}".format(self.rows, self.cols))
        self.log("NUMBER OF DUPLICATED ROWS: {}".format(self.duplicate_rows))
        self.log("HIGH CARDINALITY FEATURES: {}".format(self.high_cardinality_features))
        self.log("MISSING VALUE(s) FEATURES: {}".format(self.missing_features))
        self.log("TOTAL MISSING VALUE(s): {}".format(self.missing_values))
        self.log(
            "TOTAL UNIQUE VALUE(s): {}".format(self.inputs.X.nunique().sum().sum())
        )

    def _calculate_shap_values(self):
        """Calculate SHAP Values"""
        self.log("CALCULATING SHAP VALUES", hash_print=True)
        start_time = time()
        try:
            self.explainer = shap.Explainer(self.inputs.model)
            self.shap_values = self.explainer(self.inputs.X)
            if len(self.shap_values.shape) == 3:  # Assuming a shape of (samples, features, classes or contributions)
                # Possible handling: Sum across the third dimension if it represents positive and negative contributions
                self.shap_values = self.shap_values.sum(axis=2)
            elif len(self.shap_values.shape) == 2:
                pass  # No adjustment needed
            self.shap_values = self.shap_values.values
        except:
            # copied from https://github.com/interpretml/interpret/blob/develop/python/interpret-core/interpret/blackbox/_shap.py
            from shap import KernelExplainer
            from .utils._clean_x import preclean_X
            from .utils._unify_predict import determine_classes, unify_predict_fn

            data, n_samples = preclean_X(self.inputs.X, self.inputs.feature_names, self.inputs.feature_types)
            try:
                predict_fn, n_classes, _ = determine_classes(self.inputs.model, data[self.inputs.required_columns], n_samples)
            except:
                predict_fn, n_classes, _ = determine_classes(self.inputs.model, data[self.inputs.user_required_columns], n_samples)
            if 3 <= n_classes:
                raise Exception("Multiclass Classification is not supported")
            
            predict_fn = unify_predict_fn(predict_fn, data, 1 if n_classes == 2 else -1)
            self.shap_ = KernelExplainer(predict_fn, data[self.inputs.required_columns])
            self.shap_values = self.shap_.shap_values(pd.DataFrame(shap.kmeans(data[self.inputs.required_columns], int(data.shape[0] * self.config.get_shap_sample_percentage())).data, columns=self.inputs.required_columns))
        end_time = time()
        self.log(
            "TIME TAKEN TO CALCULATE SHAP VALUES {}(s)".format(end_time - start_time)
        )
        self.log("BUILDING LIME EXPLAINER", hash_print=True)
        data = self.inputs.X.astype(np.float64, copy=False)
        self.lime = LimeTabular(self.inputs.model, data, random_state=RANDOM_SEED)

    def _export_global_explanation(self):
        self.log("GLOBAL EXPLANATION", hash_print=True)
        if(self.supervised_type != ClassificationType.MULTICLASS):
            try:
                self.summary_fig = self.summary_plotly(
                    self.shap_values,
                    self.inputs.X,
                    feature_names=self.inputs.X.columns.to_list(),
                )
                self.export_plot(self.summary_fig, path=SUMMARY_PLOT_FILE_NAME)
            except Exception as e:
                self.log("EXCEPTION HANDLED WHILE GENERING SUMMARY PLOT: {}".format(e), is_error=True)

        self.feature_attributions_figs = list()
        for feature in self.inputs.X.columns:
            fig = self.dependence_plotly(
                f"{feature}",
                self.shap_values,
                self.inputs.X,
                feature_names=self.inputs.X.columns,
                interaction_index=f"{feature}",
            )
            self.feature_attributions_figs.append(fig)
            DEPENCENCY_PLOT_FILE_NAME = os.path.join(
                "tmp", f"{feature}_dependence_plot.json"
            )
            self.export_plot(fig, path=DEPENCENCY_PLOT_FILE_NAME)

        self.log("EXPORTED GLOBAL EXPLANATION PLOTS")

    def _export_feature_importance(self):
        # get feature importance using shap values mean
        if(self.supervised_type != ClassificationType.MULTICLASS):
            self.shap_values_mean = np.abs(self.shap_values).mean(0)
            if(self.shap_values_mean.shape != self.inputs.X.columns.shape):
                self.shap_values_mean = np.abs(self.shap_values).mean(
                    axis=(0, 2)
                )  # mean across samples and the second dimension
            self.shap_values_mean_df = pd.DataFrame(
                {"features": self.inputs.X.columns, "scores": self.shap_values_mean}
            ).sort_values(by="scores", ascending=True)
            self.feature_importance_fig = px.bar(self.shap_values_mean_df, x="scores", y="features", orientation="h")
            self.export_plot(
                self.feature_importance_fig, path=FEATURE_IMPORTANCE_PLOT_FILE_NAME
            )

    def _calculate_metrics(self):
        """Calculate Metric"""
        self.log("TRAINING METRICS", hash_print=True)
        self.predictions = self.inputs.model.predict(self.inputs.X)
        if self.supervised_type == ClassificationType.BINARY:
            self.metrics = {
                "Model": self.inputs.model.__class__.__name__,
                "Accuracy": accuracy_score(self.inputs.Y, self.predictions),
                "AUC ROC": roc_auc_score(self.inputs.Y, self.predictions),
                "Precision": precision_score(self.inputs.Y, self.predictions, average="weighted"),
                "Recall": recall_score(self.inputs.Y, self.predictions, average="weighted"),
                "F1 Score": f1_score(self.inputs.Y, self.predictions, average="weighted"),
            }
            self.y_true = self.inputs.Y
            # check if target is binary
            if len(self.y_true.unique()) == 2:
                self.y_probas = self.inputs.model.predict_proba(self.inputs.X)[:, 1] # For binary classification
            else:
                self.y_probas = self.inputs.model.predict_proba(self.inputs.X)

            classes = self.inputs.model.classes_

            if len(classes) > 2:
                pass  # sklearn doesn't support for multiclass classification
            else:
                self.plot_cumulative_gain_curve(self.y_true, self.y_probas, classes)
                self.plot_lift_curve(self.y_true, self.y_probas, classes)
                self.plot_roc_curve(self.y_true, self.y_probas)
                self.plot_confusion_matrix(
                    cm=confusion_matrix(self.y_true, self.predictions), target_names=classes
                )
        elif self.supervised_type == RegressionType.LINEAR:
            self.metrics = {
                "Model": self.inputs.model.__class__.__name__,
                "R2 Score": r2_score(self.inputs.Y, self.predictions),
                "Mean Absolute Error": mean_absolute_error(self.inputs.Y, self.predictions),
                "Mean Squared Error": mean_squared_error(self.inputs.Y, self.predictions),
            }
            self.y_true = self.inputs.Y
            self.y_pred = self.predictions 
            self.plot_decile_plot(self.y_true, self.y_pred)
            self.plot_residual_plot(self.y_true, self.y_pred)
            self.plot_predicted_vs_actual(self.y_true, self.y_pred)

        result_frame = pd.DataFrame(self.metrics, index=[0])
        print(tabulate(result_frame, headers="keys", tablefmt="pretty"))

    def explain_global(self):
        if(not hasattr(self, "explanations")):
            self.explanations = Explanations(self)
        self.explanations.explain_global()

    
    def explain_local(self, X, y=None, name=None, **kwargs):
        if(not hasattr(self, "explanations")):
            self.explanations = Explanations(self)

        self.local_expl = self.lime.explain_local(X, y=y, name=name, **kwargs)
        self.local_explanation_figs = list()
        for i in range(len(X)):
            fig = self.local_expl.visualize(key=i)
            self.local_explanation_figs.append(fig)
        
        self.explanations.explain_local()
