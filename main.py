import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.core.response_synthesizers.type import ResponseMode
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding


load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("请设置 GEMINI_API_KEY 环境变量")

# 将配置应用到全局 Settings
llm = GoogleGenAI(model="gemini-2.5-flash")
embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001")
Settings.llm = llm
Settings.embed_model = embed_model


documents = SimpleDirectoryReader(input_files=["./data/test.txt"]).load_data()
print(f"成功加载 {len(documents)} 份文档.")


# 1. 准备长内容文档
long_texts = [
    "Apple Inc., an American tech giant...",
    "Based in Redmond, Washington, Microsoft Corporation...",
    "Y Combinator (YC) is a highly influential American startup accelerator...",
]
documents = documents + ([Document(text=t) for t in long_texts])


index = VectorStoreIndex.from_documents(documents)
# 4. 创建查询引擎 (Query Engine) - 这是关键改动
query_engine = index.as_query_engine(ResponseMode=ResponseMode.NO_TEXT)

# 5. 进行查询
print("\n" + "=" * 50)

query_text_1 = "Y Combinator 是什么"
response_1 = query_engine.query(query_text_1)

# response_1.response 将会是空的 (或提示性的 None)
# 我们需要从 response_1.source_nodes 中获取信息
print(f"\n--- 对于问题 '{query_text_1}' 的原始相关文本块 ---")

if not response_1.source_nodes:
    print("没有找到相关的文本块。")
else:
    for i, node_with_score in enumerate(response_1.source_nodes):
        print(f"\n--- 相关文本块 {i+1} (相似度得分: {node_with_score.score:.4f}) ---")
        print(node_with_score.get_text())
        print(f"来源: {node_with_score.node.metadata}")

print("\n" + "=" * 50)
print("Demo 运行结束.")
