"""
Home/Search Page for Yukti AI
Universal input interface with routing logic
"""

import streamlit as st
from utils.seed_data import validate_product, is_generic_product, get_all_mvp_products
from utils.aws_services import simulate_lambda_trigger

# Page config
st.set_page_config(
    page_title="Yukti AI - Search",
    page_icon="🏠",
    layout="wide"
)


def display_mvp_notice() -> None:
    """Display MVP demo notice for invalid products"""
    st.error("""
    ⚠️ **Welcome to Yukti AI Hackathon Demo!**
    
    To ensure zero-lag performance, this MVP is currently seeded with 12 products across 6 categories.
    
    **Try searching:**
    - 'boAt Earbuds' or 'Unbranded Sling Bag'
    """)
    
    with st.expander("📋 View all available products"):
        products = get_all_mvp_products()
        for i, product in enumerate(products, 1):
            st.write(f"{i}. {product}")


def handle_product_name_input(product_name: str) -> None:
    """
    Validate and route product name to Seller Matrix
    
    Args:
        product_name: User input product name
    """
    if not product_name or product_name.strip() == "":
        st.warning("Please enter a product name")
        return
    
    # Validate product
    is_valid, category, normalized_name = validate_product(product_name)
    
    if not is_valid:
        display_mvp_notice()
        return
    
    # Simulate Lambda trigger
    simulate_lambda_trigger("Product validation and routing")
    
    # Store in session state
    st.session_state.current_product = normalized_name
    st.session_state.product_category = category
    st.session_state.is_generic = is_generic_product(normalized_name)
    
    # Navigate to Seller Matrix
    st.switch_page("pages/1_Seller_Matrix.py")


def handle_image_upload(uploaded_file) -> None:
    """
    Process uploaded image, extract text, route to Seller Matrix
    
    Args:
        uploaded_file: Streamlit uploaded file object
    """
    if uploaded_file is None:
        return
    
    # Validate file
    if uploaded_file.type not in ["image/jpeg", "image/jpg", "image/png"]:
        st.error("⚠️ Please upload JPG, JPEG, or PNG format only")
        return
    
    if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        st.error("⚠️ File size must be under 10MB")
        return
    
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Simulate Lambda + Rekognition OCR
    simulate_lambda_trigger("Image processing with Rekognition OCR")
    
    # For demo, randomly select a product (in real app, would use OCR)
    import random
    products = get_all_mvp_products()
    extracted_product = random.choice(products)
    
    st.info(f"🔍 Extracted product name: **{extracted_product}**")
    
    # Validate and route
    is_valid, category, normalized_name = validate_product(extracted_product)
    
    if is_valid:
        st.session_state.current_product = normalized_name
        st.session_state.product_category = category
        st.session_state.is_generic = is_generic_product(normalized_name)
        
        # Navigate to Seller Matrix
        st.switch_page("pages/1_Seller_Matrix.py")
    else:
        display_mvp_notice()


def is_product_url(url: str) -> bool:
    """Check if URL is a product page"""
    product_indicators = ["/product/", "/dp/", "/item/", "/p/"]
    return any(indicator in url.lower() for indicator in product_indicators)


def is_store_url(url: str) -> bool:
    """Check if URL is a seller store page"""
    store_indicators = ["/store/", "/seller/", "/shop/", "/brand/"]
    return any(indicator in url.lower() for indicator in store_indicators)


def handle_url_input(url: str) -> None:
    """
    Determine URL type and route appropriately
    
    Args:
        url: User input URL
    """
    if not url or url.strip() == "":
        st.warning("Please enter a URL")
        return
    
    # Check if it's a store URL
    if is_store_url(url):
        st.error("""
        ⚠️ **Yukti AI compares Original vs. Fake for specific products.**
        
        Please enter a **Product Name**, **Product URL**, or **upload an image**.
        
        Store URLs are not supported.
        """)
        return
    
    # Check if it's a product URL
    if is_product_url(url):
        # Simulate Lambda trigger
        simulate_lambda_trigger("URL analysis and product extraction")
        
        # For demo, randomly select a product
        import random
        products = get_all_mvp_products()
        extracted_product = random.choice(products)
        
        st.info(f"🔍 Extracted product from URL: **{extracted_product}**")
        
        # Validate and route directly to Satya View
        is_valid, category, normalized_name = validate_product(extracted_product)
        
        if is_valid:
            st.session_state.current_product = normalized_name
            st.session_state.product_category = category
            st.session_state.is_generic = is_generic_product(normalized_name)
            
            # For product URL, skip Seller Matrix and go to Satya View
            st.switch_page("pages/2_Satya_View.py")
        else:
            display_mvp_notice()
    else:
        st.warning("⚠️ URL doesn't appear to be a valid product page. Please check and try again.")


