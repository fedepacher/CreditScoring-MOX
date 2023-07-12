"""API creation"""
from fastapi import FastAPI
from .app.models import PredictionResponse, PredictionRequest
from .app.views import get_prediction


app = FastAPI(docs_url='/')


@app.post('/v1/prediction')
def make_model_prediction(request: PredictionRequest):
    """API call to predict incoming data.

    Args:
        request (PredictionRequest): Incoming JSON request.

    Returns:
        JSON: JSON format scoring predicted output.
    """
    return PredictionResponse(scoring=get_prediction(request))
