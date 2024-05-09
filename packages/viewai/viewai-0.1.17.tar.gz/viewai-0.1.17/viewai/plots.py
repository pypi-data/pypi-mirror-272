# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

import plotly.graph_objs as go
import numpy as np
import pandas as pd
from shap.utils import approximate_interactions, convert_name
from plotly import figure_factory
from sklearn.metrics import roc_curve, auc
import plotly.express as px

class Plots:

    def __init__(self) -> None:
        pass

    def export_plot(self, fig, path=None, title=None, isMetric=False):
        if not title:
            title = fig.layout.title.text
        
        if not path:
            path = f"./tmp/{title}.json"

        # if not isMetric:
        #     # fig.show()

        fig.write_json(path)

    def dependence_plotly(
        self,
        ind,
        shap_values,
        features,
        feature_names=None,
        display_features=None,
        interaction_index="auto",
        color_scale="Viridis",
        dot_size=5,
        x_jitter=0,
        alpha=0.8,
        title=None,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
    ):
        """
        Create a SHAP dependence plot using Plotly, colored by an interaction feature.
        """
        # Convert DataFrame inputs to numpy arrays if needed
        if isinstance(features, pd.DataFrame):
            if feature_names is None:
                feature_names = features.columns.tolist()
            features = features.values

        if isinstance(display_features, pd.DataFrame):
            display_features = display_features.values
        elif display_features is None:
            display_features = features

        # Ensure feature names are assigned
        if feature_names is None:
            feature_names = [
                "Feature {}".format(i) for i in range(shap_values.shape[1])
            ]

        # Determine the main feature and interaction index
        ind = convert_name(ind, shap_values, feature_names)
        if interaction_index == "auto":
            interaction_index = approximate_interactions(ind, shap_values, features)[0]
        interaction_index = convert_name(interaction_index, shap_values, feature_names)

        # Handle single dimension shap_values and features
        if len(shap_values.shape) == 1:
            shap_values = np.reshape(shap_values, (len(shap_values), 1))
        if len(features.shape) == 1:
            features = np.reshape(features, (len(features), 1))

        xv = features[:, ind]
        sv = shap_values[:, ind]
        if interaction_index is not None:
            cv = features[:, interaction_index]
        else:
            cv = "#0096FF"

        # Define the plot
        shap_colorscale = [[0, "#0096FF"], [1, "red"]]
        trace = go.Scattergl(
            x=xv,
            y=sv,
            mode="markers",
            marker=dict(
                size=dot_size,
                color=cv,
                colorscale=shap_colorscale,
                showscale=True if interaction_index is not None else False,
                colorbar=(
                    dict(title=feature_names[interaction_index])
                    if interaction_index is not None
                    else None
                ),
                opacity=alpha,
            ),
        )
        layout = go.Layout(
            title=title,
            xaxis=dict(title=feature_names[ind]),
            yaxis=dict(title="SHAP value"),
            # plot_bgcolor='white'
        )
        fig = go.Figure(data=[trace], layout=layout)

        # Handle axis limits
        if xmin is not None or xmax is not None:
            fig.update_xaxes(range=[xmin, xmax])
        if ymin is not None or ymax is not None:
            fig.update_yaxes(range=[ymin, ymax])

        return fig

    def summary_plotly(self, shap_values, features=None, feature_names=None, max_display=20):
        if isinstance(shap_values, list):
            shap_values = np.vstack(shap_values)

        if isinstance(features, pd.DataFrame):
            if feature_names is None:
                feature_names = features.columns.tolist()
            features = features.values

        # Adjusting feature_importance calculation to handle 3D shap_values
        feature_importance = np.abs(shap_values).mean(axis=(0, 2))  # Averaging over samples and the last dimension
        feature_order = np.argsort(feature_importance)[-max_display:]

        data = []
        for i in feature_order:
            feature_data = features[:, i] if features is not None else None
            if feature_data is not None:
                normalized_feature_values = (feature_data - np.nanmin(feature_data)) / (np.nanmax(feature_data) - np.nanmin(feature_data))
                colors = normalized_feature_values
            else:
                colors = "rgba(30, 136, 229, 0.8)"  # Default color if no feature data is provided

            # Handling 3D SHAP values by averaging or choosing one dimension
            shap_vals_to_plot = shap_values[:, i].mean(axis=1)  # Assuming you want to average the two values per feature

            scatter = go.Scatter(
                x=shap_vals_to_plot,
                y=[feature_names[i] for _ in range(shap_values.shape[0])],
                mode="markers",
                marker=dict(
                    size=8,
                    color=colors,
                    colorscale=[(0, "#0096FF"), (1, "red")],
                    colorbar=dict(title="Feature Impact"),
                    showscale=True,
                ),
                name=feature_names[i],
            )
            data.append(scatter)

        layout = go.Layout(
            title="SHAP Summary Plot",
            xaxis=dict(title="SHAP Value"),
            yaxis=dict(title="Feature", automargin=True),
            showlegend=False,
            hovermode="closest",
            height=800,
        )

        fig = go.Figure(data=data, layout=layout)
        return fig

    def cumulative_gain_curve(self, y_true, y_score, pos_label=None):
        """
        This function generates the points necessary to plot the Cumulative Gain
        Note: This implementation is restricted to the binary classification task.
        Args:
            y_true (array-like, shape (n_samples)): True labels of the data.
            y_score (array-like, shape (n_samples)): Target scores, can either be
                probability estimates of the positive class, confidence values, or
                non-thresholded measure of decisions (as returned by
                decision_function on some classifiers).
            pos_label (int or str, default=None): Label considered as positive and
                others are considered negative
        Returns:
            percentages (numpy.ndarray): An array containing the X-axis values for
                plotting the Cumulative Gains chart.
            gains (numpy.ndarray): An array containing the Y-axis values for one
                curve of the Cumulative Gains chart.
        Raises:
            ValueError: If `y_true` is not composed of 2 classes. The Cumulative
                Gain Chart is only relevant in binary classification.
        """
        y_true, y_score = np.asarray(y_true), np.asarray(y_score)

        # ensure binary classification if pos_label is not specified
        classes = np.unique(y_true)
        if pos_label is None and not (
            np.array_equal(classes, [0, 1])
            or np.array_equal(classes, [-1, 1])
            or np.array_equal(classes, [0])
            or np.array_equal(classes, [-1])
            or np.array_equal(classes, [1])
        ):
            raise ValueError("Data is not binary and pos_label is not specified")
        elif pos_label is None:
            pos_label = 1.0

        # make y_true a boolean vector
        y_true = y_true == pos_label

        sorted_indices = np.argsort(y_score)[::-1]
        y_true = y_true[sorted_indices]
        gains = np.cumsum(y_true)

        percentages = np.arange(start=1, stop=len(y_true) + 1)

        gains = gains / float(np.sum(y_true))
        percentages = percentages / float(len(y_true))

        gains = np.insert(gains, 0, [0])
        percentages = np.insert(percentages, 0, [0])

        return percentages, gains

    def plot_cumulative_gain_curve(self, y_true, y_probas, classes):
        """
        Generates the Cumulative Gains Plot from labels and scores/probabilities
        The implementation here works only for binary classification.
        Args:
            y_true (array-like, shape (n_samples)):
                Ground truth (correct) target values.
            y_probas (array-like, shape (n_samples, n_classes)):
                Prediction probabilities for each class returned by a classifier.
            classes (array-like, shape (n_classes)):
                Array of Unique labels
        """
        # create labels
        class0 = "Class_{}".format(classes[0])
        class1 = "Class_{}".format(classes[1])

        # calculate gain
        perc, gains0 = self.cumulative_gain_curve(
            y_true, pd.Series(y_probas).apply(lambda x: 1 - x), pos_label=classes[0]
        )
        perc, gains1 = self.cumulative_gain_curve(
            y_true, y_probas, pos_label=classes[1]
        )

        # make df
        df = pd.DataFrame(
            {"Percentage of Sample": perc, class0: gains0, class1: gains1}
        )
        df = pd.melt(df, id_vars=["Percentage of Sample"], value_vars=[class0, class1])
        df = df.rename(columns={"value": "Gain", "variable": "Target Class"})

        # plot
        fig = px.line(
            df, x="Percentage of Sample", y="Gain", color="Target Class", markers=True
        )

        # add title
        fig.update_layout(
            title="CUMULATIVE GAINS CURVE",
            yaxis_title="Gain",
            xaxis_title="Percentage of Sample",
        )

        self.export_plot(fig, isMetric=True)

    def plot_lift_curve(self, y_true, y_probas, classes):
        # create labels
        class0 = "Class_{}".format(classes[0])
        class1 = "Class_{}".format(classes[1])

        # calculate gain
        perc, gains0 = self.cumulative_gain_curve(
            y_true, pd.Series(y_probas).apply(lambda x: 1 - x), pos_label=classes[0]
        )
        perc, gains1 = self.cumulative_gain_curve(
            y_true, y_probas, pos_label=classes[1]
        )

        perc = perc[1:]
        gains0 = gains0[1:]
        gains1 = gains1[1:]

        gains0 = gains0 / perc
        gains1 = gains1 / perc

        # make df
        df = pd.DataFrame(
            {"Percentage of Sample": perc, class0: gains0, class1: gains1}
        )
        df = pd.melt(df, id_vars=["Percentage of Sample"], value_vars=[class0, class1])
        df = df.rename(columns={"value": "Lift", "variable": "Target Class"})

        # plot
        fig = px.line(
            df, x="Percentage of Sample", y="Lift", color="Target Class", markers=True
        )

        # add title
        fig.update_layout(
            title="LIFT CURVE",
            yaxis_title="Lift",
            xaxis_title="Percentage of Sample",
        )

        self.export_plot(fig, isMetric=True)

    def plot_confusion_matrix(self, cm, target_names, normalise=True):
        """
        given a confusion matrix (cm), make a nice plot

        Arguments
        ---------
        cm:           confusion matrix from sklearn.metrics.confusion_matrix

        target_names: given classification classes such as [0, 1, 2]
                    the class names, for example: ['high', 'medium', 'low']

        normalize:    If False, plot the raw numbers
                    If True, plot the proportions

        """
        # create labels
        target_names = list(target_names)

        accuracy = np.trace(cm) / float(np.sum(cm))
        misclass = 1 - accuracy

        accuracy = np.round(accuracy, 2)
        misclass = np.round(misclass, 2)

        if normalise:
            cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
            cm = np.round(cm, 2)

        # plot
        fig = figure_factory.create_annotated_heatmap(
            cm, x=target_names, y=target_names, colorscale="blues"
        )

        # add title
        fig.update_layout(
            title="CONFUSION MATRIX",
            yaxis_title="Actual Labels",
            xaxis_title="Predicted Labels \n\n(accuracy={:0.4f}; misclass={:0.4f})".format(
                accuracy, misclass
            ),
        )
        self.export_plot(fig, isMetric=True)

    def plot_roc_curve(self, y_true, y_probas):
        # make df
        fpr, tpr, _ = roc_curve(y_true, y_probas)

        fig = px.area(
            x=fpr,
            y=tpr,
            title=f"ROC Curve (AUC={np.round(auc(fpr, tpr),2):.4f})",
            labels=dict(x="False Positive Rate", y="True Positive Rate"),
        )

        # add baseline
        fig.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=0, y1=1)

        fig.update_yaxes(scaleanchor="x", scaleratio=0.5)
        fig.update_xaxes(constrain="domain")

        self.export_plot(fig, title="ROC Curve", isMetric=True)

    def plot_decile_plot(self, y_true, y_pred):
        decile = pd.qcut(y_true, 10, labels=np.arange(10, 0, -1))
        decile = np.round(decile.astype(float))

        # make df
        df = pd.DataFrame({"Decile": decile, "Y_true": y_true, "Y_pred": y_pred})
        df = df.groupby("Decile", as_index=False).mean()[["Decile", "Y_true", "Y_pred"]]
        df = pd.melt(
            df,
            id_vars=["Decile"],
            value_vars=["Y_true", "Y_pred"],
            value_name="Mean Values per Decile",
        )

        # plot
        fig = px.line(
            df, x="Decile", y="Mean Values per Decile", color="variable", markers=True
        )

        # add title
        fig.update_layout(
            title="DECILE",
            yaxis_title="MEAN VALUES PER DECILE",
            xaxis_title="DECILE",
        )
        self.export_plot(fig, isMetric=True)

    def plot_residual_plot(self, y_true, y_pred):
        # make df
        df = pd.DataFrame(
            {
                "Y_pred": y_pred,
                "Y_true": y_true,
                "Residual": np.array(y_true) - np.array(y_pred),
            }
        )

        # plot
        fig = px.scatter(
            df, x="Y_true", y="Residual", marginal_y="violin", trendline="ols"
        )

        # add title
        fig.update_layout(
            title="RESIDUALS OF PREDICTIONS",
            yaxis_title="RESIDUALS",
            xaxis_title="ACTUAL TARGET VALUES",
        )
        self.export_plot(fig, isMetric=True)

    def plot_predicted_vs_actual(self, y_true, y_pred):
        # make df
        df = pd.DataFrame(
            {
                "Y_pred": y_pred,
                "Y_true": y_true,
                "Residual": np.array(y_true) - np.array(y_pred),
            }
        )

        # plot
        fig = px.scatter(
            df, x="Y_true", y="Y_pred", marginal_y="violin", trendline="ols"
        )

        # add title
        fig.update_layout(
            title="ACTUAL VS PREDICTED",
            yaxis_title="PREDICTED VALUES",
            xaxis_title="ACTUAL TARGET VALUES",
        )
        self.export_plot(fig, isMetric=True)
