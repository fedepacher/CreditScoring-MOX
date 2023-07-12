from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_null_prediction():
    response = client.post('/v1/prediction', json={
                                                   "ingreso": 0,
                                                   "antiguedad_laboral_meses": 0,
                                                   "trabajos_ultimos_5": 0,
                                                   "edad": 0,
                                                   "crecimiento_ingreso": 0
                                                   })
    assert response.status_code == 200
    assert response.json()['scoring'] >= 0


def test_random_prediction():
    response = client.post('/v1/prediction', json={
                                                   "ingreso": 500,
                                                   "antiguedad_laboral_meses": 5,
                                                   "trabajos_ultimos_5": 5,
                                                   "edad": 56,
                                                   "crecimiento_ingreso": 555
                                                   })
    assert response.status_code == 200
    assert response.json()['scoring'] >= 0
