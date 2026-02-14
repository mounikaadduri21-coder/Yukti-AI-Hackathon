# Design Document: Yukti AI

## Overview

Yukti AI is a Streamlit-based e-commerce intelligence platform that provides three analytical tools to help consumers make informed purchasing decisions. The architecture follows a modular page-based design where each feature (Seller Matrix, Satya-View, True-Cost Calculator) operates as an independent Streamlit page with shared utilities and state management.

The platform uses Streamlit's native session state for data persistence, Plotly for interactive visualizations, and mocked AWS services (Rekognition, Bedrock) for the prototype phase. The design emphasizes simplicity, modularity, and user experience with a consistent Trust Blue (#0056D2) theme throughout.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit App (app.py)               │
│  ┌───────────────────────────────────────────────────┐  │
│  │     Navigation Menu (streamlit-option-menu)       │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                              │
│         ┌────────────────┼────────────────┐             │
│         │                │                │             │
│    ┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐       │
│    │  Seller  │    │  Satya   │    │   True   │       │
│    │  Matrix  │    │   View   │    │   Cost   │       │
│    │  Page    │    │   Page   │    │   Page   │       │
│    └────┬─────┘    └────┬─────┘    └────┬─────┘       │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│              ┌───────────▼───────────┐                  │
│              │   Shared Utilities    │                  │
│              │  - aws_mock.py        │                  │
│              │  - calculations.py    │                  │
│              │  - visualization.py   │                  │
│              └───────────────────────┘                  │
│                          │                              │
│              ┌───────────▼───────────┐                  │
│              │   st.session_state    │                  │
│              │  (Data Persistence)   │                  │
│              └───────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Navigation Layer**: User selects a feature from the navigation menu
2. **Page Layer**: Selected page component loads and accesses session state
3. **Utility Layer**: Page components call shared utilities for calculations, API mocks, and visualizations
4. **State Layer**: All data persists in st.session_state across page transitions

## Components and Interfaces

### 1. Main Application (app.py)

**Responsibility**: Application entry point, navigation setup, and global configuration

**Interface**:
```python
def main() -> None:
    """Initialize Streamlit app with navigation and theme configuration"""
    
def setup_page_config() -> None:
    """Configure Streamlit page settings (title, icon, layout, theme)"""
    
def render_navigation() -> str:
    """Render navigation menu and return selected page"""
    
def display_header() -> None:
    """Display Yukti AI logo and tagline"""
```

**Key Behaviors**:
- Sets page configuration with Trust Blue theme
- Initializes session state keys if not present
- Renders navigation menu using streamlit-option-menu
- Routes to selected page component

### 2. Seller Matrix Page (pages/1_Seller_Matrix.py)

**Responsibility**: Aggregate and visualize seller data across e-commerce platforms

**Interface**:
```python
def render_seller_matrix_page() -> None:
    """Main page rendering function"""
    
def fetch_seller_data(sku: str) -> List[SellerData]:
    """Fetch seller data from multiple platforms for given SKU"""
    
def filter_organic_sellers(sellers: List[SellerData]) -> List[SellerData]:
    """Remove sponsored sellers from the list"""
    
def normalize_trust_score(raw_score: float, platform: str) -> float:
    """Normalize platform-specific trust scores to 0.0-5.0 scale"""
    
def create_scatter_plot(sellers: List[SellerData]) -> plotly.graph_objects.Figure:
    """Generate interactive scatter plot with color-coded trust/price visualization"""
    
def calculate_seller_color(trust_score: float, price: float, 
                          max_price: float) -> str:
    """Calculate color gradient from green (good) to red (bad)"""
```

**Data Structures**:
```python
@dataclass
class SellerData:
    seller_name: str
    platform: str
    price: float  # INR
    trust_score: float  # 0.0-5.0
    is_sponsored: bool
    review_count: int
    product_url: str  # URL to product page for "Buy Now" functionality
```

### 3. Satya-View Page (pages/2_Satya_View.py)

**Responsibility**: Visual product authenticity verification using image comparison

