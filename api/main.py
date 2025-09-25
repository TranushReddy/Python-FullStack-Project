from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Set up the path to include the 'src' directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import FarmerManager, BuyerManager, CropManager, OrderManager

# -----------------------------------------------------------App Setup------------------------------------------------
app = FastAPI(title="Crop Management API", version="1.0")

# ------------------------------------------------------------Allow Frontend(Streamlit/React) to call the API------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

# Creating Manager Instances (Business logic)
farmer_manager = FarmerManager()
buyer_manager = BuyerManager()
crop_manager = CropManager()
order_manager = OrderManager()

# ------Data Models ------


class CROPCreate(BaseModel):
    """
    Schema for creating a new crop listing.
    """

    farmer_id: int
    crop_name: str
    description: str = None
    available_quantity: float
    price_per_unit: float
    unit: str


class CROPUpdate(BaseModel):
    """
    Schema for updating an existing crop listing.
    """

    price_per_unit: float = None
    description: str = None


class PurchaseRequest(BaseModel):
    """
    Schema for a buyer initiating a purchase.
    """

    buyer_id: int
    crop_id: int
    quantity_purchased: float
    price_per_unit: float


class UserCreate(BaseModel):
    name: str
    email: str
    contact_number: str


# -----------------------------------------------------------API Endpoints------------------------------------------------


@app.get("/", tags=["App Status"])
def home():
    """check if the API is running"""
    return {"message": "Crop Management API is running."}


# ---------------------------------------------------------- CROP ENDPOINTS ------------------------------------------------


@app.post("/crops/", tags=["Crops"])
def create_crop_listing(crop: CROPCreate):
    """Create a new crop listing."""
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
    else:
        raise HTTPException(
            status_code=400, detail=response.get("message") or response.get("error")
        )


@app.get("/crops/farmer/{farmer_id}", tags=["Crops"])
def get_crops_for_farmer(farmer_id: int):
    """Fetch all crops listed by a specific farmer."""
    response = crop_manager.get_crops_for_farmer(farmer_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail=response.get("message") or "Crops not found for farmer.",
        )


@app.get("/crops/available", tags=["Crops"])
def get_available_crops():
    """Fetch all currently available crop listings for buyers."""
    response = crop_manager.get_all_available_crops()
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail=response.get("message") or "No available crops found.",
        )


@app.put("/crops/{crop_id}", tags=["Crops"])
def update_crop_listing(crop_id: int, crop: CROPUpdate):
    """Update price or description of an existing crop listing."""
    response = crop_manager.db.update_crop_details(
        crop_id, crop.price_per_unit, crop.description
    )

    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=400, detail=response.get("message") or response.get("error")
        )


@app.delete("/crops/{crop_id}", tags=["Crops"])
def remove_crop_listing(crop_id: int):
    """Delete a crop listing by its ID."""
    response = crop_manager.remove_crop_listing(crop_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "Crop listing not found."
        )


# ---------------------------------------------------------- ORDER ENDPOINTS ------------------------------------------------


@app.post("/orders/purchase", tags=["Orders"])
def initiate_purchase(request: PurchaseRequest):
    """
    Handles the core business transaction: processes the order and atomically
    """
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
    else:
        raise HTTPException(
            status_code=409, detail=response.get("message") or response.get("error")
        )


@app.get("/orders/buyer/{buyer_id}", tags=["Orders"])
def get_buyer_orders(buyer_id: int):
    """Fetch all orders placed by a specific buyer."""
    response = order_manager.get_orders_by_buyer(buyer_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail=response.get("message") or "Orders not found for buyer.",
        )


@app.get("/orders/farmer/{farmer_id}", tags=["Orders"])
def get_farmer_orders(farmer_id: int):
    """Fetch all orders for a specific farmer's crops."""
    response = order_manager.get_orders_for_farmer(farmer_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail=response.get("message") or "Orders not found for farmer.",
        )


# ---------------------------------------------------------- FARMER & BUYER ENDPOINTS ------------------------------------------------


@app.post("/farmers/register", tags=["Farmers"])
def register_farmer(user_data: UserCreate):
    """Register a new farmer."""
    response = farmer_manager.add_farmer(
        user_data.name, user_data.email, user_data.contact_number
    )
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=400, detail=response.get("message") or response.get("error")
        )


@app.get("/farmers/", tags=["Farmers"])
def list_farmers():
    """List all registered farmers."""
    response = farmer_manager.get_farmers()
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "No farmers found."
        )


@app.post("/buyers/register", tags=["Buyers"])
def register_buyer(user_data: UserCreate):
    """Register a new buyer."""
    response = buyer_manager.add_buyer(
        user_data.name, user_data.email, user_data.contact_number
    )
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=400, detail=response.get("message") or response.get("error")
        )


@app.get("/buyers/", tags=["Buyers"])
def list_buyers():
    """List all registered buyers."""
    response = buyer_manager.get_buyers()
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "No buyers found."
        )


@app.delete("/farmers/{farmer_id}", tags=["Farmers"])
def delete_farmer(farmer_id: int):
    """Delete a farmer by their ID."""
    response = farmer_manager.delete_farmer(farmer_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "Farmer not found."
        )


@app.delete("/buyers/{buyer_id}", tags=["Buyers"])
def delete_buyer(buyer_id: int):
    """Delete a buyer by their ID."""
    response = buyer_manager.remove_buyer(buyer_id)
    if response.get("Success"):
        return response
    else:
        raise HTTPException(
            status_code=404, detail=response.get("message") or "Buyer not found."
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
