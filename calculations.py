"""
Calculation utilities for Yukti AI e-commerce intelligence platform.

This module provides core calculation functions for:
- Trust score normalization across platforms
- Price competitiveness analysis
- Yukti Score aggregation
- Total cost of ownership (TCO) calculations
- Cost multipliers for different product categories and usage profiles

Validates: Requirements 2.4, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3
"""

from typing import Dict, List, Optional
from .models import UsageProfile


# Platform-specific trust score normalization configuration
# UNIVERSAL E-COMMERCE: Supports ANY platform, not limited to specific ones
# Maps platform names to their normalization parameters
TRUST_SCORE_NORMALIZATION = {
    "Amazon": {
        "max_raw_score": 5.0,
        "verified_review_weight": 1.0,
    },
    "Flipkart": {
        "max_raw_score": 5.0,
        "verified_review_weight": 0.9,
    },
    "Myntra": {
        "max_raw_score": 5.0,
        "verified_review_weight": 0.85,
    },
    "Croma": {
        "max_raw_score": 5.0,
        "verified_review_weight": 0.88,
    },
    "JioMart": {
        "max_raw_score": 5.0,
        "verified_review_weight": 0.87,
    },
    "Nykaa": {
        "max_raw_score": 5.0,
        "verified_review_weight": 0.86,
    },
    "Default": {  # Fallback for ANY unknown platform
        "max_raw_score": 5.0,
        "verified_review_weight": 0.8,
    },
}


# Category-based cost multipliers for TCO calculations
# Each category defines power consumption, consumable costs, and maintenance costs
COST_MULTIPLIERS = {
    "Air Purifier": {
        "power_kwh_per_hour": 0.05,
        "filter_cost_per_year": 3000,
        "maintenance_cost_per_year": 500,
    },
    "Vacuum Cleaner": {
        "power_kwh_per_hour": 1.2,
        "bag_cost_per_year": 800,
        "maintenance_cost_per_year": 1000,
    },
    "Water Purifier": {
        "power_kwh_per_hour": 0.025,
        "filter_cost_per_year": 4000,
        "maintenance_cost_per_year": 1500,
    },
    "Washing Machine": {
        "power_kwh_per_hour": 0.5,
        "filter_cost_per_year": 500,
        "maintenance_cost_per_year": 2000,
    },
    "Refrigerator": {
        "power_kwh_per_hour": 0.15,
        "filter_cost_per_year": 1000,
        "maintenance_cost_per_year": 1500,
    },
    "Air Conditioner": {
        "power_kwh_per_hour": 1.5,
        "filter_cost_per_year": 1500,
        "maintenance_cost_per_year": 3000,
    },
    "Microwave Oven": {
        "power_kwh_per_hour": 1.0,
        "filter_cost_per_year": 0,
        "maintenance_cost_per_year": 500,
    },
    "Electric Kettle": {
        "power_kwh_per_hour": 1.5,
        "filter_cost_per_year": 0,
        "maintenance_cost_per_year": 200,
    },
    "Generic": {  # Fallback for unknown product categories - prevents crashes
        "power_kwh_per_hour": 0.1,
        "filter_cost_per_year": 2000,
        "maintenance_cost_per_year": 1000,
    },
}


# Usage profile multipliers for adjusting costs based on consumption patterns
USAGE_MULTIPLIERS = {
    UsageProfile.HEAVY: 1.5,
    UsageProfile.MEDIUM: 1.0,
    UsageProfile.LIGHT: 0.5,
}


def normalize_trust_score(raw_score: float, platform: str) -> float:
    """
    Normalize platform-specific trust scores to a uniform 0.0-5.0 scale.
    
    Different e-commerce platforms use different rating systems and have
    varying levels of review verification. This function normalizes scores
    to a consistent scale while accounting for platform-specific reliability.
    
    Args:
        raw_score: The original trust score from the platform
        platform: The e-commerce platform name (e.g., "Amazon", "Flipkart")
    
    Returns:
        Normalized trust score in the range [0.0, 5.0]
    
    Validates: Requirements 2.4
    
    Examples:
        >>> normalize_trust_score(4.5, "Amazon")
        4.5
        >>> normalize_trust_score(4.5, "Flipkart")
        4.05
    """
    # Get platform-specific normalization parameters
    # Use "Default" fallback for unknown platforms
    platform_config = TRUST_SCORE_NORMALIZATION.get(platform, TRUST_SCORE_NORMALIZATION["Default"])
    
    # Normalize to 0.0-5.0 scale
    max_score = platform_config["max_raw_score"]
    weight = platform_config["verified_review_weight"]
    
    # Clamp raw_score to valid range
    clamped_score = max(0.0, min(raw_score, max_score))
    
    # Normalize and apply platform weight
    normalized = (clamped_score / max_score) * 5.0 * weight
    
    # Ensure result is within bounds
    return max(0.0, min(normalized, 5.0))


