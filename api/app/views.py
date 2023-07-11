"""API view that gives the predicted elements"""
from .models import PredictionRequest
from .utils import get_model, transform_to_dataframe


model = get_model()


def get_prediction(request: PredictionRequest):
    """Get the scoring prediction based on request.

    Args:
        request (PredictionRequest): Objet to be predicted.

    Returns:
        float: Scoring predicted.
    """
    data_to_predict = transform_to_dataframe(request)
    prediction = model.predict(data_to_predict)[0]
    return max(0, prediction)
