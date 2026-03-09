"""
Seed Data Module for Yukti AI
Provides MVP product database and dynamic seller data generation
"""

import random
from typing import Dict, List, Tuple

# 12 MVP Products across 6 categories
MVP_PRODUCTS = {
    "Electronics": ["boAt Earbuds", "Titan Smartwatch"],
    "Fashion": ["Uppada Saree", "Manyavar Dhotis", "Unbranded Sling Bag"],
    "Home": ["Kent RO", "Hawkins Cooker"],
    "Health": ["Lifelong Spin Bike"],
    "Office": ["Zebronics Keyboard", "Milton Lunch Box"],
    "Beauty": ["Lakmé Kajal", "Mamaearth Oil"]
}

# Realistic Base Prices for each product (in INR)
BASE_PRICES = {
    'Kent RO': 15000,
    'Hawkins Cooker': 2000,
    'Manyavar Dhotis': 3000,
    'Milton Lunch Box': 800,
    'Mamaearth Oil': 400,
    'Lifelong Spin Bike': 9000,
    'Zebronics Keyboard': 1200,
    'Titan Smartwatch': 2500,
    'Lakmé Kajal': 150,
    'Uppada Saree': 3000,
    'boAt Earbuds': 899,
    'Unbranded Sling Bag': 600
}

# Price ranges in INR for each category (DEPRECATED - using BASE_PRICES now)
PRICE_RANGES = {
    "Electronics": (500, 5000),
    "Fashion": (300, 3000),
    "Home": (2000, 15000),
    "Health": (5000, 25000),
    "Office": (200, 2000),
    "Beauty": (100, 1000)
}

# Platform-specific seller name templates - expanded for uniqueness
PLATFORM_SELLER_TEMPLATES = {
    "Amazon": [
        "TechStore Official", "ElectroHub", "GadgetWorld", "PrimeDeals", "AmazonChoice",
        "Digital Emporium", "SmartBuy Store", "Elite Electronics", "Premium Gadgets", "TechVista",
        "Quantum Retail", "NextGen Store", "Alpha Electronics", "ProTech Hub", "Mega Electronics"
    ],
    "Flipkart": [
        "SuperMart", "MegaStore", "ValueShop", "FlipDeals", "FlipkartAssured",
        "RetailKing", "ShopSmart", "BestBuy India", "ValuePlus", "TopChoice Store",
        "FlipMart Pro", "Express Retail", "Quality Store", "TrustMart", "Premier Shop"
    ],
    "Myntra": [
        "FashionHub", "StyleStore", "TrendyWear", "ChicBoutique", "MyntraFashion",
        "Vogue Retail", "Glamour Store", "Style Avenue", "Fashion Forward", "Trendsetter",
        "Elite Fashion", "Couture Corner", "Style Studio", "Fashion Palace", "Chic Collection"
    ],
    "Meesho": [
        "MeeshoMart", "BudgetBazaar", "ValueDeals", "MeeshoOfficial", "SmartShopper",
        "Affordable Store", "Economy Shop", "Budget King", "Value Vault", "Saver's Choice",
        "Discount Hub", "Thrift Store", "Smart Deals", "Budget Friendly", "Value Express"
    ],
    "Croma": [
        "ElectroWorld", "TechZone", "CromaRetail", "GadgetStore", "CromaOfficial",
        "Electronics Pro", "Tech Paradise", "Digital World", "Gadget Galaxy", "Tech Empire",
        "Electro Hub", "Tech Mart", "Digital Store", "Gadget Central", "Tech Bazaar"
    ],
    "JioMart": [
        "JioRetail", "SmartMart", "JioDeals", "ValueMart", "JioMartOfficial",
        "Reliance Store", "Jio Express", "Digital Mart", "Smart Retail", "Jio Plus",
        "Mega Mart", "Jio Select", "Prime Retail", "Jio Choice", "Super Store"
    ]
}

# Track used seller names globally to ensure uniqueness across products
_USED_SELLER_NAMES = set()

# 6 platforms to aggregate from
PLATFORMS = ["Amazon", "Flipkart", "Myntra", "Meesho", "Croma", "JioMart"]


def validate_product(product_name: str) -> Tuple[bool, str, str]:
    """
    Validate product against MVP list with fuzzy matching
    
    Args:
        product_name: User input product name
        
    Returns:
        Tuple of (is_valid, category, normalized_name)
    """
    product_name_lower = product_name.lower().strip()
    
    for category, products in MVP_PRODUCTS.items():
        for product in products:
            # Exact match or fuzzy match (contains)
            if product.lower() == product_name_lower or product.lower() in product_name_lower or product_name_lower in product.lower():
                return (True, category, product)
    
    return (False, "", "")


