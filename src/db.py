# db_manager.py
import os
from supabase import create_client
from dotenv import load_dotenv

# loading environment variables from .env file
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)


## Farmer table Operations
# Create Farmers
def create_Farmers(name, email, contact_number):
    data = {"name": name, "email": email, "contact_number": contact_number}
    response = supabase.table("Farmers").insert(data).execute()
    return response


# Get all Farmers
def get_all_Farmers():
    response = supabase.table("Farmers").select("*").execute()
    return response


# Update Farmer
def update_Farmer(farmer_id, name=None, email=None, contact_number=None):
    data = {}
    if name:
        data["name"] = name
    if email:
        data["email"] = email
    if contact_number:
        data["contact_number"] = contact_number
    response = supabase.table("Farmers").update(data).eq("id", farmer_id).execute()
    return response


# Delete Farmer
def delete_Farmer(farmer_id):
    response = supabase.table("Farmers").delete().eq("id", farmer_id).execute()
    return response


## Buyer table Operations
# Create Buyer
def create_buyer(name, email, contact_number):
    data = {"name": name, "email": email, "contact_number": contact_number}
    response = supabase.table("buyers").insert(data).execute()
    return response


# Get all Buyers
def get_all_buyers():
    response = supabase.table("buyers").select("*").execute()
    return response


# Update Buyer
def update_buyer(buyer_id, name=None, email=None, contact_number=None):
    data = {}
    if name:
        data["name"] = name
    if email:
        data["email"] = email
    if contact_number:
        data["contact_number"] = contact_number
    response = supabase.table("buyers").update(data).eq("id", buyer_id).execute()
    return response


# Delete Buyer
def delete_buyer(buyer_id):
    response = supabase.table("buyers").delete().eq("id", buyer_id).execute()
    return response


## Crop table Operations
# Create Crop Listing
def create_crop_listing(
    farmer_id, crop_name, description, available_quantity, price_per_unit, unit
):
    data = {
        "farmer_id": farmer_id,
        "crop_name": crop_name,
        "description": description,
        "available_quantity": available_quantity,
        "price_per_unit": price_per_unit,
        "unit": unit,
    }
    response = supabase.table("crops").insert(data).execute()
    return response


# Get all Available Crops (for buyers)
def get_all_available_crops():
    response = supabase.table("crops").select("*").gt("available_quantity", 0).execute()
    return response


# Get Crops by Farmer ID
def get_crops_by_farmer(farmer_id):
    response = supabase.table("crops").select("*").eq("farmer_id", farmer_id).execute()
    return response


# Update Crop Details
def update_crop_details(crop_id, price_per_unit=None, description=None):
    data = {}
    if price_per_unit is not None:
        data["price_per_unit"] = price_per_unit
    if description:
        data["description"] = description
    response = supabase.table("crops").update(data).eq("id", crop_id).execute()
    return response


# Update Crop Quantity
def update_crop_quantity(crop_id, quantity_change):
    response = (
        supabase.table("crops")
        .update({"available_quantity": quantity_change})
        .eq("id", crop_id)
        .execute()
    )
    return response


# Delete Crop Listing
def delete_crop_listing(crop_id):
    response = supabase.table("crops").delete().eq("id", crop_id).execute()
    return response


## Order table Operations
# Create New Order
def create_order(buyer_id, crop_id, quantity_purchased, total_price):
    data = {
        "buyer_id": buyer_id,
        "crop_id": crop_id,
        "quantity_purchased": quantity_purchased,
        "total_price": total_price,
    }
    response = supabase.table("orders").insert(data).execute()
    return response


# Get Orders by Buyer ID
def get_orders_by_buyer(buyer_id):
    response = (
        supabase.table("orders")
        .select("*, crops(*)")
        .eq("buyer_id", buyer_id)
        .execute()
    )
    return response


# Get Orders for Farmer
def get_orders_for_farmer(farmer_id):
    response = supabase.rpc("get_farmer_orders", {"p_farmer_id": farmer_id}).execute()
    return response


# Get All Orders
def get_all_orders():
    response = supabase.table("orders").select("*, buyers(*), crops(*)").execute()
    return response
