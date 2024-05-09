# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

class Explanations:

    def __init__(self, xai):
        self.xai = xai

    def setup_layout(self):
        tabs_style = {
            'height': '44px',
            'backgroundColor': 'white',
        }
        tab_style = {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            'fontWeight': 'bold',
            'backgroundColor': 'white',  
        }
        tab_selected_style = {
            'borderTop': 'none',  
            'borderBottom': 'none',
            'backgroundColor': 'white',
            'color': 'black',
            'padding': '6px',
        }
        content_style = {
            'border': 'none',
            'padding': '0px',
        }

        if self.mode == "global":
            self.app.layout = html.Div(
                [
                    dcc.Tabs(
                        id="tabs",
                        value="tab-overall",
                        children=[
                            dcc.Tab(label="Overall", value="tab-overall", style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label="Feature Attribution", value="tab-features", style=tab_style, selected_style=tab_selected_style),
                        ],
                        style=tabs_style
                    ),
                    html.Div(id="tabs-content", style=content_style),
                ],
                className="container-fluid",  # Use 'container-fluid' for full width
                style={'padding': '0px', 'backgroundColor': 'white'}  # Remove padding and set background to white
            )
        else:
            self.app.layout = html.Div(
                [
                    dcc.Tabs(
                        id="tabs",
                        value="predictions",
                        children=[
                            dcc.Tab(label="Local Explanations", value="predictions", style=tab_style, selected_style=tab_selected_style),
                        ],
                        style=tabs_style
                    ),
                    html.Div(id="tabs-content"),
                ],
                className="container mt-4",
                style={'padding': '0px', 'backgroundColor': 'white'}  # Remove padding and set background to white
            )

    def setup_callbacks(self):
        @self.app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
        def render_content(tab):
            if self.mode == "global":
                if tab == "tab-overall":
                    return html.Div(
                        [dcc.Graph(figure=self.xai.feature_importance_fig)],
                        style={'marginTop': 20, 'marginBottom': 20}
                    )
                elif tab == "tab-features":
                    dropdown_options = [{'label': feat, 'value': feat} for feat in self.xai.inputs.X.columns.to_list()]
                    return html.Div(
                        [
                            dcc.Dropdown(
                                id='feature-dropdown',
                                options=dropdown_options,
                                value=self.xai.inputs.X.columns.to_list()[0],
                                style={'marginBottom': 20, 'marginTop': 20}  # Add spacing around the dropdown
                            ),
                            html.Div(id='feature-graph-container', style={'marginTop': 20})  # Add spacing above the graph container if needed
                        ]
                    )
            elif self.mode == "local":
                dropdown_options = [{'label': f'Row {i+1}', 'value': i} for i in range(len(self.xai.local_explanation_figs))]
                return html.Div(
                    [
                        dcc.Dropdown(
                            id='local-figure-dropdown',
                            options=dropdown_options,
                            value=0,
                            style={'marginBottom': 20, 'marginTop': 20}  # Add spacing around the dropdown
                        ),
                        html.Div(id='local-figure-container', style={'marginTop': 20})  # Container for the graph
                    ]
                )
            
        # This callback updates the graph based on the selected figure from the dropdown
        @self.app.callback(Output('local-figure-container', 'children'), [Input('local-figure-dropdown', 'value')])
        def update_local_figure(selected_index):
            if selected_index is not None:
                return dcc.Graph(figure=self.xai.local_explanation_figs[selected_index])


        @self.app.callback(Output('feature-graph-container', 'children'), [Input('feature-dropdown', 'value')])
        def update_graph(selected_feature):
            selected_index = self.xai.inputs.X.columns.to_list().index(selected_feature)
            return dcc.Graph(figure=self.xai.feature_attributions_figs[selected_index])
        
    def create_app(self):
        self.app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'], suppress_callback_exceptions=True)
        self.setup_layout()
        self.setup_callbacks()
        self.app.run_server(debug=True, jupyter_mode="inline")

    def explain_global(self):
        self.mode = "global"
        self.create_app()

    def explain_local(self):
        self.mode = "local"
        self.create_app()
