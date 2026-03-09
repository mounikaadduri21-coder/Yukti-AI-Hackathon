"""
Data models for Yukti AI e-commerce intelligence platform.

This module defines the core data structures used across the application:
- SellerData: Represents seller information from e-commerce platforms
- AuthenticityStatus: Enum for product authenticity verification results
- UsageProfile: Enum for user consumption patterns
- ProductInput: User input for TCO calculations
- TCOBreakdown: Total cost of ownership calculation results
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class AuthenticityStatus(Enum):
    """
    Traffic light indicator for product authenticity verification.
    
    Maps Feature_Match_Score ranges to visual status indicators:
    - AUTHENTIC: >90% match (green indicator)
    - UNCERTAIN: 50-90% match (yellow indicator)
    - FAKE: <50% match (red indicator)
    
    Validates: Requirements 5.3, 5.4, 5.5
    """
    AUTHENTIC = ("green", "✅ Authentic", ">90% Match")
    UNCERTAIN = ("yellow", "⚠️ Uncertain - Manual Review Recommended", "50-90% Match")
    FAKE = ("red", "❌ Potential Fake", "<50% Match")
    
    def __init__(self, color: str, label: str, description: str):
        self.color = color
        self.label = label
        self.description = description


class UsageProfile(Enum):
    """
    User-defined consumption patterns for TCO calculations.
    
    Affects cost multipliers for power, consumables, and maintenance:
    - HEAVY: Daily usage, >4 hours (1.5x multiplier)
    - MEDIUM: 3-4 times/week, 2-4 hours (1.0x multiplier)
    - LIGHT: Weekly usage, <2 hours (0.5x multiplier)
    
    Validates: Requirements 6.2, 6.3
    """
    HEAVY = ("Heavy", "Daily usage, >4 hours per day")
    MEDIUM = ("Medium", "3-4 times per week, 2-4 hours per session")
    LIGHT = ("Light", "Weekly usage, <2 hours per session")
    
    def __init__(self, name: str, description: str):
        self.profile_name = name
        self.description = description


@dataclass
class SellerData:
    """
    Represents seller information aggregated from e-commerce platforms.
    
    Attributes:
        seller_name: Name of the seller/merchant
        platform: E-commerce platform (e.g., "Amazon", "Flipkart", "Myntra")
        price: Product price in INR
        trust_score: Normalized trust score (0.0-5.0) based on verified reviews
        is_sponsored: Whether the listing is a paid advertisement
        review_count: Number of verified customer reviews
        product_url: URL to product page for "Buy Now" functionality
    
    Validates: Requirements 2.3, 2.4, 2.6
    """
    seller_name: str
    platform: str
    price: float
    trust_score: float
    is_sponsored: bool
    review_count: int
    product_url: str


@dataclass
class ProductInput:
    """
    User input for True-Cost Calculator.
    
    Attributes:
        name: Product name/description
        sticker_price: Initial purchase price in INR
        category: Product category (e.g., "Air Purifier", "Vacuum Cleaner")
        usage_profile: User's consumption pattern (HEAVY, MEDIUM, or LIGHT)
    
    Validates: Requirements 6.1, 6.2
    """
    name: str
    sticker_price: float
    category: str
    usage_profile: UsageProfile


@dataclass
class TCOBreakdown:
    """
    Total cost of ownership calculation results over 3 years.
    
    Attributes:
        sticker_price: Initial purchase price in INR
        year_1_costs: Total costs in year 1 (power + consumables + maintenance)
        year_2_costs: Total costs in year 2
        year_3_costs: Total costs in year 3
        total_3_year_cost: Sum of sticker price and all 3 years of costs
        monthly_cost: Effective monthly cost (total_3_year_cost / 36)
        breakdown_details: Detailed cost breakdown by category
            - "power": List of yearly power costs [year1, year2, year3]
            - "consumables": List of yearly consumable costs
            - "maintenance": List of yearly maintenance costs
    
    Validates: Requirements 7.5, 7.6
    """
    sticker_price: float
    year_1_costs: float
    year_2_costs: float
    year_3_costs: float
    total_3_year_cost: float
    monthly_cost: float
    breakdown_details: Dict[str, List[float]]