**Interface**:
```python
def render_satya_view_page() -> None:
    """Main page rendering function"""
    
def handle_image_upload() -> Optional[bytes]:
    """Handle file upload and validation"""
    
def validate_image(image_bytes: bytes) -> Tuple[bool, str]:
    """Validate image format and size, return (is_valid, error_message)"""
    
def compare_images(user_image: bytes, golden_source: bytes) -> float:
    """Compare images and return Feature_Match_Score (0-100%)"""
    
def determine_authenticity_status(match_score: float) -> AuthenticityStatus:
    """Map match score to traffic light status"""
    
def display_comparison_result(status: AuthenticityStatus, 
                              match_score: float,
                              user_image: bytes,
                              golden_source: bytes) -> None:
    """Display side-by-side comparison with traffic light indicator"""
```

**MockProductDatabase Component**:
```python
# Mock product database for Golden Source images (prototype)
MOCK_PRODUCT_DATABASE = {
    "default": {
        "name": "Generic Product",
        "golden_source_url": None,  # Uses generated placeholder
        "brand": "Official Brand",
    },
    # Additional products can be added here
}

def get_golden_source_from_database(product_id: str = "default") -> bytes:
    """
    Retrieve Golden Source image from mock database.
    For prototype: generates placeholder image to prevent crashes.
    In production: would fetch from actual product database or CDN.
    """
```

**Data Structures**:
```python
from enum import Enum

class AuthenticityStatus(Enum):
    AUTHENTIC = ("green", "✅ Authentic", ">90% Match")
    UNCERTAIN = ("yellow", "⚠️ Uncertain", "50-90% Match")
    FAKE = ("red", "❌ Potential Fake", "<50% Match")
```

### 4. True-Cost Calculator Page (pages/3_True_Cost.py)

**Responsibility**: Calculate and display total cost of ownership over 3 years

**Interface**:
```python
def render_true_cost_page() -> None:
    """Main page rendering function"""
    
def collect_product_inputs() -> Optional[ProductInput]:
    """Render input form and return validated data"""
    
def calculate_tco(product: ProductInput) -> TCOBreakdown:
    """Calculate 3-year total cost of ownership"""
    
def calculate_power_costs(category: str, usage: UsageProfile, 
                         years: int) -> List[float]:
    """Calculate yearly power consumption costs"""
    
def calculate_consumable_costs(category: str, usage: UsageProfile,
                               years: int) -> List[float]:
    """Calculate yearly consumable costs"""
    
def calculate_maintenance_costs(category: str, usage: UsageProfile,
                                years: int) -> List[float]:
    """Calculate yearly maintenance costs"""
    
def display_tco_breakdown(tco: TCOBreakdown) -> None:
    """Display breakdown table and visualizations"""
```

**Data Structures**:
```python
from enum import Enum

class UsageProfile(Enum):
    HEAVY = "Heavy (Daily, >4 hours)"
    MEDIUM = "Medium (3-4 times/week, 2-4 hours)"
    LIGHT = "Light (Weekly, <2 hours)"

@dataclass
class ProductInput:
    name: str
    sticker_price: float  # INR
    category: str
    usage_profile: UsageProfile

@dataclass
class TCOBreakdown:
    sticker_price: float
    year_1_costs: float
    year_2_costs: float
    year_3_costs: float
    total_3_year_cost: float
    monthly_cost: float
    breakdown_details: Dict[str, List[float]]  # power, consumables, maintenance
```

### 5. AWS Mock Utilities (utils/aws_mock.py)

**Responsibility**: Mock AWS Rekognition and Bedrock services for prototype

**Interface**:
```python
def mock_rekognition_compare_faces(source_image: bytes, 
                                   target_image: bytes) -> float:
    """Mock AWS Rekognition face/feature comparison, return similarity score"""
    
def mock_rekognition_detect_labels(image: bytes) -> List[Dict[str, Any]]:
    """Mock AWS Rekognition label detection"""
    
def mock_bedrock_invoke(prompt: str, model_id: str) -> str:
    """Mock AWS Bedrock LLM invocation"""
    
def simulate_api_delay() -> None:
    """Simulate realistic API response time (0.5-2 seconds)"""
```

**Implementation Notes**:
- Uses simple image hashing (perceptual hash) for similarity comparison
- Returns randomized but realistic scores for demonstration
- Includes configurable delay to simulate network latency
- Can be swapped with real AWS SDK calls via configuration flag

