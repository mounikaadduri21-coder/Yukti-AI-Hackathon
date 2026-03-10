"""
Satya View Page for Yukti AI
Visual authenticity verification with Rekognition and Bedrock
"""

import streamlit as st
import random
import os
from utils.aws_services import simulate_lambda_trigger, simulate_rekognition_analysis, simulate_bedrock_sentiment_analysis
from utils.visualization import create_sentiment_bar_chart, apply_trust_blue_theme
from utils.seed_data import is_generic_product

# Page config
st.set_page_config(
    page_title="Yukti AI - Satya View",
    page_icon="🔍",
    layout="wide"
)

# POSITIVE DEMO DICTIONARY - Hackathon Safe Data (12 Products)
DEMO_DATA = {
    'boAt': {
        'score': 92.5,
        'color': 'Yellow',
        'reason': 'Minor lighting variation in customer photo, but overall shape matches.'
    },
    'Hawkins Cooker': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Hardware and branding match perfectly.'
    },
    'Kent RO': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Water purifier housing and logo perfectly matched.'
    },
    'Lakmé Kajal': {
        'score': 95.5,
        'color': 'Yellow',
        'reason': 'Print quality on pencil matches. Minor packaging wear detected.'
    },
    'Lifelong Spin Bike': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Frame structure aligns with factory specifications.'
    },
    'Mamaearth Oil': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Bottle shape and labels match specifications perfectly.'
    },
    'Manyavar Dhotis': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Fabric texture and official tags match.'
    },
    'Milton Lunch Box': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Shape, color, and logo match perfectly.'
    },
    'Sling Bag': {
        'score': 88.0,
        'color': 'Yellow',
        'reason': 'Unbranded item. Customer received structure matches the seller upload.'
    },
    'Titan Smartwatch': {
        'score': 98.1,
        'color': 'Yellow',
        'reason': 'Bezel ratio matches exactly. Slight glare in customer photo.'
    },
    'Uppada Saree': {
        'score': 94.2,
        'color': 'Yellow',
        'reason': 'Zari pattern matches exactly. Color saturation slightly varies.'
    },
    'Zebronics Keyboard': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Verified Authentic. Keycap layout and branding are an exact match.'
    }
}


def extract_product_keyword(product_name: str) -> str:
    """
    Extract exact product keyword matching DEMO_DATA keys
    
    Args:
        product_name: Full product name from session state
        
    Returns:
        Exact keyword matching DEMO_DATA (e.g., 'boAt', 'Titan Smartwatch', 'Sling Bag')
    """
    product_lower = product_name.lower()
    
    # Match to exact DEMO_DATA keys
    if 'boat' in product_lower:
        return 'boAt'
    elif 'mamaearth' in product_lower:
        return 'Mamaearth Oil'
    elif 'lifelong' in product_lower:
        return 'Lifelong Spin Bike'
    elif 'titan' in product_lower:
        return 'Titan Smartwatch'
    elif 'sling' in product_lower or 'unbranded' in product_lower:
        return 'Sling Bag'
    elif 'hawkins' in product_lower:
        return 'Hawkins Cooker'
    elif 'kent' in product_lower:
        return 'Kent RO'
    elif 'lakme' in product_lower or 'lakmé' in product_lower:
        return 'Lakmé Kajal'
    elif 'manyavar' in product_lower:
        return 'Manyavar Dhotis'
    elif 'milton' in product_lower:
        return 'Milton Lunch Box'
    elif 'uppada' in product_lower:
        return 'Uppada Saree'
    elif 'zebronics' in product_lower:
        return 'Zebronics Keyboard'
    
    # Fallback
    return product_name


def load_images_from_s3(product_name: str, seller_data: dict, is_generic: bool) -> dict:
    """
    Load local images with safe fallback - 100% DYNAMIC
    
    Args:
        product_name: Product name from session state
        seller_data: Selected seller data
        is_generic: Whether product is generic/unbranded
        
    Returns:
        Dictionary with image paths (local or placeholder URLs)
    """
    with st.spinner("📦 Loading product images..."):
        import time
        time.sleep(random.uniform(0.3, 0.6))
    
    st.success("✅ Images loaded successfully")
    
    # Rule 1: The boAt Fix - clean the name before building paths
    file_name = 'boAt' if product_name == 'boAt Earbuds' else product_name
    
    # Build paths DYNAMICALLY using pure f-strings with file_name
    brand_path = f"brand_{file_name}.jpg"
    upload_path = f"upload_{file_name}.jpg"
    received_path = f"received_{file_name}.jpg"
    
    images = {}
    
    # Rule 2: Sling Bag Fix - No brand image for Sling Bag
    if file_name == 'Sling Bag' or is_generic:
        # 2 images only (upload, received) - NO brand image
        if os.path.exists(upload_path):
            images["seller"] = upload_path
        else:
            images["seller"] = f"https://dummyimage.com/400x400/FFC107/000000.png&text=Upload"
        
        if os.path.exists(received_path):
            images["customer"] = received_path
        else:
            images["customer"] = f"https://dummyimage.com/400x400/2196F3/ffffff.png&text=Received"
    else:
        # 3 images (brand, upload, received)
        if os.path.exists(brand_path):
            images["original"] = brand_path
        else:
            images["original"] = f"https://dummyimage.com/400x400/4CAF50/ffffff.png&text=Brand"
        
        if os.path.exists(upload_path):
            images["seller"] = upload_path
        else:
            images["seller"] = f"https://dummyimage.com/400x400/FFC107/000000.png&text=Upload"
        
        if os.path.exists(received_path):
            images["customer"] = received_path
        else:
            images["customer"] = f"https://dummyimage.com/400x400/2196F3/ffffff.png&text=Received"
    
    return images


