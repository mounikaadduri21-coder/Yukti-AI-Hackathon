"""
AWS Services Simulation Module for Yukti AI
Simulates Lambda, S3, Rekognition, and Bedrock with realistic delays
"""

import os
import time
import random
import streamlit as st
from typing import Dict, List


def get_aws_credentials() -> Dict[str, str]:
    """Retrieve AWS credentials from environment variables"""
    return {
        "access_key_id": os.getenv("AWS_ACCESS_KEY_ID", "demo_access_key_12345"),
        "secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", "demo_secret_key_67890"),
        "region": os.getenv("AWS_REGION", "ap-south-1")
    }


def simulate_lambda_trigger(operation: str) -> None:
    """
    Simulate AWS Lambda trigger with delay and indicator
    
    Args:
        operation: Description of Lambda operation
    """
    with st.spinner(f"🔄 Lambda: {operation}..."):
        delay = random.uniform(0.5, 1.0)
        time.sleep(delay)
    
    st.success(f"✅ Lambda: {operation} Complete ($0 idle cost)")
    
    # Increment counter for demo
    if "lambda_calls" not in st.session_state:
        st.session_state.lambda_calls = 0
    st.session_state.lambda_calls += 1


def simulate_s3_cache_access(data_type: str) -> None:
    """
    Simulate AWS S3 cache access with delay and cost indicator
    
    Args:
        data_type: Type of data being cached
    """
    with st.spinner(f"📦 S3: Loading {data_type} from cache..."):
        delay = random.uniform(0.2, 0.5)
        time.sleep(delay)
    
    st.info("💰 S3 Smart Caching: -40% AI retrieval cost reduction")
    
    # Increment counter for demo
    if "s3_cache_hits" not in st.session_state:
        st.session_state.s3_cache_hits = 0
    st.session_state.s3_cache_hits += 1


def simulate_rekognition_analysis(image_data: bytes, is_fake: bool = False) -> Dict:
    """
    Simulate AWS Rekognition visual analysis
    
    Args:
        image_data: Image bytes (not actually processed in simulation)
        is_fake: Whether product is fake (determines match percentage)
        
    Returns:
        Dictionary with match_percentage, flaws_detected, processing_time
    """
    with st.spinner("🔍 AWS Rekognition: Analyzing product images..."):
        delay = random.uniform(1.0, 2.0)
        time.sleep(delay)
    
    # Generate match percentage based on authenticity
    if is_fake:
        match_percentage = random.uniform(0, 59.9)
    else:
        match_percentage = random.uniform(85, 100)
    
    # Generate visual flaws for fake products
    flaws_detected = []
    if is_fake:
        possible_flaws = [
            "🔴 Missing hologram seal",
            "🔴 Font mismatch on logo",
            "🔴 Color variation detected",
            "🔴 Packaging quality difference",
            "🔴 Barcode missing or incorrect",
            "🔴 Brand label misalignment"
        ]
        num_flaws = random.randint(0, 3)
        flaws_detected = random.sample(possible_flaws, num_flaws) if num_flaws > 0 else []
    
    st.success("✅ AWS Rekognition: Visual Analysis Complete")
    
    return {
        "match_percentage": round(match_percentage, 1),
        "flaws_detected": flaws_detected,
        "processing_time": delay
    }


def simulate_bedrock_sentiment_analysis(product_name: str, rating: float) -> Dict:
    """
    Simulate AWS Bedrock NLP sentiment analysis
    
    Args:
        product_name: Product name
        rating: Product rating (influences sentiment)
        
    Returns:
        Dictionary with sentiment percentages and critical alert
    """
    with st.spinner("🤖 AWS Bedrock: Analyzing customer sentiment..."):
        delay = random.uniform(1.0, 1.5)
        time.sleep(delay)
    
    # Generate sentiment based on rating
    if rating >= 4.0:
        positive_pct = random.uniform(60, 80)
        negative_pct = random.uniform(5, 15)
        neutral_pct = 100 - positive_pct - negative_pct
        critical_alert = "✅ Majority of reviews are positive"
    elif rating >= 3.0:
        positive_pct = random.uniform(40, 60)
        negative_pct = random.uniform(20, 35)
        neutral_pct = 100 - positive_pct - negative_pct
        critical_alert = "⚠️ Mixed reviews - check product details carefully"
    else:
        positive_pct = random.uniform(10, 30)
        negative_pct = random.uniform(45, 70)
        neutral_pct = 100 - positive_pct - negative_pct
        critical_alert = f"⚠️ {int(negative_pct)}% of reviews mention 'fake product' or 'not original'"
    
    review_count = random.randint(100, 5000)
    
    st.success("✅ AWS Bedrock: Sentiment Analysis Complete")
    
    return {
        "positive_pct": round(positive_pct, 1),
        "neutral_pct": round(neutral_pct, 1),
        "negative_pct": round(negative_pct, 1),
        "critical_alert": critical_alert,
        "review_count": review_count
    }