def render_home_page() -> None:
    """Main search page with clean, professional UI"""
    
    # Logo at the top (centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image('assets/logo.png', width=150)
        except:
            # Fallback if logo doesn't exist yet
            st.markdown("<div style='text-align: center; font-size: 60px;'>🛡️</div>", unsafe_allow_html=True)
    
    # Title and Tagline (centered)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #0056D2; font-size: 48px; margin-bottom: 10px;">Yukti AI</h1>
        <p style="color: #666; font-size: 20px; font-style: italic;">See the Real, Know the Worth</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Interface
    st.markdown("<h3 style='text-align: center; color: #0056D2;'>Search for Products</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Choose your preferred input method</p>", unsafe_allow_html=True)
    
    # Create 3 tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📝 Product Name", "🔗 Product URL", "📸 Upload Image"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        product_name_input = st.text_input(
            "Enter Product Name",
            placeholder="e.g., boAt Earbuds, Kent RO, Unbranded Sling Bag",
            key="product_name_tab"
        )
        if product_name_input and product_name_input.strip():
            st.session_state['search_query'] = product_name_input
            st.success(f"✅ Product entered: {product_name_input}")
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        product_url_input = st.text_input(
            "Enter E-commerce URL",
            placeholder="e.g., https://amazon.in/product/...",
            key="product_url_tab"
        )
        
        # HACKATHON DEMO MODE: Disable live URL processing
        if st.button("🔍 Analyze URL", key="url_submit_btn", use_container_width=True):
            st.info("""
            🚀 **Hackathon Demo Mode:** Live URL scraping and live image processing are disabled in this environment to save API limits. 
            
            Please select one of the 12 verified products from the catalog below to explore the Yukti AI platform.
            """)
    
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "Upload Product Image",
            type=['jpg', 'jpeg', 'png'],
            key="image_upload_tab"
        )
        
        # HACKATHON DEMO MODE: Disable live image processing
        if st.button("🔍 Process Image", key="image_submit_btn", use_container_width=True):
            st.info("""
            🚀 **Hackathon Demo Mode:** Live URL scraping and live image processing are disabled in this environment to save API limits. 
            
            Please select one of the 12 verified products from the catalog below to explore the Yukti AI platform.
            """)
    
    # Initialize search_query if not set
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ""
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Cards - 3 Core Features (Now Interactive!)
    st.markdown("<h3 style='text-align: center; color: #0056D2; margin-top: 50px; margin-bottom: 30px;'>Choose Your Destination</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0056D2 0%, #003d99 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 220px; margin-bottom: 15px;">
            <div style="font-size: 50px; margin-bottom: 15px;">📊</div>
            <h3 style="color: white; margin-bottom: 15px;">Seller Matrix</h3>
            <p style="color: #e0e0e0; font-size: 14px;">
                Compare verified sellers across top platforms. Find the best deals.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Go to Seller Matrix", use_container_width=True, type="primary", key="btn_seller_matrix"):
            search_query = st.session_state.get('search_query', '')
            if not search_query or search_query.strip() == "":
                st.warning("⚠️ Please enter a product name first.")
            else:
                # Validate product
                is_valid, category, normalized_name = validate_product(search_query)
                if not is_valid:
                    display_mvp_notice()
                else:
                    # Save to session state
                    simulate_lambda_trigger("Product validation and routing")
                    st.session_state.current_product = normalized_name
                    st.session_state.product_category = category
                    st.session_state.is_generic = is_generic_product(normalized_name)
                    # Clear previous seller data to force regeneration
                    st.session_state.all_sellers = []
                    st.switch_page("pages/1_Seller_Matrix.py")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 220px; margin-bottom: 15px;">
            <div style="font-size: 50px; margin-bottom: 15px;">🔍</div>
            <h3 style="color: white; margin-bottom: 15px;">Satya View</h3>
            <p style="color: #e0e0e0; font-size: 14px;">
                AI-powered authenticity verification using AWS Rekognition.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Go to Satya View", use_container_width=True, type="primary", key="btn_satya_view"):
            search_query = st.session_state.get('search_query', '')
            if not search_query or search_query.strip() == "":
                st.warning("⚠️ Please enter a product name first.")
            else:
                # Validate and save to session state
                is_valid, category, normalized_name = validate_product(search_query)
                if not is_valid:
                    display_mvp_notice()
                else:
                    simulate_lambda_trigger("Product validation and routing")
                    st.session_state.current_product = normalized_name
                    st.session_state.product_category = category
                    st.session_state.is_generic = is_generic_product(normalized_name)
                    # Clear previous data to force regeneration
                    st.session_state.all_sellers = []
                    st.session_state.selected_seller = None
                    st.switch_page("pages/2_Satya_View.py")
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 220px; margin-bottom: 15px;">
            <div style="font-size: 50px; margin-bottom: 15px;">💰</div>
            <h3 style="color: white; margin-bottom: 15px;">True Cost</h3>
            <p style="color: #e0e0e0; font-size: 14px;">
                Discover hidden costs and financial traps over time.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💰 Go to True Cost", use_container_width=True, type="primary", key="btn_true_cost"):
            search_query = st.session_state.get('search_query', '')
            if not search_query or search_query.strip() == "":
                st.warning("⚠️ Please enter a product name first.")
            else:
                # Validate and save to session state
                is_valid, category, normalized_name = validate_product(search_query)
                if not is_valid:
                    display_mvp_notice()
                else:
                    simulate_lambda_trigger("Product validation and routing")
                    st.session_state.current_product = normalized_name
                    st.session_state.product_category = category
                    st.session_state.is_generic = is_generic_product(normalized_name)
                    # Clear previous data to force regeneration
                    st.session_state.all_sellers = []
                    st.session_state.selected_seller = None
                    st.switch_page("pages/3_True_Cost.py")
    
    # Collapsible product list (hidden by default)
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("📋 View Available Products (MVP Demo)", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Electronics:**
            - boAt Earbuds
            - Titan Smartwatch
            
            **Fashion:**
            - Uppada Saree
            - Manyavar Dhotis
            - Unbranded Sling Bag
            
            **Home:**
            - Kent RO
            - Hawkins Cooker
            """)
        
        with col2:
            st.markdown("""
            **Health:**
            - Lifelong Spin Bike
            
            **Office:**
            - Zebronics Keyboard
            - Milton Lunch Box
            
            **Beauty:**
            - Lakmé Kajal
            - Mamaearth Oil
            """)


# Main execution
if __name__ == "__main__":
    render_home_page()
