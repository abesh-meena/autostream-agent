"""
Graph module for AutoStream Agent
Manages the workflow graph and agent orchestration
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import json
from dataclasses import dataclass
from datetime import datetime

class NodeType(Enum):
    """Types of nodes in the workflow graph"""
    START = "start"
    INTENT_CLASSIFICATION = "intent_classification"
    KNOWLEDGE_RETRIEVAL = "knowledge_retrieval"
    TOOL_EXECUTION = "tool_execution"
    RESPONSE_GENERATION = "response_generation"
    END = "end"

@dataclass
class Node:
    """Represents a node in the workflow graph"""
    id: str
    type: NodeType
    description: str
    function: Optional[Callable] = None
    next_nodes: List[str] = None
    
    def __post_init__(self):
        if self.next_nodes is None:
            self.next_nodes = []

@dataclass
class Edge:
    """Represents an edge between nodes"""
    from_node: str
    to_node: str
    condition: Optional[str] = None

@dataclass
class WorkflowState:
    """Represents the current state of the workflow with memory across turns"""
    user_input: str
    intent: Optional[str] = None
    context: Dict[str, Any] = None
    tools_used: List[str] = None
    response: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    # Lead qualification state
    name: Optional[str] = None
    email: Optional[str] = None
    platform: Optional[str] = None
    
    # Conversation history
    conversation_history: List[Dict[str, Any]] = None
    
    # Lead qualification stage
    qualification_stage: str = "initial"
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.tools_used is None:
            self.tools_used = []
        if self.metadata is None:
            self.metadata = {}
        if self.conversation_history is None:
            self.conversation_history = []

class WorkflowGraph:
    """Manages the workflow graph for the AutoStream agent with state management"""
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.current_node: Optional[str] = None
        self.state: Optional[WorkflowState] = None
        self._build_workflow()
    
    def _build_workflow(self):
        """Build the default workflow graph"""
        # Create nodes
        self.nodes = {
            "start": Node("start", NodeType.START, "Entry point for user requests"),
            "intent_classification": Node(
                "intent_classification", 
                NodeType.INTENT_CLASSIFICATION, 
                "Classify user intent",
                self._classify_intent
            ),
            "knowledge_retrieval": Node(
                "knowledge_retrieval",
                NodeType.KNOWLEDGE_RETRIEVAL,
                "Retrieve relevant knowledge",
                self._retrieve_knowledge
            ),
            "tool_execution": Node(
                "tool_execution",
                NodeType.TOOL_EXECUTION,
                "Execute relevant tools",
                self._execute_tools
            ),
            "response_generation": Node(
                "response_generation",
                NodeType.RESPONSE_GENERATION,
                "Generate final response",
                self._generate_response
            ),
            "end": Node("end", NodeType.END, "Workflow completion")
        }
        
        # Create edges (workflow connections)
        self.edges = [
            Edge("start", "intent_classification"),
            Edge("intent_classification", "knowledge_retrieval"),
            Edge("knowledge_retrieval", "tool_execution"),
            Edge("tool_execution", "response_generation"),
            Edge("response_generation", "end")
        ]
        
        # Set next nodes for each node
        self.nodes["start"].next_nodes = ["intent_classification"]
        self.nodes["intent_classification"].next_nodes = ["knowledge_retrieval"]
        self.nodes["knowledge_retrieval"].next_nodes = ["tool_execution"]
        self.nodes["tool_execution"].next_nodes = ["response_generation"]
        self.nodes["response_generation"].next_nodes = ["end"]
    
    def execute_workflow(self, user_input: str, existing_state: Optional[WorkflowState] = None) -> WorkflowState:
        """
        Execute the complete workflow for a user input with state management
        
        Args:
            user_input: The user's input string
            existing_state: Previous state to maintain conversation context
            
        Returns:
            WorkflowState containing the results
        """
        # Use existing state or create new one
        if existing_state:
            state = existing_state
            state.user_input = user_input
            # Add to conversation history
            state.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "user",
                "content": user_input
            })
        else:
            state = WorkflowState(user_input=user_input)
            state.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "user",
                "content": user_input
            })
        
        self.state = state
        self.current_node = "start"
        
        print(f"\n📝 Processing request: '{user_input}'")
        print(f"🧠 Current state: Stage={state.qualification_stage}, Intent={state.intent}")
        
        try:
            while self.current_node != "end":
                current_node_obj = self.nodes[self.current_node]
                
                # Execute node function if available
                if current_node_obj.function:
                    current_node_obj.function(state)
                
                # Move to next node
                if current_node_obj.next_nodes:
                    self.current_node = current_node_obj.next_nodes[0]
                else:
                    break
            
            # Add execution metadata
            state.metadata["execution_time"] = datetime.now().isoformat()
            if self.current_node in self.nodes:
                node_index = list(self.nodes.keys()).index(self.current_node)
                state.metadata["nodes_executed"] = list(self.nodes.keys())[:node_index + 1]
            else:
                state.metadata["nodes_executed"] = []
            
            # Add agent response to conversation history
            if state.response:
                state.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "type": "agent",
                    "content": state.response,
                    "intent": state.intent,
                    "stage": state.qualification_stage
                })
            
        except Exception as e:
            state.metadata["error"] = str(e)
            state.response = f"An error occurred during processing: {str(e)}"
        
        return state
    
    def _classify_intent(self, state: WorkflowState):
        """Classify user intent (placeholder implementation)"""
        from .intent import IntentClassifier
        
        classifier = IntentClassifier()
        
        # During lead qualification, preserve the original HIGH_INTENT
        if state.qualification_stage != "initial" and state.intent == "HIGH_INTENT":
            # Keep the original intent during lead qualification
            pass
        else:
            intent_obj = classifier.classify_intent(state.user_input)
            state.intent = intent_obj.value
        
        # Extract entities
        entities = classifier.extract_entities(state.user_input)
        state.context["entities"] = entities
    
    def _retrieve_knowledge(self, state: WorkflowState):
        """Retrieve relevant knowledge (placeholder implementation)"""
        from .rag import RAGEngine
        
        # Initialize RAG engine with knowledge base path
        rag_engine = RAGEngine("knowledge_base/autostream_data.json")
        result = rag_engine.generate_response(state.user_input, state.intent)
        
        state.context["retrieved_knowledge"] = result["context"]
        state.context["sources"] = result["sources"]
    
    def _execute_tools(self, state: WorkflowState):
        """Execute relevant tools based on intent and lead qualification stage"""
        # Handle lead qualification flow for HIGH_INTENT
        if state.intent == "HIGH_INTENT":
            self._handle_lead_qualification(state)
            return
        
        # Handle INQUIRY with RAG only (no content creation)
        if state.intent == "INQUIRY":
            self._handle_inquiry(state)
            return
        
        # Handle GREET with simple response
        if state.intent == "GREET":
            self._handle_greeting(state)
            return
    
    def _handle_inquiry(self, state: WorkflowState):
        """Handle inquiry intent with RAG knowledge retrieval"""
        from .rag import RAGEngine
        
        rag_engine = RAGEngine("knowledge_base/autostream_data.json")
        result = rag_engine.generate_response(state.user_input, state.intent)
        
        # Direct RAG response without any wrapper
        state.response = result["response"]
        state.context["retrieved_knowledge"] = result["context"]
        state.context["sources"] = result["sources"]
    
    def _handle_greeting(self, state: WorkflowState):
        """Handle greeting intent with simple response"""
        state.response = "Hello 👋 How can I help you today?"
    
    def _handle_lead_qualification(self, state: WorkflowState):
        """Handle the lead qualification flow for HIGH_INTENT users"""
        print(f"🎯 Handling lead qualification at stage: {state.qualification_stage}")
        
        if state.qualification_stage == "initial":
            # Ask for name first
            state.response = "Great! I'd be happy to help you get started. What's your name?"
            state.qualification_stage = "asking_name"
            return  # Return early to avoid overriding response
            
        elif state.qualification_stage == "asking_name":
            # Extract name from user input
            name = self._extract_name(state.user_input)
            if name:
                state.name = name
                state.response = f"Nice to meet you, {name}! Now, what's your email address?"
                state.qualification_stage = "asking_email"
                return  # Return early to avoid overriding response
            else:
                state.response = "I didn't catch your name. Could you please tell me your name?"
                return  # Return early to avoid overriding response
                
        elif state.qualification_stage == "asking_email":
            # Extract email from user input
            email = self._extract_email(state.user_input)
            if email:
                state.email = email
                state.response = "Perfect! One last question - what creator platform are you planning to use? (e.g., YouTube, TikTok, Instagram, etc.)"
                state.qualification_stage = "asking_platform"
                return  # Return early to avoid overriding response
            else:
                state.response = "I need a valid email address. Could you please provide your email?"
                return  # Return early to avoid overriding response
                
        elif state.qualification_stage == "asking_platform":
            # Extract platform from user input
            platform = self._extract_platform(state.user_input)
            if platform:
                state.platform = platform
                # All information collected - call the lead capture tool
                self._capture_lead(state)
                state.response = f"Thanks {state.name}! I've captured your information. Our team will be in touch soon!"
                state.qualification_stage = "completed"
                return  # Return early to avoid overriding response
            else:
                state.response = "Which creator platform will you be using? For example: YouTube, TikTok, Instagram, LinkedIn, etc.?"
                return  # Return early to avoid overriding response
                
        elif state.qualification_stage == "completed":
            # Lead already captured
            state.response = f"Thanks {state.name}! I've captured your information. Our team will be in touch soon!"
            return  # Return early to avoid overriding response
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from user input"""
        # Simple extraction - look for common patterns
        text = text.strip()
        
        # Remove common prefixes
        prefixes = ["my name is", "i'm", "i am", "call me", "it's"]
        for prefix in prefixes:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].strip()
                break
        
        # Take first word as name (simple approach)
        words = text.split()
        if words and len(words[0]) > 1:  # At least 2 characters
            return words[0].title()
        
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email from user input"""
        import re
        
        # Simple email regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        
        return match.group(0) if match else None
    
    def _extract_platform(self, text: str) -> Optional[str]:
        """Extract platform from user input"""
        platforms = ["youtube", "tiktok", "instagram", "linkedin", "twitter", "facebook", "twitch"]
        text_lower = text.lower()
        
        for platform in platforms:
            if platform in text_lower:
                return platform.title()
        
        return None
    
    def _capture_lead(self, state: WorkflowState):
        """Capture the lead using the mock_lead_capture function"""
        # Import the mock_lead_capture function
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from lead_capture import mock_lead_capture
        
        # This is the critical tool call that must happen AFTER collecting all info
        mock_lead_capture(state.name, state.email, state.platform)
        
        # Store in context for tracking
        state.context["lead_captured"] = {
            "name": state.name,
            "email": state.email,
            "platform": state.platform,
            "captured_at": datetime.now().isoformat()
        }
    
    def _prepare_tool_params(self, state: WorkflowState) -> Dict[str, Any]:
        """Prepare parameters for tool execution"""
        entities = state.context.get("entities", {})
        
        base_params = {}
        
        # Handle different intents with proper parameters
        if state.intent == "INQUIRY":
            base_params = {
                "content_type": "post",
                "topic": state.user_input,
                "platform": entities.get("platform", "linkedin")
            }
        elif state.intent == "GREET":
            base_params = {
                "content_type": "post",
                "topic": "welcome message",
                "platform": "linkedin"
            }
        else:
            # Default parameters for other cases
            base_params = {
                "content_type": "post",
                "topic": state.user_input,
                "platform": "linkedin"
            }
        
        return base_params
    
    def _generate_response(self, state: WorkflowState):
        """Generate the final response"""
        # If lead qualification is in progress, don't override the response
        if state.intent == "HIGH_INTENT" and state.qualification_stage in ["asking_name", "asking_email", "asking_platform", "completed"]:
            # Response already set by _handle_lead_qualification
            return
        
        # If response already set by _handle_inquiry or _handle_greeting, don't override
        if state.response:
            return
        
        tool_result = state.context.get("tool_result", {})
        
        if tool_result.get("status") == "success":
            if state.intent == "INQUIRY":
                content = tool_result.get("content", "")
                platform = tool_result.get("platform", "linkedin")
                state.response = f"I've created content for {platform}:\n\n{content}\n\nCharacter count: {tool_result.get('character_count', 0)}"
                
            elif state.intent == "GREET":
                content = tool_result.get("content", "")
                state.response = f"Hello! I'm here to help you. Here's a welcome message for you:\n\n{content}"
                
        else:
            # Fallback response if no tools were executed
            if state.intent == "INQUIRY":
                state.response = f"I understand you're interested in {state.intent}. Let me help you with pricing and plan information."
            elif state.intent == "GREET":
                state.response = "Hello! Welcome to AutoStream. How can I help you today?"
            else:
                state.response = f"I understand you're interested in {state.intent.replace('_', ' ')}. Let me help you with that."
    
    def get_workflow_info(self) -> Dict[str, Any]:
        """Get information about the current workflow"""
        return {
            "nodes": {id: {"type": node.type.value, "description": node.description} 
                     for id, node in self.nodes.items()},
            "edges": [{"from": edge.from_node, "to": edge.to_node} for edge in self.edges],
            "current_node": self.current_node
        }
