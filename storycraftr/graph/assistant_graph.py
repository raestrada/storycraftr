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

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_prompt}"),
            ("human", "{question}"),
        ]
    )

    def retrieve(question: str):
        return assistant.retriever.invoke(question)

    def prepare_inputs(inputs):
        question = inputs["question"]
        documents = inputs.get("documents") or []
        if not isinstance(documents, list):
            documents = [documents]
        context = _format_context(documents)
        system_prompt = assistant.system_prompt
        if context:
            system_prompt = f"{system_prompt}\n\nContext:\n{context}"
        return {
            "system_prompt": system_prompt,
            "question": question,
        }

    graph = (
        RunnableParallel(
            question=RunnablePassthrough(),
            documents=RunnableLambda(retrieve),
        )
        | RunnableLambda(prepare_inputs)
        | prompt
        | assistant.llm
        | StrOutputParser()
    )

    return graph
