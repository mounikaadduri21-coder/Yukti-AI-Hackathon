# Requirements Document: Yukti AI

## Introduction

Yukti AI is a Streamlit-based e-commerce intelligence platform designed to empower consumers with data-driven insights for making informed purchasing decisions. The platform provides three core analytical tools: The Seller Matrix for cross-platform seller comparison, Satya-View for visual product authenticity verification, and True-Cost Calculator for total cost of ownership analysis. The system aims to reduce consumer risk by aggregating trust signals, detecting counterfeit products, and revealing hidden long-term costs.

## Glossary

- **Yukti_AI_Platform**: The complete Streamlit-based web application
- **Seller_Matrix**: The cross-platform seller aggregation and visualization module
- **Satya_View**: The image-based product authenticity verification module
- **True_Cost_Calculator**: The total cost of ownership calculation module
- **Trust_Score**: A normalized metric (0.0-5.0) derived from verified customer reviews
- **SKU**: Stock Keeping Unit - a unique product identifier
- **Golden_Source**: Official brand-provided reference image for authenticity comparison
- **Feature_Match_Score**: Percentage similarity between user-uploaded image and Golden Source
- **TCO**: Total Cost of Ownership over a specified time period
- **Yukti_Score**: An aggregated metric (0-100) representing overall purchase recommendation confidence
- **Organic_Seller**: A seller whose listing is not marked as "Sponsored" or paid advertisement
- **Usage_Profile**: User-defined consumption pattern (Heavy/Medium/Light)

## Requirements

### Requirement 1: Platform Navigation and Structure

**User Story:** As a user, I want to navigate between different analytical tools seamlessly, so that I can access all features from a unified interface.

#### Acceptance Criteria

