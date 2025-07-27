from datetime import datetime
from typing import List
from ActionExecutor import ConversationContext, DialogueEvent
from DataModels import get_utc_now


class ContextEngine:
    def __init__(self, archive_db_client, context_db_client):
        self.archive_db = archive_db_client
        self.context_db = context_db_client

    # --- 对应流程 步骤 1 ---
    def load_or_create_context(self, session_id: str) -> ConversationContext:
        """从数据库加载上下文，如果不存在则创建一个新的。"""
        context_data = self.context_db.find_one({"session_id": session_id})
        if context_data:
            return ConversationContext(**context_data)
        else:
            return ConversationContext(session_id=session_id)

    # --- 对应流程 步骤 2 ---
    def update_context_with_new_data(self, context: ConversationContext, new_events: List[DialogueEvent]) -> ConversationContext:
        """
        用新事件和历史记录，对上下文进行系统级更新 (象限一、二)。
        """
        # 更新象限二
        context.q2_recent_events.extend(new_events)
        # (这里可以加入截断逻辑，比如只保留最近50条)

        # 更新象限一
        # (这里可以加入总结逻辑，比如当事件超过一定数量时触发)
        context.q1_summary = self._summarize(context.q2_recent_events)
        
        return context

    # --- 对应流程 步骤 10 ---
    def save_context(self, context: ConversationContext):
        """将修改后的完整上下文对象持久化保存。"""
        context.last_updated = get_utc_now()
        self.context_db.replace_one(
            {"session_id": context.session_id},
            context.model_dump(),
            upsert=True # 如果不存在则创建
        )
        print(f"Context Saved for session: {context.session_id}")
    
    # 私有辅助方法
    def _summarize(self, events: List[DialogueEvent]) -> str: ...