from llama_index.core import SimpleDirectoryReader
from datasets import load_dataset
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate
import gradio as gr
input_dir_path = "./dataset"
dataset = load_dataset("zigistry/zigistry-complete-dataset", split="train")
df = dataset.to_pandas()
df.to_csv("./dataset/zigistry.csv", index=False)
loader = SimpleDirectoryReader(
    input_dir=input_dir_path, required_exts=[".csv"], recursive=True
)
docs = loader.load_data()
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5", trust_remote_code=True
)
Settings.embed_model = embed_model
index = VectorStoreIndex.from_documents(docs)
llm = HuggingFaceLLM(model_name="unsloth/Llama-3.2-1B-Instruct")
Settings.llm = llm
query_engine = index.as_query_engine(streaming=True, similarity_top_k=4)
qa_prompt_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
    "Query: {query_str}\n"
    "Answer: "
)

qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})


def respond(query: str) -> str:
    """Respond to the query"""
    response = query_engine.query(query)
    return str(response)

def chat_interface(query):
    return respond(query)

iface = gr.Interface(
    fn=chat_interface,
    inputs="text",
    outputs="text",
    title="Chat Interface",
    allow_flagging="never",
    description="A basic chat interface using Gradio.",
)

if __name__ == "__main__":
    iface.launch()