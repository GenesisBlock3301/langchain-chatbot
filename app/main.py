from fastapi import FastAPI
from .schemas import MessageRequest, MessageResponse
from .chat_state import app_workflow
from datetime import datetime, timezone
from .db import threads_collection, chats_collection
from langchain_core.messages import BaseMessage

app = FastAPI(title="LangGraph Chat App")


def _msg_to_dict(role: str, content: str) -> dict:
    """Normalize a message for Mongo storage"""
    return {
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _normalize_msg(msg) -> dict:
    """
    Convert either a dict-based message or a LangChain BaseMessage into a
    consistent dict shape: {role, content, timestamp}.
    """
    if isinstance(msg, dict):
        return {
            "role": msg.get("role"),
            "content": msg.get("content"),
            "timestamp": msg.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        }
    if isinstance(msg, BaseMessage):
        # LangChain messages expose role via `.type` and text via `.content`
        return {
            "role": getattr(msg, "type", None) or "ai",
            "content": getattr(msg, "content", ""),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    # Fallback to stringifying unknown types
    return {
        "role": "unknown",
        "content": str(msg),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/chat/", response_model=MessageResponse)
async def chat(req: MessageRequest):
    # 1. Ensure a thread exists (upsert thread metadata only)
    threads_collection.update_one(
        {"thread_id": req.thread_id},
        {
            "$set": {
                "thread_id": req.thread_id,
                "user_id": req.user_id,
                "language": "english",
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }
        },
        upsert=True,
    )

    # 2. Insert a new user message
    user_msg = _msg_to_dict("user", req.text)
    chats_collection.insert_one(
        {**user_msg, "thread_id": req.thread_id}
    )

    # 3. Collect last N messages for context (e.g., last 20)
    recent_msgs = list(
        chats_collection.find({"thread_id": req.thread_id})
        .sort("timestamp", -1)
        .limit(20)
    )
    recent_msgs.reverse()  # oldest first

    # 4. Run workflow with state
    state = {
        "thread_id": req.thread_id,
        "user_id": req.user_id,
        "language": "english",
        "messages": [
            {"role": m["role"], "content": m["content"], "timestamp": m["timestamp"]}
            for m in recent_msgs
        ],
    }

    output = app_workflow.invoke(
        state, config={"configurable": {"thread_id": req.thread_id}}
    )

    # 5. Save assistant messages from output (if any new ones exist)
    normalized_output_messages = [
        _normalize_msg(m) for m in output.get("messages", [])
    ]
    for msg in normalized_output_messages:
        if msg["role"] == "ai":
            chats_collection.insert_one(
                {
                    "thread_id": req.thread_id,
                    "role": "ai",
                    "content": msg["content"],
                    "timestamp": msg["timestamp"],
                }
            )

    # 6. Update thread last_updated
    threads_collection.update_one(
        {"thread_id": req.thread_id},
        {"$set": {"last_updated": datetime.now(timezone.utc).isoformat()}},
    )

    # 7. Return messages (last 20 for frontend)
    # Prefer the normalized workflow output if present; otherwise fall back to state
    return {
        "messages": normalized_output_messages[-20:] if normalized_output_messages else state["messages"],
        "language": state.get("language", "english"),
    }