def display_image_truth_table(images: dict, is_generic: bool, product_name: str) -> None:
    """
    Display 2 or 3 image comparison layout - 100% DYNAMIC
    
    Args:
        images: Dictionary of image paths
        is_generic: Whether product is generic/unbranded
        product_name: Product name from session state
    """
    # Get the selected product from session state
    selected_product = st.session_state.get('current_product', product_name)
    
    # Check if this is Sling Bag (only 2 images)
    if 'Sling Bag' in selected_product:
        # TWO COLUMNS for Sling Bag
        st.info("🔔 Unbranded/Upload Mode: Comparing Seller Upload vs Customer Received only.")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📤 Seller Upload")
            st.image('images/upload_Sling Bag.jpg', use_container_width=True, caption="Image uploaded by seller")
        
        with col2:
            st.markdown("#### 📦 Customer Received")
            st.image('images/received_Sling Bag.jpg', use_container_width=True, caption="Actual product received")
    else:
        # THREE COLUMNS for all other 11 products
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### ✅ Original Brand")
            st.image(images["original"], use_container_width=True, caption="Official brand image")
        
        with col2:
            st.markdown("#### 📤 Seller Upload")
            st.image(images["seller"], use_container_width=True, caption="Image uploaded by seller")
        
        with col3:
            st.markdown("#### 📦 Customer Received")
            st.image(images["customer"], use_container_width=True, caption="Actual product received")


def display_visual_flaws(flaws: list) -> None:
    """
    Display detected visual flaws
    
    Args:
        flaws: List of flaw descriptions
    """
    st.markdown("### 🔍 Visual Analysis Results")
    
    if not flaws:
        st.success("✅ No physical flaws detected - Product appears authentic")
    else:
        st.warning("⚠️ Physical flaws detected:")
        for flaw in flaws:
            st.markdown(f"- {flaw}")


def calculate_match_percentage(seller_data: dict, is_generic: bool) -> float:
    """
    Calculate match percentage based on seller rating and product type
    
    Args:
        seller_data: Seller information
        is_generic: Whether product is generic
        
    Returns:
        Match percentage (0-100)
    """
    rating = seller_data.get("rating", 3.0)
    is_scam = seller_data.get("is_scam", False)
    
    if is_scam:
        # Scam products: low match
        return random.uniform(10, 45)
    elif rating >= 4.5:
        # High rating: high match
        return random.uniform(92, 100)
    elif rating >= 4.0:
        # Good rating: good match
        return random.uniform(85, 95)
    elif rating >= 3.5:
        # Medium rating: medium match
        return random.uniform(65, 85)
    else:
        # Low rating: low match
        return random.uniform(30, 60)


def determine_signal_status(match_pct: float, is_generic: bool) -> str:
    """
    Determine Green/Yellow/Red signal based on match percentage
    
    Args:
        match_pct: Match percentage
        is_generic: Whether product is generic
        
    Returns:
        Signal status: "Green", "Yellow", or "Red"
    """
    if is_generic:
        # Generic products: simpler logic
        if match_pct >= 80:
            return "Green"
        else:
            return "Red"
    else:
        # Branded products: 3-tier logic
        if match_pct == 100 or match_pct >= 90:
            return "Green"
        elif match_pct >= 60:
            return "Yellow"
        else:
            return "Red"


