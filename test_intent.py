"""
Test script for Intent Detection Module
Verifies the three intent classifications work correctly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.intent import IntentClassifier

def test_intent_detection():
    """Test the intent detection with various examples"""
    
    classifier = IntentClassifier()
    
    test_cases = [
        # Greeting tests
        ("hi", "GREET"),
        ("hello", "GREET"),
        ("hey there", "GREET"),
        ("good morning", "GREET"),
        
        # Inquiry tests
        ("what's the price?", "INQUIRY"),
        ("tell me about your plans", "INQUIRY"),
        ("what features do you offer?", "INQUIRY"),
        ("how much does it cost?", "INQUIRY"),
        
        # High intent tests
        ("I want to try", "HIGH_INTENT"),
        ("sign up now", "HIGH_INTENT"),
        ("I want to buy", "HIGH_INTENT"),
        ("use for YouTube", "HIGH_INTENT"),
        ("ready to purchase", "HIGH_INTENT")
    ]
    
    print("🧪 Testing Intent Detection")
    print("=" * 50)
    
    all_passed = True
    
    for input_text, expected in test_cases:
        result = classifier.classify_intent_simple(input_text)
        status = "✅" if result == expected else "❌"
        
        print(f"{status} '{input_text}' → {result} (expected: {expected})")
        
        if result != expected:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed!")
    
    return all_passed

if __name__ == "__main__":
    test_intent_detection()
