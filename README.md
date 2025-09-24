# Crop Mangement System

A simple and intuitive crop management system designed to connect farmers and buyers. This application empowers farmers to list their produce and enables buyers to purchase crops directly. The project showcases a complete full-stack application using Python, Supabase, Streamlit, and FastAPI.

## Features

## 👨‍🌾 Farmer-side Features

- **Crop Management** : Farmers can list, view, update, and delete their crop listings.

- **Inventory Tracking**: The system automatically updates the available crop quantity after each sale.

- **Price and Details**: Farmers can set the price per unit and provide detailed descriptions for their produce.

- **Sales History**: View a history of all crops sold, including quantity and total revenue.

## 🛒 Buyer-side Features

- **Crop Discovery**: Buyers can browse and search for crops based on type, price, or availability.

- **Direct Purchase**: The ability to immediately purchase a specified quantity of a crop.

- **Order Tracking**: A dashboard to monitor all placed orders.

- **Simple Interface**: A clean and modern web interface for a smooth user experience.

## Project Structure

CROP-MANAGEMENT-SYSTEM/
|--- src/ # core application logic
| |--- logic.py # Business logic and tasks
Operations
| |--- db.py # Database operations
|
|--- api/
│ |--- main.py # FastAPI endpoint
|
|--- frontend/ # Frontend application
| |--- app.py # Streamlit web interface
|
|--- requirements.txt # Project dependencies
|
|--- README.md # Project documentation
|
|--- .env # Python variables

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,Cloning)

### 1. Clone or Download the Project

# Option 1: Clone with Git

git clone <repository-url>

# Option 2: Download and extract zip files

### 2. Install Dependicies

pip install -r requirements.txt

### 3. Set up Supabase Database

1. Create a Supabse Project:

2. Create a Task table:

- Go to the SQL Editor in your Supabase
  dashboard
- Run this SQL command:

```sql

CREATE TABLE farmers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    contact_number VARCHAR(20)
);

CREATE TABLE buyers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    contact_number VARCHAR(20)
);

CREATE TABLE crops (
    id SERIAL PRIMARY KEY,
    farmer_id INTEGER REFERENCES farmers(id),
    crop_name VARCHAR(255),
    description TEXT,
    available_quantity DECIMAL,
    price_per_unit DECIMAL,
    unit VARCHAR(50)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER REFERENCES buyers(id),
    crop_id INTEGER REFERENCES crops(id),
    quantity_purchased DECIMAL,
    total_price DECIMAL
);

```

3.  Get Your Credentials:

### 4. Configure Environment Variables

1. create a `.env` file in the project root

2. Add your Supabase credentials to `.env` :
   SUPABASE_URL=your_project_url_here
   SUPABASE_KEY=your_anon_key_here

** Example: **

SUPABASE_URL=http://abcdefghijf.supabase.co
SUPABASE_KEY=eeebwcbbcekjdsbsjcjj....

### 5. Run The Application

## streamlit Frontend

- streamlit run frontend/app.py

- The app will open in your browser at `http://localhost:5000`

## FastAPI Backend

- cd api
- python main.py

- The app will be available at `http://localhost:5000`

## How to Use Application

## As a Farmer:

- You can log in to your dashboard.

- From there, you can create new crop listings, specifying details like quantity, price, and description.

- Your dashboard will also show a summary of your active listings and past sales.

## As a Buyer:

- You will be taken to the crop discovery page.

- You can browse available crops, search by name, and view details.

- To make a purchase, you'll select a crop, specify the desired quantity, and confirm the order. The system will automatically update the crop's available quantity in the database.

## Technical Details

### Technologies Used

- **Frontend**: Streamlit (python web framework)

- **Backend**: FastAP1 (Python REST API framework)

- **Database**: Supabase (PostgreSQL-basedbackend-as-a-service)

- **Language**: python 3.8+

### Key components

1. **`src/db.py`** : Database operations

- Handles all CRUD operations with Supabase

2. **`src/logic.py`** : Business logic

- Task validation and processing

## Troubleshooting

## Common Issues

1. **"Module not found" errors**

- Make sure you've installed all dependencies:` pip install -r requirements.txt`

- Check that you're running commands from are correct directory

## Fucture Enhancements

- **User Authentication**: Implement robust user accounts and secure login features to ensure only registered farmers and buyers can access the application.

- **Notifications**: Add a system to send notifications to farmers when a new order is placed and to buyers when their order status changes.

- **Payment Gateway**: Integrate a payment service like Stripe or PayPal to enable direct, secure transactions within the application.

- **Geospatial Data**: Use location data to allow buyers to search for crops by proximity and provide farmers with a better understanding of local market demand.

- **Data Analytics**: Create dashboards with visual reports for farmers, showing sales trends, total revenue, and popular crops.

- **Ratings and Reviews**: Implement a system where buyers can rate and review crops and farmers to build trust and credibility in the marketplace.

- **Mobile App**: Develop a mobile version of the application using a framework like React Native or Flutter to provide a more convenient experience for users on the go.

## support

- If you encounter any issues or have questions:

- **Mobile No**: 8463926604
- **Maild Id**: Tranush.3789@gmail.com
