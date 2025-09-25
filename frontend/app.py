import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

# --- CONFIGURATION ---
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title=" Crop Marketplace",
    layout="wide",
)


# --- UTILITY FUNCTIONS ---


def api_call(method, endpoint, json_data: Dict[str, Any] = None):
    """Generic function to handle API requests."""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, json=json_data, timeout=10)

        if response.status_code >= 400:
            error_detail = response.json().get(
                "detail", f"Status {response.status_code}"
            )
            st.error(f"API Error: {error_detail}")
            return {"Success": False, "error": error_detail}

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to API at {API_BASE_URL}")
        st.warning(
            "Please ensure your FastAPI backend is running: uvicorn api.main:app --reload --port 8000"
        )
        return {"Success": False, "error": str(e)}


# --- HELPER FOR NESTED DATA EXTRACTION (FINAL FIX) ---


def get_nested_crop_detail(row_data, key: str) -> str:
    """
    Safely extracts a value from the nested 'crops' object,
    """
    if isinstance(row_data, list) and row_data and isinstance(row_data[0], dict):
        return row_data[0].get(key, "N/A")
    elif isinstance(row_data, dict):
        return row_data.get(key, "N/A")
    return "N/A"


# --- APPLICATION LAYOUT ---

st.title("🌾 Crop Marketplace")
st.markdown("A direct-to-consumer platform for crop listing and purchasing.")

tab1, tab2, tab3 = st.tabs(["🛒 Buy Crops", "👨‍🌾 List a Crop", "📦 View All Orders"])

# ====================================================================
# --- TAB 1: BUY CROPS (DISCOVERY & PURCHASE) ---
# ====================================================================

with tab1:
    st.subheader("Available Crops for Purchase")

    crops_response = api_call("GET", "/crops/available")

    if crops_response and crops_response.get("Success") and crops_response.get("data"):
        crops = crops_response["data"]
        df = pd.DataFrame(crops)

        # --- COLUMN RENAMING ---
        df.rename(
            columns={
                "crop_name": "Crop Name",
                "available_quantity": "Available",
                "price_per_unit": "Price/Unit",
                "id": "Crop ID",
                "farmer_name": "Seller",
                "unit": "Unit",
            },
            inplace=True,
        )

        # Display available crops
        st.dataframe(
            df[
                [
                    "Crop ID",
                    "Crop Name",
                    "Seller",
                    "Available",
                    "Unit",
                    "Price/Unit",
                    "description",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.subheader("Place an Order")

        purchase_col1, purchase_col2, purchase_col3 = st.columns(3)

        # --- User/Crop Selection Setup ---
        crop_options = {
            f"{row['Crop Name']} ({row['Crop ID']}) - ${row['Price/Unit']}/{row['Unit']}": row[
                "Crop ID"
            ]
            for index, row in df.iterrows()
        }

        selected_crop = None
        price_per_unit = 0.0
        available = 0.0

        with purchase_col1:
            buyer_name = st.text_input("Your Name", key="buyer_name_input")
            buyer_contact = st.text_input("Your Contact No.", key="buyer_contact_input")

        with purchase_col2:
            selected_label = st.selectbox(
                "Select Crop to Buy", list(crop_options.keys())
            )
            selected_crop_id = crop_options.get(selected_label)

            if selected_crop_id:
                selected_crop = df[df["Crop ID"] == selected_crop_id].iloc[0]
                price_per_unit = selected_crop["Price/Unit"]
                available = selected_crop["Available"]

        with purchase_col3:
            if selected_crop is not None:
                quantity = st.number_input(
                    f"Quantity to Purchase ({selected_crop['Unit']})",
                    min_value=0.01,
                    max_value=float(available),
                    step=1.0,
                    key="purchase_quantity",
                )
                estimated_total = quantity * price_per_unit
                st.info(f"Total Price: **${estimated_total:,.2f}**")
            else:
                quantity = 0.0

            # Purchase Button
            if st.button("Confirm Purchase", type="primary"):
                if not buyer_name or not buyer_contact:
                    st.error("Please enter your Name and Contact details.")
                elif quantity <= 0:
                    st.error("Quantity must be greater than zero.")
                elif selected_crop is None:
                    st.error("Please select a crop.")
                else:
                    purchase_data = {
                        "crop_id": int(selected_crop_id),
                        "buyer_name": buyer_name,
                        "buyer_contact": buyer_contact,
                        "quantity_purchased": quantity,
                        "price_per_unit": price_per_unit,
                    }
                    response = api_call("POST", "/orders/purchase", purchase_data)
                    if response and response.get("order_status") == "Success":
                        st.success("🎉 Purchase successful! Stock updated.")
                    st.rerun()

    else:
        st.info("No available crops listed in the marketplace.")

# ====================================================================
# --- TAB 2: LIST A CROP ---
# ====================================================================

with tab2:
    st.subheader("Add a New Crop Listing")

    col_a, col_b = st.columns(2)
    with col_a:
        farmer_name = st.text_input("Your Name (Farmer)", key="farmer_name_input")
        farmer_contact = st.text_input("Your Contact No.", key="farmer_contact_input")
        crop_name = st.text_input("Crop Name", placeholder="e.g., Organic Tomatoes")
    with col_b:
        available_quantity = st.number_input(
            "Available Quantity", min_value=0.01, step=1.0
        )
        price_per_unit = st.number_input(
            "Price per Unit (USD)", min_value=0.01, step=0.1
        )
        unit = st.text_input("Unit of Measure", placeholder="e.g., kg, dozen, bushel")

    description = st.text_area("Description (Optional)", max_chars=500)

    if st.button("Submit New Listing", type="secondary"):
        if not all([farmer_name, crop_name, available_quantity, price_per_unit, unit]):
            st.error(
                "Please fill in all required fields (Name, Crop, Quantity, Price, Unit)."
            )
        else:
            data = {
                "farmer_name": farmer_name,
                "farmer_contact": farmer_contact,
                "crop_name": crop_name,
                "description": description,
                "available_quantity": available_quantity,
                "price_per_unit": price_per_unit,
                "unit": unit,
            }
            response = api_call("POST", "/crops/", data)
            if response and response.get("Success"):
                st.success(f"Crop '{crop_name}' listed successfully!")
            st.rerun()

# ====================================================================
# --- TAB 3: VIEW ALL ORDERS ---
# ====================================================================

with tab3:
    st.subheader("All Purchase Orders")

    order_response = api_call("GET", "/orders/")

    if order_response and order_response.get("Success") and order_response.get("data"):
        df = pd.DataFrame(order_response["data"])
        if "crops" in df.columns:
            df["Crop Name"] = df["crops"].apply(
                lambda x: get_nested_crop_detail(x, "crop_name")
            )
            df["Unit"] = df["crops"].apply(lambda x: get_nested_crop_detail(x, "unit"))

        if "ordered_at" in df.columns:
            df["ordered_at"] = pd.to_datetime(df["ordered_at"]).dt.strftime(
                "%Y-%m-%d %H:%M"
            )

        df.rename(
            columns={
                "ordered_at": "Order Date",
                "quantity_purchased": "Quantity",
                "total_price": "Total Paid ($)",
                "buyer_name": "Buyer Name",
                "buyer_contact": "Buyer Contact",
            },
            inplace=True,
        )

        st.dataframe(
            df[
                [
                    "Order Date",
                    "Buyer Name",
                    "Crop Name",
                    "Quantity",
                    "Unit",
                    "Total Paid ($)",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No purchase orders found yet.")
