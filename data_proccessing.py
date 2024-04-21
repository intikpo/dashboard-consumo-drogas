import pandas as pd

def load_data():
    # Carga de datos
    df = pd.read_excel("data/consumo-drogas.xlsx", sheet_name=None)
    return df

def get_data_prevalencia(df):
    df_prevalencia = df['prevalencia']
    return df_prevalencia

def get_data_incidencia(df):
    df_incidencia = df['incidencia']
    return df_incidencia

def get_data_edad(df):
    df_edad = df['edad']
    return df_edad