def calculate_price_competitiveness(price: float, all_prices: List[float]) -> float:
    """
    Calculate how competitive a price is compared to all available prices.
    
    Returns a score from 0.0 (most expensive) to 1.0 (least expensive).
    Uses inverse ranking where lower prices get higher scores.
    
    Args:
        price: The price to evaluate
        all_prices: List of all available prices for comparison
    
    Returns:
        Price competitiveness score in the range [0.0, 1.0]
        Returns 1.0 if only one price is provided
    
    Validates: Requirements 8.1
    
    Examples:
        >>> calculate_price_competitiveness(100, [100, 200, 300])
        1.0
        >>> calculate_price_competitiveness(200, [100, 200, 300])
        0.5
        >>> calculate_price_competitiveness(300, [100, 200, 300])
        0.0
    """
    if not all_prices or len(all_prices) == 0:
        return 1.0
    
    if len(all_prices) == 1:
        return 1.0
    
    # Find min and max prices
    min_price = min(all_prices)
    max_price = max(all_prices)
    
    # Handle case where all prices are the same
    if max_price == min_price:
        return 1.0
    
    # Calculate competitiveness (inverse of normalized price)
    # Lower price = higher competitiveness
    competitiveness = 1.0 - ((price - min_price) / (max_price - min_price))
    
    return max(0.0, min(competitiveness, 1.0))


def calculate_yukti_score(
    trust_score: Optional[float] = None,
    price_competitiveness: Optional[float] = None,
    authenticity_score: Optional[float] = None,
    tco_competitiveness: Optional[float] = None
) -> Optional[int]:
    """
    Calculate overall Yukti Score (0-100) from available metrics.
    
    The Yukti Score is an aggregated recommendation confidence metric that
    combines multiple factors when available:
    - Trust score: Seller reliability (0.0-5.0 normalized to 0-100)
    - Price competitiveness: How good the price is (0.0-1.0 normalized to 0-100)
    - Authenticity score: Product authenticity (0-100)
    - TCO competitiveness: Total cost of ownership ranking (0.0-1.0 normalized to 0-100)
    
    Args:
        trust_score: Normalized trust score (0.0-5.0), optional
        price_competitiveness: Price ranking (0.0-1.0), optional
        authenticity_score: Feature match score (0-100), optional
        tco_competitiveness: TCO ranking (0.0-1.0), optional
    
    Returns:
        Yukti Score (0-100) or None if insufficient data available
        Returns None if no metrics are provided
    
    Validates: Requirements 8.1, 8.2, 8.3, 8.6
    
    Examples:
        >>> calculate_yukti_score(trust_score=4.5, price_competitiveness=0.8)
        86
        >>> calculate_yukti_score(authenticity_score=95)
        95
        >>> calculate_yukti_score()
        None
    """
    # Collect available metrics and normalize them to 0-100 scale
    metrics = []
    
    if trust_score is not None:
        # Normalize trust score from 0.0-5.0 to 0-100
        normalized_trust = (trust_score / 5.0) * 100
        metrics.append(normalized_trust)
    
    if price_competitiveness is not None:
        # Normalize price competitiveness from 0.0-1.0 to 0-100
        normalized_price = price_competitiveness * 100
        metrics.append(normalized_price)
    
    if authenticity_score is not None:
        # Authenticity score is already 0-100
        metrics.append(authenticity_score)
    
    if tco_competitiveness is not None:
        # Normalize TCO competitiveness from 0.0-1.0 to 0-100
        normalized_tco = tco_competitiveness * 100
        metrics.append(normalized_tco)
    
    # Return None if no metrics available
    if not metrics:
        return None
    
    # Calculate average of available metrics
    yukti_score = sum(metrics) / len(metrics)
    
    # Round to integer and ensure bounds
    return int(max(0, min(yukti_score, 100)))


def get_cost_multipliers(category: str, usage: UsageProfile) -> Dict[str, float]:
    """
    Get cost multipliers for power, consumables, and maintenance.
    
    Returns category-specific base costs adjusted by usage profile multiplier.
    Used for calculating total cost of ownership (TCO) over time.
    
    Args:
        category: Product category (e.g., "Air Purifier", "Vacuum Cleaner")
        usage: User's consumption pattern (HEAVY, MEDIUM, or LIGHT)
    
    Returns:
        Dictionary with keys:
        - "power_kwh_per_hour": Power consumption in kWh per hour
        - "consumable_cost_per_year": Annual consumable costs (filters, bags, etc.)
        - "maintenance_cost_per_year": Annual maintenance costs
        
        All values are adjusted by the usage profile multiplier.
    
    Validates: Requirements 7.2, 7.3, 7.4
    
    Examples:
        >>> multipliers = get_cost_multipliers("Air Purifier", UsageProfile.HEAVY)
        >>> multipliers["power_kwh_per_hour"]
        0.075
        >>> multipliers["consumable_cost_per_year"]
        4500.0
    """
    # Get base cost multipliers for category
    # Use "Generic" fallback for unknown categories
    base_multipliers = COST_MULTIPLIERS.get(category, COST_MULTIPLIERS["Generic"]).copy()
    
    # Get usage profile multiplier
    usage_multiplier = USAGE_MULTIPLIERS.get(usage, 1.0)
    
    # Apply usage multiplier to all costs
    # Handle both filter_cost_per_year and bag_cost_per_year keys
    consumable_key = None
    if "filter_cost_per_year" in base_multipliers:
        consumable_key = "filter_cost_per_year"
    elif "bag_cost_per_year" in base_multipliers:
        consumable_key = "bag_cost_per_year"
    
    consumable_cost = base_multipliers.get(consumable_key, 0) if consumable_key else 0
    
    adjusted_multipliers = {
        "power_kwh_per_hour": base_multipliers["power_kwh_per_hour"] * usage_multiplier,
        "consumable_cost_per_year": consumable_cost * usage_multiplier,
        "maintenance_cost_per_year": base_multipliers["maintenance_cost_per_year"] * usage_multiplier,
    }
    
    return adjusted_multipliers