### 6. Calculation Utilities (utils/calculations.py)

**Responsibility**: Shared calculation logic for scores, costs, and metrics

**Interface**:
```python
def calculate_yukti_score(trust_score: Optional[float],
                         price_competitiveness: Optional[float],
                         authenticity_score: Optional[float],
                         tco_competitiveness: Optional[float]) -> Optional[int]:
    """Calculate overall Yukti Score (0-100) from available metrics"""
    
def normalize_score(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to 0.0-1.0 range"""
    
def calculate_price_competitiveness(price: float, 
                                   all_prices: List[float]) -> float:
    """Calculate how competitive a price is (0.0-1.0, higher is better)"""
    
def get_cost_multipliers(category: str, 
                        usage: UsageProfile) -> Dict[str, float]:
    """Get cost multipliers for power, consumables, maintenance"""
```

### 7. Visualization Utilities (utils/visualization.py)

**Responsibility**: Shared visualization components and styling

**Interface**:
```python
def create_yukti_score_gauge(score: int) -> plotly.graph_objects.Figure:
    """Create animated gauge chart for Yukti Score"""
    
def get_score_color(score: int) -> str:
    """Return color based on score: green (80-100), yellow (50-79), red (0-49)"""
    
def apply_yukti_theme(fig: plotly.graph_objects.Figure) -> plotly.graph_objects.Figure:
    """Apply consistent Yukti AI theme to Plotly figures"""
    
def create_cost_comparison_chart(products: List[TCOBreakdown]) -> plotly.graph_objects.Figure:
    """Create comparative bar chart for TCO analysis"""
```

## Data Models

### Session State Schema

```python
# Session state keys and their types
session_state = {
    # Seller Matrix
    "seller_matrix_sku": str,
    "seller_matrix_data": List[SellerData],
    "seller_matrix_plot": plotly.graph_objects.Figure,
    
    # Satya-View
    "satya_uploaded_image": bytes,
    "satya_golden_source": bytes,
    "satya_match_score": float,
    "satya_status": AuthenticityStatus,
    
    # True-Cost Calculator
    "tco_product_input": ProductInput,
    "tco_breakdown": TCOBreakdown,
    "tco_comparison_products": List[TCOBreakdown],
    
    # Global
    "yukti_score": Optional[int],
    "current_page": str,
}
```

### Cost Multiplier Configuration

```python
# Category-based cost multipliers (stored in calculations.py)
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
    # ... more categories
    "Generic": {  # Fallback for unknown product categories - prevents crashes
        "power_kwh_per_hour": 0.1,
        "filter_cost_per_year": 2000,
        "maintenance_cost_per_year": 1000,
    },
}

# Usage profile multipliers
USAGE_MULTIPLIERS = {
    UsageProfile.HEAVY: 1.5,
    UsageProfile.MEDIUM: 1.0,
    UsageProfile.LIGHT: 0.5,
}
```

### Platform Trust Score Normalization

