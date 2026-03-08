"""
Visualization Utilities for Yukti AI
Provides reusable UI components and charts
"""

import plotly.graph_objects as go
import streamlit as st
from typing import Dict

# Trust Blue theme color
TRUST_BLUE = "#0056D2"

# Platform-specific colors
PLATFORM_COLORS = {
    "Amazon": "#FF9900",
    "Flipkart": "#2874F0",
    "Myntra": "#FF3F6C",
    "Meesho": "#9F2089",
    "Croma": "#00A699",
    "JioMart": "#E60000"
}


def create_sentiment_bar_chart(sentiment: Dict) -> go.Figure:
    """
    Create horizontal bar chart for sentiment analysis
    
    Args:
        sentiment: Dictionary with positive_pct, neutral_pct, negative_pct
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=["Sentiment"],
        x=[sentiment["positive_pct"]],
        name="Positive",
        orientation='h',
        marker=dict(color='#28a745'),
        text=f"{sentiment['positive_pct']}%",
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        y=["Sentiment"],
        x=[sentiment["neutral_pct"]],
        name="Neutral",
        orientation='h',
        marker=dict(color='#ffc107'),
        text=f"{sentiment['neutral_pct']}%",
        textposition='inside'
    ))
    
    fig.add_trace(go.Bar(
        y=["Sentiment"],
        x=[sentiment["negative_pct"]],
        name="Negative",
        orientation='h',
        marker=dict(color='#dc3545'),
        text=f"{sentiment['negative_pct']}%",
        textposition='inside'
    ))
    
    fig.update_layout(
        barmode='stack',
        title="Customer Sentiment Analysis",
        xaxis_title="Percentage",
        showlegend=True,
        height=200,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return apply_trust_blue_theme(fig)


def create_cost_comparison_chart(cost_data: Dict) -> go.Figure:
    """
    Create bar chart comparing costs
    
    Args:
        cost_data: Dictionary with cost breakdown
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    if "fake_monthly_cost" in cost_data:
        # Scenario A: Fake vs Original
        fig.add_trace(go.Bar(
            x=["Fake Product", "Original Product"],
            y=[cost_data["fake_monthly_cost"], cost_data["original_monthly_cost"]],
            marker=dict(color=['#dc3545', '#28a745']),
            text=[f"₹{cost_data['fake_monthly_cost']}/mo", f"₹{cost_data['original_monthly_cost']}/mo"],
            textposition='outside'
        ))
        fig.update_layout(title="Monthly Cost Comparison", yaxis_title="Cost per Month (₹)")
    
    elif "base_price" in cost_data:
        # Scenario B: Cost breakdown
        fig.add_trace(go.Bar(
            x=["Base Price", "Filter Costs", "Maintenance", "Total 1-Year"],
            y=[cost_data["base_price"], cost_data["filter_costs_yearly"], 
               cost_data["maintenance_costs_yearly"], cost_data["total_1_year_cost"]],
            marker=dict(color=[TRUST_BLUE, '#ffc107', '#ffc107', '#dc3545']),
            text=[f"₹{cost_data['base_price']}", f"₹{cost_data['filter_costs_yearly']}", 
                  f"₹{cost_data['maintenance_costs_yearly']}", f"₹{cost_data['total_1_year_cost']}"],
            textposition='outside'
        ))
        fig.update_layout(title="1-Year Total Cost Breakdown", yaxis_title="Cost (₹)")
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return apply_trust_blue_theme(fig)


