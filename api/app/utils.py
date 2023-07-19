"""Utils function to open ML model and transform dato to dataframe"""
import os
from io import BytesIO
import pandas as pd
import numpy as np
from joblib import load
from pydantic import BaseModel
from pandas import DataFrame
from sklearn.decomposition import PCA
from dvc import api
from io import StringIO


Entities = ['Aguascalientes', 'Baja California', 'Baja California Sur',
			'Campeche', 'Coahuila de Zaragoza', 'Colima', 'Chiapas', 'Chihuahua',
			'Ciudad de México', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo',
			'Jalisco', 'México', 'Michoacán de Ocampo', 'Morelos', 'Nayarit',
			'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo',
			'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas',
			'Tlaxcala', 'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']


def get_model(logging, filenema=''):
    """Get the ML model from google storage.

    Args:
        logging (loggin): Logging format.
        filenema (str): Filename.

    Returns:
        Pipeline: Return the model pipeline.
    """
    logging.info('Get model')
    try:
        model_path = os.environ.get('MODEL_PATH', f'model/{filenema}.pkl')
        logging.info(f'Path {model_path} loaded')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    try:
        with open(model_path,'rb') as model_file:
            model = load(BytesIO(model_file.read()))
            logging.info('Model file loaded')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    return model


def convert_input_data(logging, request: BaseModel):
    """Convert input JSON data into dataframe available for the ML model.

    Args:
        logging (logging): Logging format.
        request (BaseModel): JSON to be converted.

    Returns:
        Dataframe: Dataframe for the ML model.
    """
    df_path = api.read('./dataset/enigh.csv', remote='dataset-track')
    tabla_enigh = pd.read_csv(StringIO(df_path))
    df_path = api.read('./dataset/itaee_gral_2023.csv', remote='dataset-track')
    itaee_gral = pd.read_csv(StringIO(df_path))
    logging.info(f'Dataframe: {tabla_enigh.head(1)}')
    logging.info(f'Dataframe: {itaee_gral.head(1)}')
    client = transform_to_dataframe(logging=logging, class_model=request)
    merge_data_enigh(client, tabla_enigh)
    client['liquidez_porcentual'] = client.apply(calculate_percentage_liquidity, axis=1)
    client['costo_de_vida'] = client.apply(cost_of_living, axis=1)

    client = client.drop(['liquidez_lugar_actual', 'gasto_lugar_actual'] , axis= 1)

    merge_data_itaee(client, itaee_gral)

    df_modelo = client.drop(['lugar_actual'] , axis= 1)

    variables = ['decil_ingreso_ENIGH', 'liquidez_porcentual', 'costo_de_vida']
    pca = PCA(n_components=1)
    df_modelo['ENIGH'] = pca.fit_transform(df_modelo[variables])
    df_modelo = df_modelo.drop(columns=variables)

    return df_modelo


def transform_to_dataframe(logging, class_model: BaseModel) -> DataFrame:
    """Transform JSON data to a dataframe

    Args:
        logging (loggin): Loggin format.
        class_model (BaseModel): JSON data.

    Returns:
        DataFrame: Dataframe.
    """
    try:
        transition_dictionary = {key:[value] for key, value in class_model.model_dump().items()}
        data_frame = DataFrame(transition_dictionary)
        logging.info('Dataframe loaded')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    return data_frame



def merge_data_enigh(client, tabla_enigh):
    """Merge data from enigh table.

    Args:
        client (Dataframe): Input dataframe.
        tabla_enigh (Dataframe): Enigh dataframe.
    """
    for index, row in client.iterrows():
        lugar_actual = row['lugar_actual'].lower()
        matching_row = tabla_enigh[tabla_enigh['Entidades'].str.lower() == lugar_actual]
        if not matching_row.empty:
            client.loc[index, 'liquidez_lugar_actual'] = matching_row['Liquidez'].values[0]
            client.loc[index, 'gasto_lugar_actual'] = matching_row['Gasto Total'].values[0]
            decil_ingreso = np.digitize(row['ingreso'],
                                        bins=matching_row.loc[:, '1':'10'].values[0], right=False)
            client.loc[index, 'decil_ingreso_ENIGH'] = decil_ingreso
        else:
            client.loc[index, 'liquidez_lugar_actual'] = None
            client.loc[index, 'gasto_lugar_actual'] = None
            client.loc[index, 'decil_ingreso_ENIGH'] = None


def calculate_percentage_liquidity(row):
    """Calculate the liquidity percentage.

    Args:
        row (Series): Row of the dataframe.

    Returns:
        float: Liquidity percentage.
    """
    return ((row['ingreso'] - row['liquidez_lugar_actual']) / row['liquidez_lugar_actual']) * 100


def cost_of_living(row):
    """Calculate the living cost.

    Args:
        row (Series): Row of the dataframe.

    Returns:
        float: Living cost percentage.
    """
    return ((row['ingreso'] - row['gasto_lugar_actual']) / row['gasto_lugar_actual']) * 100


def merge_data_itaee(client, itaee_gral):
    """Merge data from itaee table.

    Args:
        client (Dataframe): Input dataframe.
        itaee_gral (Dataframe): Itaee dataframe.
    """
    if 'crecimiento_gral' not in client.columns:
        client['crecimiento_gral'] = None
    for index, row in client.iterrows():
        try:
            lugar_actual = row['lugar_actual'].lower()
            matching_row = itaee_gral[itaee_gral['entidad_federativa'].str.lower() == lugar_actual]
            if not matching_row.empty:
                client.loc[index, 'crecimiento_gral'] = matching_row['2023|Anual'].values[0]
        except AttributeError:
            client.loc[index, 'crecimiento_gral'] = None
