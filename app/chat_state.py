import os
from typing import Sequence
from datetime import datetime, timezone

from typing_extensions import TypedDict
from langchain_core.messages import trim_messages, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.mongodb import MongoDBSaver

from .db import client, DB_NAME, MONGO_URI


# Environment variables (consider using .env for security)
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "api_key"
os.environ["GOOGLE_API_KEY"] = "api_key"

# Initialize chat model
model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai"
)

# Initialize message trimmer
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant. Answer all questions politely."),
    MessagesPlaceholder(variable_name="messages"),
])

# Chat state schema
class ChatState(TypedDict):
    messages: Sequence[BaseMessage]
    language: str
    user_id: str
    thread_id: str
    last_updated: str

# Workflow setup
workflow = StateGraph(state_schema=ChatState)


def call_model(state: ChatState) -> ChatState:
    print(f"Message before trimming: {len(state['messages'])}")
    trimmed_messages = trimmer.invoke(state["messages"])
    print(f"Message after trimming: {len(trimmed_messages)}")
    for msg in trimmed_messages:
        print(f"  {type(msg).__name__}: {msg.content}")

    prompt = prompt_template.invoke({
        "messages": trimmed_messages
    })
    response = model.invoke(prompt)

    return {
        "messages": state["messages"] + [response],
        "language": state["language"],
        "user_id": state["user_id"],
        "thread_id": state["thread_id"],
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }


# Register workflow nodes & edges
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# MongoDB memory
memory = MongoDBSaver(
    connection_string=MONGO_URI,
    db_name=DB_NAME,
    collection_name="chat_state",
    client=client
)

# Compile workflow with persistence
app_workflow = workflow.compile(checkpointer=memory)
