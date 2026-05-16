from app.src.app import app


client = app.test_client()


def test_health():

    response = client.get("/health")

    assert response.status_code == 200


def test_version():

    response = client.get("/version")

    assert response.status_code == 200


def test_create_order():

    payload = {
        "customer": "Elvis",
        "items": [
            {
                "name": "Pizza",
                "quantity": 1
            }
        ]
    }

    response = client.post("/orders", json=payload)

    assert response.status_code == 201
