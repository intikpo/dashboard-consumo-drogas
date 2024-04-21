import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts import get_tab_1_layout, get_tab_2_layout, get_tab_3_layout
from callbacks import register_callbacks
import data_proccessing as dp

# cargar datos
df = dp.load_data()
df_prevalencia = dp.get_data_prevalencia(df)
df_incidencia = dp.get_data_incidencia(df)
df_edad = dp.get_data_edad(df)

# Iniciar la aplicación de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/styles.css'])

# Establecer el diseño de la aplicación
app.layout = html.Div([
    dbc.Row([
        html.Header([
            html.H1("Bolivia: Consumo de Drogas lícitas e ilícitas")
        ])
    ]),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Prevalencia de consumo', value='tab-1', children=get_tab_1_layout(df_prevalencia)),
        dcc.Tab(label='Edad de inicio de consumo', value='tab-2', children=get_tab_2_layout(df_incidencia)),
        dcc.Tab(label='Información', value='tab-3', children=get_tab_3_layout())
    ])
])

# Registrar los callbacks
register_callbacks(app, df_prevalencia, df_incidencia, df_edad)

if __name__ == "__main__":
    app.run_server()