1. WHEN the application starts, THE Yukti_AI_Platform SHALL display a navigation menu with three options: Seller Matrix, Satya-View, and True-Cost Calculator
2. WHEN a user selects a navigation option, THE Yukti_AI_Platform SHALL load the corresponding feature page without page refresh
3. THE Yukti_AI_Platform SHALL maintain consistent branding with Trust Blue (#0056D2) theme across all pages
4. THE Yukti_AI_Platform SHALL persist user session data across page navigation using session state management
5. WHEN the application loads, THE Yukti_AI_Platform SHALL display the Yukti AI logo and tagline on all pages

### Requirement 2: Seller Matrix - Data Aggregation

**User Story:** As a consumer, I want to see all sellers offering a specific product across multiple platforms, so that I can compare options comprehensively.

#### Acceptance Criteria

1. WHEN a user enters a SKU identifier, THE Seller_Matrix SHALL retrieve seller data from multiple e-commerce platforms (universal support for any platform, not limited to specific ones)
2. THE Seller_Matrix SHALL filter out all sellers marked as "Sponsored" from the aggregated results
3. WHEN aggregating seller data, THE Seller_Matrix SHALL extract seller name, price, trust score, platform source, and product_url for each organic seller
4. THE Seller_Matrix SHALL normalize trust scores from different platforms to a uniform 0.0-5.0 scale based on verified reviews, with fallback support for unknown platforms
5. IF a platform is unavailable or returns an error, THEN THE Seller_Matrix SHALL continue processing remaining platforms and log the failure
6. THE Seller_Matrix SHALL include product_url field in seller data to enable direct "Buy Now" functionality

### Requirement 3: Seller Matrix - Visualization

**User Story:** As a consumer, I want to visualize seller options on a scatter plot, so that I can quickly identify the best combination of trust and price.

#### Acceptance Criteria

1. THE Seller_Matrix SHALL display organic sellers on a 2D scatter plot with Trust Score on X-axis (0.0-5.0) and Price on Y-axis (INR)
2. WHEN rendering the scatter plot, THE Seller_Matrix SHALL color-code data points using a gradient from green (high trust, low price) to red (low trust, high price)
3. WHEN a user hovers over a data point, THE Seller_Matrix SHALL display a tooltip showing seller name, exact trust score, price, and platform
4. THE Seller_Matrix SHALL make the scatter plot interactive with zoom and pan capabilities, and clickable nodes that open product_url in new tab
5. WHEN no organic sellers are found, THE Seller_Matrix SHALL display a message indicating no results and suggest alternative search terms
6. THE Seller_Matrix SHALL display product_url in the seller details table for direct access

### Requirement 4: Satya-View - Image Upload and Processing

**User Story:** As a consumer, I want to upload a product photo for authenticity verification, so that I can avoid purchasing counterfeit items.

#### Acceptance Criteria

1. THE Satya_View SHALL provide a file upload interface accepting image formats: JPG, JPEG, PNG
2. WHEN a user uploads an image, THE Satya_View SHALL validate the file format and size (maximum 10MB)
3. IF an invalid file is uploaded, THEN THE Satya_View SHALL display an error message and prevent processing
4. WHEN a valid image is uploaded, THE Satya_View SHALL display a preview of the uploaded image
5. THE Satya_View SHALL store the uploaded image in session state for comparison processing

### Requirement 5: Satya-View - Authenticity Detection

**User Story:** As a consumer, I want to compare my product photo against official brand images, so that I can determine if the product is authentic.

#### Acceptance Criteria

1. WHEN an image is submitted for analysis, THE Satya_View SHALL compare it against the Golden_Source image using computer vision feature matching
2. THE Satya_View SHALL calculate a Feature_Match_Score as a percentage (0-100%) representing visual similarity
3. WHEN the Feature_Match_Score is greater than 90%, THE Satya_View SHALL display a green indicator with "Authentic" label
4. WHEN the Feature_Match_Score is less than 50%, THE Satya_View SHALL display a red indicator with "Potential Fake" warning
5. WHEN the Feature_Match_Score is between 50% and 90%, THE Satya_View SHALL display a yellow indicator with "Uncertain - Manual Review Recommended" message
6. THE Satya_View SHALL display the exact Feature_Match_Score percentage alongside the traffic light indicator
7. THE Satya_View SHALL show a side-by-side comparison of the uploaded image and Golden_Source image
8. THE Satya_View SHALL use MockProductDatabase component to retrieve Golden Source images with safe placeholder fallback to prevent crashes when images are not found

### Requirement 6: True-Cost Calculator - Input Collection

**User Story:** As a consumer, I want to input product details and my usage pattern, so that I can calculate the total cost of ownership.

#### Acceptance Criteria

1. THE True_Cost_Calculator SHALL provide input fields for product name, sticker price (INR), and product category
2. THE True_Cost_Calculator SHALL provide a selection interface for Usage_Profile with three options: Heavy, Medium, Light
3. WHEN a user selects a Usage_Profile, THE True_Cost_Calculator SHALL display a description of what each profile means
4. THE True_Cost_Calculator SHALL validate that sticker price is a positive number
5. IF invalid input is provided, THEN THE True_Cost_Calculator SHALL display field-specific error messages and prevent calculation

### Requirement 7: True-Cost Calculator - TCO Computation

**User Story:** As a consumer, I want to see the total cost of ownership over 3 years, so that I can understand hidden costs beyond the sticker price.

#### Acceptance Criteria

1. WHEN a user submits valid inputs, THE True_Cost_Calculator SHALL calculate TCO over a 3-year period
2. THE True_Cost_Calculator SHALL include power consumption costs based on product category and Usage_Profile
3. THE True_Cost_Calculator SHALL include consumable costs (filters, cartridges, etc.) based on product category and Usage_Profile
4. THE True_Cost_Calculator SHALL include maintenance costs based on product category and Usage_Profile
5. THE True_Cost_Calculator SHALL display a breakdown table showing: Sticker Price, Year 1 Costs, Year 2 Costs, Year 3 Costs, and Total 3-Year Cost
6. THE True_Cost_Calculator SHALL calculate and display the effective monthly cost (Total TCO / 36 months)
7. WHERE multiple product options are compared, THE True_Cost_Calculator SHALL display a comparative table highlighting the lowest TCO option
8. THE True_Cost_Calculator SHALL use "Generic" fallback category for unknown product types to prevent crashes

### Requirement 8: Yukti Score Calculation

**User Story:** As a consumer, I want to see an overall recommendation score, so that I can quickly assess purchase confidence.

#### Acceptance Criteria

1. WHERE Seller_Matrix data is available, THE Yukti_AI_Platform SHALL calculate a Yukti_Score (0-100) based on trust score and price competitiveness
2. WHERE Satya_View analysis is available, THE Yukti_AI_Platform SHALL incorporate Feature_Match_Score into the Yukti_Score calculation
3. WHERE True_Cost_Calculator data is available, THE Yukti_AI_Platform SHALL incorporate TCO competitiveness into the Yukti_Score calculation
4. THE Yukti_AI_Platform SHALL display the Yukti_Score with color coding: Green (80-100), Yellow (50-79), Red (0-49)
5. THE Yukti_AI_Platform SHALL animate the Yukti_Score display with a progress bar or gauge visualization
6. WHEN insufficient data is available, THE Yukti_AI_Platform SHALL display "Insufficient Data" instead of a score

### Requirement 9: Mock AWS Service Integration

**User Story:** As a developer, I want to use mocked AWS services for the prototype, so that I can demonstrate functionality without incurring cloud costs.

#### Acceptance Criteria

1. THE Yukti_AI_Platform SHALL use a mock implementation of AWS Rekognition for image comparison in Satya_View
2. THE mock AWS Rekognition service SHALL return realistic Feature_Match_Score values based on simple image similarity algorithms
3. WHERE AWS Bedrock integration is planned, THE Yukti_AI_Platform SHALL use a mock implementation returning predefined responses
4. THE mock services SHALL simulate realistic response times (0.5-2 seconds) to mimic actual API behavior
5. THE Yukti_AI_Platform SHALL include configuration flags to switch between mock and real AWS services

### Requirement 10: Data Persistence and State Management

**User Story:** As a user, I want my inputs and results to persist during my session, so that I can navigate between features without losing data.

#### Acceptance Criteria

1. THE Yukti_AI_Platform SHALL store all user inputs in session state when navigating between pages
2. WHEN a user returns to a previously visited page, THE Yukti_AI_Platform SHALL restore the previous state including inputs and results
3. THE Yukti_AI_Platform SHALL clear session state when the user explicitly requests a reset or closes the browser
4. THE Yukti_AI_Platform SHALL handle session state initialization gracefully when keys are not yet defined
5. THE Yukti_AI_Platform SHALL persist uploaded images in session state without exceeding memory limits

### Requirement 11: Error Handling and User Feedback

**User Story:** As a user, I want clear error messages and feedback, so that I understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN an error occurs during data fetching, THE Yukti_AI_Platform SHALL display a user-friendly error message explaining the issue
2. WHEN processing is in progress, THE Yukti_AI_Platform SHALL display a loading indicator or progress message
3. IF a required field is empty, THEN THE Yukti_AI_Platform SHALL highlight the field and display a validation message
4. WHEN an operation completes successfully, THE Yukti_AI_Platform SHALL display a success confirmation message
5. THE Yukti_AI_Platform SHALL log technical errors to console while showing simplified messages to users

### Requirement 12: Responsive Design and Accessibility

**User Story:** As a user, I want the platform to work well on different screen sizes, so that I can use it on various devices.

#### Acceptance Criteria

1. THE Yukti_AI_Platform SHALL render correctly on desktop screens (1920x1080 and above)
2. THE Yukti_AI_Platform SHALL render correctly on tablet screens (768x1024)
3. THE Yukti_AI_Platform SHALL adjust layout and font sizes appropriately for different screen widths
4. THE Yukti_AI_Platform SHALL ensure interactive elements (buttons, inputs) are touch-friendly with minimum 44x44px target size
5. THE Yukti_AI_Platform SHALL maintain readability with sufficient color contrast ratios for text and backgrounds
