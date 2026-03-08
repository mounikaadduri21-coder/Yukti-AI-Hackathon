# Yukti AI - Enterprise E-Commerce Aggregator & Scam Detection Platform

**Tagline:** *See the Real, Know the Worth*

## Overview

Yukti AI is an advanced enterprise-grade e-commerce aggregator and scam-detection application built with Python and Streamlit. The platform simulates a complete AWS cloud architecture (Lambda, S3, Rekognition, Bedrock) using seeded/cached dictionary data to provide seamless product comparison, visual authenticity verification, and hidden cost analysis.

## Features

### Phase 1: Search Bar Logic
- Universal input: Product Name, Product URL, or Image Upload
- AWS Lambda routing simulation
- MVP product validation (12 seeded products)

### Phase 2: Seller Matrix
- Aggregates from 6 platforms: Amazon, Flipkart, Myntra, Meesho, Croma, JioMart
- Top Pick identification (highest rating per platform)
- Verified seller filtering (same rating as top picks)
- Scam target injection for demonstration
- S3 cache simulation (-40% cost indicator)

### Phase 3: Satya View
- 3-image truth table (Original | Seller | Customer)
- AWS Rekognition visual flaw detection
- AWS Bedrock sentiment analysis
- Match percentage & traffic light signals (Green/Yellow/Red)
- Generic product support

### Phase 4: True Cost Calculator
- **Scenario A:** Dare to Buy Trap (fake vs original lifespan cost)
- **Scenario B:** Maintenance Trap (recurring costs for appliances)
- **Scenario C:** Discount Explainer (sale legitimacy analysis)
- **Scenario D:** Unbranded Reality Check (market price comparison)

## MVP Products (12 Total)

### Electronics
- boAt Earbuds
- Titan Smartwatch

### Fashion
- Uppada Saree
- Manyavar Dhotis
- Unbranded Sling Bag

### Home
- Kent RO
- Hawkins Cooker

### Health
- Lifelong Spin Bike

### Office
- Zebronics Keyboard
- Milton Lunch Box

### Beauty
- Lakmé Kajal
- Mamaearth Oil

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   cd yukti-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   The `.env` file is already created with demo AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=demo_access_key_12345
   AWS_SECRET_ACCESS_KEY=demo_secret_key_67890
   AWS_REGION=ap-south-1
   ```
   
   **Note:** These are demo credentials for simulation only. No actual AWS API calls are made.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   
   Open your browser and navigate to: `http://localhost:8501`

## Usage Guide

### 1. Search for Products
- Navigate to **Home (Search)** page
- Enter a product name (e.g., "boAt Earbuds")
- Or upload a product image
- Or paste a product URL

### 2. View Seller Matrix
- After searching, navigate to **Seller Matrix**
- View Top Picks from each platform
- Compare verified sellers
- Click **🔍 Run Satya View** on any seller

### 3. Verify Authenticity (Satya View)
- View 3-image comparison
- Check visual flaws detected by Rekognition
- Review sentiment analysis from Bedrock
- See match percentage and traffic light signal

### 4. Calculate True Cost
- Navigate to **True Cost** page
- View scenario-specific analysis
- Understand hidden costs and financial traps

## Project Structure

```
yukti-ai/
├── app.py                      # Main application entry point
├── pages/
│   ├── 0_Home.py              # Search page ✅
│   ├── 1_Seller_Matrix.py     # Seller aggregation ✅
│   ├── 2_Satya_View.py        # Authenticity verification ✅
│   └── 3_True_Cost.py         # Cost calculator ✅
├── utils/
│   ├── seed_data.py           # MVP product database & data generation
│   ├── aws_services.py        # AWS service simulations
│   └── visualization.py       # UI components & charts
├── assets/                     # Product images (to be added)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (demo)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## AWS Architecture Simulation

The platform simulates the following AWS services:

- **Lambda:** Serverless triggers ($0 idle cost)
- **S3:** Smart caching (-40% retrieval cost)
- **Rekognition:** Visual AI for flaw detection
- **Bedrock:** GenAI for sentiment & cost analysis

All services are simulated locally with realistic delays:
- Lambda: 0.5-1.0 seconds
- S3: 0.2-0.5 seconds
- Rekognition: 1.0-2.0 seconds
- Bedrock: 1.0-1.5 seconds

## Technology Stack

- **Frontend:** Streamlit
- **Visualization:** Plotly
- **Image Processing:** Pillow
- **Environment:** python-dotenv
- **AWS Simulation:** boto3 (for demo structure)

## Development Status

### ✅ Completed
- Project structure and dependencies
- Seed data module with 12 MVP products
- AWS services simulation (Lambda, S3, Rekognition, Bedrock)
- Visualization utilities
- Main application with navigation
- Home/Search page with 3 input methods
- Seller Matrix page with Top Picks
- Satya View page with image comparison and authenticity verification
- True Cost Calculator page with all 4 scenarios

### 📋 Optional Enhancements
- Add real product images to assets/
- Add comprehensive testing
- Performance optimization
- Additional product categories

## Contributing

This is a hackathon demo project. For questions or suggestions, please contact the development team.

## License

This project is for demonstration purposes only.

## Acknowledgments

- Built for enterprise e-commerce intelligence
- Simulates AWS cloud-native architecture
- Focuses on consumer protection and transparency

---

**Yukti AI** - *See the Real, Know the Worth* 🛡️
