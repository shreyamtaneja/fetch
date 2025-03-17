from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_process_receipt_valid():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "Klarbrunn 12-PK 12 FL OZ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json()

def test_process_receipt_invalid_field():
    receipt = {
        "store": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            }
        ],
        "total": "35.35"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.json() == {"detail": "The receipt is invalid."}

def test_process_receipt_invalid_data():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "22-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            }
        ],
        "total": "35.35"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.json() == {"detail": "The receipt is invalid."}

def test_process_receipt_invalid_item():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.5"
            }
        ],
        "total": "35.35"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.json() == {"detail": "The receipt is invalid."}

def test_get_points_28():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "Klarbrunn 12-PK 12 FL OZ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    }
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}/points")
    assert response.status_code == 200
    assert "points" in response.json()
    assert response.json()["points"] == 28

def test_get_points_109():
    receipt = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            },{
            "shortDescription": "Gatorade",
            "price": "2.25"
            }
        ],
        "total": "9.00"
    }
    process_response = client.post("/receipts/process", json=receipt)
    receipt_id = process_response.json()["id"]

    response = client.get(f"/receipts/{receipt_id}/points")
    assert response.status_code == 200
    assert "points" in response.json()
    assert response.json()["points"] == 109

def test_get_points_invalid_id():
    response = client.get("/receipts/invalid_id/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "No receipt found for that ID."}