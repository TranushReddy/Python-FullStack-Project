from src.db import DatabaseManager


# ====================================================================
# --- 👨‍🌾 FARMER LOGIC ---
# ====================================================================
class FarmerManager:

    def __init__(self):
        self.db = DatabaseManager()

    # --- Create ----
    def add_farmer(self, name, email, contact_number):
        """Adds a new farmer to the database."""
        if not all([name, email, contact_number]):
            return {
                "Success": False,
                "message": "Name, email, and contact number are required.",
            }

        response = self.db.create_farmer(name, email, contact_number)

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Farmer added successfully.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Failed to add farmer.",
                "error": response.get("error"),
            }

    # --- Read ----
    def get_farmers(self):
        """Retrieves all farmers from the database."""
        return self.db.get_all_farmers()

    # --- Delete ----
    def remove_farmer(self, farmer_id):
        """Deletes a farmer from the database."""
        if not farmer_id:
            return {"Success": False, "message": "Farmer ID is required for deletion."}

        response = self.db.delete_farmer(farmer_id)

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Farmer deleted successfully.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Failed to delete farmer.",
                "error": response.get("error"),
            }


# ====================================================================
# --- 🛒 BUYER LOGIC ---
# ====================================================================
class BuyerManager:

    def __init__(self):
        self.db = DatabaseManager()

    # --- Create Buyer ----
    def add_buyer(self, name, email, contact_number):
        """Adds a new buyer to the database."""
        if not all([name, email, contact_number]):
            return {
                "Success": False,
                "message": "Name, email, and contact number are required.",
            }

        response = self.db.create_buyer(name, email, contact_number)

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Buyer added successfully.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Failed to add buyer.",
                "error": response.get("error"),
            }

    # --- Read Buyers ----
    def get_buyers(self):
        """Retrieves all buyers from the database."""
        return self.db.get_all_buyers()

    # --- Delete Buyer ----
    def remove_buyer(self, buyer_id):
        """Deletes a buyer from the database."""
        if not buyer_id:
            return {"Success": False, "message": "Buyer ID is required for deletion."}

        response = self.db.delete_buyer(buyer_id)

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Buyer deleted successfully.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Failed to delete buyer.",
                "error": response.get("error"),
            }


# ====================================================================
# --- 🌾 CROP LOGIC ---
# ====================================================================
class CropManager:

    def __init__(self):
        self.db = DatabaseManager()

    # --- Create Crop Listing ----
    def add_crop_listing(
        self,
        farmer_id,
        crop_name,
        description,
        available_quantity,
        price_per_unit,
        unit,
    ):
        """Creates a new crop listing."""
        if not all([farmer_id, crop_name, available_quantity, price_per_unit]):
            return {"Success": False, "message": "Missing required crop details."}

        response = self.db.create_crop_listing(
            farmer_id, crop_name, description, available_quantity, price_per_unit, unit
        )

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Crop listing created successfully.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Failed to create crop listing.",
                "error": response.get("error"),
            }

    # --- Read Crops ----
    def get_crops_for_farmer(self, farmer_id):
        """Retrieves all crops listed by a specific farmer."""
        return self.db.get_crops_by_farmer(farmer_id)

    def get_all_available_crops(self):
        """Retrieves all crops available for buying."""
        return self.db.get_all_available_crops()

    # --- Delete Crop Listing ----
    def remove_crop_listing(self, crop_id):
        """Deletes a crop listing."""
        if not crop_id:
            return {"Success": False, "message": "Crop ID is required for deletion."}

        response = self.db.delete_crop_listing(crop_id)

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Crop listing deleted successfully.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Failed to delete crop listing.",
                "error": response.get("error"),
            }


# ====================================================================
# --- 💰 ORDER LOGIC ---
# ====================================================================
class OrderManager:

    def __init__(self):
        self.db = DatabaseManager()

    # --- Process Order (Direct Purchase) ----
    def handle_purchase(self, buyer_id, crop_id, quantity_purchased, price_per_unit):
        """
        Handles the core business logic of a direct purchase.
        Calculates total price and calls the atomic SQL stored procedure.
        """
        if quantity_purchased <= 0:
            return {"Success": False, "message": "Quantity must be greater than zero."}

        total_price = quantity_purchased * price_per_unit

        response = self.db.process_order(
            buyer_id, crop_id, quantity_purchased, total_price
        )

        if response.get("Success"):
            return {
                "Success": True,
                "message": "Purchase successful! Stock updated.",
                "data": response.get("data"),
            }
        else:
            return {
                "Success": False,
                "message": "Purchase failed. Check stock or details.",
                "error": response.get("error"),
            }

    # --- Read Orders ----
    def get_orders_by_buyer(self, buyer_id):
        """Retrieves all orders made by a specific buyer."""
        return self.db.get_orders_by_buyer(buyer_id)

    def get_orders_for_farmer(self, farmer_id):
        """Retrieves all orders placed for a specific farmer's crops."""
        return self.db.get_orders_for_farmer(farmer_id)
