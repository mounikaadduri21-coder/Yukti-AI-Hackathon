"""
Seller Matrix Page for Yukti AI
Cross-platform seller aggregation with Top Picks
"""

import streamlit as st
import os
from utils.seed_data import generate_seller_data
from utils.aws_services import simulate_s3_cache_access, simulate_lambda_trigger
from utils.visualization import create_buy_box, PLATFORM_COLORS
from typing import List, Dict

# Page config
st.set_page_config(
    page_title="Yukti AI - Seller Matrix",
    page_icon="📊",
    layout="wide"
)


def get_safe_product_image(product_name: str, image_type: str = "upload") -> str:
    """
    Get safe product image path - 100% DYNAMIC
    
    Args:
        product_name: Product name from session state (used directly in path)
        image_type: Type of image (upload, brand, received)
        
    Returns:
        Local path if exists, otherwise placeholder URL
    """
    # Rule 1: The boAt Fix - clean the name before building paths
    file_name = 'boAt' if product_name == 'boAt Earbuds' else product_name
    
    # Construct DYNAMIC local path using pure f-string with file_name
    local_path = f"{image_type}_{file_name}.jpg"
    
    # Check if local file exists
    if os.path.exists(local_path):
        return local_path
    
    # Safe fallback to placeholder
    return f"https://dummyimage.com/200x200/4ECDC4/ffffff.png&text={image_type.title()}"


def identify_top_picks(sellers: List[Dict]) -> List[Dict]:
    """
    Identify 1 top pick per platform (highest rating, tie-breaker: price, delivery)
    
    Args:
        sellers: List of all sellers
        
    Returns:
        List of top picks (1 per platform)
    """
    platforms = {}
    
    # Group sellers by platform (all sellers are high-rated now)
    for seller in sellers:
        platform = seller["platform"]
        if platform not in platforms:
            platforms[platform] = []
        platforms[platform].append(seller)
    
    top_picks = []
    
    # For each platform, find top pick
    for platform, platform_sellers in platforms.items():
        # Sort by rating (desc), then price (asc), then delivery_days (asc)
        sorted_sellers = sorted(
            platform_sellers,
            key=lambda x: (-x["rating"], x["price"], x["delivery_days"])
        )
        
        if sorted_sellers:
            top_pick = sorted_sellers[0]
            top_pick["is_top_pick"] = True
            top_picks.append(top_pick)
    
    return top_picks


def filter_same_rating_sellers(sellers: List[Dict], top_picks: List[Dict]) -> List[Dict]:
    """
    Filter sellers to only include those with same rating as their platform's top pick
    
    Args:
        sellers: List of all sellers
        top_picks: List of top picks
        
    Returns:
        Filtered list of sellers
    """
    # Create platform -> top rating mapping
    platform_top_ratings = {tp["platform"]: tp["rating"] for tp in top_picks}
    
    filtered = []
    
    for seller in sellers:
        if seller.get("is_top_pick"):
            continue  # Skip top picks (already displayed)
        
        platform = seller["platform"]
        top_rating = platform_top_ratings.get(platform)
        
        # Only include if rating matches top pick rating
        if top_rating and seller["rating"] == top_rating:
            filtered.append(seller)
    
    return filtered