```python
# Platform-specific normalization (stored in calculations.py)
# UNIVERSAL E-COMMERCE: Supports ANY platform, not limited to specific ones
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
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, I've identified several areas where properties can be consolidated:

**Consolidations:**
- Properties 2.3, 7.2, 7.3, 7.4, 7.5 all test "data completeness" - can be combined into comprehensive data structure validation properties
- Properties 5.3, 5.4, 5.5 all test score-to-status mapping - can be combined into one comprehensive classification property
- Properties 8.1, 8.2, 8.3 all test Yukti Score calculation - can be combined into one property about score composition
- Properties 10.1, 10.2 both test session state persistence - the round-trip property (10.2) subsumes the storage property (10.1)
- Properties 11.1, 11.3, 11.5 all test error handling - can be combined into comprehensive error handling properties

**Redundancies Eliminated:**
- Removed separate properties for each cost component (7.2, 7.3, 7.4) in favor of one comprehensive TCO calculation property
- Removed individual status mapping properties (5.3, 5.4, 5.5) in favor of one classification property
- Removed separate Yukti Score component properties in favor of one composition property

### Core Properties

**Property 1: Session State Round-Trip Preservation**
*For any* user input data stored in session state, navigating away from a page and returning to it should restore the exact same data without loss or corruption.
**Validates: Requirements 1.4, 10.2**

**Property 2: Sponsored Seller Filtering**
*For any* list of sellers containing both sponsored and organic sellers, the filter function should return only sellers where is_sponsored is False.
**Validates: Requirements 2.2**

**Property 3: Trust Score Normalization Bounds**
*For any* trust score from any platform, the normalized score should be in the range [0.0, 5.0] inclusive.
**Validates: Requirements 2.4**

**Property 4: Platform Failure Resilience**
*For any* SKU query where at least one platform fails, the system should still return results from successful platforms and not raise an exception.
**Validates: Requirements 2.5**

**Property 5: Scatter Plot Axis Configuration**
*For any* set of seller data, the generated scatter plot should have Trust Score on the X-axis with range [0.0, 5.0] and Price (INR) on the Y-axis.
**Validates: Requirements 3.1**

**Property 6: Color Gradient Calculation**
*For any* seller with trust score and price, the calculated color should be a valid hex color code, with higher trust and lower price producing colors closer to green (#00FF00) and lower trust and higher price producing colors closer to red (#FF0000).
**Validates: Requirements 3.2**

**Property 7: Image Validation**
*For any* uploaded file, if the file format is not in [JPG, JPEG, PNG] or size exceeds 10MB, the validation function should return (False, error_message).
**Validates: Requirements 4.2**

**Property 8: Invalid File Rejection**
*For any* invalid file upload, the system should prevent processing and display an error message without attempting image comparison.
**Validates: Requirements 4.3**

**Property 9: Feature Match Score Bounds**
*For any* two images compared, the Feature_Match_Score should be in the range [0, 100] inclusive.
**Validates: Requirements 5.2**

**Property 10: Authenticity Status Classification**
*For any* Feature_Match_Score, the status should be: AUTHENTIC if score > 90, FAKE if score < 50, UNCERTAIN if score is in [50, 90].
**Validates: Requirements 5.3, 5.4, 5.5**

**Property 11: Sticker Price Validation**
*For any* input price value, validation should reject (return False) if the value is less than or equal to zero.
**Validates: Requirements 6.4**

**Property 12: TCO Calculation Completeness**
*For any* valid ProductInput, the calculated TCOBreakdown should include all required fields: sticker_price, year_1_costs, year_2_costs, year_3_costs, total_3_year_cost, monthly_cost, and breakdown_details with power, consumables, and maintenance costs.
**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**

**Property 13: Monthly Cost Calculation**
*For any* TCOBreakdown, the monthly_cost should equal total_3_year_cost / 36.
**Validates: Requirements 7.6**

**Property 14: Minimum TCO Identification**
*For any* list of TCOBreakdown objects with at least one element, the comparison function should correctly identify the product with the minimum total_3_year_cost.
**Validates: Requirements 7.7**

**Property 15: Yukti Score Bounds**
*For any* combination of available metrics (trust score, price competitiveness, authenticity score, TCO competitiveness), the calculated Yukti_Score should be in the range [0, 100] inclusive, or None if insufficient data.
**Validates: Requirements 8.1, 8.2, 8.3**

**Property 16: Yukti Score Color Mapping**
*For any* Yukti_Score value, the color should be: green for scores in [80, 100], yellow for scores in [50, 79], red for scores in [0, 49].
**Validates: Requirements 8.4**

**Property 17: Mock Rekognition Score Bounds**
*For any* two images passed to the mock Rekognition service, the returned similarity score should be in the range [0, 100] inclusive.
**Validates: Requirements 9.2**

**Property 18: Mock API Response Time**
*For any* mock API call, the response time should be between 0.5 and 2.0 seconds inclusive.
**Validates: Requirements 9.4**

**Property 19: Session State Initialization Safety**
*For any* session state key access, if the key does not exist, the system should handle it gracefully (using .get() with defaults) without raising KeyError.
**Validates: Requirements 10.4**

**Property 20: Session State Reset**
*For any* reset action, all user-specific session state keys should be cleared or reset to their initial values.
**Validates: Requirements 10.3**

**Property 21: Error Message Display**
*For any* error during data fetching or processing, the system should display a user-friendly error message (not a raw exception trace) to the user.
**Validates: Requirements 11.1, 11.5**

**Property 22: Required Field Validation**
*For any* form with required fields, if any required field is empty, the validation function should return False and provide field-specific error messages.
**Validates: Requirements 11.3**

**Property 23: Color Contrast Compliance**
*For any* text-background color combination in the UI theme, the contrast ratio should meet WCAG AA standards (minimum 4.5:1 for normal text, 3:1 for large text).
**Validates: Requirements 12.5**

## Error Handling

### Error Categories and Strategies

**1. Input Validation Errors**
- **Trigger**: Invalid user inputs (empty fields, wrong formats, out-of-range values)
- **Strategy**: Validate at the point of input, display field-specific error messages, prevent form submission
- **User Experience**: Inline validation with red highlights and descriptive messages
- **Example**: "Price must be a positive number" for negative price input

**2. File Upload Errors**
- **Trigger**: Invalid file format, oversized files, corrupted images
- **Strategy**: Validate file before processing, check format and size limits
- **User Experience**: Display error message with accepted formats and size limits
- **Example**: "Please upload a JPG, JPEG, or PNG file under 10MB"

**3. External Service Errors**
- **Trigger**: Platform API failures, network timeouts, rate limiting
- **Strategy**: Implement retry logic with exponential backoff, continue with partial results
- **User Experience**: Show which platforms succeeded/failed, display available data
- **Example**: "Unable to fetch data from Flipkart. Showing results from Amazon and Myntra."

**4. Image Processing Errors**
- **Trigger**: Corrupted images, unsupported formats, processing failures
- **Strategy**: Catch exceptions during image comparison, provide fallback behavior
- **User Experience**: Display error message and suggest re-uploading
- **Example**: "Unable to process image. Please try uploading a different photo."

**5. Calculation Errors**
- **Trigger**: Missing cost multipliers, invalid category, division by zero
- **Strategy**: Validate inputs before calculation, use default values for missing data
- **User Experience**: Display warning about assumptions made
- **Example**: "Using default cost estimates for this product category."

**6. Session State Errors**
- **Trigger**: Missing session keys, corrupted state data
- **Strategy**: Initialize all keys with defaults, use .get() with fallbacks
- **User Experience**: Graceful degradation, prompt user to re-enter data if needed
- **Example**: "Session expired. Please enter your search criteria again."

### Error Handling Implementation Patterns

```python
# Pattern 1: Input Validation with User Feedback
def validate_product_input(name: str, price: float, category: str) -> Tuple[bool, List[str]]:
    """Validate product inputs and return (is_valid, error_messages)"""
    errors = []
    
    if not name or name.strip() == "":
        errors.append("Product name is required")
    
    if price <= 0:
        errors.append("Price must be a positive number")
    
    if category not in SUPPORTED_CATEGORIES:
        errors.append(f"Category must be one of: {', '.join(SUPPORTED_CATEGORIES)}")
    
    return (len(errors) == 0, errors)

