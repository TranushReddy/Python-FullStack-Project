from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.logic import FarmerManager, BuyerManager, CropManager, OrderManager

# -----------------------------------------------------------App Setup------------------------------------------------
app = FastAPI(title="Crop Management API", version="1.0")

# ------------------------------------------------------------CORS Middleware------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------Manager Instances------------------------------------------------
farmer_manager = FarmerManager()
buyer_manager = BuyerManager()
crop_manager = CropManager()
order_manager = OrderManager()


# ------------------------------------------------------------Data Models------------------------------------------------
class UserCreate(BaseModel):
    name: str
    email: str
    contact_number: str


class CROPCreate(BaseModel):
    farmer_id: int
    crop_name: str
    description: str = None
    available_quantity: float
    price_per_unit: float
    unit: str


class CROPUpdate(BaseModel):
    price_per_unit: float = None
    description: str = None


class PurchaseRequest(BaseModel):
    buyer_id: int
    crop_id: int
    quantity_purchased: float
    price_per_unit: float


# ------------------------------------------------------------Health Check------------------------------------------------
@app.get("/", tags=["App Status"])
def home():
    return {"message": "Crop Management API is running."}


# ------------------------------------------------------------Farmer Endpoints------------------------------------------------
@app.post("/farmers/register", tags=["Farmers"])
def register_farmer(user_data: UserCreate):
    response = farmer_manager.add_farmer(
        user_data.name, user_data.email, user_data.contact_number
    )
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400, detail=response.get("message") or response.get("error")
    )


@app.get("/farmers/", tags=["Farmers"])
def list_farmers():
    response = farmer_manager.get_farmers()
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="No farmers found.")


@app.delete("/farmers/{farmer_id}", tags=["Farmers"])
def delete_farmer(farmer_id: int):
    response = farmer_manager.remove_farmer(farmer_id)
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="Farmer not found.")


# ------------------------------------------------------------Buyer Endpoints------------------------------------------------
@app.post("/buyers/register", tags=["Buyers"])
def register_buyer(user_data: UserCreate):
    response = buyer_manager.add_buyer(
        user_data.name, user_data.email, user_data.contact_number
    )
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400, detail=response.get("message") or response.get("error")
    )


@app.get("/buyers/", tags=["Buyers"])
def list_buyers():
    response = buyer_manager.get_buyers()
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="No buyers found.")


@app.delete("/buyers/{buyer_id}", tags=["Buyers"])
def delete_buyer(buyer_id: int):
    response = buyer_manager.remove_buyer(buyer_id)
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="Buyer not found.")


# ------------------------------------------------------------Crop Endpoints------------------------------------------------
@app.post("/crops/", tags=["Crops"])
def create_crop_listing(crop: CROPCreate):
    response = crop_manager.add_crop_listing(
        crop.farmer_id,
        crop.crop_name,
        crop.description,
        crop.available_quantity,
        crop.price_per_unit,
        crop.unit,
    )
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400, detail=response.get("message") or response.get("error")
    )


@app.get("/crops/available", tags=["Crops"])
def get_available_crops():
    response = crop_manager.get_all_available_crops()
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="No available crops found.")


@app.get("/crops/farmer/{farmer_id}", tags=["Crops"])
def get_crops_for_farmer(farmer_id: int):
    response = crop_manager.get_crops_for_farmer(farmer_id)
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="Crops not found for farmer.")


@app.put("/crops/{crop_id}", tags=["Crops"])
def update_crop_listing(crop_id: int, crop: CROPUpdate):
    response = crop_manager.db.update_crop_details(
        crop_id, crop.price_per_unit, crop.description
    )
    if response.get("Success"):
        return response
    raise HTTPException(
        status_code=400, detail=response.get("message") or response.get("error")
    )


@app.delete("/crops/{crop_id}", tags=["Crops"])
def remove_crop_listing(crop_id: int):
    response = crop_manager.remove_crop_listing(crop_id)
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="Crop listing not found.")


# ------------------------------------------------------------Order Endpoints------------------------------------------------
@app.post("/orders/purchase", tags=["Orders"])
def initiate_purchase(request: PurchaseRequest):
    response = order_manager.handle_purchase(
        request.buyer_id,
        request.crop_id,
        request.quantity_purchased,
        request.price_per_unit,
    )
    if response.get("Success"):
        return {
            "message": "Purchase completed successfully.",
            "order_status": "Success",
        }
    raise HTTPException(
        status_code=409, detail=response.get("message") or response.get("error")
    )


@app.get("/orders/buyer/{buyer_id}", tags=["Orders"])
def get_buyer_orders(buyer_id: int):
    response = order_manager.get_orders_by_buyer(buyer_id)
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="Orders not found for buyer.")


@app.get("/orders/farmer/{farmer_id}", tags=["Orders"])
def get_farmer_orders(farmer_id: int):
    response = order_manager.get_orders_for_farmer(farmer_id)
    if response.get("Success"):
        return response
    raise HTTPException(status_code=404, detail="Orders not found for farmer.")