def display_signal_indicator(signal: str, match_pct: float, is_generic: bool = False) -> None:
    """
    Display large traffic light signal with emoji and text
    
    Args:
        signal: "Green", "Yellow", or "Red"
        match_pct: Match percentage
        is_generic: Whether product is generic/unbranded
    """
    if signal == "Green":
        emoji = "🟢"
        color = "#28a745"
        if is_generic:
            verdict = "Verified Safe (Generic Item)"
            warning = "⚠️ Generic / Unbranded Item"
        else:
            verdict = "Verified Safe"
            warning = None
    elif signal == "Yellow":
        emoji = "🟡"
        color = "#ffc107"
        verdict = "Honest seller, but likely a replica/old packaging"
        warning = None
    else:  # Red
        emoji = "🔴"
        color = "#dc3545"
        if is_generic:
            verdict = "Seller misrepresentation detected"
        else:
            verdict = "Scam/Bait & Switch"
        warning = None
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: {color}20; border-radius: 10px; border: 3px solid {color};">
        <h1 style="font-size: 80px; margin: 0;">{emoji}</h1>
        <h2 style="color: {color}; margin: 10px 0;">{verdict}</h2>
        <h3 style="margin: 10px 0;">Match: {match_pct}%</h3>
        {f'<p style="color: #ff6b00; font-weight: bold; font-size: 18px;">{warning}</p>' if warning else ''}
    </div>
    """, unsafe_allow_html=True)


def display_platform_badge(platform: str, seller_name: str) -> None:
    """
    Display platform badge with brand colors
    
    Args:
        platform: Platform name
        seller_name: Seller name
    """
    color = PLATFORM_COLORS.get(platform, TRUST_BLUE)
    
    st.markdown(f"""
    <div style="display: inline-block; padding: 5px 15px; background-color: {color}; color: white; 
                border-radius: 5px; font-weight: bold; margin-bottom: 10px;">
        {platform} • {seller_name}
    </div>
    """, unsafe_allow_html=True)


def display_aws_service_indicator(service: str, message: str, status: str = "processing") -> None:
    """
    Display AWS service indicator with icon and message
    
    Args:
        service: Service name (Lambda, S3, Rekognition, Bedrock)
        message: Status message
        status: "processing", "complete", or "info"
    """
    icons = {
        "Lambda": "🔄",
        "S3": "📦",
        "Rekognition": "🔍",
        "Bedrock": "🤖"
    }
    
    icon = icons.get(service, "☁️")
    
    if status == "processing":
        st.spinner(f"{icon} {service}: {message}")
    elif status == "complete":
        st.success(f"✅ {service}: {message}")
    else:
        st.info(f"{icon} {service}: {message}")


def apply_trust_blue_theme(fig: go.Figure) -> go.Figure:
    """
    Apply Trust Blue theme to Plotly figures
    
    Args:
        fig: Plotly figure
        
    Returns:
        Updated figure with theme applied
    """
    fig.update_layout(
        font=dict(family="Arial, sans-serif", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_font=dict(color=TRUST_BLUE, size=16, family="Arial, sans-serif")
    )
    
    return fig


def create_buy_box(seller: Dict) -> None:
    """
    Create clean Buy Box UI for a seller
    
    Args:
        seller: Seller dictionary
    """
    platform_color = PLATFORM_COLORS.get(seller["platform"], TRUST_BLUE)
    
    # Determine if this is a top pick or scam
    badge = ""
    if seller.get("is_top_pick"):
        badge = '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 5px; font-size: 12px; margin-left: 10px;">✅ TOP PICK</span>'
    elif seller.get("is_scam"):
        badge = '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 5px; font-size: 12px; margin-left: 10px;">⚠️ SUSPICIOUS</span>'
    
    # Star rating display
    stars = "⭐" * int(seller["rating"])
    
    st.markdown(f"""
    <div style="border: 2px solid {platform_color}; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: white;">
        <div style="background-color: {platform_color}; color: white; padding: 8px 15px; border-radius: 5px; display: inline-block; font-weight: bold; margin-bottom: 15px;">
            {seller["platform"]}
        </div>
        {badge}
        <h3 style="margin: 10px 0; color: #333;">{seller["seller_name"]}</h3>
        <div style="font-size: 32px; color: {TRUST_BLUE}; font-weight: bold; margin: 10px 0;">
            ₹{seller["price"]}
        </div>
        <div style="margin: 10px 0;">
            <span style="font-size: 20px;">{stars}</span>
            <span style="color: #666; margin-left: 10px;">{seller["rating"]} ({seller["review_count"]} reviews)</span>
        </div>
        <div style="color: #666; margin: 10px 0;">
            🚚 Delivery: {seller["delivery_days"]} days
        </div>
    </div>
    """, unsafe_allow_html=True)
