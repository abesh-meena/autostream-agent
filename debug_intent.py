"""
Debug intent classification to see what's happening
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.intent import IntentClassifier

def debug_intent():
    """Debug the intent classification"""
    
    classifier = IntentClassifier()
    
    test_inputs = [
        "I want to try Pro plan for my YouTube channel",
        "I want to try", 
        "Pro plan for my YouTube",
        "my YouTube channel",
        "for my YouTube"
    ]
    
    print("🔍 Debugging Intent Classification")
    print("=" * 40)
    
    for user_input in test_inputs:
        print(f"\n📝 Testing: '{user_input}'")
        print("-" * 30)
        
        intent_obj = classifier.classify_intent(user_input)
        simple_intent = classifier.classify_intent_simple(user_input)
        
        print(f"🎯 Intent Object: {intent_obj}")
        print(f"🎯 Simple Intent: {simple_intent}")
        
        # Check which pattern matches
        text_lower = user_input.lower()
        for intent_type, patterns in classifier.intent_patterns.items():
            for pattern in patterns:
                if pattern.startswith('\\b'):
                    # Word boundary pattern
                    import re
                    if re.search(pattern, text_lower):
                        print(f"✅ MATCHED {intent_type.value}: {pattern}")
                        break
                else:
                    # Simple pattern
                    if pattern in text_lower:
                        print(f"✅ MATCHED {intent_type.value}: {pattern}")
                        break
        print()

if __name__ == "__main__":
    debug_intent()
