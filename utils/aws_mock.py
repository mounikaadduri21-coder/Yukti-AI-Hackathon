"""
AWS mock services for Yukti AI prototype.

This module provides mock implementations of AWS services (Rekognition, Bedrock)
to enable prototype development without incurring cloud costs. The mock services
simulate realistic behavior including response times and return values.

Mock services included:
- AWS Rekognition: Image comparison and label detection
- AWS Bedrock: LLM invocation for text generation

Configuration:
- USE_REAL_AWS: Flag to switch between mock and real AWS services (default: False)

Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5
"""

import hashlib
import random
import time
from typing import Any, Dict, List


# Configuration flag to switch between mock and real AWS services
USE_REAL_AWS = False


def simulate_api_delay() -> None:
    """
    Simulate realistic API response time.
    
    Sleeps for a random duration between 0.5 and 2.0 seconds to mimic
    actual AWS API network latency and processing time.
    
    Validates: Requirements 9.4
    
    Examples:
        >>> import time
        >>> start = time.time()
        >>> simulate_api_delay()
        >>> elapsed = time.time() - start
        >>> 0.5 <= elapsed <= 2.0
        True
    """
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)


def _calculate_image_hash(image_bytes: bytes) -> str:
    """
    Calculate a perceptual hash of an image for similarity comparison.
    
    Uses SHA-256 hash as a simple proxy for image similarity.
    In a real implementation, this would use perceptual hashing algorithms
    like pHash or dHash that are robust to minor image variations.
    
    Args:
        image_bytes: Raw image data as bytes
    
    Returns:
        Hexadecimal hash string
    
    Note:
        This is a simplified implementation. Real perceptual hashing would
        be more sophisticated and handle image transformations better.
    """
    return hashlib.sha256(image_bytes).hexdigest()


def mock_rekognition_compare_faces(source_image: bytes, target_image: bytes) -> float:
    """
    Mock AWS Rekognition face/feature comparison.
    
    Compares two images and returns a similarity score. Uses simple image
    hashing to determine similarity. In production, this would be replaced
    with actual AWS Rekognition CompareFaces API.
    
    Args:
        source_image: Reference image as bytes (Golden Source)
        target_image: User-uploaded image as bytes
    
    Returns:
        Similarity score as a percentage (0.0-100.0)
        - Higher scores indicate greater similarity
        - Scores are based on hash comparison with added randomness
    
    Validates: Requirements 9.1, 9.2
    
    Examples:
        >>> img1 = b"fake_image_data_1"
        >>> img2 = b"fake_image_data_2"
        >>> score = mock_rekognition_compare_faces(img1, img2)
        >>> 0.0 <= score <= 100.0
        True
        >>> # Same image should have high similarity
        >>> score_same = mock_rekognition_compare_faces(img1, img1)
        >>> score_same > 90.0
        True
    """
    # Simulate API delay
    simulate_api_delay()
    
    # Calculate hashes for both images
    source_hash = _calculate_image_hash(source_image)
    target_hash = _calculate_image_hash(target_image)
    
    # If images are identical, return high similarity with slight variation
    if source_hash == target_hash:
        return random.uniform(92.0, 98.0)
    
    # Calculate similarity based on hash differences
    # Count matching characters in the first 16 characters of hash
    matching_chars = sum(1 for s, t in zip(source_hash[:16], target_hash[:16]) if s == t)
    base_similarity = (matching_chars / 16) * 100
    
    # Add some randomness to make it more realistic
    # Adjust by +/- 15% to simulate real-world variation
    variation = random.uniform(-15.0, 15.0)
    similarity_score = base_similarity + variation
    
    # Ensure score is within valid bounds [0.0, 100.0]
    similarity_score = max(0.0, min(similarity_score, 100.0))
    
    return round(similarity_score, 2)


def mock_rekognition_detect_labels(image: bytes) -> List[Dict[str, Any]]:
    """
    Mock AWS Rekognition label detection.
    
    Analyzes an image and returns detected labels with confidence scores.
    Returns a predefined set of realistic labels for demonstration purposes.
    
    Args:
        image: Image data as bytes
    
    Returns:
        List of detected labels, each containing:
        - Name: Label name (e.g., "Product", "Electronics", "Box")
        - Confidence: Confidence score (0.0-100.0)
        - Instances: List of bounding boxes (empty for mock)
        - Parents: List of parent categories (empty for mock)
    
    Validates: Requirements 9.1, 9.3
    
    Examples:
        >>> img = b"fake_image_data"
        >>> labels = mock_rekognition_detect_labels(img)
        >>> len(labels) > 0
        True
        >>> all(0.0 <= label["Confidence"] <= 100.0 for label in labels)
        True
    """
    # Simulate API delay
    simulate_api_delay()
    
    # Generate a seed from image hash for consistent results
    image_hash = _calculate_image_hash(image)
    seed = int(image_hash[:8], 16)
    random.seed(seed)
    
    # Predefined label pool for realistic mock responses
    label_pool = [
        "Product",
        "Electronics",
        "Box",
        "Package",
        "Device",
        "Appliance",
        "Container",
        "Label",
        "Text",
        "Logo",
        "Brand",
        "Seal",
        "Barcode",
        "QR Code",
    ]
    
    # Select 5-8 random labels
    num_labels = random.randint(5, 8)
    selected_labels = random.sample(label_pool, min(num_labels, len(label_pool)))
    
    # Generate mock label responses with confidence scores
    labels = []
    for label_name in selected_labels:
        confidence = random.uniform(75.0, 99.0)
        labels.append({
            "Name": label_name,
            "Confidence": round(confidence, 2),
            "Instances": [],
            "Parents": [],
        })
    
    # Sort by confidence (highest first)
    labels.sort(key=lambda x: x["Confidence"], reverse=True)
    
    # Reset random seed
    random.seed()
    
    return labels


