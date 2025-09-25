import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")


class DatabaseManager:
    """
    Manages all direct interaction with the Supabase database for the simple marketplace.
    """

    def __init__(self):
        # Initialize Supabase client
        self.supabase: Client = create_client(URL, KEY)

    def _process_response(self, func_with_execute, *args, **kwargs):
        """
        Standardizes the response structure and handles exceptions.
        'func_with_execute' must be a callable method (e.g., query.execute or rpc_call.execute).
        """
        try:
            response = func_with_execute(*args, **kwargs)
            if hasattr(response, "error") and response.error is not None:
                raise Exception(str(response.error))

            return {
                "Success": True,
                "message": "Operation successful.",
                "data": response.data,
            }

        except Exception as e:
            print(f"Postgres Error Details: {e}")  # Log to console
            return {
                "Success": False,
                "message": "Transaction Failed. See console for error details.",
                "error": str(e),
            }

    # ====================================================================
    # --- 🌾 CROP TABLE OPERATIONS ---
    # ====================================================================

    def create_crop_listing(self, data: dict):
        """Creates a new crop listing."""
        query = self.supabase.table("crops").insert(data)
        return self._process_response(query.execute)

    def get_all_available_crops(self):
        """Retrieves all crops with available quantity > 0."""

        # Build the full query object
        query_builder = (
            self.supabase.table("crops").select("*").gt("available_quantity", 0)
        )
        return self._process_response(query_builder.execute)

    # ====================================================================
    # --- 💰 ORDER TABLE OPERATIONS (RPC) ---
    # ====================================================================

    def get_all_orders(self):
        """Retrieves all orders with joined crop details."""
        # Build the full query object
        query = self.supabase.table("orders").select("*, crops(crop_name, unit)")
        return self._process_response(query.execute)

    def process_order(self, crop_id, buyer_name, buyer_contact, quantity, total_price):
        """Uses the atomic SQL function with the new unique name via RPC."""

        params = {
            "p_crop_id": int(crop_id),
            "p_buyer_name": str(buyer_name),
            "p_buyer_contact": str(buyer_contact),
            "p_quantity_purchased": float(quantity),
            "p_total_price": float(total_price),
        }
        rpc_call = self.supabase.rpc("marketplace_process_order", params)

        return self._process_response(rpc_call.execute)


db_manager = DatabaseManager()
