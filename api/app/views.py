"""API view that gives the predicted elements"""
from .models import PredictionRequest
from .utils import get_model, transform_to_dataframe


model_reg = get_model('model_reg')
model_clf = get_model('model_clf')
scaler = get_model('model_scaler')

# Función para clasificar a los clientes
def get_prediction(request: PredictionRequest):
    """Get the scoring and cluster prediction based on request.

    Args:
        request (PredictionRequest): Objet to be predicted.

    Returns:
        tuple: scoring and cluster predicted
    """
    client = transform_to_dataframe(request)
    cliente_scaled = scaler.transform(client)
    puntuacion_credito = model_reg.predict(cliente_scaled)[0]
    cluster_predicho = model_clf.predict(cliente_scaled)[0]

    return puntuacion_credito, cluster_predicho
