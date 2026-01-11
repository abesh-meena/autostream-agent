"""
AutoStream Agent - Main Application
Social Media to Lead Generation Agentic Workflow
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime

# Add agent module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.graph import WorkflowGraph, WorkflowState
from agent.intent import IntentClassifier
from agent.rag import RAGEngine
from agent.tools import ToolRegistry

class AutoStreamAgent:
    """Main AutoStream Agent class with state management"""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base/autostream_data.json"):
        """
        Initialize the AutoStream Agent
        
        Args:
            knowledge_base_path: Path to the knowledge base JSON file
        """
        self.knowledge_base_path = knowledge_base_path
        self.workflow_graph = WorkflowGraph()
        self.intent_classifier = IntentClassifier()
        self.rag_engine = RAGEngine(knowledge_base_path)
        self.tool_registry = ToolRegistry()
        
        # Initialize session and state management
        self.session_id = f"session_{datetime.now().timestamp()}"
        self.current_state: Optional[WorkflowState] = None
        
        print("🚀 AutoStream Agent initialized successfully!")
        print(f"📁 Knowledge base: {knowledge_base_path}")
        print(f"🆔 Session ID: {self.session_id}")
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request through the complete workflow with state management
        
        Args:
            user_input: User's input string
            
        Returns:
            Dictionary containing the response and metadata
        """
        print(f"\n📝 Processing request: '{user_input}'")
        
        try:
            # Execute workflow with existing state (maintains conversation context)
            workflow_state = self.workflow_graph.execute_workflow(user_input, self.current_state)
            
            # Update current state for next interaction
            self.current_state = workflow_state
            
            # Prepare response data
            response_data = {
                "status": "success",
                "response": workflow_state.response,
                "intent": workflow_state.intent,
                "tools_used": workflow_state.tools_used,
                "context": workflow_state.context,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "qualification_stage": workflow_state.qualification_stage,
                "conversation_history": workflow_state.conversation_history
            }
            
            # Add lead information if available
            if workflow_state.name:
                response_data["lead_info"] = {
                    "name": workflow_state.name,
                    "email": workflow_state.email,
                    "platform": workflow_state.platform
                }
            
            print(f"✅ Request processed successfully")
            print(f"🎯 Intent: {workflow_state.intent}")
            print(f"🔄 Stage: {workflow_state.qualification_stage}")
            print(f"🔧 Tools used: {workflow_state.tools_used}")
            
            return response_data
            
        except Exception as e:
            error_response = {
                "status": "error",
                "error": str(e),
                "response": f"I apologize, but I encountered an error while processing your request: {str(e)}",
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"❌ Error processing request: {str(e)}")
            return error_response
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get agent capabilities and available tools"""
        return {
            "intents": [
                "GREET",
                "INQUIRY", 
                "HIGH_INTENT"
            ],
            "tools": {
                "knowledge_retrieval": "RAG-based knowledge retrieval",
                "mock_lead_capture": "Lead capture function"
            },
            "workflow_info": self.workflow_graph.get_workflow_info(),
            "knowledge_base_path": self.knowledge_base_path
        }
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        print("🗑️ Conversation history cleared")

def main():
    """Main function to run the AutoStream Agent"""
    print("=" * 60)
    print("🎯 AutoStream Agent - Social Media to Lead Generation")
    print("=" * 60)
    
    # Initialize agent
    try:
        agent = AutoStreamAgent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")
        return
    
    # Display capabilities
    capabilities = agent.get_capabilities()
    print(f"\n📋 Available Intents: {', '.join(capabilities['intents'])}")
    print(f"🔧 Available Tools: {list(capabilities['tools'].keys())}")
    
    # Interactive mode
    print("\n💬 Enter your requests (type 'exit' to quit, 'help' for commands):")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            if user_input.lower() == 'capabilities':
                print_capabilities(agent)
                continue
            
            if user_input.lower() == 'history':
                print_history(agent)
                continue
            
            if user_input.lower() == 'clear':
                agent.clear_conversation_history()
                continue
            
            # Process the request
            result = agent.process_request(user_input)
            
            print(f"\n🤖 Agent: {result['response']}")
            
            # Show additional info if available
            if result.get('tools_used'):
                print(f"🔧 Tools used: {', '.join(result['tools_used'])}")
            
            if result.get('status') == 'error':
                print(f"⚠️  Error details: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")

def print_help():
    """Print help information"""
    print("\n📖 Available Commands:")
    print("  help     - Show this help message")
    print("  capabilities - Show agent capabilities")
    print("  history  - Show conversation history")
    print("  clear    - Clear conversation history")
    print("  exit     - Exit the application")
    print("\n💡 Example requests:")
    print("  'Generate leads for technology companies'")
    print("  'Create a LinkedIn post about digital marketing'")
    print("  'Analyze my Twitter performance'")
    print("  'Write content about artificial intelligence'")

def print_capabilities(agent: AutoStreamAgent):
    """Print agent capabilities"""
    capabilities = agent.get_capabilities()
    
    print(f"\n🎯 Supported Intents:")
    for intent in capabilities['intents']:
        print(f"  • {intent}")
    
    print(f"\n🔧 Available Tools:")
    for tool_name, description in capabilities['tools'].items():
        print(f"  • {tool_name}: {description}")

def print_history(agent: AutoStreamAgent):
    """Print conversation history"""
    history = agent.get_conversation_history()
    
    if not history:
        print("\n📝 No conversation history yet")
        return
    
    print(f"\n📝 Conversation History ({len(history)} messages):")
    print("-" * 40)
    
    for i, message in enumerate(history, 1):
        prefix = "👤" if message['type'] == 'user' else "🤖"
        content = message['content']
        
        # Truncate long messages
        if len(content) > 100:
            content = content[:100] + "..."
        
        print(f"{i}. {prefix} {content}")
        
        if message['type'] == 'agent' and message.get('intent'):
            print(f"   🎯 Intent: {message['intent']}")

if __name__ == "__main__":
    main()
