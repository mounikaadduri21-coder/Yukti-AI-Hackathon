# Design Document: Yukti AI

## Overview

Yukti AI is an enterprise-grade e-commerce aggregator built with Python and Streamlit, simulating AWS cloud architecture for product comparison, authenticity verification, and cost analysis.

## Architecture

The platform uses simulated AWS services (Lambda, S3, Rekognition, Bedrock) with seeded data for 12 MVP products across 6 categories, aggregating from 6 platforms (Amazon, Flipkart, Myntra, Meesho, Croma, JioMart).

## Key Components

### 1. Search Bar (Phase 1)
- Universal input: Product Name, URL, or Image
- Lambda routing simulation
- MVP product validation

### 2. Seller Matrix (Phase 2)
- 6-platform aggregation
- Top Pick identification (highest rating per platform)
- Scam target injection
- S3 cache simulation (-40% cost)

### 3. Satya View (Phase 3)
- 3-image truth table
- Rekognition visual flaw detection
- Bedrock sentiment analysis
- Match percentage & traffic light signals

### 4. True Cost Calculator (Phase 4)
- Scenario A: Dare to Buy Trap (fake vs original)
- Scenario B: Maintenance Trap (recurring costs)
- Scenario C: Discount Explainer (sale legitimacy)
- Scenario D: Unbranded Reality Check (market comparison)

## Data Models

### MVP Products (12 total)
- Electronics: boAt Earbuds, Titan Smartwatch
- Fashion: Uppada Saree, Manyavar Dhotis, Unbranded Sling Bag
- Home: Kent RO, Hawkins Cooker
- Health: Lifelong Spin Bike
- Office: Zebronics Keyboard, Milton Lunch Box
- Beauty: Lakmé Kajal, Mamaearth Oil

### Seller Data Structure
```python
{
    "seller_name": str,
    "platform": str,  # Amazon, Flipkart, Myntra, Meesho, Croma, JioMart
    "price": float,   # Dynamic INR
    "rating": float,  # 0.0-5.0
    "review_count": int,
    "delivery_days": int,
    "product_url": str,
    "is_top_pick": bool,
    "is_scam": bool
}
```

### Session State
- current_product, product_category, is_generic
- all_sellers, top_picks, remaining_sellers, scam_target
- images, match_percentage, signal_status
- scenario_type, cost_results
- aws_credentials, navigation_history

## AWS Simulation

- Lambda: 0.5-1.0s delay, $0 idle cost indicator
- S3: 0.2-0.5s delay, -40% cost indicator
- Rekognition: 1.0-2.0s delay, visual flaw detection
- Bedrock: 1.0-1.5s delay, NLP & cost calculations

## UI Theme

- Primary: Trust Blue (#0056D2)
- Tagline: "See the Real, Know the Worth"
- Platform colors: Amazon (orange), Flipkart (blue), Myntra (pink), Meesho (purple), Croma (green), JioMart (red)

## Error Handling

- Invalid product → MVP demo notice
- Store URL → Specific error message
- Image upload fail → Format/size guidance
- AWS simulation → User-friendly fallback messages