def generate_ai_explanation(match_pct: float, signal_status: str, seller_data: dict, rekognition_results: dict, is_generic: bool) -> str:
    """
    Generate detailed AI analysis breakdown explaining the authenticity score
    
    Args:
        match_pct: Match percentage
        signal_status: Signal status (Green/Yellow/Red)
        seller_data: Seller information
        rekognition_results: Rekognition analysis results
        is_generic: Whether product is generic
        
    Returns:
        AI explanation text
    """
    rating = seller_data.get("rating", 3.0)
    flaws = rekognition_results.get("flaws_detected", [])
    
    if signal_status == "Green":
        # 100% or 90-99.9%
        if match_pct == 100:
            return f"""
**AI Analysis: Product matches {match_pct:.1f}%**

Our comprehensive analysis confirms this product is authentic:
- Logos, packaging, and material textures align perfectly with original specifications
- Visual comparison shows exact match across all verification points
- Seller has excellent rating ({rating}⭐) with verified track record
- No physical flaws or discrepancies detected in any images
- Product images match customer-received photos with 100% accuracy
- Packaging fonts, colors, and branding are identical to official product

**Verdict:** Verified Safe - This is an authentic product from a trusted seller.
"""
        else:
            return f"""
**AI Analysis: Product matches {match_pct:.1f}%**

Our analysis indicates this product is likely authentic:
- Visual comparison shows strong match with original brand specifications
- Logos and packaging align with official product standards
- Minor variations detected ({100 - match_pct:.1f}% difference) but within acceptable tolerance
- Seller has good rating ({rating}⭐) with positive history
- {len(flaws)} minor discrepancies noted: {', '.join(flaws[:2]) if flaws else 'None'}
- Overall authenticity indicators are positive

**Verdict:** Verified Safe - Product appears authentic with minor acceptable variations.
"""
    
    elif signal_status == "Yellow":
        # 70-89.9%
        reasons = []
        if rating < 4.5:
            reasons.append(f"Seller rating is moderate ({rating}⭐)")
        if flaws:
            reasons.append(f"Visual discrepancies detected: {', '.join(flaws[:2])}")
        if match_pct < 85:
            reasons.append("Packaging fonts do not perfectly match original brand specifications")
        if match_pct < 80:
            reasons.append("Material texture appears slightly different from official product")
        if not reasons:
            reasons.append("Product may be older version or have updated packaging")
        
        return f"""
**AI Analysis: Product matches {match_pct:.1f}%**

Our analysis flagged potential concerns:
{chr(10).join(f'- {r}' for r in reasons)}
- Product authenticity cannot be fully verified at this confidence level
- May be replica, refurbished, old stock, or regional variant
- Recommend additional verification before purchase

**Verdict:** Caution Required - Contact seller for clarification and request additional photos.
"""
    
    else:  # Red
        # Below 70%
        reasons = []
        if rating < 4.0:
            reasons.append(f"Seller has concerning rating ({rating}⭐) indicating poor reputation")
        if flaws:
            reasons.append(f"Critical visual flaws: {', '.join(flaws)}")
        if seller_data.get("is_scam"):
            reasons.append("Seller flagged as suspicious with unusually low pricing")
        if match_pct < 50:
            reasons.append("The fonts on the packaging do not match the original brand")
            reasons.append("Material appears low-quality in the customer photo")
            reasons.append("Logos and branding significantly differ from official specifications")
        elif match_pct < 70:
            reasons.append("Packaging design and colors do not align with original brand")
            reasons.append("Product dimensions appear inconsistent with official specifications")
        if not reasons:
            reasons.append("Multiple authenticity indicators failed verification")
        
        return f"""
**AI Analysis: High risk of counterfeit ({match_pct:.1f}% match)**

Our analysis detected serious red flags:
{chr(10).join(f'- {r}' for r in reasons)}
- Product shows strong signs of being fake or misrepresented
- Visual comparison failed multiple authenticity checks
- Significant discrepancies in packaging, logos, and material quality

**Verdict:** High Risk/Fake - DO NOT PURCHASE. Choose a verified seller with higher ratings and better authenticity scores.
"""


