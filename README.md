# AutoStream Agent

A sophisticated agentic workflow system that transforms social media interactions into qualified sales leads. This project demonstrates advanced AI agent capabilities including intent recognition, knowledge retrieval, tool execution, and automated response generation.

## 🎯 Overview

AutoStream Agent is designed to help businesses automate their social media to lead generation pipeline. It can:
- Classify user intent from social media interactions
- Generate qualified sales leads based on specific criteria
- Create engaging social media content
- Analyze social media performance metrics
- Manage social media operations automatically

## 🏗️ Project Structure

```
autostream-agent/
│── app.py                          # Main application entry point
│── knowledge_base/
│   └── autostream_data.json         # Knowledge base for RAG operations
│── agent/
│   ├── intent.py                    # Intent classification module
│   ├── rag.py                       # Retrieval-Augmented Generation
│   ├── tools.py                     # Tool execution framework
│   └── graph.py                     # Workflow orchestration
│── requirements.txt                 # Python dependencies
│── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autostream-agent
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

### How to Run the Project Locally

1. **Navigate to the project directory**
   ```bash
   cd autostream-agent
   ```

2. **Set up the environment**
   - Create virtual environment: `python -m venv venv`
   - Activate environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
   - Install dependencies: `pip install -r requirements.txt`

3. **Start the agent**
   ```bash
   python app.py
   ```

4. **Interactive Mode**
   The agent will start in interactive mode. You can:
   - Type your questions directly
   - Use commands like `help`, `capabilities`, `history`, `clear`
   - Type `exit` to quit

5. **Testing**
   Run test scripts to verify functionality:
   ```bash
   python test_intent.py          # Test intent classification
   python test_rag.py             # Test RAG pipeline
   python test_lead_qualification.py  # Test lead qualification flow
   ```

## 🏗️ Architecture Explanation

**Why LangGraph for State Management**

I chose LangGraph for its robust state management capabilities in conversational AI workflows. Unlike traditional chatbot frameworks, LangGraph provides persistent state across conversation turns, which is critical for lead qualification. The WorkflowState class maintains conversation history, detected intent, and lead information (name, email, platform) throughout multi-turn interactions. This ensures the agent remembers context and can guide users through the complete lead qualification sequence without losing information.

**State Management Architecture**

The system uses a centralized state management approach where WorkflowState serves as the single source of truth. Each conversation turn updates the state with new information while preserving previous context. The state includes: conversation history (for context awareness), current intent (for routing), qualification stage (for lead flow tracking), and captured lead data. This architecture enables seamless transitions between greeting, inquiry, and lead qualification phases while maintaining data consistency across the entire conversation lifecycle.

## 📱 WhatsApp Deployment Integration

**WhatsApp Webhook Integration Strategy**

To deploy this agent on WhatsApp, I would implement a webhook-based architecture using the WhatsApp Business API. The integration would involve:

1. **Webhook Endpoint**: Create a FastAPI endpoint that receives WhatsApp webhook events for incoming messages
2. **Message Processing**: Parse WhatsApp message format and extract text content for intent classification
3. **State Management**: Use Redis or database to maintain conversation state per WhatsApp user phone number
4. **Response Delivery**: Send agent responses back through WhatsApp Business API message endpoints
5. **Media Handling**: Support for WhatsApp media types (images, documents) in the knowledge base

The webhook would handle WhatsApp's specific message format while maintaining the same core agent logic. Each WhatsApp user would have a unique session ID based on their phone number, ensuring proper state isolation. The system would also need to handle WhatsApp's message delivery confirmations and rate limiting requirements.
## 🧠 Core Components

### 1. Intent Classification (`agent/intent.py`)
- **Purpose**: Classify user input into specific intents
- **Supported Intents**:
  - `lead_generation`: Generate sales leads
  - `content_creation`: Create social media content
  - `social_media_management`: Manage social media operations
  - `analytics`: Analyze performance metrics
  - `general_query`: Handle general inquiries

### 2. Retrieval-Augmented Generation (`agent/rag.py`)
- **Purpose**: Enhance responses with knowledge base information
- **Features**:
  - Knowledge base management
  - Context retrieval based on queries
  - Relevance scoring for retrieved information

### 3. Tool Execution (`agent/tools.py`)
- **Purpose**: Execute specific business operations
- **Available Tools**:
  - `LeadGenerationTool`: Generate qualified leads
  - `ContentCreationTool`: Create platform-specific content
  - `SocialMediaManagementTool`: Manage social media operations

### 4. Workflow Orchestration (`agent/graph.py`)
- **Purpose**: Coordinate the entire agent workflow
- **Workflow Stages**:
  1. Start → Intent Classification
  2. Intent Classification → Knowledge Retrieval
  3. Knowledge Retrieval → Tool Execution
  4. Tool Execution → Response Generation
  5. Response Generation → End

## 🔧 Configuration

### Knowledge Base
The knowledge base is stored in `knowledge_base/autostream_data.json`. You can customize this file with:
- Industry-specific information
- Company profiles
- Content templates
- Performance benchmarks

### Testing

Run the test suite:
```bash
pytest tests/
```
## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- **Multi-language Support**: Extend intent classification to support multiple languages
- **Advanced Analytics**: Implement machine learning models for predictive analytics
- **Real-time Integration**: Add real-time social media monitoring
- **CRM Integration**: Connect with popular CRM systems
- **AI-powered Content**: Integrate with advanced language models for content generation
- **Web Dashboard**: Build a web-based interface for monitoring and management

## 📞 Support

For questions, issues, or feature requests, please:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

## 🙏 Acknowledgments

This project demonstrates advanced agentic AI capabilities and serves as a reference implementation for social media to lead generation automation.

---

**AutoStream Agent** - Transforming social media interactions into business opportunities. 🚀
