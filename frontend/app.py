import streamlit as st
import requests
import pandas as pd

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000"

# --- Helper Functions to Call Backend API ---


def api_get(endpoint):
    """Generic GET request to the FastAPI backend."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(
            f"API Error: Could not connect to the backend. Is it running? Details: {e}"
        )
        return {"Success": False, "message": "Backend connection failed."}


def api_post(endpoint, data):
    """Generic POST request to the FastAPI backend."""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.json().get("detail", "Unknown error.")
        st.error(f"API returned an error: {error_detail}")
        return {"Success": False, "message": error_detail}
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: Backend connection failed. Details: {e}")
        return {"Success": False, "message": "Backend connection failed."}


# --- UI Components ---


def farmer_dashboard(farmer_id):
    """Interface for managing crop listings and viewing sales."""
    st.title(f"👨‍🌾 Farmer Dashboard (ID: {farmer_id})")

    # 1. Create New Listing Form
    with st.expander("➕ Create New Crop Listing"):
        with st.form("new_crop_form", clear_on_submit=True):
            st.subheader("Enter Crop Details")
            crop_name = st.text_input("Crop Name")
            description = st.text_area("Description (e.g., Organic, Harvest Date)")
            available_quantity = st.number_input(
                "Available Quantity", min_value=0.01, step=0.01
            )
            price_per_unit = st.number_input(
                "Price Per Unit", min_value=0.01, step=0.01
            )
            unit = st.selectbox("Unit", ["kg", "quintal", "ton", "piece"])

            submitted = st.form_submit_button("List Crop")

            if submitted:
                data = {
                    "farmer_id": farmer_id,
                    "crop_name": crop_name,
                    "description": description,
                    "available_quantity": available_quantity,
                    "price_per_unit": price_per_unit,
                    "unit": unit,
                }
                result = api_post("/crops/", data)
                if result.get("Success"):
                    st.success("✅ Crop successfully listed!")
                    st.rerun()

    # 2. View and Manage Listings
    st.header("Your Active Listings")
    listings_response = api_get(f"/crops/farmer/{farmer_id}")

    if listings_response.get("Success") and listings_response.get("data"):
        df = pd.DataFrame(listings_response["data"])
        df = df.set_index("id")
        st.dataframe(
            df[
                [
                    "crop_name",
                    "available_quantity",
                    "price_per_unit",
                    "unit",
                    "description",
                ]
            ],
            use_container_width=True,
        )
        st.info(f"You have {len(df)} active listings.")
    else:
        st.info("You have no active crop listings.")

    # 3. View Sales History (Orders)
    st.header("Recent Sales")
    orders_response = api_get(f"/orders/farmer/{farmer_id}")

    if orders_response.get("Success") and orders_response.get("data"):
        orders_df = pd.DataFrame(orders_response["data"])
        st.dataframe(orders_df, use_container_width=True)
    else:
        st.info("No sales history found.")


def buyer_dashboard(buyer_id):
    """Interface for browsing crops and making purchases."""
    st.title(f"🛒 Buyer Marketplace (ID: {buyer_id})")
    st.header("Available Crops")

    # 1. Fetch and Filter Crops
    crops_response = api_get("/crops/available")

    if crops_response.get("Success") and crops_response.get("data"):
        crops_data = crops_response["data"]
        df = pd.DataFrame(crops_data)

        # Simple search and filter
        search_term = st.text_input("Search by Crop Name", "").strip()
        if search_term:
            df = df[df["crop_name"].str.contains(search_term, case=False)]

        # DataFrame Display
        st.dataframe(
            df[
                [
                    "crop_name",
                    "available_quantity",
                    "price_per_unit",
                    "unit",
                    "description",
                    "farmer_id",
                ]
            ],
            use_container_width=True,
        )

        # 2. Purchase Form
        st.header("Initiate Purchase")

        # Map crop ID to display name for selection
        crop_options_map = {
            f"{row['crop_name']} (Available: {row['available_quantity']} {row['unit']})": row
            for index, row in df.iterrows()
        }
        selected_key = st.selectbox("Select Crop to Buy", list(crop_options_map.keys()))

        if selected_key:
            selected_crop = crop_options_map[selected_key]

            st.markdown(
                f"**Price:** ${selected_crop['price_per_unit']}/{selected_crop['unit']}"
            )
            max_qty = selected_crop["available_quantity"]

            with st.form("purchase_form"):
                buy_quantity = st.number_input(
                    f"Quantity to Purchase ({selected_crop['unit']})",
                    min_value=0.01,
                    max_value=max_qty,
                    value=0.01,
                    step=0.01,
                )

                total_price = buy_quantity * selected_crop["price_per_unit"]
                st.info(f"Estimated Total Price: **${total_price:.2f}**")

                purchase_submitted = st.form_submit_button("Confirm Purchase")

                if purchase_submitted:
                    purchase_data = {
                        "buyer_id": buyer_id,
                        "crop_id": selected_crop["id"],
                        "quantity_purchased": buy_quantity,
                        "price_per_unit": selected_crop["price_per_unit"],
                    }

                    result = api_post("/orders/purchase", purchase_data)

                    if result.get("order_status") == "Success":
                        st.success(
                            f"🎉 Successfully purchased {buy_quantity} {selected_crop['unit']} of {selected_crop['crop_name']}!"
                        )
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Purchase failed. Check stock or details.")
    else:
        st.info("Currently, no crops are available in the marketplace.")

    # 3. View Order History
    st.header("Your Order History")
    orders_response = api_get(f"/orders/buyer/{buyer_id}")
    if orders_response.get("Success") and orders_response.get("data"):
        orders_df = pd.DataFrame(orders_response["data"])
        st.dataframe(orders_df, use_container_width=True)
    else:
        st.info("You have no past orders.")


# --- Main Application Flow ---


def main():
    """Handles the initial role selection and routes to the correct dashboard."""
    st.sidebar.title("Select Your Role")

    # Placeholder for images, removing deprecated warnings
    try:
        st.sidebar.image("https://i.imgur.com/7p4G2fU.png", width=150)
    except Exception:
        pass  # Ignore image errors

    # Initialize role state
    if "role" not in st.session_state:
        st.session_state.role = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    # Role Selection
    role = st.sidebar.radio("I am a:", ["Select Role", "Farmer", "Buyer"])

    if role == "Select Role":
        st.title("Welcome to the Crop Management System")
        st.markdown("Please select your role on the sidebar to continue.")
        st.info(
            "Note: The system currently requires manual entry of a User ID (integer) for testing."
        )

    elif role in ["Farmer", "Buyer"]:

        # Simple ID entry for testing (Authentication would replace this)
        user_id = st.sidebar.number_input(
            f"Enter {role} ID (Integer)", min_value=1, step=1
        )
        st.session_state.user_id = user_id
        st.session_state.role = role

        if user_id:
            if role == "Farmer":
                farmer_dashboard(user_id)
            elif role == "Buyer":
                buyer_dashboard(user_id)
        else:
            st.warning("Please enter your User ID.")


if __name__ == "__main__":
    main()
