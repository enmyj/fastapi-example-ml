import pytest
import pandas as pd
from fastapi.testclient import TestClient

from iris_model_api import app

client = TestClient(app)

test_data = {
    'sepal_length': [0, 1],
    'sepal_width': [1, 2],
    'petal_length': [2, 3],
    'petal_width': [3, 4]
}
test_df = pd.DataFrame(test_data)


class TestIris():
    response = client.post(
        "/predict/",
        json={'data': test_df.to_dict(orient='records')}
    )

    def test_status_code(self):
        assert self.response.status_code == 200

    def test_success_json(self):
        assert self.response.json() == '["Iris-setosa", "Iris-virginica"]'

    def test_bad_body(self):
        r = client.post(
            '/predict/',
            json={'data': [{'sepal': 4}]}
        )
        assert r.status_code == 422

    def test_bad_types(self):
        r = client.post(
            '/predict/',
            json={
                'data': [{
                    'sepal_length': 'a',
                    'sepal_width': 'b',
                    'petal_length': 'c',
                    'petal_width': 'd'
                }]
            }
        )
        assert r.status_code == 422
