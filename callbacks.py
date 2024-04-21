import os
import base64
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from dash import html, dcc

# Directorio donde se encuentran las banderas
FLAG_DIR = "assets/flags/"

# configuraciones disponibles en cada gráfico plotly
config_options = {
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan', 'lasso', 'zoom', 'select']
}

# Ubicación de íconos de banderas
city_flags = {
    "Sucre": "Sucre.png",
    "La Paz": "La Paz.png",
    "El Alto": "El Alto.png",
    "Cochabamba": "Cochabamba.png",
    "Oruro": "Oruro.png",
    "Potosí": "Potosí.png",
    "Tarija": "Tarija.png",
    "Santa Cruz de la Sierra": "Santa Cruz de la Sierra.png",
    "Trinidad": "Trinidad.png",
    "Cobija": "Cobija.png"
}

def register_callbacks(app, df_prevalencia, df_incidencia, df_edad):
    
    @app.callback(
        Output('tab-1-content', 'children'),
        [Input('gestion-slider-1', 'value'),
         Input('sustancia-dropdown-1', 'value'),
         Input('lugar-dropdown-1', 'value')])
    def render_tab_1(gestion_range, sustancia, lugar):
        # Filtros para grafico 1 de Prevalencia de consumo
        start_year, end_year = gestion_range
        filtered_df_bars = df_prevalencia[
            (df_prevalencia['Gestion'] >= start_year) &
            (df_prevalencia['Gestion'] <= end_year) &
            (df_prevalencia['Sustancia'] == sustancia) &
            (df_prevalencia['Lugar'] == lugar) &
            (df_prevalencia['Sexo'] == 'Total')]
        
        # Gráfico 1 de Prevalencia de consumo
        fig_bars = px.bar(filtered_df_bars, x='Gestion', y='Valor', 
                         color='Prevalencia de consumo', barmode='group', text_auto=True)
        fig_bars.update_layout(
            title= {
                'text': f"{lugar}: Prevalencia de Consumo de {sustancia}",
                'xanchor': 'center',
                'yanchor': 'top',
                'x': 0.5,
                }
            )

        # Filtros para grafico 2 de Ranking de ciudades
        filtered_df_ciudades = df_prevalencia[
            (df_prevalencia['Sustancia'] == sustancia) &
            (df_prevalencia['Lugar'] != 'Bolivia') &
            (df_prevalencia['Prevalencia de consumo'] == 'Vida') &
            (df_prevalencia['Sexo'] == 'Total')
        ].sort_values('Valor', ascending=True)

        # Gráfico 2 de Ranking de ciudades
        fig_ciudades = go.Figure(data=[
            go.Bar(
                name=str(g), 
                y=filtered_df_ciudades[filtered_df_ciudades['Gestion'] == g]['Lugar'], 
                x=filtered_df_ciudades[filtered_df_ciudades['Gestion'] == g]['Valor'], 
                orientation='h',
                textposition='auto',
                marker=dict(color=filtered_df_ciudades[filtered_df_ciudades['Gestion'] == g]['Valor'],
                    colorscale='Greens')
            )
            for g in sorted(filtered_df_ciudades['Gestion'].unique(), reverse=True)
        ])
       
        # Obtener nombres de ciudades y sus respectivas banderas
        city_names = []
        city_images = []
        for city, flag_file in city_flags.items():
            city_names.append(city)
            flag_path = os.path.join(FLAG_DIR, flag_file)
            encoded_image = base64.b64encode(open(flag_path, 'rb').read())
            city_images.append(f"data:image/png;base64,{encoded_image.decode()}")
        
        #  Agregamos las banderas al gráficos
        for city, flag_url in zip(city_names, city_images):
            fig_ciudades.add_layout_image(
                dict(
                    source=flag_url,
                    xref="x2 domain", yref="y",
                    x=0, y=city,
                    sizex=0.5, sizey=0.5,
                    xanchor="left", yanchor="middle"
                )
            )
            
        fig_ciudades.update_layout(
            barmode='group', 
            yaxis={'categoryorder': 'total ascending'},
            title={
                'text': f"Bolivia: Ranking de ciudades por <br>prevalencia de Consumo de {sustancia}",
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.00,
                xanchor="right",
                x=1
            )
        )
        # Establecer la leyenda seleccionada por defecto solo para el año 2023
        fig_ciudades.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                                    if trace.name != str(2023) 
                                    else trace.update(visible=True))
        
        # Filtros para gráfico 3 de prevalencia por sexo
        df_sexo = df_prevalencia[
            (df_prevalencia['Gestion'] == 2023) &
            (df_prevalencia['Lugar'] == 'Bolivia') &
            (df_prevalencia['Sexo'] != 'Total') &
            (df_prevalencia['Prevalencia de consumo'] == 'Vida')]
        df_sexo.loc[:,'Suma_Hombres_Mujeres'] = df_sexo.groupby('Sustancia')['Valor'].transform('sum')
        df_sexo = df_sexo.sort_values(by='Suma_Hombres_Mujeres', ascending=False).drop(columns='Suma_Hombres_Mujeres')
        
        # Gráfico 3 de prevalencia por sexo, para gestion 2023
        fig_sexo = px.funnel(df_sexo, 
                             x='Valor', 
                             y='Sustancia', 
                             color='Sexo')
        fig_sexo.update_layout(
            title = {
                'text': "Bolivia: Prevalencia de consumo en 2023, <br>por sexo y sustancia",
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
                },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.00,
                xanchor="right",
                x=1,
                title=''
            ),
            margin=dict(
                t=100,  # Margen superior para el título
            )
        )
        
        # Devolvemos los gráficos
        return html.Div([
            dbc.Row(className='responsive-row', children=[
                dbc.Col(dcc.Graph(figure=fig_bars, 
                                  className='plot-container',
                                  config=config_options))
            ]),
            html.Hr(),
            dbc.Row(className='responsive-row', children=[
                dbc.Col(dcc.Graph(figure=fig_ciudades, className='plot-container',
                                  config=config_options)),
                dbc.Col(dcc.Graph(figure=fig_sexo, className='plot-container',
                                  config=config_options)),
            ])
        ])

    @app.callback(
        Output('tab-2-content', 'children'),
        [Input('gestion-slider-2', 'value'),
         Input('sustancia-dropdown-2', 'value')])
    def render_tab_2(gestion_range, droga):
        start_year, end_year = gestion_range
        
        # Filtros para gráfico 4 de edad de inicio de consumo
        filtered_df_edad = df_edad[
            (df_edad['Lugar'] == 'Bolivia') &
            (df_edad['Medida'] == 'Media')
        ]
        
        # Gráfico 4 de edad de inicio de consumo
        sustancias_unicas = filtered_df_edad['Sustancia'].unique()
        
        fig_edad = make_subplots(rows=1, cols=2, shared_yaxes=True,
                                 subplot_titles=("Sustancias ilícitas", "Sustancias lícitas"))
        
        for i, sustancia in enumerate(sustancias_unicas):
            fig_edad.add_trace(
                go.Scatter(
                    x=filtered_df_edad[filtered_df_edad['Sustancia'] == sustancia]['Gestion'],
                    y=filtered_df_edad[(filtered_df_edad['Sustancia'] == sustancia) &
                                       (filtered_df_edad['Tipo Sustancia'] == 'Ilícita')]['Valor'],
                    mode='lines+markers',
                    name=sustancia,
                ),
                row=1, col=1
            )
            
            fig_edad.add_trace(
                go.Scatter(
                    x=filtered_df_edad[filtered_df_edad['Sustancia'] == sustancia]['Gestion'],
                    y=filtered_df_edad[(filtered_df_edad['Sustancia'] == sustancia) &
                                       (filtered_df_edad['Tipo Sustancia'] == 'Lícita')]['Valor'],                    mode='lines+markers',
                    name=sustancia,
                ),
                row=1, col=2
            )
        fig_edad.update_layout(
            title={
                'text':"Bolivia: Edad promedio de inicio de consumo",
                'xanchor': 'center',
                'yanchor': 'top',
                'x': 0.5,
            },
            xaxis1_title="Año",
            xaxis2_title="Año",
            yaxis_title="Edad promedio (años)",
            legend_title="Sustancia",
        )
        
        # Filtros para grafico 5 de incidencia
        filtered_df_incidencia = df_incidencia[
            (df_incidencia['Gestion'] >= start_year) &
            (df_incidencia['Gestion'] <= end_year) &
            (df_incidencia['Sustancia'] == droga)]
        
        # Gráfico 5 de incidencia de consumo
        fig_bars = px.bar(filtered_df_incidencia, x='Gestion', y='Valor', 
                         color='Incidencia', barmode='group', text_auto=True)
        fig_bars.update_layout(
            title= {
                'text': f"Bolivia: Incidencia de Consumo de {droga}",
                'xanchor': 'center',
                'yanchor': 'top',
                'x': 0.5,
                } 
            )
        
        # Devolvemos gráficos
        return html.Div([
                dcc.Graph(figure=fig_edad, className='plot-container',
                          config=config_options),
                dbc.Row([
                    dbc.Alert(
                        [
                        "La ",
                        html.B("incidencia "),
                        " es la proporción de personas que admiten haber consumido alguna determinada droga por ",
                        html.B("primera vez "),
                        " en el último año, o en los últimos 30 días"
                        ], 
                        color="success"),
                    ]),
                dcc.Graph(figure=fig_bars, className='plot-container',
                          config=config_options)
            ])
