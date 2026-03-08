# Requirements Document: Yukti AI - Enterprise E-Commerce Aggregator & Scam Detection Platform

## Introduction

Yukti AI is an advanced enterprise-grade e-commerce aggregator and scam-detection application built with Python and Streamlit. The platform simulates a complete AWS cloud architecture using seeded/cached dictionary data to provide seamless product comparison, visual authenticity verification, and hidden cost analysis across multiple e-commerce platforms. The system aims to protect consumers from counterfeit products and financial traps while demonstrating cloud-native architecture patterns.

**Tagline**: "See the Real, Know the Worth"

## Glossary

- **Yukti_AI**: The complete Streamlit-based enterprise application
- **Search_Bar**: Universal input interface accepting product names, URLs, or images
- **Seller_Matrix**: Cross-platform seller aggregation displaying top picks and verified sellers
- **Satya_View**: AWS Rekognition-powered visual authenticity scanner
- **True_Cost_Calculator**: AWS Bedrock-powered financial trap detector
- **Top_Pick**: Seller with highest available rating on each platform (tie-breaker: lowest price, fastest delivery)
- **Scam_Target**: Artificially injected low-rated, suspiciously priced seller for demonstration
- **Match_Percentage**: Visual similarity score (0-100%) between product images
- **Signal_Status**: Traffic light indicator (Green/Yellow/Red) for authenticity
- **AWS_Lambda**: Simulated serverless triggers for scan operations
- **AWS_S3**: Simulated image storage and data caching layer
- **AWS_Rekognition**: Visual scanner for detecting physical product flaws
- **AWS_Bedrock**: GenAI engine for sentiment analysis and cost calculations
- **MVP_Products**: 12 seeded products across 6 categories for demo validation

## Requirements

### Requirement 1: Platform Configuration and Branding

**User Story:** As a user, I want to see consistent enterprise branding and cloud architecture indicators, so that I understand the platform's capabilities.

#### Acceptance Criteria

