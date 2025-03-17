from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import uuid
import math
from datetime import datetime

app = FastAPI(
    title="Receipt Processor",
    description="A simple receipt processor",
    version="1.0.0"
)

# In-memory storage for receipts and points
receipts_db = {}
points_db = {}

# Pydantic models for request and response validation
class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$")
    purchaseDate: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    purchaseTime: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    items: List[Item]
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")

class ReceiptResponse(BaseModel):
    id: str = Field(..., pattern=r"^\S+$")

class PointsResponse(BaseModel):
    points: int

# Custom exception handler for RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path == "/receipts/process":
        return JSONResponse(
            status_code=400,
            content={"detail": "The receipt is invalid."}
        )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.post("/receipts/process", response_model=ReceiptResponse)
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    receipts_db[receipt_id] = receipt
    # Points calculation
    points = sum([1 for c in receipt.retailer if c.isalpha()])
    if float(receipt.total).is_integer():
        points += 50
    if float(receipt.total) % 0.25 == 0:
        points += 25
    points += 5 * (len(receipt.items) // 2)
    for item in receipt.items:
        if len(item.shortDescription) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)
    if int(receipt.purchaseDate[-2:]) % 2 != 0:
        points += 6
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M").time()
    if purchase_time > datetime.strptime("14:00", "%H:%M").time() and purchase_time < datetime.strptime("16:00", "%H:%M").time():
        points += 10
    points_db[receipt_id] = points
    return {"id": receipt_id}

@app.get("/receipts/{id}/points", response_model=PointsResponse)
async def get_points(id: str = Path(..., pattern=r"^\S+$")):
    if id not in points_db:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": points_db[id]}

