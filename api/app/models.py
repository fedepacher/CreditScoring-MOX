"""Model prediction request and response classes"""
from pydantic import BaseModel


Entities = ['Aguascalientes', 'Baja California', 'Baja California Sur',
			'Campeche', 'Coahuila de Zaragoza', 'Colima', 'Chiapas', 'Chihuahua',
			'Ciudad de México', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo',
			'Jalisco', 'México', 'Michoacán de Ocampo', 'Morelos', 'Nayarit',
			'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo',
			'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas',
			'Tlaxcala', 'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']


class IncomeRequest(BaseModel):
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
    lugar_actual: str


    def values_checker(self):
        """Check input parameters.

        Returns:
            bool: True if request has correct params.
        """
        if self.ingreso < 0 or self.antiguedad_laboral_meses < 0 or self.tiempo_desempleado < 0 or \
           self.trabajos_ultimos_5 < 0 or self.semanasCotizadas < 0 or self.edad < 0 or \
           self.crecimiento_ingreso < 0 or (self.crecimiento_ingreso > 0 and self.ingreso == 0) or \
           (self.lugar_actual.lower() not in [x.lower() for x in Entities]):
            return False
        return True


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
    ENIGH: float


class PredictionResponse(BaseModel):
    """Prediction response class that contains the target features.

    Args:
        BaseModel (BaseModel): JSON element response.
    """
    scoring: float
    cluster: int
