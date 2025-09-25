from src.db import db_manager as DatabaseManager


# ====================================================================
# --- 🌾 CROP MARKETPLACE LOGIC ---
# ====================================================================
class CropMarketplaceManager:

    def __init__(self):
        self.db = DatabaseManager

    def add_crop_listing(self, data: dict):
        """Creates a new crop listing with minimal validation."""
        required_fields = [
            "farmer_name",
            "crop_name",
            "available_quantity",
            "price_per_unit",
            "unit",
        ]
        if not all(data.get(field) for field in required_fields):
            return {"Success": False, "message": "Missing required crop details."}

        return self.db.create_crop_listing(data)

    def get_all_available_crops(self):
        """Retrieves all crops available for buying."""
        return self.db.get_all_available_crops()


# ====================================================================
# --- 💰 ORDER LOGIC ---
# ====================================================================
class OrderManager:

    def __init__(self):
        self.db = DatabaseManager

    def handle_purchase(
        self, crop_id, buyer_name, buyer_contact, quantity_purchased, price_per_unit
    ):
        total_price = float(quantity_purchased) * float(price_per_unit)
        response = self.db.process_order(
            crop_id, buyer_name, buyer_contact, quantity_purchased, total_price
        )

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Purchase successful! Stock updated.",
            }
        else:
            error_msg = response.get("error", "Purchase failed.")
            if "insufficient stock" in error_msg.lower():
                response["message"] = "Purchase failed: Insufficient stock available."

            return {
                "Success": False,
                "message": response.get("message")
                or "Purchase failed. Check stock or details.",
                "error": error_msg,
            }

    def get_all_orders(self):
        """Retrieves all orders."""
        return self.db.get_all_orders()
