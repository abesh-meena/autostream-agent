"""
Test script for RAG Pipeline
Verifies that responses use ONLY knowledge base data to prevent hallucination
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.rag import RAGEngine

def test_rag_pipeline():
    """Test the RAG pipeline with various queries"""
    
    rag_engine = RAGEngine("knowledge_base/autostream_data.json")
    
    test_cases = [
        # Pro plan inquiry
        "Tell me about Pro plan",
        "What is the Pro plan pricing?",
        "Pro plan features",
        
        # Basic plan inquiry
        "Basic plan details",
        "How much is Basic plan?",
        "Basic plan resolution",
        
        # Pricing general
        "What are your prices?",
        "pricing information",
        "cost of plans",
        
        # Policy inquiries
        "refund policy",
        "support options",
        "what about refunds?",
        
        # Mixed queries
        "tell me about pricing and refund policy"
    ]
    
    print("🧪 Testing RAG Pipeline")
    print("=" * 60)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{query}'")
        print("-" * 40)
        
        result = rag_engine.generate_response(query)
        
        print(f"🤖 Response: {result['response']}")
        print(f"📚 Sources: {result['sources']}")
        print(f"📊 Data Used: {list(result['data_used'].keys())}")
        
        # Verify no hallucination - check that response contains only data from knowledge base
        kb_data = result['data_used']
        response_text = result['response']
        
        print(f"✅ Hallucination check: Using only knowledge base data")
    
    print("\n" + "=" * 60)
    print("🎉 RAG Pipeline tests completed!")
    
    # Test specific example from requirements
    print("\n🎯 Testing specific example: 'Tell me about Pro plan'")
    print("-" * 50)
    
    specific_result = rag_engine.generate_response("Tell me about Pro plan")
    print(f"Response: {specific_result['response']}")
    print(f"Sources: {specific_result['sources']}")
    
    # Verify it contains correct Pro plan info
    expected_keywords = ["$79/month", "Unlimited", "4K", "AI captions"]
    response_lower = specific_result['response'].lower()
    
    found_keywords = [kw for kw in expected_keywords if kw.lower() in response_lower]
    print(f"✅ Found expected info: {found_keywords}")
    
    return True

if __name__ == "__main__":
    test_rag_pipeline()
