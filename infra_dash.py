import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_bootstrap_components as dbc

from infra_layers import get_layers, get_tiles
import infra_assets
from infra_callbacks import map_callbacks

app = dash.Dash(
    title="dataSdec - Infra PE",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.LUX])

# para producao
# server = app.server

app.layout = html.Div([
    infra_assets.navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H2("Infraestrutura PE"),
            )],
            style={'marginBottom': 25}
        ),
        dbc.Row([
            dbc.Col(
                html.P(infra_assets.intro),
            ),
            dbc.Col(
                infra_assets.layer_dropdown
            )
        ],
            style={'marginBottom': 0}
        ),
        dbc.Row([
            dbc.Col(
                id="legendas"
            )],
            style={'marginBottom': 25}
        ),
        dbc.Row([
            dbc.Col([
                dl.Map(
                    dl.LayersControl(
                        get_tiles() +
                        [dl.EasyButton(icon=infra_assets.home_btn,
                                       n_clicks=0, id="btn")] +
                        [dl.LayerGroup(id="layer-ctrl")]),
                    center=[-6.7, -37.5],
                    id="map",
                    style={'width': '100%', 'height': '500px'}
                )]
            )],
            style={'marginBottom': 25}
        ),
        dbc.Row([
            dbc.Col(
                [html.H5("Atributos da camada"),
                 html.P("Tabelas de informações das camadas ativas.")]
            )],
            style={'marginBottom': 25}
        ),
        dbc.Row(
            dbc.Col(
                id="multi_tab",
                style={'marginBottom': 25}
            )
        ),
        dbc.Row([
            dbc.Col(
                [html.H5("Fontes de dados"),
                 html.P("CPRH, Infraero, CELPE, CHESF, EPE.")]
            )],
            style={'marginBottom': 25}
        )
    ]),
    infra_assets.footer,
],
)

map_callbacks(app)

if __name__ == '__main__':
    app.run_server("127.0.0.1", port=5000, debug=True)
    # para producao
    # server.run('0.0.0.0')