# Pattern 2: Graceful Platform Failure Handling
def fetch_seller_data(sku: str) -> List[SellerData]:
    """Fetch from multiple platforms, continue on individual failures"""
    all_sellers = []
    failed_platforms = []
    
    for platform in PLATFORMS:
        try:
            sellers = platform.fetch(sku)
            all_sellers.extend(sellers)
        except Exception as e:
            logger.error(f"Failed to fetch from {platform.name}: {e}")
            failed_platforms.append(platform.name)
    
    if failed_platforms:
        st.warning(f"Unable to fetch data from: {', '.join(failed_platforms)}")
    
    return all_sellers

# Pattern 3: Session State Safe Access
def get_session_value(key: str, default: Any = None) -> Any:
    """Safely retrieve session state value with fallback"""
    return st.session_state.get(key, default)

def initialize_session_state():
    """Initialize all session state keys with defaults"""
    defaults = {
        "seller_matrix_sku": "",
        "seller_matrix_data": [],
        "satya_uploaded_image": None,
        "yukti_score": None,
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Pattern 4: User-Friendly Error Display
def display_error(error: Exception, user_message: str):
    """Display user-friendly error while logging technical details"""
    logger.error(f"Error: {type(error).__name__}: {str(error)}", exc_info=True)
    st.error(f"❌ {user_message}")
    
    if st.session_state.get("debug_mode", False):
        st.exception(error)
```

## Testing Strategy

### Dual Testing Approach

The Yukti AI platform requires both unit tests and property-based tests for comprehensive coverage:

**Unit Tests** focus on:
- Specific examples and edge cases (empty inputs, boundary values)
- Integration points between components
- UI component rendering and configuration
- Mock service behavior verification
- Error conditions and exception handling

**Property-Based Tests** focus on:
- Universal properties that hold for all inputs
- Data structure invariants (score bounds, normalization)
- Round-trip properties (session state persistence)
- Classification logic (status mapping, color coding)
- Mathematical properties (TCO calculations)

### Property-Based Testing Configuration

**Library Selection**: Use **Hypothesis** for Python-based property testing

**Test Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: yukti-ai, Property {number}: {property_text}`

**Example Property Test Structure**:
```python
from hypothesis import given, strategies as st
import pytest

# Feature: yukti-ai, Property 3: Trust Score Normalization Bounds
@given(
    raw_score=st.floats(min_value=0.0, max_value=10.0),
    platform=st.sampled_from(["Amazon", "Flipkart", "Myntra"])
)
def test_trust_score_normalization_bounds(raw_score, platform):
    """For any trust score from any platform, normalized score should be in [0.0, 5.0]"""
    normalized = normalize_trust_score(raw_score, platform)
    assert 0.0 <= normalized <= 5.0

# Feature: yukti-ai, Property 10: Authenticity Status Classification
@given(match_score=st.floats(min_value=0.0, max_value=100.0))
def test_authenticity_status_classification(match_score):
    """For any Feature_Match_Score, status should map correctly to ranges"""
    status = determine_authenticity_status(match_score)
    
    if match_score > 90:
        assert status == AuthenticityStatus.AUTHENTIC
    elif match_score < 50:
        assert status == AuthenticityStatus.FAKE
    else:
        assert status == AuthenticityStatus.UNCERTAIN
```

### Unit Test Examples

```python
import pytest
from unittest.mock import Mock, patch

def test_navigation_menu_has_three_options():
    """Test that navigation menu contains exactly three options"""
    # Feature: yukti-ai, Example test for Requirement 1.1
    menu_options = ["Seller Matrix", "Satya-View", "True-Cost Calculator"]
    assert len(menu_options) == 3
    assert "Seller Matrix" in menu_options

def test_empty_seller_results_displays_message():
    """Test edge case of no organic sellers found"""
    # Feature: yukti-ai, Edge case for Requirement 3.5
    sellers = []
    result = filter_organic_sellers(sellers)
    assert result == []
    # UI should display "No results found" message

def test_invalid_image_format_rejected():
    """Test that non-image files are rejected"""
    # Feature: yukti-ai, Example test for Requirement 4.3
    invalid_file = b"not an image"
    is_valid, error_msg = validate_image(invalid_file)
    assert is_valid == False
    assert "format" in error_msg.lower()

def test_tco_monthly_cost_calculation():
    """Test specific example of monthly cost calculation"""
    # Feature: yukti-ai, Example test for Requirement 7.6
    tco = TCOBreakdown(
        sticker_price=10000,
        year_1_costs=2000,
        year_2_costs=2000,
        year_3_costs=2000,
        total_3_year_cost=16000,
        monthly_cost=444.44,
        breakdown_details={}
    )
    expected_monthly = 16000 / 36
    assert abs(tco.monthly_cost - expected_monthly) < 0.01
```

### Test Coverage Goals

- **Unit Test Coverage**: Minimum 80% code coverage
- **Property Test Coverage**: All 23 correctness properties implemented
- **Integration Tests**: Key user flows (SKU search → visualization, image upload → analysis, TCO calculation → comparison)
- **Edge Case Coverage**: Empty inputs, boundary values, error conditions

### Testing Tools and Framework

- **Test Framework**: pytest
- **Property Testing**: Hypothesis
- **Mocking**: unittest.mock
- **Coverage**: pytest-cov
- **Streamlit Testing**: streamlit.testing (for component testing)

### Continuous Testing

- Run unit tests on every code change
- Run property tests before commits
- Include both test suites in CI/CD pipeline
- Monitor test execution time (property tests may be slower due to 100+ iterations)
