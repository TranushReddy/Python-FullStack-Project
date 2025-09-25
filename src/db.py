import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables once outside the class
load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")


class DatabaseManager:
    """
    Manages all direct interaction with the Supabase database.
    """

    def __init__(self):
        self.supabase: Client = create_client(URL, KEY)

    # ====================================================================
    # --- 👨‍🌾 FARMER TABLE OPERATIONS ---
    # ====================================================================

    def create_farmer(self, name, email, contact_number):
        data = {"name": name, "email": email, "contact_number": contact_number}
        response = self.supabase.table("farmers").insert(data).execute()
        return response

    def get_all_farmers(self):
        response = self.supabase.table("farmers").select("*").execute()
        return response

    def update_farmer(self, farmer_id, name=None, email=None, contact_number=None):
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if contact_number:
            data["contact_number"] = contact_number
        response = (
            self.supabase.table("farmers").update(data).eq("id", farmer_id).execute()
        )
        return response

    def delete_farmer(self, farmer_id):
        response = self.supabase.table("farmers").delete().eq("id", farmer_id).execute()
        return response

    # ====================================================================
    # --- 🛒 BUYER TABLE OPERATIONS ---
    # ====================================================================

    def create_buyer(self, name, email, contact_number):
        data = {"name": name, "email": email, "contact_number": contact_number}
        response = self.supabase.table("buyers").insert(data).execute()
        return response

    def get_all_buyers(self):
        response = self.supabase.table("buyers").select("*").execute()
        return response

    def update_buyer(self, buyer_id, name=None, email=None, contact_number=None):
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if contact_number:
            data["contact_number"] = contact_number
        response = (
            self.supabase.table("buyers").update(data).eq("id", buyer_id).execute()
        )
        return response

    def delete_buyer(self, buyer_id):
        response = self.supabase.table("buyers").delete().eq("id", buyer_id).execute()
        return response

    # ====================================================================
    # --- 🌾 CROP TABLE OPERATIONS ---
    # ====================================================================

    def create_crop_listing(
        self,
        farmer_id,
        crop_name,
        description,
        available_quantity,
        price_per_unit,
        unit,
    ):
        data = {
            "farmer_id": farmer_id,
            "crop_name": crop_name,
            "description": description,
            "available_quantity": available_quantity,
            "price_per_unit": price_per_unit,
            "unit": unit,
        }
        response = self.supabase.table("crops").insert(data).execute()
        return response

    def get_all_available_crops(self):
        response = (
            self.supabase.table("crops")
            .select("*, farmers(name)")
            .gt("available_quantity", 0)
            .execute()
        )
        return response

    def get_crops_by_farmer(self, farmer_id):
        response = (
            self.supabase.table("crops")
            .select("*")
            .eq("farmer_id", farmer_id)
            .execute()
        )
        return response

    def update_crop_details(self, crop_id, price_per_unit=None, description=None):
        data = {}
        if price_per_unit is not None:
            data["price_per_unit"] = price_per_unit
        if description:
            data["description"] = description
        response = self.supabase.table("crops").update(data).eq("id", crop_id).execute()
        return response

    def update_crop_quantity(self, crop_id, quantity_change):
        response = (
            self.supabase.table("crops")
            .update({"available_quantity": quantity_change})
            .eq("id", crop_id)
            .execute()
        )
        return response

    def delete_crop_listing(self, crop_id):
        response = self.supabase.table("crops").delete().eq("id", crop_id).execute()
        return response

    # ====================================================================
    # --- 💰 ORDER TABLE OPERATIONS ---
    # ====================================================================

    def process_order(self, buyer_id, crop_id, quantity_purchased, total_price):
        params = {
            "p_buyer_id": buyer_id,
            "p_crop_id": crop_id,
            "p_quantity_purchased": quantity_purchased,
            "p_total_price": total_price,
        }
        return self.supabase.rpc("process_order", params).execute()

    def get_orders_by_buyer(self, buyer_id):
        response = (
            self.supabase.table("orders")
            .select("*, crops(crop_name, unit, price_per_unit)")
            .eq("buyer_id", buyer_id)
            .execute()
        )
        return response

    def get_orders_for_farmer(self, farmer_id):
        return self.supabase.rpc(
            "get_farmer_orders_report", {"p_farmer_id": farmer_id}
        ).execute()

    def get_all_orders(self):
        response = (
            self.supabase.table("orders")
            .select("*, buyers(name), crops(crop_name)")
            .execute()
        )
        return response