1. WHEN the application loads, THE Yukti_AI SHALL display the tagline "See the Real, Know the Worth" prominently in the header
2. THE Yukti_AI SHALL use Trust Blue (#0056D2) as the primary theme color across all pages
3. THE Yukti_AI SHALL configure AWS credentials using os.environ['AWS_ACCESS_KEY_ID'] to demonstrate enterprise security practices
4. THE Yukti_AI SHALL display cloud architecture indicators (S3 caching, Lambda triggers, Rekognition, Bedrock) in the UI
5. THE Yukti_AI SHALL maintain a wide layout optimized for data visualization

### Requirement 2: MVP Product Validation

**User Story:** As a demo user, I want to be guided to valid products, so that I experience zero-lag performance.

#### Acceptance Criteria

1. THE Yukti_AI SHALL maintain a seeded database of exactly 12 products across 6 categories:
   - Electronics: boAt Earbuds, Titan Smartwatch
   - Fashion: Uppada Saree, Manyavar Dhotis, Unbranded Sling Bag
   - Home: Kent RO, Hawkins Cooker
   - Health: Lifelong Spin Bike
   - Office: Zebronics Keyboard, Milton Lunch Box
   - Beauty: Lakmé Kajal, Mamaearth Oil
2. WHEN a user searches for a product NOT in the seeded list, THE Yukti_AI SHALL display this exact message: "⚠️ Welcome to Yukti AI Hackathon Demo! To ensure zero-lag performance, this MVP is currently seeded with 12 products across 6 categories. Try searching: 'boAt Earbuds' or 'Unbranded Sling Bag'"
3. THE Yukti_AI SHALL stop execution and prevent further processing for invalid products
4. THE Yukti_AI SHALL perform case-insensitive fuzzy matching for product name searches
5. THE Yukti_AI SHALL validate product names before routing to any feature

### Requirement 3: Search Bar Logic (Phase 1 - Input Routing)

**User Story:** As a user, I want to input products in multiple formats, so that I can access features flexibly.

#### Acceptance Criteria

1. THE Search_Bar SHALL accept three input types: Product Name, Product URL, or Uploaded Image
2. WHEN input is a Product Name, THE Search_Bar SHALL route through simulated Lambda, validate against MVP products, and open Seller Matrix
3. WHEN input is an Uploaded Image, THE Search_Bar SHALL use simulated Rekognition to extract product text, validate against MVP products, and open Seller Matrix
4. WHEN input is a Product URL (contains "http" or "www"), THE Search_Bar SHALL skip Seller Matrix and trigger Lambda to open Satya View directly
5. WHEN input is a Seller Store URL (e.g., "amazon.in/stores/"), THE Search_Bar SHALL display error: "⚠️ Yukti AI compares Original vs. Fake for specific products. Please enter a Product Name, URL, or upload an image."
6. THE Search_Bar SHALL display a file uploader widget for image inputs accepting JPG, JPEG, PNG formats
7. THE Search_Bar SHALL simulate Lambda trigger with 0.5-1.0 second delay and display "🔄 Lambda Processing..." indicator

### Requirement 4: Seller Matrix - Data Aggregation (Phase 2)

**User Story:** As a consumer, I want to see top sellers across platforms, so that I can compare verified options.

#### Acceptance Criteria

1. THE Seller_Matrix SHALL aggregate seller data from exactly 6 platforms: Amazon, Flipkart, Myntra, Meesho, Croma, and JioMart
2. THE Seller_Matrix SHALL display UI title as "Top Platforms" without mentioning specific platform count
3. THE Seller_Matrix SHALL generate dynamic seller data with variable prices and ratings (no hardcoded values)
4. THE Seller_Matrix SHALL simulate S3 caching with indicator showing "-40% AI retrieval cost reduction"
5. WHEN aggregating data, THE Seller_Matrix SHALL extract: seller_name, platform, price (INR), rating (0.0-5.0), delivery_days, product_url for each seller
6. THE Seller_Matrix SHALL use realistic Indian pricing ranges based on product category
7. THE Seller_Matrix SHALL generate 3-5 sellers per platform with varied ratings

### Requirement 5: Seller Matrix - Top Picks and Seller List (Phase 2)

**User Story:** As a consumer, I want to see the best seller from each platform first, so that I can quickly identify trusted options.

#### Acceptance Criteria

1. THE Seller_Matrix SHALL identify exactly 1 Top Pick per platform with the absolute Highest Available Rating
2. WHEN multiple sellers have the same highest rating, THE Seller_Matrix SHALL apply tie-breaker: lowest price, then fastest delivery
3. THE Seller_Matrix SHALL display Top Picks in a prominent "Green Top Pick" section with green highlighting
4. THE Seller_Matrix SHALL display remaining sellers in a scrollable list below Top Picks
5. THE Seller_Matrix SHALL ONLY include sellers in the remaining list who hold the exact same Highest Available Rating as their platform's Top Pick
6. THE Seller_Matrix SHALL hide all lower-rated sellers from the display
7. THE Seller_Matrix SHALL artificially inject exactly 1 low-rated (1.5-2.5 stars), suspiciously priced seller at the bottom as "Scam Target"
8. THE Seller_Matrix SHALL label the Scam Target with a red warning badge: "⚠️ Suspicious Listing"
9. THE Seller_Matrix SHALL place a [🔍 Run Satya View] button next to every seller in the list

### Requirement 6: Seller Matrix - Buy Box UI (Phase 2)

**User Story:** As a consumer, I want a clean comparison interface, so that I can make quick decisions.

#### Acceptance Criteria

1. THE Seller_Matrix SHALL generate a clean "Buy Box" UI for each seller showing: Platform Logo, Seller Name, Price (₹), Rating (stars), Delivery Time, [Buy Now] button, [🔍 Run Satya View] button
2. THE Seller_Matrix SHALL display Top Picks in a grid layout (2-3 columns)
3. THE Seller_Matrix SHALL display remaining sellers in a single-column scrollable list
4. THE Seller_Matrix SHALL use platform-specific color coding (Amazon: orange, Flipkart: blue, Myntra: pink, Nykaa: purple, Croma: green, JioMart: red)
5. THE Seller_Matrix SHALL display "Simulated S3 Cache: -40% Cost" indicator at the top
6. THE Seller_Matrix SHALL show total seller count: "Showing X verified sellers across top platforms"

### Requirement 7: Satya View - Trigger and Layout (Phase 3)

**User Story:** As a consumer, I want to verify product authenticity visually, so that I can avoid counterfeits.

#### Acceptance Criteria

1. THE Satya_View SHALL trigger when user clicks [🔍 Run Satya View] button or enters a Product URL
2. THE Satya_View SHALL simulate Lambda trigger with "🔄 Lambda: Rekognition Scan Initiated..." message
3. THE Satya_View SHALL display a 3-Image Truth Table layout: [Original Brand] | [Seller Upload] | [Customer Received]
4. WHEN user uploaded an image directly (no seller selected), THE Satya_View SHALL display 2-Image table: [Original Brand] | [User Upload]
5. THE Satya_View SHALL pull images from simulated S3 storage with "📦 S3: Loading product images..." indicator
6. THE Satya_View SHALL display image labels clearly above each image
7. THE Satya_View SHALL ensure all images are same size and aligned horizontally

### Requirement 8: Satya View - Visual Scan (AWS Rekognition) (Phase 3)

**User Story:** As a consumer, I want to see specific product flaws highlighted, so that I understand authenticity issues.

#### Acceptance Criteria

1. THE Satya_View SHALL simulate AWS Rekognition visual analysis with 1.0-2.0 second processing delay
2. THE Satya_View SHALL add red circles/highlights on images pointing to specific physical flaws (missing seals, wrong fonts, color mismatches)
3. THE Satya_View SHALL display a list of detected flaws below images: "🔴 Missing hologram seal", "🔴 Font mismatch on logo", "🔴 Color variation detected"
4. THE Satya_View SHALL generate 0-3 random flaws for fake products, 0 flaws for authentic products
5. THE Satya_View SHALL display "✅ No physical flaws detected" for authentic products
6. THE Satya_View SHALL show "AWS Rekognition: Visual Analysis Complete" indicator

### Requirement 9: Satya View - NLP Review Scan (AWS Bedrock) (Phase 3)

**User Story:** As a consumer, I want to see customer sentiment analysis, so that I can understand real experiences.

#### Acceptance Criteria

1. THE Satya_View SHALL simulate AWS Bedrock NLP processing with 1.0-1.5 second delay
2. THE Satya_View SHALL display a Sentiment Bar Chart with three categories: Positive (green), Neutral (yellow), Negative (red)
3. THE Satya_View SHALL generate realistic sentiment percentages totaling 100%
4. THE Satya_View SHALL display a 1-line critical alert summary: "⚠️ 45% of reviews mention 'fake product' or 'not original'"
5. THE Satya_View SHALL show "AWS Bedrock: Sentiment Analysis Complete" indicator
6. THE Satya_View SHALL display review count: "Analyzed 1,247 customer reviews"

### Requirement 10: Satya View - Match Percentage & Signals (Branded Items) (Phase 3)

**User Story:** As a consumer, I want a clear authenticity verdict, so that I can make safe purchases.

#### Acceptance Criteria

1. THE Satya_View SHALL calculate Match_Percentage (0-100%) comparing Seller Upload vs Original Brand
2. WHEN Match_Percentage is 100%, THE Satya_View SHALL display 🟢 Green Signal with "Verified Safe"
3. WHEN Match_Percentage is 60.0% to 99.9%, THE Satya_View SHALL display 🟡 Yellow Signal with "Honest seller, but likely a replica/old packaging"
4. WHEN Match_Percentage is 0.0% to 59.9%, THE Satya_View SHALL display 🔴 Red Signal with "Scam/Bait & Switch"
5. THE Satya_View SHALL display the exact Match_Percentage prominently: "Match: 87.5%"
6. THE Satya_View SHALL use large, bold signal indicators (emoji + text)

### Requirement 11: Satya View - Match Logic (Unbranded/Generic Items) (Phase 3)

**User Story:** As a consumer buying generic items, I want honest seller verification, so that I receive what's advertised.

#### Acceptance Criteria

1. WHEN product is unbranded/generic (e.g., Unbranded Sling Bag), THE Satya_View SHALL compare Seller Upload vs Customer Received (ignore Original Brand)
2. WHEN images match, THE Satya_View SHALL display 🟢 Green Signal with warning tag: "⚠️ Generic / Unbranded Item"
3. WHEN images don't match, THE Satya_View SHALL display 🔴 Red Signal with "Seller misrepresentation detected"
4. THE Satya_View SHALL display "Generic Product Mode" indicator at the top
5. THE Satya_View SHALL show 2-image comparison layout for unbranded items

### Requirement 12: True Cost Calculator - Trigger and Scenarios (Phase 4)

**User Story:** As a consumer, I want to understand hidden costs, so that I avoid financial traps.

#### Acceptance Criteria

1. THE True_Cost_Calculator SHALL trigger from Satya View results or direct navigation
2. THE True_Cost_Calculator SHALL simulate AWS Bedrock financial analysis with "🔄 Bedrock: Calculating True Cost..." indicator
3. THE True_Cost_Calculator SHALL determine scenario based on product type and signal status
4. THE True_Cost_Calculator SHALL ignore standard delivery fees in all calculations
5. THE True_Cost_Calculator SHALL display scenario type prominently at the top

### Requirement 13: True Cost Calculator - Scenario A (Dare to Buy Trap) (Phase 4)

**User Story:** As a consumer considering a fake product, I want to see long-term costs, so that I understand the true expense.

#### Acceptance Criteria

1. WHEN Satya_View shows Red Signal, THE True_Cost_Calculator SHALL activate Scenario A: "The Dare to Buy Trap"
2. THE True_Cost_Calculator SHALL calculate Lifespan Cost comparing fake vs original over 12 months
3. THE True_Cost_Calculator SHALL include replacement costs (fake breaks in 2-3 months, original lasts 12+ months)
4. THE True_Cost_Calculator SHALL display monthly cost comparison: "Fake: ₹450/month vs Original: ₹250/month"
5. THE True_Cost_Calculator SHALL show total 1-year cost with red highlighting for fake product
6. THE True_Cost_Calculator SHALL display warning: "🔴 Cheap fakes cost MORE per month than originals"

### Requirement 14: True Cost Calculator - Scenario B (Maintenance Trap) (Phase 4)

**User Story:** As a consumer buying hardware/appliances, I want to see recurring costs, so that I budget accurately.

#### Acceptance Criteria

1. WHEN product category is Home or Office (Kent RO, Hawkins Cooker, etc.), THE True_Cost_Calculator SHALL activate Scenario B: "The Maintenance Trap"
2. THE True_Cost_Calculator SHALL calculate 1-Year Total Cost: base price + mandatory recurring costs
3. THE True_Cost_Calculator SHALL include category-specific costs: water filters (₹4000/year), ink refills (₹3000/year), etc.
4. THE True_Cost_Calculator SHALL display breakdown table: Base Price, Filter Costs, Maintenance, Total 1-Year Cost
5. THE True_Cost_Calculator SHALL show monthly equivalent: "Effective Monthly Cost: ₹1,250"
6. THE True_Cost_Calculator SHALL highlight recurring costs in orange

### Requirement 15: True Cost Calculator - Scenario C (Discount Explainer) (Phase 4)

**User Story:** As a consumer seeing discounts, I want to understand if they're legitimate, so that I avoid clearance traps.

#### Acceptance Criteria

1. WHEN product is branded with Green/Yellow signal, THE True_Cost_Calculator SHALL activate Scenario C: "The Discount Explainer"
2. THE True_Cost_Calculator SHALL analyze discount legitimacy based on season, brand, and price drop percentage
3. WHEN discount is legitimate (10-30%, festive season), THE True_Cost_Calculator SHALL display 🟢 "Authorized Festive Sale"
4. WHEN discount is suspicious (>50%, near expiry), THE True_Cost_Calculator SHALL display 🔴 "Clearance Trap: Product expires soon"
5. THE True_Cost_Calculator SHALL show expiry date estimate for clearance items
6. THE True_Cost_Calculator SHALL display savings calculation for legitimate sales

### Requirement 16: True Cost Calculator - Scenario D (Unbranded Reality Check) (Phase 4)

**User Story:** As a consumer buying generic items, I want to know if the price is fair, so that I get good value.

#### Acceptance Criteria

1. WHEN product is unbranded/generic, THE True_Cost_Calculator SHALL activate Scenario D: "Unbranded Reality Check"
2. THE True_Cost_Calculator SHALL compare price against market average for similar generic items
3. WHEN price is below or at market average, THE True_Cost_Calculator SHALL display 🟢 "Honest Budget Buy! Great daily value."
4. WHEN price is above market average (>20% higher), THE True_Cost_Calculator SHALL display 🔴 "Overpriced Alert. Priced above market average."
5. THE True_Cost_Calculator SHALL show market comparison: "This item: ₹299 | Market avg: ₹250"
6. THE True_Cost_Calculator SHALL display value rating: "Value Score: 7/10"

### Requirement 17: AWS Architecture Simulation

**User Story:** As a developer, I want to demonstrate cloud-native patterns, so that I showcase enterprise architecture.

#### Acceptance Criteria

1. THE Yukti_AI SHALL simulate AWS Lambda with $0 idle-cost indicators and trigger animations
2. THE Yukti_AI SHALL simulate AWS S3 with caching indicators showing "-40% retrieval cost"
3. THE Yukti_AI SHALL simulate AWS Rekognition with processing delays (1.0-2.0 seconds) and completion messages
4. THE Yukti_AI SHALL simulate AWS Bedrock with NLP processing delays (1.0-1.5 seconds) and completion messages
5. THE Yukti_AI SHALL use os.environ for AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
6. THE Yukti_AI SHALL display architecture diagram or indicators showing service interactions
7. THE Yukti_AI SHALL log simulated API calls to console for demonstration purposes

### Requirement 18: Data Generation and Realism

**User Story:** As a demo user, I want realistic data, so that the platform feels production-ready.

#### Acceptance Criteria

1. THE Yukti_AI SHALL generate dynamic prices using realistic ranges per category (Electronics: ₹500-5000, Fashion: ₹300-3000, etc.)
2. THE Yukti_AI SHALL generate dynamic ratings using weighted distribution (70% high ratings 4.0-5.0, 20% medium 3.0-3.9, 10% low 1.5-2.9)
3. THE Yukti_AI SHALL generate realistic seller names per platform (Amazon: "TechStore Official", Flipkart: "ElectroHub", etc.)
4. THE Yukti_AI SHALL generate realistic delivery times (1-7 days) based on platform and product
5. THE Yukti_AI SHALL use Indian Rupee (₹) symbol consistently across all price displays
6. THE Yukti_AI SHALL generate realistic review counts (100-5000) per seller
7. THE Yukti_AI SHALL ensure no hardcoded prices or ratings in the codebase

### Requirement 19: Error Handling and User Guidance

**User Story:** As a user, I want clear guidance when I make mistakes, so that I can use the platform effectively.

#### Acceptance Criteria

1. WHEN user enters invalid product, THE Yukti_AI SHALL display MVP demo notice with example products
2. WHEN user enters seller store URL, THE Yukti_AI SHALL display specific error message guiding to correct input
3. WHEN image upload fails, THE Yukti_AI SHALL display error: "Unable to process image. Please upload JPG, JPEG, or PNG under 10MB"
4. WHEN network simulation fails, THE Yukti_AI SHALL display: "AWS service temporarily unavailable. Please try again."
5. THE Yukti_AI SHALL log all errors to console for debugging
6. THE Yukti_AI SHALL never display raw Python exceptions to users

### Requirement 20: Navigation and User Flow

**User Story:** As a user, I want smooth navigation between features, so that I can explore all capabilities.

#### Acceptance Criteria

1. THE Yukti_AI SHALL provide sidebar navigation with three pages: Home (Search), Seller Matrix, Satya View, True Cost
2. THE Yukti_AI SHALL maintain session state across page navigation
3. THE Yukti_AI SHALL display breadcrumb trail showing current location
4. THE Yukti_AI SHALL provide "Back to Search" button on all feature pages
5. THE Yukti_AI SHALL preserve search results when navigating between Seller Matrix, Satya View, and True Cost
6. THE Yukti_AI SHALL display progress indicators during page transitions
