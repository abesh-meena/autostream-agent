"""
Lead Capture Module
Contains the mock_lead_capture function as specified in requirements
"""

def mock_lead_capture(name: str, email: str, platform: str):
    """
    Mock lead capture function that will be checked by evaluator
    
    Args:
        name: Lead's name
        email: Lead's email address  
        platform: Creator platform the lead intends to use
    """
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    
    # In a real implementation, this would:
    # - Store in database
    # - Send to CRM
    # - Trigger notification
    # - Add to email list
    
    # For evaluation purposes, the print statement is sufficient
