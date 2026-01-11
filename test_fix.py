"""
Test script to verify all fixes are working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.graph import WorkflowGraph

def test_fixed_behavior():
    """Test the fixed agent behavior"""
    
    print("🧪 Testing Fixed Agent Behavior")
    print("=" * 50)
    
    workflow = WorkflowGraph()
    state = None
    
    # Test cases based on user's examples
    test_cases = [
        ("Hi", "GREET", "Hello 👋 How can I help you today?"),
        ("Tell me about Pro plan", "INQUIRY", "Should return Pro plan info from JSON"),
        ("I want to try Pro plan for my YouTube channel", "HIGH_INTENT", "Should start lead qualification"),
        ("Abesh", "HIGH_INTENT", "Should ask for email"),
        ("abesh@gmail.com", "HIGH_INTENT", "Should ask for platform"),
        ("YouTube", "HIGH_INTENT", "Should capture lead")
    ]
    
    for i, (user_input, expected_intent, description) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{user_input}'")
        print(f"🎯 Expected: {expected_intent} - {description}")
        print("-" * 40)
        
        state = workflow.execute_workflow(user_input, state)
        
        print(f"🤖 Agent: {state.response}")
        print(f"✅ Intent: {state.intent}")
        print(f"🔄 Stage: {state.qualification_stage}")
        
        # Verify intent classification
        if state.intent == expected_intent:
            print("✅ Intent classification CORRECT")
        else:
            print(f"❌ Intent classification WRONG - Expected {expected_intent}, got {state.intent}")
        
        # For HIGH_INTENT, verify lead qualification flow
        if expected_intent == "HIGH_INTENT":
            if state.qualification_stage in ["asking_name", "asking_email", "asking_platform", "completed"]:
                print("✅ Lead qualification progressing correctly")
            else:
                print(f"❌ Lead qualification stuck at stage: {state.qualification_stage}")
        
        print()

if __name__ == "__main__":
    test_fixed_behavior()
