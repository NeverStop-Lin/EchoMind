from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone 
import uuid

# Helper function to get timezone-aware UTC now
def get_utc_now() -> datetime:
    """Returns the current time as a timezone-aware datetime object in UTC."""
    return datetime.now(timezone.utc)

# 1. 对话档案馆中的基础事件单元
class DialogueEvent(BaseModel):
    """对话档案馆中的一个原子事件"""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str # 标识属于哪一次对话
    timestamp: datetime = Field(default_factory=get_utc_now())
    emitter: Literal["USER", "AI", "SYSTEM"] # 事件发出者
    payload: Dict[str, Any] # 事件内容, e.g., {"message": "你好"} or {"query": "..."}

# 2. 事实库中的事实单元
class Fact(BaseModel):
    """AI提炼出的结构化事实"""
    fact_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str # 事实的核心内容
    source_event_ids: List[str] = [] # 追溯事实来源
    metadata: Dict[str, Any] = {} # 用于过滤和检索, e.g., {"topic": "hotel_preference"}

# 3. 精选回忆库中的单元
class CuratedMemory(BaseModel):
    """AI决定要深刻记住的原始对话片段"""
    memory_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str # 原始的、未经修改的对话片段
    source_event_ids: List[str] # 追溯来源
    importance_score: float = 1.0 # 重要性评分，用于未来排序

# 4. 核心的、可被持久化的上下文对象
class ConversationContext(BaseModel):
    """独立的、可持久化的上下文对象，包含AI的四象限记忆"""
    session_id: str
    last_updated: datetime = Field(default_factory=get_utc_now())

    # 象限一: 历史的压缩信息
    q1_summary: str = "对话刚刚开始。"

    # 象限二: 最近的完整信息
    q2_recent_events: List[DialogueEvent] = []

    # 象限三: 事实信息
    q3_facts: List[Fact] = []

    # 象限四: 回忆记忆
    q4_curated_memories: List[CuratedMemory] = []

# 5. AI决策的输出格式：行动计划
class Action(BaseModel):
    action_type: Literal["RESPOND_TO_USER", "UPDATE_FACTS", "ADD_CURATED_MEMORY", "QUERY_RECALL"]
    payload: Dict[str, Any]

class ActionPlan(BaseModel):
    reasoning: str # AI的思考过程，用于调试
    actions: List[Action]