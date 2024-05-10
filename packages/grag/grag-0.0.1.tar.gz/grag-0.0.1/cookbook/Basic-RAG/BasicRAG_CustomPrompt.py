"""Custom Prompts
====================
This cookbook demonstrates how to use custom prompts with Basic RAG.


`Note that this cookbook assumes that you already have the` ``Llama-2-13b-chat`` `LLM ready,`
`for more details on how to quantize and run an LLM locally,`
`refer to the LLM section under Getting Started.`

`Note that this cookbook also assumes that you have already ingested documents into a DeepLake collection called 'grag'`
`for more details on how to ingest documents refer to the cookbook called` ``Document Ingestion``.
"""

from grag.components.prompt import Prompt

custom_prompt = Prompt(
    input_keys={"context", "question"},
    template="""Answer the following question based on the given context.
    question: {question}
    context: {context}
    answer: 
    """,
)

print(custom_prompt)
# client = DeepLakeClient(collection_name="grag")
# retriever = Retriever(vectordb=client)
# rag = BasicRAG(
#     model_name="Llama-2-13b-chat", custom_prompt=custom_prompt, retriever=retriever
# )
# 
# if __name__ == "__main__":
#     while True:
#         query = input("Query:")
#         rag(query)
