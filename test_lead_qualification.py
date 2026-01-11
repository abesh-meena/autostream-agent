"""
Test script for Lead Qualification Flow
Verifies the correct sequence: HIGH_INTENT → Name → Email → Platform → Tool Call
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.graph import WorkflowGraph

def test_lead_qualification_flow():
    """Test the complete lead qualification flow"""
    
    print("🧪 Testing Lead Qualification Flow")
    print("=" * 60)
    
    # Initialize workflow
    workflow = WorkflowGraph()
    state = None
    
    # Test conversation flow
    test_inputs = [
        "I want to try",           # HIGH_INTENT trigger
        "John",                   # Name
        "john@example.com",      # Email  
        "YouTube",                # Platform
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n📝 Step {i}: '{user_input}'")
        print("-" * 40)
        
        # Execute workflow with state management
        state = workflow.execute_workflow(user_input, state)
        
        print(f"🤖 Agent: {state.response}")
        print(f"🎯 Intent: {state.intent}")
        print(f"🔄 Stage: {state.qualification_stage}")
        
        if state.name:
            print(f"👤 Name: {state.name}")
        if state.email:
            print(f"📧 Email: {state.email}")
        if state.platform:
            print(f"🎬 Platform: {state.platform}")
    
    print("\n" + "=" * 60)
    print("🎉 Lead Qualification Flow Test Completed!")
    
    # Verify final state
    if state.qualification_stage == "completed":
        print("✅ Lead qualification completed successfully!")
        print(f"✅ Lead captured: {state.name}, {state.email}, {state.platform}")
    else:
        print("❌ Lead qualification not completed")
    
    return state

def test_wrong_sequence():
    """Test that tool is NOT called before collecting all info"""
    
    print("\n🧪 Testing Wrong Sequence Prevention")
    print("=" * 50)
    
    workflow = WorkflowGraph()
    
    # Test single high intent input (should not call tool yet)
    print("\n📝 Input: 'I want to buy now'")
    print("-" * 30)
    
    state = workflow.execute_workflow("I want to buy now")
    
    print(f"🤖 Agent: {state.response}")
    print(f"🔄 Stage: {state.qualification_stage}")
    
    # Verify tool was NOT called
    if state.qualification_stage == "asking_name":
        print("✅ Correctly asking for name first (no premature tool call)")
    else:
        print("❌ Wrong sequence - tool called too early")
    
    return state

def test_state_persistence():
    """Test that state persists across conversation turns"""
    
    print("\n🧪 Testing State Persistence")
    print("=" * 40)
    
    workflow = WorkflowGraph()
    state = None
    
    # Simulate conversation with interruptions
    conversations = [
        ("hi", "Greeting"),
        ("I want to try", "HIGH_INTENT trigger"),
        ("My name is Sarah", "Name provided"),
        ("sarah@email.com", "Email provided"),
        ("I'll use TikTok", "Platform provided")
    ]
    
    for user_input, description in conversations:
        print(f"\n📝 {description}: '{user_input}'")
        print("-" * 30)
        
        state = workflow.execute_workflow(user_input, state)
        
        print(f"🤖 Agent: {state.response}")
        print(f"🔄 Stage: {state.qualification_stage}")
        print(f"📊 History length: {len(state.conversation_history)}")
    
    # Verify state persistence
    if state.name == "Sarah" and state.email == "sarah@email.com" and state.platform == "Tiktok":
        print("✅ State persisted correctly across conversation turns")
    else:
        print("❌ State not persisted properly")
    
    return state

if __name__ == "__main__":
    # Run all tests
    final_state = test_lead_qualification_flow()
    test_wrong_sequence()
    test_state_persistence()
    
    print("\n" + "=" * 60)
    print("🎯 All Lead Qualification Tests Completed!")
    print("=" * 60)
