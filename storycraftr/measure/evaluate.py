import json
import logging

from openai import APIError
from rich.console import Console
from rouge_score import rouge_scorer

from storycraftr.agent.agents import initialize_openai_client
from storycraftr.state import debug_state
from storycraftr.utils.core import load_book_config


console = Console()


def extract_json_from_text(text):
    """
    Extract JSON from text that may contain explanatory wrapping.
    Looks for JSON blocks in various formats.
    """
    import re

    # Try to find JSON in code blocks first
    json_block_pattern = r"```(?:json)?\s*(\{.*?\})\s*```"
    match = re.search(json_block_pattern, text, re.DOTALL)
    if match:
        return match.group(1)

    # Try to find standalone JSON objects
    json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return match.group(0)

    # If no JSON found, return the original text
    return text


def score_structured_output(reference_text, generated_text):
    """
    Score structured output (JSON) by checking validity and field accuracy.
    Returns scores similar to ROUGE format for consistency.
    """
    try:
        reference_json = json.loads(reference_text)

        # Extract JSON from potentially wrapped text
        extracted_json = extract_json_from_text(generated_text)
        generated_json = json.loads(extracted_json)

    except json.JSONDecodeError:
        # Invalid JSON gets zero score
        return {
            "rouge1": 0.0,
            "rouge2": 0.0,
            "rougeL": 0.0,
        }

    # Check field presence and accuracy
    total_fields = len(reference_json)
    correct_fields = 0
    exact_matches = 0

    for key, ref_value in reference_json.items():
        if key in generated_json:
            correct_fields += 1
            if (
                str(generated_json[key]).lower().strip()
                == str(ref_value).lower().strip()
            ):
                exact_matches += 1

    # Convert to ROUGE-like scores for consistency
    field_accuracy = correct_fields / total_fields if total_fields > 0 else 0.0
    value_accuracy = exact_matches / total_fields if total_fields > 0 else 0.0

    return {
        "rouge1": field_accuracy,  # Field presence score
        "rouge2": value_accuracy,  # Exact value match score
        "rougeL": (field_accuracy + value_accuracy) / 2,  # Combined score
    }


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

    # Check if this is a structured output benchmark
    if benchmark.get("type") == "structured":
        if debug_state.is_debug():
            console.print(f"[yellow]DEBUG - Generated text: {generated_text}[/yellow]")
            console.print(f"[yellow]DEBUG - Reference text: {reference_text}[/yellow]")
        scores = score_structured_output(reference_text, generated_text)
    else:
        scorer = rouge_scorer.RougeScorer(
            ["rouge1", "rouge2", "rougeL"], use_stemmer=True
        )
        rouge_scores = scorer.score(reference_text, generated_text)
        scores = {
            "rouge1": rouge_scores["rouge1"].fmeasure,
            "rouge2": rouge_scores["rouge2"].fmeasure,
            "rougeL": rouge_scores["rougeL"].fmeasure,
        }

    return {
        "benchmark_id": benchmark.get("id", "unknown"),
        "benchmark_name": benchmark.get("name", "Unknown Benchmark"),
        "scores": scores,
    }
