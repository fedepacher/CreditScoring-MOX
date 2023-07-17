"""Utils function to open ML model and transform dato to dataframe"""
import os
from io import BytesIO
from joblib import load
from sklearn.pipeline import Pipeline
from pydantic import BaseModel
from pandas import DataFrame


def get_model(filenema='') -> Pipeline:
    """Get the ML model from google storage.

    Args:
        filenema (str): Filename.

    Returns:
        Pipeline: Return the model pipeline.
    """
    model_path = os.environ.get('MODEL_PATH', f'model/{filenema}.pkl')
    with open(model_path,'rb') as model_file:
        model = load(BytesIO(model_file.read()))
    return model


def transform_to_dataframe(class_model: BaseModel) -> DataFrame:
    """Transform JSON data to a dataframe

    Args:
        class_model (BaseModel): JSON data.

    Returns:
        DataFrame: Dataframe.
    """
    transition_dictionary = {key:[value] for key, value in class_model.model_dump().items()}
    data_frame = DataFrame(transition_dictionary)
    return data_frame
