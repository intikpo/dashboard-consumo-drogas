from dash import html, dcc
import dash_bootstrap_components as dbc

# Tab 1 de Prevalencia de consumo
def get_tab_1_layout(df):
    return html.Div([
        dbc.Row([
            dbc.Alert(
                [
                "La ",
                html.B("prevalencia"),
                " hace referencia a la proporción de personas que admiten haber consumido alguna determinada droga alguna vez en la vida, en los últimos 12 meses o en los últimos 30 días."
                ], 
                color="success"),
        ]),
        dbc.Row(className='responsive-row', children=[
            dbc.Col([
                html.Label('Gestión:'),
                dcc.RangeSlider(
                    id='gestion-slider-1',
                    min=min(df['Gestion']),
                    max=max(df['Gestion']),
                    value=[min(df['Gestion']), max(df['Gestion'])],
                    marks={str(year): str(year) for year in df['Gestion'].unique()},
                    step=1
                ),
            ]),
            dbc.Col([
                html.Label('Sustancia:'),
                dcc.Dropdown(
                    id='sustancia-dropdown-1',
                    options=[{'label': i, 'value': i} for i in df['Sustancia'].unique()],
                    value='Alcohol'
                ),
            ]),
            dbc.Col([
                html.Label('Lugar:'),
                dcc.Dropdown(
                    id='lugar-dropdown-1',
                    options=[{'label': i, 'value': i} for i in df['Lugar'].unique()],
                    value='Bolivia'
                )
            ]),
        ]),
        html.Div(id='tab-1-content')
    ])

# Tab 2 de Edad de inicio e incidencia de consumo
def get_tab_2_layout(df):
    return html.Div([
        html.Div(id='tab-2-content'),
        html.Div([
            dbc.Row(className='responsive-row', children=[
                dbc.Col([
                    html.Label('Gestión:'),
                    dcc.RangeSlider(
                        id='gestion-slider-2',
                        min=min(df['Gestion']),
                        max=max(df['Gestion']),
                        value=[min(df['Gestion']), max(df['Gestion'])],
                        marks={str(year): str(year) for year in df['Gestion'].unique()},
                        step=1
                    ),
                ]),
                dbc.Col([
                    html.Label('Sustancia:'),
                    dcc.Dropdown(
                        id='sustancia-dropdown-2',
                        options=[{'label': i, 'value': i} for i in df['Sustancia'].unique()],
                        value='Alcohol'
                    ),
                ]),
            ]),
        ], className='filter-box')
        
    ])

# Tab 3 de Información
def get_tab_3_layout():
    return html.Div([
        html.Div(id='tab-3-content'),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                         dbc.CardBody([
                             html.H2("Datos de consumo de drogas lícitas e ilícitas en Bolivia"),
                             html.P("Los datos presentados corresponden a los estudios realizados por el gobierno boliviano sobre consumo de drogas lícitas e ilícitas. Estos estudios son:"),
                             html.Ul([
                                 html.Li("2007 - Estudio de prevalencia del consumo de drogas en hogares de diez ciudades de Bolivia"),
                                 html.Li("2014 - II Estudio Nacional de Prevalencia y Características del Consumo de Drogas en Hogares Bolivianos de nueve Ciudades Capitales de Departamento, más la ciudad de El Alto"),
                                 html.Li("2018 - III Estudio Nacional de Prevalencia y Características de Consumo de Drogas en Hogares de Ciudades Capitales de Departamento y El Alto"),
                                 html.Li("2023 - IV Estudio nacional de prevalencia y características del consumo de drogas en hogares bolivianos de nueve ciudades capitales de departamento más la ciudad de El Alto"),
                             ]),
                             html.Hr(),
                             html.P("Puede acceder a los documento, a los datos estadísticos tabulados y al código fuente en el siguiente enlace:"),
                             html.Ul([                                 
                                 html.Li(dbc.CardLink("GitHub", href="https://github.com/intikpo/dashboard-consumo-drogas"),)
                             ])
                         ]))
            ])
        ]),
    ])