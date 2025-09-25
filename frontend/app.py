import streamlit as st
import requests
import pandas as pd

# Configure page
st.set_page_config(page_title="Crop Management System", page_icon="🌾", layout="wide")

# API Base URL
API_BASE_URL = "http://localhost:8000"


# Helper function for API calls
def api_call(method, endpoint, data=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        return response.status_code, response.json() if response.text else {}
    except Exception as e:
        return None, {"error": str(e)}


# Main header
st.title("🌾 Crop Management System")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigate:", ["Dashboard", "Farmers", "Buyers", "Crops", "Orders"]
)

# Dashboard
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)

    # Get counts
    _, farmers = api_call("GET", "/farmers/")
    _, buyers = api_call("GET", "/buyers/")
    _, crops = api_call("GET", "/crops/available")

    col1.metric("Farmers", len(farmers.get("data", [])))
    col2.metric("Buyers", len(buyers.get("data", [])))
    col3.metric("Available Crops", len(crops.get("data", [])))

    # Show available crops
    if crops.get("data"):
        st.subheader("Available Crops")
        df = pd.DataFrame(crops["data"])
        st.dataframe(
            df[["crop_name", "available_quantity", "price_per_unit", "unit"]],
            use_container_width=True,
        )

# Farmers page
elif page == "Farmers":
    tab1, tab2 = st.tabs(["Register", "Manage"])

    with tab1:
        with st.form("farmer_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            contact = st.text_input("Contact")

            if st.form_submit_button("Register Farmer"):
                if name and email and contact:
                    status, response = api_call(
                        "POST",
                        "/farmers/register",
                        {"name": name, "email": email, "contact_number": contact},
                    )
                    if status == 200:
                        st.success("Farmer registered successfully!")
                    else:
                        st.error(f"Error: {response.get('detail', 'Unknown error')}")

    with tab2:
        status, farmers = api_call("GET", "/farmers/")
        if farmers.get("data"):
            df = pd.DataFrame(farmers["data"])
            st.dataframe(df, use_container_width=True)

# Buyers page
elif page == "Buyers":
    tab1, tab2 = st.tabs(["Register", "Manage"])

    with tab1:
        with st.form("buyer_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            contact = st.text_input("Contact")

            if st.form_submit_button("Register Buyer"):
                if name and email and contact:
                    status, response = api_call(
                        "POST",
                        "/buyers/register",
                        {"name": name, "email": email, "contact_number": contact},
                    )
                    if status == 200:
                        st.success("Buyer registered successfully!")
                    else:
                        st.error(f"Error: {response.get('detail', 'Unknown error')}")

    with tab2:
        status, buyers = api_call("GET", "/buyers/")
        if buyers.get("data"):
            df = pd.DataFrame(buyers["data"])
            st.dataframe(df, use_container_width=True)

# Crops page
elif page == "Crops":
    tab1, tab2 = st.tabs(["Add Crop", "Manage"])

    with tab1:
        # Get farmers for dropdown
        _, farmers = api_call("GET", "/farmers/")
        if farmers.get("data"):
            farmer_df = pd.DataFrame(farmers["data"])
            farmer_options = {
                f"{row['name']} (ID: {row['id']})": row["id"]
                for _, row in farmer_df.iterrows()
            }

            with st.form("crop_form"):
                farmer = st.selectbox("Select Farmer", list(farmer_options.keys()))
                crop_name = st.text_input("Crop Name")
                description = st.text_area("Description")
                quantity = st.number_input("Quantity", min_value=0.01)
                price = st.number_input("Price per Unit", min_value=0.01)
                unit = st.selectbox("Unit", ["kg", "tons", "bags", "pieces", "liters"])

                if st.form_submit_button("Add Crop"):
                    if farmer and crop_name and quantity and price:
                        data = {
                            "farmer_id": farmer_options[farmer],
                            "crop_name": crop_name,
                            "description": description,
                            "available_quantity": quantity,
                            "price_per_unit": price,
                            "unit": unit,
                        }
                        status, response = api_call("POST", "/crops/", data)
                        if status == 200:
                            st.success("Crop added successfully!")
                        else:
                            st.error(
                                f"Error: {response.get('detail', 'Unknown error')}"
                            )
        else:
            st.warning("Please register farmers first.")

    with tab2:
        status, crops = api_call("GET", "/crops/available")
        if crops.get("data"):
            df = pd.DataFrame(crops["data"])
            st.dataframe(df, use_container_width=True)

# Orders page
elif page == "Orders":
    tab1, tab2 = st.tabs(["Make Purchase", "View Orders"])

    with tab1:
        # Get buyers and crops
        _, buyers = api_call("GET", "/buyers/")
        _, crops = api_call("GET", "/crops/available")

        if buyers.get("data") and crops.get("data"):
            buyer_df = pd.DataFrame(buyers["data"])
            crop_df = pd.DataFrame(crops["data"])

            buyer_options = {
                f"{row['name']} (ID: {row['id']})": row["id"]
                for _, row in buyer_df.iterrows()
            }
            crop_options = {
                f"{row['crop_name']} - ${row['price_per_unit']}/{row['unit']}": row
                for _, row in crop_df.iterrows()
            }

            with st.form("purchase_form"):
                buyer = st.selectbox("Select Buyer", list(buyer_options.keys()))
                crop = st.selectbox("Select Crop", list(crop_options.keys()))

                if crop:
                    crop_info = crop_options[crop]
                    st.info(
                        f"Available: {crop_info['available_quantity']} {crop_info['unit']}"
                    )
                    quantity = st.number_input(
                        "Quantity",
                        min_value=0.01,
                        max_value=float(crop_info["available_quantity"]),
                    )

                    if quantity > 0:
                        total = quantity * crop_info["price_per_unit"]
                        st.write(f"**Total: ${total:.2f}**")

                if st.form_submit_button("Complete Purchase"):
                    if buyer and crop and quantity > 0:
                        data = {
                            "buyer_id": buyer_options[buyer],
                            "crop_id": crop_info["id"],
                            "quantity_purchased": quantity,
                            "price_per_unit": crop_info["price_per_unit"],
                        }
                        status, response = api_call("POST", "/orders/purchase", data)
                        if status == 200:
                            st.success("Purchase completed!")
                        else:
                            st.error(
                                f"Error: {response.get('detail', 'Unknown error')}"
                            )
        else:
            st.warning("Please register buyers and add crops first.")

    with tab2:
        # View orders by buyer
        _, buyers = api_call("GET", "/buyers/")
        if buyers.get("data"):
            buyer_df = pd.DataFrame(buyers["data"])
            buyer_options = {
                f"{row['name']} (ID: {row['id']})": row["id"]
                for _, row in buyer_df.iterrows()
            }

            selected_buyer = st.selectbox(
                "Select Buyer to View Orders", list(buyer_options.keys())
            )

            if st.button("Load Orders"):
                buyer_id = buyer_options[selected_buyer]
                status, orders = api_call("GET", f"/orders/buyer/{buyer_id}")

                if orders.get("data"):
                    df = pd.DataFrame(orders["data"])
                    st.dataframe(df, use_container_width=True)
                    if "total_price" in df.columns:
                        st.metric("Total Spent", f"${df['total_price'].sum():.2f}")
                else:
                    st.info("No orders found.")

st.markdown("---")
st.markdown("© 2024 Crop Management System")
