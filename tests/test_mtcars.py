from fastapi.testclient import TestClient

from mtcars_api_sqlite_pd import app

client = TestClient(app)


class TestGet:
    response = client.get(
        '/v1/',
        params={
            'cyl': 4,
            'mpg_min': 10
        }
    )

    def test_mtcars_get(self):
        assert self.response.status_code == 200

    def test_no_data(self):
        r = client.get(
            '/v1/',
            params={'cyl': 16, 'mpg_min': 200}
        )
        assert r.status_code == 400
        assert r.json()['detail'] == 'No Rows Returned'


class TestPost:
    ferrari = {
        'name': 'Ferrari Enzo',
        'mpg': 8,
        'cyl': 12,
        'disp': 5998.80,
        'hp': 651,
        'drat': 100,  # wut?
        'wt': 3.020,
        'qsec': 11.3,
        'vs': 100,  # wut?
        'am': 1,
        'gear': 7,
        'carb': 1  # wut?
    }

    response = client.post(
        "/v1/",
        json=ferrari
    )

    def test_post(self):
        assert self.response.status_code == 200
        assert self.response.json() == 'success'

    def test_bad_data(self):
        r = client.post(
            "/v1/",
            json={'name': 'Fake Car'}
        )
        assert r.status_code == 422
