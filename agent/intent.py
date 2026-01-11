"""
Intent recognition module for AutoStream Agent
Handles user intent classification and routing
"""

from typing import Dict, List, Optional
from enum import Enum
import re

class IntentType(Enum):
    """Enumeration of supported user intents"""
    GREET = "GREET"
    INQUIRY = "INQUIRY"
    HIGH_INTENT = "HIGH_INTENT"

class IntentClassifier:
    """Classifies user intent from text input"""
    
    def __init__(self):
        # STRONG HIGH_INTENT keywords for lead qualification
        self.intent_patterns = {
            IntentType.GREET: [
                r"\bhi\b",
                r"\bhello\b",
                r"\bhey\b",
                r"\bhowdy\b",
                r"\bgreetings\b",
                r"\bgood morning\b",
                r"\bgood afternoon\b",
                r"\bgood evening\b"
            ],
            IntentType.INQUIRY: [
                r"\bprice\b",
                r"\bpricing\b",
                r"\bplan\b",
                r"\bplans\b",
                r"\bfeatures\b",
                r"\bcost\b",
                r"\bhow much\b",
                r"\bwhat does.*cost\b",
                r"\bdo you offer\b",
                r"\bwhat do you have\b",
                r"\btell me about\b",
                r"\binformation about\b"
            ],
            IntentType.HIGH_INTENT: [
                # STRONG lead generation keywords
                r"\bi want to try\b",
                r"\bsign up\b",
                r"\bsignup\b",
                r"\bbuy\b",
                r"\bpurchase\b",
                r"\border\b",
                r"\bget started\b",
                r"\bstart trial\b",
                r"\bfree trial\b",
                r"\buse for youtube\b",
                r"\buse for.*video\b",
                r"\bmy youtube\b",
                r"\bmy instagram\b",
                r"\bmy tiktok\b",
                r"\bmy facebook\b",
                r"\bmy linkedin\b",
                r"\bfor my youtube\b",
                r"\bfor my instagram\b",
                r"\bfor my tiktok\b",
                r"\bready to buy\b",
                r"\bwant to purchase\b",
                r"\binterested in\b",
                r"\bready to start\b",
                r"\blet's start\b",
                r"\bcreate account\b",
                r"\bregister\b"
            ]
        }
    
    def classify_intent(self, text: str) -> IntentType:
        """
        Classify the intent of user input text with HIGH_INTENT priority
        
        Args:
            text: User input string
            
        Returns:
            IntentType: Classified intent
        """
        text_lower = text.lower()
        
        # Special case: "yes", "yes tell me", "ok", "okay" should be INQUIRY
        if text_lower in ["yes", "yes tell me", "ok", "okay"]:
            return IntentType.INQUIRY
        
        # Check HIGH_INTENT first (highest priority)
        high_intent_patterns = self.intent_patterns[IntentType.HIGH_INTENT]
        for pattern in high_intent_patterns:
            if re.search(pattern, text_lower):
                return IntentType.HIGH_INTENT
        
        # Then check other intents
        for intent_type, patterns in self.intent_patterns.items():
            if intent_type == IntentType.HIGH_INTENT:
                continue  # Already checked
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent_type
        
        return IntentType.GREET
    
    def extract_entities(self, text: str) -> Dict[str, str]:
        """
        Extract key entities from user input
        
        Args:
            text: User input string
            
        Returns:
            Dict containing extracted entities
        """
        entities = {}
        text_lower = text.lower()
        
        # Extract pricing-related entities
        if any(word in text_lower for word in ["price", "pricing", "cost"]):
            entities["topic"] = "pricing"
        
        # Extract plan-related entities
        if "basic" in text_lower:
            entities["plan"] = "basic"
        elif "pro" in text_lower:
            entities["plan"] = "pro"
        
        # Extract feature-related entities
        if "video" in text_lower:
            entities["feature"] = "video"
        elif "resolution" in text_lower:
            entities["feature"] = "resolution"
        elif "captions" in text_lower:
            entities["feature"] = "captions"
        
        # Extract action intent
        if any(word in text_lower for word in ["buy", "purchase", "order"]):
            entities["action"] = "purchase"
        elif any(word in text_lower for word in ["try", "trial", "start"]):
            entities["action"] = "trial"
        
        return entities
    
    def classify_intent_simple(self, text: str) -> str:
        """
        Simple classification returning string values as specified
        
        Args:
            text: User input string
            
        Returns:
            String: "GREET", "INQUIRY", or "HIGH_INTENT"
        """
        intent_type = self.classify_intent(text)
        return intent_type.value
