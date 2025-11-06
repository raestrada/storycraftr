from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)


def _format_context(documents: List[Document]) -> str:
    if not documents:
        return ""
    snippets = []
    for doc in documents:
        source = doc.metadata.get("source", "context")
        text = doc.page_content.strip()
        snippets.append(f"Source: {source}\n{text}")
    return "\n\n".join(snippets)


def build_assistant_graph(assistant):
    """Create a LangChain runnable graph for the assistant."""

    if not assistant.retriever:
        raise RuntimeError("Assistant retriever is not initialised.")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("human", "{question}"),
        ]
    )

    prompt_chain = prompt | assistant.llm | StrOutputParser()

    def ensure_inputs(payload):
        if isinstance(payload, str):
            payload = {"question": payload}
        elif not isinstance(payload, dict):
            raise ValueError("Graph input must be a question string or a dict payload.")

        question = payload.get("question")
        if not question:
            raise ValueError("Missing 'question' in graph payload.")

        documents = payload.get("documents")
        if not documents:
            documents = assistant.retriever.invoke(question)

        if not isinstance(documents, list):
            documents = [documents]

        payload["question"] = question
        payload["documents"] = documents
        return payload

    def prepare_prompt_inputs(payload):
        documents = payload["documents"]
        context = _format_context(documents)
        system_prompt = assistant.system_prompt
        if context:
            system_prompt = f"{system_prompt}\n\nContext:\n{context}"
        return {
            "prompt_inputs": {
                "system_prompt": system_prompt,
                "question": payload["question"],
            },
            "documents": documents,
        }

    graph = (
        RunnablePassthrough()
        | RunnableLambda(ensure_inputs)
        | RunnableLambda(prepare_prompt_inputs)
        | RunnableParallel(
            answer=RunnableLambda(lambda x: x["prompt_inputs"]) | prompt_chain,
            documents=RunnableLambda(lambda x: x["documents"]),
        )
    )

    return graph
