from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from src.logic import CropMarketplaceManager, OrderManager

# -----------------------------------------------------------App Setup------------------------------------------------
app = FastAPI(title="Simplified Crop Marketplace API", version="1.0")

# ------------------------------------------------------------CORS Middleware------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------Manager Instances------------------------------------------------
marketplace_manager = CropMarketplaceManager()
order_manager = OrderManager()


# ------------------------------------------------------------Data Models------------------------------------------------
class CropListingCreate(BaseModel):
    farmer_name: str
    farmer_contact: Optional[str] = None
    crop_name: str
    description: Optional[str] = None
    available_quantity: float
    price_per_unit: float
    unit: str


class PurchaseRequest(BaseModel):
    crop_id: int
    buyer_name: str
    buyer_contact: str
    quantity_purchased: float
    price_per_unit: float


# ------------------------------------------------------------Health Check------------------------------------------------
@app.get("/", tags=["App Status"])
def home():
    return {"message": "Simplified Crop Marketplace API is running."}


# ------------------------------------------------------------Marketplace Endpoints------------------------------------------------
@app.post("/crops/", tags=["Marketplace"])
def create_crop_listing(crop: CropListingCreate):
    response = marketplace_manager.add_crop_listing(crop.model_dump())
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400, detail=response.get("message") or response.get("error")
    )


@app.get("/crops/available", tags=["Marketplace"])
def get_available_crops():
    response = marketplace_manager.get_all_available_crops()
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400,
        detail=response.get("error") or "Failed to connect to database.",
    )


# ------------------------------------------------------------Order Endpoints------------------------------------------------
@app.post("/orders/purchase", tags=["Orders"])
def initiate_purchase(request: PurchaseRequest):
    response = order_manager.handle_purchase(
        request.crop_id,
        request.buyer_name,
        request.buyer_contact,
        request.quantity_purchased,
        request.price_per_unit,
    )
    if response.get("Success"):
        return {
            "message": "Purchase completed successfully.",
            "order_status": "Success",
        }

    status_code = 400
    if "insufficient stock" in response.get("message", "").lower():
        status_code = 409

    raise HTTPException(
        status_code=status_code, detail=response.get("message") or response.get("error")
    )


@app.get("/orders/", tags=["Orders"])
def get_all_orders():
    response = order_manager.get_all_orders()
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400,
        detail=response.get("error") or "Failed to connect to database.",
    )