def render_satya_view_page() -> None:
    """Main Satya View page - NO CACHING"""
    st.title("🔍 Satya View - Authenticity Verification")
    
    # CRITICAL: Read fresh from session state on every rerun (NO CACHING)
    product_name = st.session_state.get('current_product', '')
    seller_data = st.session_state.get('selected_seller', None)
    is_generic = st.session_state.get('is_generic', False)
    
    # Check if product and seller are set
    if not product_name:
        st.warning("⚠️ Please search for a product first from the Home page!")
        return
    
    if not seller_data:
        st.warning("⚠️ Please select a seller from the Seller Matrix page!")
        st.info("👉 Navigate to **Seller Matrix** and click **🔍 Run Satya View** on any seller")
        return
    
    # Product header with image
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Product image placeholder - use dummyimage.com
        product_img_url = f"https://dummyimage.com/150x150/0056D2/ffffff.png&text={product_name.replace(' ', '+')}"
        st.image(product_img_url, use_container_width=True)
    
    with col2:
        st.markdown(f"### Analyzing: **{product_name}**")
        st.markdown(f"**Seller:** {seller_data['seller_name']} ({seller_data['platform']})")
        st.markdown(f"**Price:** ₹{seller_data['price']} | **Rating:** {seller_data['rating']}⭐")
    
    st.markdown("---")
    
    # REMOVED: Lambda trigger note (Requirement 1 - Keep UI clean)
    
    # Clear cached images when product changes (FIX CACHING BUG)
    if "cached_product" not in st.session_state or st.session_state.cached_product != product_name:
        st.session_state.images = None
        st.session_state.rekognition_results = None
        st.session_state.sentiment_data = None
        st.session_state.cached_product = product_name
    
    # Load images (fresh on product change)
    if not st.session_state.get('images'):
        images = load_images_from_s3(product_name, seller_data, is_generic)
        st.session_state.images = images
    else:
        images = st.session_state.images
    
    # Display image truth table with enhanced styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #0056D2;">📸 Image Truth Table</h3>
    </div>
    """, unsafe_allow_html=True)
    
    display_image_truth_table(images, is_generic, product_name)
    
    st.markdown("---")
    
    # TRAFFIC LIGHT SIGNAL - Read score and render colored block
    product_key = extract_product_keyword(product_name)
    demo_info = DEMO_DATA.get(product_key, {'score': 85.0, 'color': 'Yellow', 'reason': 'Analysis in progress.'})
    
    match_pct = demo_info['score']
    ai_reason = demo_info['reason']
    
    # Apply mathematical rule and render massive colored UI block
    if match_pct == 100.0:
        # GREEN: Exactly 100%
        st.success("""
        # ✅ Match Found: Verified Authentic
        
        **Authenticity Score: {:.1f}%**
        
        {}
        """.format(match_pct, ai_reason), icon="✅")
    elif match_pct >= 70.0:
        # YELLOW: 70.0% to 99.9%
        st.warning("""
        # ⚠️ Match Found: Highly Likely Authentic (Verify Reason Below)
        
        **Authenticity Score: {:.1f}%**
        
        {}
        """.format(match_pct, ai_reason), icon="⚠️")
    else:
        # RED: Below 66.9%
        st.error("""
        # ❌ Mismatch Detected: High Risk of Counterfeit
        
        **Authenticity Score: {:.1f}%**
        
        {}
        """.format(match_pct, ai_reason), icon="❌")
    
    st.markdown("---")
    
    # Run Rekognition analysis with enhanced card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">🤖 AWS Rekognition Analysis</h3>
        <p style="margin: 5px 0 0 0; color: #f0f0f0; font-size: 14px;">Visual authenticity detection powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    is_fake = seller_data.get("is_scam", False) or seller_data.get("rating", 5.0) < 3.5
    
    if not st.session_state.get('rekognition_results'):
        rekognition_results = simulate_rekognition_analysis(b"dummy_image_data", is_fake=is_fake)
        st.session_state.rekognition_results = rekognition_results
    else:
        rekognition_results = st.session_state.rekognition_results
    
    # Display visual flaws
    display_visual_flaws(rekognition_results["flaws_detected"])
    
    st.markdown("---")
    
    # Run Bedrock sentiment analysis with enhanced card
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">🤖 AWS Bedrock - Sentiment Analysis</h3>
        <p style="margin: 5px 0 0 0; color: #f0f0f0; font-size: 14px;">Customer review sentiment powered by generative AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.get('sentiment_data'):
        sentiment_data = simulate_bedrock_sentiment_analysis(product_name, seller_data.get("rating", 4.0))
        st.session_state.sentiment_data = sentiment_data
    else:
        sentiment_data = st.session_state.sentiment_data
    
    # Display sentiment chart
    fig = create_sentiment_bar_chart(sentiment_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display critical alert
    st.markdown(f"**📊 Analyzed {sentiment_data['review_count']} customer reviews**")
    
    if sentiment_data["negative_pct"] > 40:
        st.error(sentiment_data["critical_alert"])
    elif sentiment_data["negative_pct"] > 25:
        st.warning(sentiment_data["critical_alert"])
    else:
        st.success(sentiment_data["critical_alert"])
    
    st.markdown("---")
    
    # Next steps
    st.markdown("### 📊 Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔙 Back to Seller Matrix", use_container_width=True):
            st.info("👈 Use the sidebar to navigate back to Seller Matrix")
    
    with col2:
        if st.button("💰 Calculate True Cost", use_container_width=True):
            st.info("👉 Navigate to **True Cost** page using the sidebar!")


# Main execution
if __name__ == "__main__":
    render_satya_view_page()

