"""Model prediction request and response classes"""
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """Prediction request class that contains the relevant features.

    Args:
        BaseModel (BaseModel): JSON element request.
    """
    ingreso: float
    antiguedad_laboral_meses: int
    tiempo_desempleado: int
    trabajos_ultimos_5: int
    semanasCotizadas: int
    edad: int
    crecimiento_ingreso: float
    crecimiento_gral: float
    enigh: float


class PredictionResponse(BaseModel):
    """Prediction response class that contains the target features.

    Args:
        BaseModel (BaseModel): JSON element response.
    """
    scoring: float
    cluster: int
