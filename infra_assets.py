"""
elementos que farão parte do dashboard como textos, imgs,
e dash-components como dropdowns, checklists, tabelas, etc.
"""
import json

import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

# ----- textos
intro = "No mapa abaixo é possível visualizar os principais equipamentos de " \
        "infraestrutura do estado como aeroportos, subestações, gasodutos, " \
        "usinas eólicas e fotovoltáicas - e cruzar com as principais " \
        "indústrias e empresas de diversas cadeias produtivas instaladas. " \
        "Use a caixa de seleção abaixo para adicionar ou remover camadas."

# ----- assets
assets = {
    "municipios": {
        "nome": "Municípios",
        "tipo": "area",
        "url": "assets/icons/municipios.png",
        "color": "#c0c0c0",
        "weight": "1",
        "opacity": "0",
        "geojson": "assets/layers/limite_municipal.geojson"},
    "aero": {
        "nome": "Aeroportos/Aeródromos",
        "tipo": "point",
        "url": "assets/icons/aero.png",
        "geojson": "assets/layers/aerodromos.geojson"},
    "vias": {
        "nome": "Vias",
        "tipo": "line",
        "url": "assets/icons/vias.png",
        "color": "#F8981D",
        "weight": "2",
        "opacity": "0.8",
        "geojson": "assets/layers/vias_principais.geojson"},
    "gasoduto": {
        "nome": "Gasodutos",
        "tipo": "line",
        "url": "assets/icons/gasodutos.png",
        "color": "#F93F17",
        "weight": "2",
        "opacity": "0.8",
        "geojson": "assets/layers/gasodutos.geojson"},
    "hidreletricas": {
        "nome": "Hidrelétricas",
        "tipo": "point",
        "url": "assets/icons/hidreletricas.png",
        "geojson": "assets/layers/hidreletricas.geojson"},
    "lt_chesf": {
        "nome": "Linhas de transmissão (CHESF)",
        "tipo": "line",
        "url": "assets/icons/lt_chesf.png",
        "color": "#6494AF",
        "weight": "2",
        "opacity": "0.8",
        "geojson": "assets/layers/linhas_transmissao.geojson"},
    "sub_chesf": {
        "nome": "Subestações (CHESF)",
        "tipo": "point",
        "url": "assets/icons/sub_chesf.png",
        "geojson": "assets/layers/subestacoes.geojson"},
    "eolica": {
        "nome": "Parques eólicos",
        "tipo": "point",
        "url": "assets/icons/eolica.png",
        "geojson": "assets/layers/parques_eolicos.geojson"},
    "resid_sol": {
        "nome": "Resíduos sólidos",
        "tipo": "point",
        "url": "assets/icons/resid.png",
        "geojson": "assets/layers/residuos_solidos.geojson"},
}

# ----- legendas
subtitles = {k: [html.Img(src=v['url']),
                 html.Span(f" {v['nome']}", style={"marginRight": "15px"})]
             for k, v in assets.items()}


# ---- df info layers
def get_dataframe(path):
    with open(path, 'r') as f:
        data = json.load(f)
        df = pd.DataFrame([x['properties'] for x in data['features']])
        df.drop_duplicates(inplace=True)
        return df


dfs_dict = {k: {'nome': v['nome'], 'df': get_dataframe(v['geojson'])}
            for k, v in assets.items()}


def get_tabs(layers_name):
    dfs = {k: v for k, v in dfs_dict.items() if k in layers_name}

    table_dict = dict()
    for key, value in dfs.items():
        table = dash_table.DataTable(
            id=f"table_{key}",
            columns=[{"name": i.upper(), "id": i}
                     for i in value['df'].columns],
            data=value['df'].to_dict('records'),
            # page_size=40,  # paginação
            fixed_rows={'headers': True},
            # style_table={'overflowX': 'auto', 'overflowY': 'auto'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'height': 'auto',
                'minWidth': 100, 'maxWidth': 200, 'width': 125},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'backgroundColor': 'lavender'
            }
        )
        table_dict[value['nome']] = table
    tabs = [dcc.Tab(label=k, children=[v]) for k, v in table_dict.items()]
    return dcc.Tabs(tabs)


# ---- botão centralizar
home_btn = f"<img src='assets/icons/home.png'>"

# ---- dash components
navbar = dbc.Navbar(
    [
        html.A([
            dbc.Row(
                dbc.Col(dbc.NavbarBrand("SDECdata"), width=2)
            )]
        ),
        html.A([
            dbc.Row(
                dbc.Col(dbc.NavbarBrand("Secretaria de Desenvolvimento "
                                        "Econômico de Pernambuco",
                                        style={'fontSize': '75%'}),
                        width=8)
            )]
        )
    ],
    id="navbar-content",
    color="#0f3057",
    dark=True,
    className="desktop-navbar",
    style={'marginBottom': 25, 'height': 50}
)

layer_dropdown = html.Div([
    dcc.Dropdown(
        id="layer-dropdown",
        options=[{"label": v['nome'], "value": k}
                 for k, v in assets.items()],
        value="municipios", multi=True, searchable=False,
        placeholder="Selecione uma camada"
    )
])

footer = html.Footer(
    [
        dbc.Container(
            dbc.Row([
                dbc.Col([
                    html.P("SDECdata"),
                    html.P("Sec. de Desenvolvimento Econômico "
                           "de Pernambuco")
                ]),
                dbc.Col([
                    html.P("Confira outro de nosso paineis:"),
                    html.Ul([
                        html.Li("Comércio Exterior"),
                         html.Li("Emprego")
                    ])
                ])
            ], style={'marginTop': '25px'})
        )
    ],
    id="footer-content",
    className="desktop-footer",
    style={'height': 150, 'backgroundColor': '#e7e7de',
           'display': 'flex'}
)
