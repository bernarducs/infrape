"""
manipulação dos dash-callbacks
"""
import dash_html_components as html
from dash.dependencies import Output, Input

from infra_layers import get_layers
from infra_assets import subtitles, get_tabs

map_layers = get_layers()


def map_callbacks(app):
    @app.callback(Output("vias_popup", "children"),
                  [Input("vias", "click_feature")])
    def vias_click(feature):
        if feature is not None:
            return f"Trecho: {feature['properties']['Código de Trecho']}"

    @app.callback(Output("gasoduto_popup", "children"),
                  [Input("gasoduto", "click_feature")])
    def gas_click(feature):
        if feature is not None:
            return [html.P(f"Nome: {feature['properties']['Name']}"),
                    html.P(f"Finalidade: {feature['properties']['Finalidade']}")]

    @app.callback(Output("lt_chesf_popup", "children"),
                  [Input("lt_chesf", "click_feature")])
    def lt_chesf_click(feature):
        if feature is not None:
            return [html.P(f"nome: {feature['properties']['Nome']}"),
                    html.P(f"Tensão: {feature['properties']['Tensão']}")]

    @app.callback(Output("municipios_popup", "children"),
                  [Input("municipios", "click_feature")])
    def municipios_click(feature):
        if feature is not None:
            return f"{feature['properties']['Município']}"

    @app.callback(Output("layer-ctrl", "children"),
                  Input("layer-dropdown", "value"))
    def show_layers(dropdown_values):
        if dropdown_values is not None:
            return [layer for layer in map_layers
                    if layer.id in dropdown_values]

    @app.callback(Output("map", "center"),
                  Output("map", "zoom"),
                  [Input("btn", "n_clicks")])
    def center_map(click_center):
        center = [-6.7, -37.5]
        zoom = 6.5
        return center, zoom

    @app.callback(Output("legendas", "children"),
                  Input("layer-dropdown", "value"))
    def show_subs(dropdown_values):
        if dropdown_values is not None:
            layers = [layer.id for layer in map_layers
                      if layer.id in dropdown_values]
            result = list()
            result.extend([html.P("Legendas:")])
            for layer in layers:
                result.extend(subtitles[layer])
            return result

    @app.callback(Output("multi_tab", "children"),
                  Input("layer-dropdown", "value"))
    def multi_tab(values):
        if values is not None:
            tabs = get_tabs(values)
            return tabs