def mock_bedrock_invoke(prompt: str, model_id: str = "anthropic.claude-v2") -> str:
    """
    Mock AWS Bedrock LLM invocation.
    
    Simulates calling an LLM through AWS Bedrock. Returns predefined responses
    based on prompt keywords for demonstration purposes.
    
    Args:
        prompt: The text prompt to send to the LLM
        model_id: The model identifier (e.g., "anthropic.claude-v2")
    
    Returns:
        Generated text response from the mock LLM
    
    Validates: Requirements 9.3, 9.5
    
    Examples:
        >>> response = mock_bedrock_invoke("Is this product authentic?")
        >>> len(response) > 0
        True
        >>> "authentic" in response.lower() or "product" in response.lower()
        True
    """
    # Simulate API delay
    simulate_api_delay()
    
    # Predefined responses based on prompt keywords
    prompt_lower = prompt.lower()
    
    if "authentic" in prompt_lower or "fake" in prompt_lower or "counterfeit" in prompt_lower:
        responses = [
            "Based on the visual analysis, the product shows characteristics consistent with authentic items. "
            "However, I recommend verifying with the official brand for complete certainty.",
            
            "The product features appear to match authentic specifications. Key indicators include proper "
            "branding, quality materials, and correct packaging details.",
            
            "While the visual inspection suggests authenticity, please note that sophisticated counterfeits "
            "can be difficult to detect from images alone. Consider purchasing from authorized retailers.",
        ]
    
    elif "price" in prompt_lower or "cost" in prompt_lower or "expensive" in prompt_lower:
        responses = [
            "The pricing appears competitive compared to market averages. Consider the total cost of "
            "ownership including maintenance and consumables for a complete picture.",
            
            "This price point is within the typical range for this product category. However, be sure to "
            "factor in long-term costs such as filters, power consumption, and maintenance.",
            
            "The sticker price is reasonable, but remember that the true cost includes operational expenses "
            "over the product's lifetime. Use the TCO calculator for a comprehensive analysis.",
        ]
    
    elif "seller" in prompt_lower or "trust" in prompt_lower or "reliable" in prompt_lower:
        responses = [
            "When evaluating sellers, consider multiple factors: trust score, number of reviews, platform "
            "reputation, and return policies. Higher trust scores generally indicate better reliability.",
            
            "Seller reliability is crucial for a positive purchase experience. Look for sellers with high "
            "trust scores, verified reviews, and good customer service ratings.",
            
            "The seller's trust score reflects their track record. Combine this with price competitiveness "
            "to make an informed decision. Avoid sponsored listings for unbiased results.",
        ]
    
    else:
        # Generic responses for other prompts
        responses = [
            "Thank you for your question. For the most accurate analysis, I recommend using the specific "
            "tools available in Yukti AI: Seller Matrix for price comparison, Satya-View for authenticity "
            "verification, and True-Cost Calculator for TCO analysis.",
            
            "Yukti AI provides comprehensive tools to help you make informed purchasing decisions. Each "
            "feature is designed to address specific aspects of product evaluation.",
            
            "For detailed insights, please use the appropriate Yukti AI tool based on your needs: seller "
            "comparison, authenticity verification, or cost analysis.",
        ]
    
    # Select a random response from the appropriate category
    response = random.choice(responses)
    
    return response


# Example usage and testing
if __name__ == "__main__":
    print("Testing AWS Mock Services\n")
    
    # Test image comparison
    print("1. Testing mock_rekognition_compare_faces:")
    img1 = b"sample_image_data_1"
    img2 = b"sample_image_data_2"
    img3 = b"sample_image_data_1"  # Same as img1
    
    score_different = mock_rekognition_compare_faces(img1, img2)
    print(f"   Different images similarity: {score_different}%")
    
    score_same = mock_rekognition_compare_faces(img1, img3)
    print(f"   Same images similarity: {score_same}%")
    
    # Test label detection
    print("\n2. Testing mock_rekognition_detect_labels:")
    labels = mock_rekognition_detect_labels(img1)
    print(f"   Detected {len(labels)} labels:")
    for label in labels[:3]:
        print(f"   - {label['Name']}: {label['Confidence']}% confidence")
    
    # Test Bedrock invocation
    print("\n3. Testing mock_bedrock_invoke:")
    prompts = [
        "Is this product authentic?",
        "What about the price?",
        "Can I trust this seller?",
    ]
    
    for prompt in prompts:
        response = mock_bedrock_invoke(prompt)
        print(f"   Prompt: {prompt}")
        print(f"   Response: {response[:100]}...")
        print()
    
    print("All tests completed!")
