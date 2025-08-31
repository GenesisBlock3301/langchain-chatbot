# FastAPI Chatbot with MongoDB and LangGraph

A professional-grade conversational AI chatbot built with FastAPI, MongoDB, and LangGraph, featuring persistent conversation history and real-time message streaming.

## 🚀 Features

- **Conversational Memory**: Persistent chat history stored in MongoDB
- **Multi-user Support**: Separate conversation threads for different users
- **Real-time Streaming**: Token-by-token response streaming for better UX
- **Professional Architecture**: Clean separation of concerns with modular design
- **RESTful API**: FastAPI-powered endpoints for easy integration
- **State Management**: Custom state handling with LangGraph
- **Database Integration**: MongoDB for scalable conversation persistence

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB instance (local or cloud)
- API keys for your chosen LLM provider

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd <your-project-name>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=chatbot_db
   COLLECTION_NAME=conversations
   LLM_API_KEY=your_llm_api_key_here
   ```

5. **Start MongoDB**
   - For local MongoDB: Ensure MongoDB service is running
   - For MongoDB Atlas: Use your connection string in MONGODB_URL

## 🏃‍♂️ Running the Application

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Main Endpoints

#### Start/Continue Conversation
```http
POST /chat
Content-Type: application/json
{
  "user_id": "3",
  "thread_id": "thread_3",
  "text": "who am I"
}
```


#### Get Conversation History
```http
GET /conversation/{thread_id}
```

#### Delete Conversation
```http
DELETE /conversation/{thread_id}
```

## 🏗️ Project Structure

```
langchain-chatbot/
├── app/                    # All application code
│   ├── main.py             # FastAPI application and route handlers
│   ├── db.py               # MongoDB configuration and connection
│   ├── chatstate.py        # Custom state management and LangGraph setup
│   └── __init__.py         # Makes it a Python package
├── tests/                  # Unit and integration tests
│   └── test_main.py
├── requirements.txt        # Python dependencies (outside app folder)
├── .env                    # Environment variables (outside app folder)
└── README.md 
```

### File Descriptions

- **`main.py`**: Contains the FastAPI application, route definitions, and business logic for handling chat requests
- **`db.py`**: Database configuration, MongoDB connection setup, and database utility functions
- **`chatstate.py`**: Custom state schema definition, LangGraph workflow configuration, and model integration
- **`requirements.txt`**: All Python package dependencies needed for the project

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name for storing conversations | `chatbot_db` |
| `COLLECTION_NAME` | Collection name for conversation documents | `conversations` |
| `LLM_API_KEY` | API key for your LLM provider | Required |

### MongoDB Setup

The application automatically creates the necessary database and collections. Ensure your MongoDB instance is accessible and the user has read/write permissions.


## 📊 Features in Detail

### Conversation Memory
- Persistent storage of all chat interactions
- Thread-based conversation isolation
- Automatic message history trimming to manage a context window

### State Management
- Custom state schema with message history and metadata
- LangGraph-powered conversation flow
- Efficient state persistence and retrieval


### Common Issues

1. **MongoDB Connection Error**
   - Verify MongoDB is running
   - Check connection string in `.env`
   - Ensure network connectivity

2. **LLM API Rate Limits**
   - Verify API key is correct
   - Check your API provider's rate limits
   - Implement retry logic if needed

3. **Memory Issues with Long Conversations**
   - Adjust message trimming parameters in `chatstate.py`
   - Monitor token usage in long conversations

## 🔒 Security Considerations

- Store API keys securely in environment variables
- Implement proper authentication for production use
- Sanitize user inputs before processing
- Set up proper CORS policies for web clients
- Use HTTPS in production environments

## 🚀 Deployment

### Production Deployment Checklist

- [ ] Set up production MongoDB instance
- [ ] Configure environment variables securely
- [ ] Set up reverse proxy (nginx/Apache)
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure logging and monitoring
- [ ] Set up automated backups for MongoDB
- [ ] Implement rate limiting
- [ ] Set up health checks



## 🔗 Related Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MongoDB Documentation](https://docs.mongodb.com/)

---

Built with ❤️ using FastAPI, LangGraph, and MongoDB