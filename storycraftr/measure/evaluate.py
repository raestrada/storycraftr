import logging

from openai import APIError
from rich.console import Console
from rouge_score import rouge_scorer

from storycraftr.agent.agents import initialize_openai_client
from storycraftr.state import debug_state
from storycraftr.utils.core import load_book_config


console = Console()


def run_benchmark(book_path, benchmark):
    """
    Runs a single performance benchmark by generating text and comparing to a reference.
    """
    # Suppress verbose logging from the OpenAI client during benchmarks
    logging.getLogger("openai").setLevel(logging.WARNING)

    client = initialize_openai_client(book_path)
    config = load_book_config(book_path)
    model = getattr(config, "openai_model", "gpt-4o")

    prompt = benchmark.get("prompt")
    reference_text = benchmark.get("reference_text")

    if not prompt or not reference_text:
        return {
            "benchmark_id": benchmark.get("id", "unknown"),
            "benchmark_name": benchmark.get("name", "Unknown Benchmark"),
            "scores": {},
        }

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        generated_text = completion.choices[0].message.content
    except APIError as e:
        console.print(
            f"[bold red]API Error on benchmark '{benchmark.get('name')}': {e}[/bold red]"
        )
        return {
            "benchmark_id": benchmark.get("id", "unknown"),
            "benchmark_name": benchmark.get("name", "Unknown Benchmark"),
            "scores": {},
            "error": str(e),
        }

    if isinstance(generated_text, list):
        # The model might be returning a structured response (e.g., with reasoning).
        # We will attempt to extract text from the structure.
        text_parts = []
        for part in generated_text:
            if isinstance(part, str):
                text_parts.append(part)
            elif (
                isinstance(part, dict)
                and "text" in part
                and isinstance(part["text"], str)
            ):
                text_parts.append(part["text"])
        generated_text = "\n".join(text_parts)

    if not isinstance(generated_text, str):
        error_message = (
            f"Unexpected response type from API: {type(generated_text)}. "
            f"Expected a string. Content: {generated_text}"
        )
        if debug_state.is_debug():
            console.print(f"[red]DEBUG: {error_message}[/red]")
        raise TypeError(error_message)

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference_text, generated_text)

    return {
        "benchmark_id": benchmark.get("id", "unknown"),
        "benchmark_name": benchmark.get("name", "Unknown Benchmark"),
        "scores": {
            "rouge1": scores["rouge1"].fmeasure,
            "rouge2": scores["rouge2"].fmeasure,
            "rougeL": scores["rougeL"].fmeasure,
        },
    }
