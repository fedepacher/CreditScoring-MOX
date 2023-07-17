"""API view that gives the predicted elements"""
from .models import PredictionRequest
from .utils import get_model, transform_to_dataframe


def get_models(logging=''):
    """Get model from DVC storage

    Args:
        logging (str, optional): Logging format.
    """
    global scaler
    global model_reg
    global model_clf
    scaler = get_model(logging, filenema='model_scaler')
    model_reg = get_model(logging, filenema='model_reg')
    model_clf = get_model(logging, filenema='model_clf')


# Función para clasificar a los clientes
def get_prediction(logging, request: PredictionRequest):
    """Get the scoring and cluster prediction based on request.

    Args:
        logging (loggin): Loggin format.
        request (PredictionRequest): Objet to be predicted.

    Returns:
        tuple: scoring and cluster predicted
    """
    client = transform_to_dataframe(logging=logging, class_model=request)
    try:
        cliente_scaled = scaler.transform(client)
        logging.info('Loaded scaler')
    except Exception as err:
        logging.error('Error getting data: ' + str(err))
    puntuacion_credito = model_reg.predict(cliente_scaled)[0]
    cluster_predicho = model_clf.predict(cliente_scaled)[0]

    return puntuacion_credito, cluster_predicho
