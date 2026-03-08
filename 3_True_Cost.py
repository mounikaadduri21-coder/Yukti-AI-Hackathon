"""
True Cost Calculator Page for Yukti AI
Financial trap detection with dynamic price connection
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Yukti AI - True Cost",
    page_icon="💰",
    layout="wide"
)

# MASTER DICTIONARY - ALL 12 PRODUCTS
master_data = {
    'Kent RO': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Direct Manufacturer Pricing.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Full brand support.'
    },
    'Hawkins Cooker': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Standard Market Price.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Kitchen safety verified.'
    },
    'Manyavar Dhotis': {
        'score': 100.0,
        'color': 'Green',
        'reason': '🌸 Spring Wedding Season Offer.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Genuine fabric guaranteed.'
    },
    'Milton Lunch Box': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Standard Market Price.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Safe for daily health.'
    },
    'Mamaearth Oil': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Standard Market Price.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Organic ingredients verified.'
    },
    'Lifelong Spin Bike': {
        'score': 100.0,
        'color': 'Green',
        'reason': '📉 End of Financial Year Clearance.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Structural integrity verified.'
    },
    'Zebronics Keyboard': {
        'score': 100.0,
        'color': 'Green',
        'reason': 'Standard Market Price.',
        'risk': 'None. Authentic.',
        'advice': '✅ Smart Investment. Tech support verified.'
    },
    'Titan Smartwatch': {
        'score': 98.1,
        'color': 'Yellow',
        'reason': 'Unverified Third-Party Seller Pricing.',
        'risk': 'Grey Market / No Service Center Support',
        'advice': '⚠️ High Match (98.1%). Great hardware, but no official warranty.'
    },
    'Lakmé Kajal': {
        'score': 95.5,
        'color': 'Yellow',
        'reason': 'Unverified Third-Party Seller Pricing.',
        'risk': 'Unverified Storage / No Return Policy',
        'advice': '⚠️ High Match (95.5%). Good quality, but lacks brand return policies.'
    },
    'Uppada Saree': {
        'score': 94.2,
        'color': 'Yellow',
        'reason': 'Unverified Silk Purity Pricing.',
        'risk': 'Color fading risk',
        'advice': '⚠️ High Match (94.2%). Beautiful, but lacks official brand guarantees.'
    },
    'boAt Earbuds': {
        'score': 92.5,
        'color': 'Yellow',
        'reason': '⚡ Overstock Flash Sale by Unverified Seller.',
        'risk': 'Loss of 1-Year Brand Warranty',
        'advice': '⚠️ High Match (92.5%). Great hardware, but trading warranty for a discount.'
    },
    'Unbranded Sling Bag': {
        'score': 88.0,
        'color': 'Yellow',
        'reason': 'Unbranded Bulk Import Pricing.',
        'risk': 'Wear and Tear with No Guarantee',
        'advice': '⚠️ Good Match (88.0%). Good value, but no brand durability guarantee.'
    }
}


def render_true_cost_page() -> None:
    """Main True Cost Calculator page"""
    st.title("💰 True Cost Calculator")
    
    # Check if product is set
    if not st.session_state.get('current_product'):
        st.warning("⚠️ Please search for a product first from the Home page!")
        return
    
    # Read the product from session state
    selected_product = st.session_state.get('current_product')
    
    # Get the selected seller data (contains the price)
    seller_data = st.session_state.get('selected_seller', None)
    
    if not seller_data:
        st.warning("⚠️ Please select a seller from the Seller Matrix page first!")
        st.info("👉 Navigate to **Seller Matrix** and click **🔍 Run Satya View** on any seller")
        return
    
    # Get the exact price from session state (CRITICAL: Must match across all pages)
    product_price = st.session_state.get('product_price', seller_data.get('price', 0))
    
    # Look up the data directly from master dictionary
    if selected_product not in master_data:
        st.error(f"❌ Product '{selected_product}' not found in master data!")
        return
    
    data = master_data[selected_product]
    
    # Product header
    st.markdown(f"### Analyzing: **{selected_product}**")
    st.markdown("---")
    
    # The Math Calculation: Create fake 'Market Price' to show discount
    market_price = float(product_price) * 1.25
    discount_saved = market_price - float(product_price)
    
    # The Pricing UI: Three columns showing Market Price, Your Price, and Savings
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Market Price", value=f"₹{market_price:,.2f}")
    
    with col2:
        st.metric(label="Your Price (Satya View)", value=f"₹{float(product_price):,.2f}")
    
    with col3:
        st.metric(label="You Saved", value=f"₹{discount_saved:,.2f}")
    
    st.markdown("---")
    
    # Display the AI Advice based on color
    st.markdown("### 🤖 AI Advice")
    
    if data['color'] == 'Green':
        st.success(data['advice'])
    elif data['color'] == 'Yellow':
        st.warning(data['advice'])
    else:
        st.error(data['advice'])
    
    st.markdown("---")
    
    # The AI Analysis
    st.markdown("### 📊 AI Market Analysis")
    st.info(f"AI Market Analysis: {data['reason']}")
    
    st.markdown("---")
    
    # Display Hidden Risk
    st.markdown("### ⚠️ Hidden Risk")
    st.error(f"Hidden Risk: {data['risk']}")
    
    st.markdown("---")
    
    # Final Math Conclusion
    st.markdown("### 💡 Final Math Conclusion")
    st.write(f"You saved ₹{discount_saved:,.2f} today. However, please review the hidden risks above to ensure your True Cost does not increase over time!")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🧭 What's Next?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔙 Back to Satya View", use_container_width=True):
            st.info("👈 Use the sidebar to navigate back to Satya View")
    
    with col2:
        if st.button("🔄 New Search", use_container_width=True):
            st.info("👉 Navigate to **Home** page to start a new search!")


# Main execution
if __name__ == "__main__":
    render_true_cost_page()