def get_price_range(category: str) -> Tuple[float, float]:
    """Get realistic price range for category in INR"""
    return PRICE_RANGES.get(category, (100, 1000))


def generate_product_image_url(product_name: str, seller_name: str = None) -> str:
    """
    Generate realistic product image URL for visual display
    
    Args:
        product_name: Product name
        seller_name: Optional seller name for variation
        
    Returns:
        Image URL from placeholder service
    """
    # Create unique image based on product and seller
    if seller_name:
        seed = hash(f"{product_name}_{seller_name}") % 1000
    else:
        seed = hash(product_name) % 1000
    
    # Use different placeholder services for variety
    services = [
        f"https://picsum.photos/seed/{seed}/400/400",
        f"https://via.placeholder.com/400x400/FF6B6B/FFFFFF?text={product_name.replace(' ', '+')}",
        f"https://via.placeholder.com/400x400/4ECDC4/FFFFFF?text={product_name.replace(' ', '+')}"
    ]
    
    # Choose service based on seed for consistency
    return services[seed % len(services)]


def generate_seller_data(product_name: str, category: str) -> List[Dict]:
    """
    Generate dynamic seller data for all 6 platforms with unique sellers and prices
    
    Args:
        product_name: Product name
        category: Product category
        
    Returns:
        List of seller dictionaries
    """
    # Get realistic base price for this specific product
    base_price = BASE_PRICES.get(product_name, 1000)
    
    all_sellers = []
    
    for platform in PLATFORMS:
        platform_sellers = generate_platform_sellers(platform, product_name, base_price)
        all_sellers.extend(platform_sellers)
    
    # NO scam target injection - all sellers are high-rated
    
    return all_sellers


def generate_platform_sellers(platform: str, product_name: str, base_price: float) -> List[Dict]:
    """
    Generate 3-5 sellers for a specific platform with unique data and HIGH RATINGS ONLY
    
    Args:
        platform: Platform name
        product_name: Product name
        base_price: Base price for variance calculation
        
    Returns:
        List of seller dictionaries for this platform
    """
    num_sellers = random.randint(3, 5)
    sellers = []
    seller_templates = PLATFORM_SELLER_TEMPLATES.get(platform, ["Store1", "Store2", "Store3"])
    
    # Create unique seed for this product-platform combination
    combo_seed = hash(f"{product_name}_{platform}") % 10000
    random.seed(combo_seed)
    
    for i in range(num_sellers):
        # Seller Variation Logic: Slight discount (2% to 10% off base price)
        # This ensures no two sellers have the exact same price
        discount_percentage = random.uniform(0.02, 0.10)  # 2% to 10% discount
        price = round(base_price * (1 - discount_percentage), 2)
        
        # HIGH RATINGS ONLY: 4.8, 4.9, or 5.0
        rating = random.choice([4.8, 4.9, 5.0])
        
        # Dynamic review count
        review_count = random.randint(500, 8000)
        
        # Dynamic delivery days
        delivery_days = random.randint(1, 5)
        
        # Get unique seller name
        available_names = [name for name in seller_templates if name not in _USED_SELLER_NAMES]
        if not available_names:
            # If all names used, create a unique variant
            seller_name = f"{random.choice(seller_templates)} {random.randint(100, 999)}"
        else:
            seller_name = random.choice(available_names)
        
        _USED_SELLER_NAMES.add(seller_name)
        
        seller = {
            "seller_name": seller_name,
            "platform": platform,
            "price": price,
            "rating": rating,
            "review_count": review_count,
            "delivery_days": delivery_days,
            "product_url": f"https://{platform.lower()}.com/product/{product_name.replace(' ', '-').lower()}-{random.randint(1000, 9999)}",
            "thumbnail_url": generate_product_image_url(product_name, seller_name),  # Add thumbnail
            "is_top_pick": False,
            "is_scam": False
        }
        
        sellers.append(seller)
    
    # Reset random seed
    random.seed()
    
    return sellers


def is_generic_product(product_name: str) -> bool:
    """Check if product is unbranded/generic"""
    generic_keywords = ["unbranded", "generic", "no brand"]
    return any(keyword in product_name.lower() for keyword in generic_keywords)


def get_all_mvp_products() -> List[str]:
    """Get flat list of all MVP products"""
    all_products = []
    for products in MVP_PRODUCTS.values():
        all_products.extend(products)
    return all_products
