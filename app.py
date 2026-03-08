"""
Yukti AI - Enterprise E-Commerce Aggregator & Scam Detection Platform
Main Application Entry Point
"""

import streamlit as st
import os

# Import utilities
from utils.aws_services import get_aws_credentials, display_aws_architecture_info


def setup_aws_credentials() -> None:
    """Configure AWS credentials from environment variables"""
    credentials = get_aws_credentials()
    
    # Store in session state for demo purposes
    if "aws_credentials" not in st.session_state:
        st.session_state.aws_credentials = credentials


def setup_page_config() -> None:
    """Configure Streamlit with Trust Blue theme and wide layout"""
    st.set_page_config(
        page_title="Yukti AI - See the Real, Know the Worth",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for Trust Blue theme
    st.markdown("""
    <style>
        .main {
            background-color: #FFFFFF;
        }
        h1, h2, h3 {
            color: #0056D2;
        }
        .stButton>button {
            background-color: #0056D2;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #003d99;
        }
    </style>
    """, unsafe_allow_html=True)


def display_header() -> None:
    """Display Yukti AI logo and tagline"""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; background: linear-gradient(135deg, #0056D2 0%, #003d99 100%); border-radius: 10px; margin-bottom: 30px;">
        <h1 style="color: white; font-size: 48px; margin: 0; font-weight: bold;">
            🛡️ Yukti AI
        </h1>
        <p style="color: white; font-size: 24px; margin: 10px 0; font-style: italic;">
            See the Real, Know the Worth
        </p>
        <p style="color: #e0e0e0; font-size: 14px; margin: 5px 0;">
            Enterprise E-Commerce Aggregator & Scam Detection Platform
        </p>
    </div>
    """, unsafe_allow_html=True)


def initialize_session_state() -> None:
    """Initialize all session state keys with defaults"""
    defaults = {
        # Search/Product Data
        "current_product": "",
        "product_category": "",
        "is_generic": False,
        
        # Seller Matrix Data
        "all_sellers": [],
        "top_picks": [],
        "remaining_sellers": [],
        "scam_target": None,
        "selected_seller": None,
        
        # Satya View Data
        "images": {},
        "match_percentage": 0.0,
        "signal_status": "",
        "visual_flaws": [],
        "sentiment_data": {},
        
        # True Cost Data
        "scenario_type": "",
        "cost_results": {},
        
        # AWS Simulation
        "lambda_calls": 0,
        "s3_cache_hits": 0,
        
        # Navigation
        "current_page": "Home",
        "navigation_history": []
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def render_sidebar_navigation() -> str:
    """Render sidebar navigation and return selected page"""
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        # Page selection
        page = st.radio(
            "Select Page",
            ["🏠 Home (Search)", "📊 Seller Matrix", "🔍 Satya View", "💰 True Cost"],
            index=0
        )
        
        st.markdown("---")
        
        # Display AWS architecture info
        display_aws_architecture_info()
        
        st.markdown("---")
        
        # Current product info
        if st.session_state.current_product:
            st.markdown("### 📦 Current Product")
            st.info(f"**{st.session_state.current_product}**")
            st.caption(f"Category: {st.session_state.product_category}")
            
            if st.button("🔄 New Search"):
                # Reset session state
                st.session_state.current_product = ""
                st.session_state.all_sellers = []
                st.session_state.selected_seller = None
                st.rerun()
    
    # Extract page name
    page_name = page.split(" ")[1].replace("(", "").replace(")", "")
    return page_name


def main() -> None:
    """Main application entry point"""
    # Setup
    setup_page_config()
    setup_aws_credentials()
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Render navigation and get selected page
    selected_page = render_sidebar_navigation()
    
    # Update current page in session state
    st.session_state.current_page = selected_page
    
    # Route to selected page
    if selected_page == "Home":
        st.info("👈 Navigate to **Home (Search)** page using the sidebar to start searching for products!")
        st.markdown("""
        ### Welcome to Yukti AI! 🛡️
        
        **Your trusted companion for safe online shopping**
        
        #### How it works:
        
        1. **🔍 Search** - Enter a product name, URL, or upload an image
        2. **📊 Seller Matrix** - Compare verified sellers across top platforms
        3. **🔍 Satya View** - Verify product authenticity with AI-powered visual analysis
        4. **💰 True Cost** - Discover hidden costs and financial traps
        
        #### Try these products:
        - Electronics: boAt Earbuds, Titan Smartwatch
        - Fashion: Uppada Saree, Manyavar Dhotis, Unbranded Sling Bag
        - Home: Kent RO, Hawkins Cooker
        - Health: Lifelong Spin Bike
        - Office: Zebronics Keyboard, Milton Lunch Box
        - Beauty: Lakmé Kajal, Mamaearth Oil
        
        **Start by navigating to the Home (Search) page!**
        """)
    
    elif selected_page == "Seller":
        if not st.session_state.current_product:
            st.warning("⚠️ Please search for a product first from the Home page!")
        else:
            st.info("📊 Seller Matrix page will be implemented in the pages/ directory")
    
    elif selected_page == "Satya":
        if not st.session_state.current_product:
            st.warning("⚠️ Please search for a product first from the Home page!")
        else:
            st.info("🔍 Satya View page will be implemented in the pages/ directory")
    
    elif selected_page == "True":
        if not st.session_state.current_product:
            st.warning("⚠️ Please search for a product first from the Home page!")
        else:
            st.info("💰 True Cost page will be implemented in the pages/ directory")


if __name__ == "__main__":
    main()
