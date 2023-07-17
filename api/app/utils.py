"""Utils function to open ML model and transform dato to dataframe"""
import os
from io import BytesIO
from joblib import load
from sklearn.pipeline import Pipeline
from pydantic import BaseModel
from pandas import DataFrame


def get_model(logging, filenema=''):
    """Get the ML model from google storage.

    Args:
        logging (loggin): Loggin format.
        filenema (str): Filename.

    Returns:
        Pipeline: Return the model pipeline.
    """
    logging.info('Get model')
    try:
        model_path = os.environ.get('MODEL_PATH', f'model/{filenema}.pkl')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    try:
        with open(model_path,'rb') as model_file:
            model = load(BytesIO(model_file.read()))
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    return model


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
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    return data_frame
