import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")


class DatabaseManager:
    """
    Manages all direct interaction with the Supabase database.
    Standardizes responses for the logic layer.
    """

    def __init__(self):
        self.supabase: Client = create_client(URL, KEY)

    # --- Helper to process standard table responses ---
    def _process_response(self, func, *args, **kwargs):
        """Standardizes the response structure for table operations, handling exceptions."""
        try:
            response = func(*args, **kwargs).execute()

            if response.error:
                raise Exception(
                    response.error.get("message", "Database operation failed")
                )

            return {
                "Success": True,
                "message": "Operation successful.",
                "data": response.data,
            }

        except Exception as e:
            return {
                "Success": False,
                "message": "Database error occurred.",
                "error": str(e),
            }

    # ====================================================================
    # --- 👨‍🌾 FARMER TABLE OPERATIONS ---
    # ====================================================================

    def create_farmer(self, name, email, contact_number):
        data = {"name": name, "email": email, "contact_number": contact_number}
        return self._process_response(self.supabase.table("farmers").insert, data)

    def get_all_farmers(self):
        return self._process_response(self.supabase.table("farmers").select, "*")

    def delete_farmer(self, farmer_id):
        return self._process_response(
            self.supabase.table("farmers").delete().eq, "id", farmer_id
        )

    # ====================================================================
    # --- 🛒 BUYER TABLE OPERATIONS ---
    # ====================================================================

    def create_buyer(self, name, email, contact_number):
        data = {"name": name, "email": email, "contact_number": contact_number}
        return self._process_response(self.supabase.table("buyers").insert, data)

    def get_all_buyers(self):
        return self._process_response(self.supabase.table("buyers").select, "*")

    def delete_buyer(self, buyer_id):
        return self._process_response(
            self.supabase.table("buyers").delete().eq, "id", buyer_id
        )

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
        return self._process_response(self.supabase.table("crops").insert, data)

    def get_all_available_crops(self):
        return self._process_response(
            self.supabase.table("crops").select("*, farmers(name)").gt,
            "available_quantity",
            0,
        )

    def get_crops_by_farmer(self, farmer_id):
        return self._process_response(
            self.supabase.table("crops").select("*").eq, "farmer_id", farmer_id
        )

    def update_crop_details(self, crop_id, price_per_unit=None, description=None):
        data = {}
        if price_per_unit is not None:
            data["price_per_unit"] = price_per_unit
        if description:
            data["description"] = description
        return self._process_response(
            self.supabase.table("crops").update(data).eq, "id", crop_id
        )

    def delete_crop_listing(self, crop_id):
        return self._process_response(
            self.supabase.table("crops").delete().eq, "id", crop_id
        )

    # ====================================================================
    # --- 💰 ORDER TABLE OPERATIONS (RPC) ---
    # ====================================================================

    def process_order(self, buyer_id, crop_id, quantity_purchased, total_price):
        # Calls the atomic SQL stored procedure via RPC
        params = {
            "p_buyer_id": buyer_id,
            "p_crop_id": crop_id,
            "p_quantity_purchased": quantity_purchased,
            "p_total_price": total_price,
        }
        try:
            response = self.supabase.rpc("process_order", params).execute()
            if response.error:
                raise Exception(response.error.get("message", "SQL procedure failed"))
            return {
                "Success": True,
                "message": "Procedure executed successfully.",
                "data": response.data,
            }
        except Exception as e:
            return {
                "Success": False,
                "message": "Purchase failed at the database level.",
                "error": str(e),
            }

    def get_orders_by_buyer(self, buyer_id):
        return self._process_response(
            self.supabase.table("orders").select("*, crops(crop_name, unit)").eq,
            "buyer_id",
            buyer_id,
        )

    def get_orders_for_farmer(self, farmer_id):
        # Calls the custom analytical SQL function/procedure via RPC for sales reports
        return self._process_response(
            self.supabase.rpc, "get_farmer_orders_report", {"p_farmer_id": farmer_id}
        )