def simulate_bedrock_cost_calculation(scenario: str, product_data: Dict) -> Dict:
    """
    Simulate AWS Bedrock financial analysis for different scenarios
    
    Args:
        scenario: Scenario type (A/B/C/D)
        product_data: Product and seller data
        
    Returns:
        Scenario-specific cost breakdown
    """
    with st.spinner("🤖 AWS Bedrock: Calculating True Cost..."):
        delay = random.uniform(1.0, 1.5)
        time.sleep(delay)
    
    results = {}
    
    if scenario == "A":
        # Scenario A: Dare to Buy Trap
        fake_price = product_data.get("price", 1000)
        original_price = fake_price * random.uniform(1.5, 2.5)
        
        fake_lifespan_months = random.randint(2, 3)
        original_lifespan_months = random.randint(12, 24)
        
        fake_monthly_cost = fake_price / fake_lifespan_months
        original_monthly_cost = original_price / original_lifespan_months
        
        results = {
            "fake_price": round(fake_price, 2),
            "fake_lifespan_months": fake_lifespan_months,
            "fake_monthly_cost": round(fake_monthly_cost, 2),
            "original_price": round(original_price, 2),
            "original_lifespan_months": original_lifespan_months,
            "original_monthly_cost": round(original_monthly_cost, 2),
            "verdict": "🔴 Cheap fakes cost MORE per month than originals"
        }
    
    elif scenario == "B":
        # Scenario B: Maintenance Trap
        base_price = product_data.get("price", 5000)
        category = product_data.get("category", "Home")
        
        # Category-specific recurring costs
        if "RO" in product_data.get("product_name", ""):
            filter_costs_yearly = 4000
            maintenance_costs_yearly = 1500
        elif "Cooker" in product_data.get("product_name", ""):
            filter_costs_yearly = 500
            maintenance_costs_yearly = 800
        else:
            filter_costs_yearly = 2000
            maintenance_costs_yearly = 1000
        
        total_1_year_cost = base_price + filter_costs_yearly + maintenance_costs_yearly
        monthly_equivalent = total_1_year_cost / 12
        
        results = {
            "base_price": round(base_price, 2),
            "filter_costs_yearly": filter_costs_yearly,
            "maintenance_costs_yearly": maintenance_costs_yearly,
            "total_1_year_cost": round(total_1_year_cost, 2),
            "monthly_equivalent": round(monthly_equivalent, 2)
        }
    
    elif scenario == "C":
        # Scenario C: Discount Explainer
        current_price = product_data.get("price", 1000)
        original_price = current_price * random.uniform(1.2, 2.0)
        discount_percentage = ((original_price - current_price) / original_price) * 100
        
        # Determine legitimacy
        is_legitimate = discount_percentage <= 40 and random.random() > 0.3
        
        if is_legitimate:
            verdict = "🟢 Authorized Festive Sale"
            expiry_date = None
        else:
            verdict = "🔴 Clearance Trap: Product expires soon"
            expiry_date = f"{random.randint(1, 6)} months from now"
        
        results = {
            "original_price": round(original_price, 2),
            "discounted_price": round(current_price, 2),
            "discount_percentage": round(discount_percentage, 1),
            "is_legitimate": is_legitimate,
            "verdict": verdict,
            "expiry_date": expiry_date
        }
    
    elif scenario == "D":
        # Scenario D: Unbranded Reality Check
        item_price = product_data.get("price", 500)
        market_average = item_price * random.uniform(0.8, 1.3)
        price_difference_pct = ((item_price - market_average) / market_average) * 100
        
        if price_difference_pct <= 20:
            verdict = "🟢 Honest Budget Buy! Great daily value."
            value_score = random.randint(7, 10)
        else:
            verdict = "🔴 Overpriced Alert. Priced above market average."
            value_score = random.randint(3, 6)
        
        results = {
            "item_price": round(item_price, 2),
            "market_average": round(market_average, 2),
            "price_difference_pct": round(price_difference_pct, 1),
            "verdict": verdict,
            "value_score": value_score
        }
    
    st.success("✅ AWS Bedrock: Financial Analysis Complete")
    
    return results


def display_aws_architecture_info():
    """Display AWS architecture information in sidebar"""
    with st.sidebar:
        st.markdown("### ☁️ AWS Cloud Architecture")
        st.markdown("""
        **Active Services:**
        - 🔄 Lambda (Serverless)
        - 📦 S3 (Smart Caching)
        - 🔍 Rekognition (Visual AI)
        - 🤖 Bedrock (GenAI)
        """)
        
        if "lambda_calls" in st.session_state:
            st.metric("Lambda Invocations", st.session_state.lambda_calls)
        if "s3_cache_hits" in st.session_state:
            st.metric("S3 Cache Hits", st.session_state.s3_cache_hits)
