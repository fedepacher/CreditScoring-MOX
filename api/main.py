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
    score_cliente, cluster_cliente = get_prediction(request)
    return PredictionResponse(scoring=round(score_cliente*1000, 2), cluster=cluster_cliente)