def display_top_picks_grid(top_picks: List[Dict]) -> None:
    """Display top picks with dynamic thumbnails"""
    st.markdown("### 🏆 Top Picks (Best from Each Platform)")
    st.markdown("*Highest rated sellers with best price and fastest delivery*")
    
    # Get current product for image loading
    product_name = st.session_state.get('current_product', '')
    
    # Sling Bag Fix - Use upload image for Sling Bag
    if 'Sling Bag' in product_name:
        thumbnail_path = 'upload_Sling Bag.jpg'
    else:
        # Rule 1: The boAt Fix - clean the name before building paths
        file_name = 'boAt' if product_name == 'boAt Earbuds' else product_name
        thumbnail_path = f"upload_{file_name}.jpg"
    
    # Display in 3 columns
    cols = st.columns(3)
    
    for idx, seller in enumerate(top_picks):
        with cols[idx % 3]:
            # TOP PICK THUMBNAIL - 100% dynamic with os.path.exists check
            if os.path.exists(thumbnail_path):
                st.image(thumbnail_path, 
                        use_container_width=True, 
                        caption=f"Top Pick - {seller['platform']}")
            else:
                st.image(f"https://dummyimage.com/200x200/4ECDC4/ffffff.png&text=Product", 
                        use_container_width=True, 
                        caption=f"Top Pick - {seller['platform']}")
            
            # Display seller name prominently
            st.markdown(f"**{seller['seller_name']}**")
            st.caption(f"{seller['platform']}")
            
            create_buy_box(seller)
            
            # Add Satya View button
            if st.button(f"🔍 Run Satya View", key=f"top_pick_{idx}"):
                handle_satya_view_button(seller)


def display_remaining_sellers_list(sellers: List[Dict]) -> None:
    """Display scrollable list with dynamic thumbnails"""
    if not sellers:
        return
    
    st.markdown("### ✅ Other Verified Sellers (Same Top Rating)")
    st.markdown("*All sellers below have the same rating as their platform's top pick*")
    
    # Get current product for image loading
    product_name = st.session_state.get('current_product', '')
    
    # Sling Bag Fix - Use upload image for Sling Bag
    if 'Sling Bag' in product_name:
        thumbnail_path = 'upload_Sling Bag.jpg'
    else:
        # Rule 1: The boAt Fix - clean the name before building paths
        file_name = 'boAt' if product_name == 'boAt Earbuds' else product_name
        thumbnail_path = f"upload_{file_name}.jpg"
    
    for idx, seller in enumerate(sellers):
        col1, col2 = st.columns([1, 4])
        
        with col1:
            # Thumbnail - 100% dynamic with os.path.exists check
            if os.path.exists(thumbnail_path):
                st.image(thumbnail_path, use_container_width=True)
            else:
                st.image(f"https://dummyimage.com/200x200/4ECDC4/ffffff.png&text=Product", 
                        use_container_width=True)
        
        with col2:
            # Display seller name
            st.markdown(f"**{seller['seller_name']}** - {seller['platform']}")
            create_buy_box(seller)
            
            # Add Satya View button
            if st.button(f"🔍 Run Satya View", key=f"remaining_{idx}"):
                handle_satya_view_button(seller)


def handle_satya_view_button(seller: Dict) -> None:
    """
    Trigger Satya View for selected seller
    
    Args:
        seller: Selected seller dictionary
    """
    # Store selected seller
    st.session_state.selected_seller = seller
    
    # CRITICAL: Save the exact price to session state for True Cost Calculator
    st.session_state.product_price = seller['price']
    
    # Simulate Lambda trigger
    simulate_lambda_trigger("Initiating Satya View scan")
    
    st.success(f"✅ Seller selected: **{seller['seller_name']}** from {seller['platform']}")
    st.info("👉 Navigate to **Satya View** page to see authenticity analysis!")


