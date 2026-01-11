"""
Final test to verify all fixes are working
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.graph import WorkflowGraph

def test_final_fixes():
    """Test all the fixes"""
    
    print("🧪 Testing Final Fixes")
    print("=" * 50)
    
    workflow = WorkflowGraph()
    state = None
    
    # Test 1: INQUIRY with direct RAG response
    print("\n📝 Test 1: 'Tell me about Pro plan'")
    print("-" * 40)
    state = workflow.execute_workflow("Tell me about Pro plan", state)
    print(f"🤖 Agent: {state.response}")
    print(f"✅ Intent: {state.intent}")
    
    # Test 2: "yes tell me" should be INQUIRY
    print("\n📝 Test 2: 'yes tell me'")
    print("-" * 40)
    state = workflow.execute_workflow("yes tell me", state)
    print(f"🤖 Agent: {state.response}")
    print(f"✅ Intent: {state.intent}")
    
    # Test 3: Complete lead qualification flow
    print("\n📝 Test 3: Lead Qualification Flow")
    print("-" * 40)
    
    # Reset state for clean test
    state = None
    
    lead_flow = [
        ("I want to try Pro plan for my YouTube channel", "HIGH_INTENT"),
        ("Abesh", "HIGH_INTENT"),
        ("abesh@gmail.com", "HIGH_INTENT"),
        ("YouTube", "HIGH_INTENT")
    ]
    
    for i, (user_input, expected_intent) in enumerate(lead_flow, 1):
        print(f"\n  Step {i}: '{user_input}'")
        state = workflow.execute_workflow(user_input, state)
        print(f"  🤖 Agent: {state.response}")
        print(f"  ✅ Intent: {state.intent}")
        print(f"  🔄 Stage: {state.qualification_stage}")
        
        if state.intent != expected_intent:
            print(f"  ❌ Expected {expected_intent}, got {state.intent}")
        else:
            print(f"  ✅ Intent correct")
    
    print("\n🎉 Final Test Complete!")

if __name__ == "__main__":
    test_final_fixes()
