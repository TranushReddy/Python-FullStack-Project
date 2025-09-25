# 🌾 Crop Marketplace API

A streamlined, **full-stack crop marketplace system** that connects farmers directly with buyers. This **FastAPI**-powered backend provides robust APIs for crop listing, inventory management, and order processing, complemented by a modern **Streamlit** frontend interface.

---

## ✨ Features

### 👨‍🌾 Farmer-side Features

- **Crop Listing Management**: Create detailed crop listings with pricing, quantity, and descriptions.
- **Real-time Inventory**: Automatic stock updates after each sale transaction.
- **Flexible Pricing**: Set custom price per unit with various measurement units.
- **Contact Integration**: Include farmer contact information for direct communication.

### 🛒 Buyer-side Features

- **Crop Discovery**: Browse all available crops with detailed information.
- **Instant Purchase**: Place orders with automatic inventory validation and updates.
- **Order Tracking**: Complete order history with crop details and pricing.
- **Stock Validation**: Real-time stock checking prevents overselling.

### 🔧 Technical Features

- **RESTful API**: Clean, documented **FastAPI** endpoints.
- **Database Transactions**: Atomic order processing with **Supabase RPC** functions.
- **CORS Support**: Cross-origin requests enabled for web frontend integration.
- **Error Handling**: Comprehensive error responses with appropriate HTTP status codes.
- **Data Validation**: **Pydantic** models ensure data integrity.

---

## 🏗️ Project Structure

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

-- Create crops table
CREATE TABLE crops (
    id SERIAL PRIMARY KEY,
    farmer_name VARCHAR(255) NOT NULL,
    farmer_contact VARCHAR(50),
    crop_name VARCHAR(255) NOT NULL,
    description TEXT,
    available_quantity DECIMAL(10,2) NOT NULL CHECK (available_quantity >= 0),
    price_per_unit DECIMAL(10,2) NOT NULL CHECK (price_per_unit > 0),
    unit VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    crop_id INTEGER REFERENCES crops(id) ON DELETE CASCADE,
    buyer_name VARCHAR(255) NOT NULL,
    buyer_contact VARCHAR(50) NOT NULL,
    quantity_purchased DECIMAL(10,2) NOT NULL CHECK (quantity_purchased > 0),
    total_price DECIMAL(10,2) NOT NULL,
    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

- The app will open in your browser at `http://localhost:8501`

## FastAPI Backend

- cd api
- uvicorn api.main:app --reload --port 8000

- API will be available at: `http://127.0.0.1:8000`

## How to Use Application

## As a Farmer:

- Navigate to the "List a Crop" tab.

- Fill in crop details including name, quantity, price, and unit.

- Add optional description and contact information.

- Submit the listing to make it available for purchase.

## As a Buyer:

- Browse available crops in the "Buy Crops" tab.

- Select desired crop and specify quantity to purchase.

- Enter buyer details (name and contact).

- Confirm purchase - inventory updates automatically.

## Order Tracking

- View all completed orders in the "View All Orders" tab.

- See buyer details, crop information, quantities, and total prices.

- Orders include timestamps for tracking purposes.

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

- **Authentication**: JWT-based user authentication and role management.

- **Payment Processing**: Stripe/PayPal integration for secure transactions.

- **Image Upload**: Crop photo support with cloud storage.

- **Notification System**: Email/SMS alerts for orders and stock updates.

- **Advanced Search**: Filtering by location, price range, organic certification.

- **Mobile API**: Enhanced endpoints for mobile app development.

- **Analytics Dashboard**: Sales trends and revenue insights.

- **Review System**: Buyer ratings and farmer reviews.

## support

- If you encounter any issues or have questions:

- **Mobile No**: 8463926604
- **Maild Id**: Tranush.3789@gmail.com