def render_seller_matrix_page() -> None:
    """Main Seller Matrix page"""
    st.title("📊 Seller Matrix")
    
    # Check if product is set
    if not st.session_state.current_product:
        st.warning("⚠️ Please search for a product first from the Home page!")
        return
    
    # MAIN PRODUCT IMAGE - 100% DYNAMIC (No hardcoded names)
    selected_product = st.session_state.current_product
    
    # Sling Bag Fix - Use upload image for Sling Bag
    if 'Sling Bag' in selected_product:
        # Sling Bag has no brand image, use upload
        main_image_path = 'upload_Sling Bag.jpg'
    else:
        # Rule 1: The boAt Fix - clean the name before building paths
        file_name = 'boAt' if selected_product == 'boAt Earbuds' else selected_product
        
        # All other products use brand image
        main_image_path = f'brand_{file_name}.jpg'
    
    # Check if file exists on hard drive
    if not os.path.exists(main_image_path):
        main_image_path = f"https://dummyimage.com/400x400/4ECDC4/ffffff.png&text=Product"
    
    # Product header with large main image
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Main product image - 100% dynamic
        st.image(main_image_path, use_container_width=True, caption=selected_product)
    
    with col2:
        st.markdown(f"### Comparing sellers for: **{st.session_state.current_product}**")
        st.caption(f"Category: {st.session_state.product_category}")
        
        # Display S3 cache indicator
        simulate_s3_cache_access("seller data")
    
    st.markdown("---")
    
    # Generate seller data if not already generated
    if not st.session_state.all_sellers:
        with st.spinner("🔄 Aggregating sellers from top platforms..."):
            sellers = generate_seller_data(
                st.session_state.current_product,
                st.session_state.product_category
            )
            st.session_state.all_sellers = sellers
    
    sellers = st.session_state.all_sellers
    
    # All sellers are high-rated (no scam filtering needed)
    
    # Identify top picks
    top_picks = identify_top_picks(sellers)
    st.session_state.top_picks = top_picks
    
    # Filter remaining sellers
    remaining_sellers = filter_same_rating_sellers(sellers, top_picks)
    st.session_state.remaining_sellers = remaining_sellers
    
    # Display total count
    total_verified = len(top_picks) + len(remaining_sellers)
    st.info(f"📊 Showing **{total_verified} verified sellers** across **6 platforms**")
    
    st.markdown("---")
    
    # Display top picks
    display_top_picks_grid(top_picks)
    
    st.markdown("---")
    
    # COMPREHENSIVE DATA TABLE - All Sellers (High Ratings Only) - TEXT ONLY
    st.markdown("### 📋 Complete Seller Comparison Table")
    st.markdown("*Sortable table showing all high-rated sellers across all platforms*")
    
    # Prepare data for dataframe - TEXT ONLY (NO IMAGES)
    import pandas as pd
    
    table_data = []
    for seller in sellers:
        table_data.append({
            "Platform": seller["platform"],
            "Seller Name": seller["seller_name"],
            "Price (₹)": f"₹{seller['price']:.2f}",
            "Rating": f"{seller['rating']}⭐",
            "Reviews": seller["review_count"],
            "Delivery (days)": seller["delivery_days"],
            "Top Pick": "✅" if seller.get("is_top_pick") else ""
        })
    
    df = pd.DataFrame(table_data)
    
    # Display sortable dataframe - TEXT ONLY
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )
    
    # Download button for data
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Seller Data (CSV)",
        data=csv,
        file_name=f"{st.session_state.current_product}_sellers.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # WARNING NOTE - Requirement 4
    st.warning("🚨 Note: High-rating sellers do not always deliver the original brand. Always check Satya View before buying!")
    
    # SATYA VIEW SELECTOR - Requirement 4
    st.markdown("### 🔍 Quick Satya View Check")
    
    # Create list of seller names for selectbox
    seller_names = [s["seller_name"] for s in sellers]
    
    selected_seller_name = st.selectbox(
        "Select a seller to verify authenticity:",
        options=seller_names,
        key="seller_selector"
    )
    
    if st.button("🔍 Run Satya View for Selected", use_container_width=True):
        # Find the selected seller object
        selected_seller = next((s for s in sellers if s["seller_name"] == selected_seller_name), None)
        
        if selected_seller:
            # Save to session state
            st.session_state.selected_seller = selected_seller
            
            # CRITICAL: Save the exact price to session state for True Cost Calculator
            st.session_state.product_price = selected_seller['price']
            
            # Navigate to Satya View
            st.switch_page("pages/2_Satya_View.py")


# Main execution
if __name__ == "__main__":
    render_seller_matrix_page()




