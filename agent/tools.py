"""
Tools module for AutoStream Agent
Provides various tools for social media management, lead generation, and content creation
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Base class for all tools"""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get tool description"""
        pass

class LeadGenerationTool(BaseTool):
    """Tool for generating and managing sales leads"""
    
    def execute(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate leads based on specified criteria
        
        Args:
            criteria: Dictionary containing lead generation criteria
            
        Returns:
            Dictionary containing generated leads
        """
        leads = []
        
        # Mock lead generation logic
        for i in range(5):  # Generate 5 mock leads
            lead = {
                "id": f"lead_{i+1}",
                "name": f"Prospect {i+1}",
                "company": f"Company {chr(65+i)}",
                "email": f"prospect{i+1}@company{i+1}.com",
                "phone": f"+1-555-010{i:02d}",
                "industry": criteria.get("industry", "Technology"),
                "source": "AutoStream Agent",
                "created_at": datetime.now().isoformat(),
                "score": 0.8 + (i * 0.02)
            }
            leads.append(lead)
        
        return {
            "status": "success",
            "leads": leads,
            "total_count": len(leads),
            "criteria_used": criteria
        }
    
    def get_description(self) -> str:
        return "Generate sales leads based on specified criteria like industry, company size, location, etc."

class ContentCreationTool(BaseTool):
    """Tool for creating social media content"""
    
    def execute(self, content_type: str, topic: str, platform: str, **kwargs) -> Dict[str, Any]:
        """
        Create content for social media platforms
        
        Args:
            content_type: Type of content (post, article, tweet, etc.)
            topic: Content topic
            platform: Target social media platform
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing generated content
        """
        content_templates = {
            "twitter": {
                "max_length": 280,
                "template": f"🚀 Excited to share insights on {topic}! {self._generate_hashtags(topic)} #innovation"
            },
            "linkedin": {
                "max_length": 1300,
                "template": f"📈 Professional insights on {topic}\n\nIn today's rapidly evolving landscape, {topic} continues to transform how we approach business challenges. Here are my key takeaways:\n\n• Point 1: Strategic importance\n• Point 2: Implementation strategies\n• Point 3: Future outlook\n\nWhat are your thoughts on {topic}? Share in the comments below!\n\n{self._generate_hashtags(topic)}\n\n#ProfessionalDevelopment #BusinessStrategy"
            },
            "facebook": {
                "max_length": 63206,
                "template": f"🌟 Great news! We're diving deep into {topic} and wanted to share some exciting developments. This topic has been gaining tremendous traction, and for good reason!\n\n{self._generate_content_body(topic)}\n\nWhat's your experience with {topic}? Let us know in the comments! 👇\n\n{self._generate_hashtags(topic)}"
            }
        }
        
        template = content_templates.get(platform.lower(), content_templates["linkedin"])
        content = template["template"]
        
        return {
            "status": "success",
            "content": content,
            "content_type": content_type,
            "platform": platform,
            "topic": topic,
            "character_count": len(content),
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_hashtags(self, topic: str) -> str:
        """Generate relevant hashtags for a topic"""
        hashtags = [f"#{topic.replace(' ', '').replace(',', '')}"]
        if "business" in topic.lower():
            hashtags.append("#Business")
        if "technology" in topic.lower():
            hashtags.append("#Tech")
        if "marketing" in topic.lower():
            hashtags.append("#Marketing")
        return " ".join(hashtags[:3])
    
    def _generate_content_body(self, topic: str) -> str:
        """Generate content body for longer posts"""
        return f"""
        The impact of {topic} cannot be overstated. As we navigate through this digital transformation, organizations that embrace these changes are seeing remarkable results.

        Key benefits include:
        ✅ Increased efficiency
        ✅ Better engagement
        ✅ Improved ROI
        ✅ Enhanced customer experience

        Stay tuned for more updates on how {topic} is reshaping our industry!
        """
    
    def get_description(self) -> str:
        return "Create engaging social media content for various platforms including Twitter, LinkedIn, and Facebook"

class SocialMediaManagementTool(BaseTool):
    """Tool for managing social media operations"""
    
    def execute(self, action: str, platform: str, **kwargs) -> Dict[str, Any]:
        """
        Execute social media management actions
        
        Args:
            action: Action to perform (schedule, post, analyze, etc.)
            platform: Social media platform
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing action results
        """
        if action == "schedule":
            return self._schedule_post(platform, **kwargs)
        elif action == "analyze":
            return self._analyze_performance(platform, **kwargs)
        elif action == "post":
            return self._create_post(platform, **kwargs)
        else:
            return {"status": "error", "message": f"Unsupported action: {action}"}
    
    def _schedule_post(self, platform: str, **kwargs) -> Dict[str, Any]:
        """Schedule a social media post"""
        scheduled_time = kwargs.get("scheduled_time", datetime.now().isoformat())
        content = kwargs.get("content", "Default scheduled content")
        
        return {
            "status": "success",
            "action": "schedule",
            "platform": platform,
            "scheduled_time": scheduled_time,
            "content": content,
            "post_id": f"post_{datetime.now().timestamp()}"
        }
    
    def _analyze_performance(self, platform: str, **kwargs) -> Dict[str, Any]:
        """Analyze social media performance"""
        metrics = {
            "engagement_rate": 0.058,
            "reach": 12500,
            "impressions": 45000,
            "likes": 725,
            "comments": 89,
            "shares": 34,
            "clicks": 156
        }
        
        return {
            "status": "success",
            "action": "analyze",
            "platform": platform,
            "metrics": metrics,
            "period": kwargs.get("period", "last_30_days"),
            "analysis_date": datetime.now().isoformat()
        }
    
    def _create_post(self, platform: str, **kwargs) -> Dict[str, Any]:
        """Create and publish a social media post"""
        content = kwargs.get("content", "Default post content")
        
        return {
            "status": "success",
            "action": "post",
            "platform": platform,
            "content": content,
            "post_id": f"post_{datetime.now().timestamp()}",
            "published_at": datetime.now().isoformat(),
            "url": f"https://{platform}.com/posts/{datetime.now().timestamp()}"
        }
    
    def get_description(self) -> str:
        return "Manage social media operations including scheduling posts, analyzing performance, and publishing content"

class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self.tools = {
            "lead_generation": LeadGenerationTool(),
            "content_creation": ContentCreationTool(),
            "social_media_management": SocialMediaManagementTool()
        }
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools and their descriptions"""
        return {name: tool.get_description() for name, tool in self.tools.items()}
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool with given parameters"""
        tool = self.get_tool(tool_name)
        if not tool:
            return {"status": "error", "message": f"Tool '{tool_name}' not found"}
        
        return tool.execute(**kwargs)
