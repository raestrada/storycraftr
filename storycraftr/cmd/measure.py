import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from storycraftr.utils.core import verify_book_path
from storycraftr.measure.benchmarks import BENCHMARKS
from storycraftr.measure.evaluate import run_benchmark
from storycraftr.measure.golden import load_golden_scores, save_golden_scores
from storycraftr.utils.core import load_book_config


def average_benchmark_results(benchmark_runs):
    """
    Average the scores from multiple benchmark runs.
    """
    if not benchmark_runs:
        return {}

    # Use the first result as template
    averaged_result = {
        "benchmark_id": benchmark_runs[0]["benchmark_id"],
        "benchmark_name": benchmark_runs[0]["benchmark_name"],
        "scores": {},
    }

    # Average each score metric
    score_keys = benchmark_runs[0].get("scores", {}).keys()
    for key in score_keys:
        scores = [
            run["scores"][key]
            for run in benchmark_runs
            if run.get("scores", {}).get(key) is not None
        ]
        if scores:
            averaged_result["scores"][key] = sum(scores) / len(scores)

    return averaged_result


@click.command()
@click.option(
    "--book-path",
    default=None,
    help="The path to the book project. Optional.",
)
@click.option(
    "--update-golden-standards",
    is_flag=True,
    help="Update the golden standard scores with the results from the current model.",
)
@click.option(
    "--runs",
    default=3,
    type=int,
    help="Number of runs to average for each benchmark (default: 3).",
)
def measure(book_path: str, update_golden_standards: bool, runs: int):
    """
    Measure the performance of the configured LLM against golden standards.

    Environment Variables:
      OPENAI_API_KEY    OpenAI API key (can also be in ~/.storycraftr/openai_api_key.txt)
      OPENAI_API_URL    OpenAI API base URL (default: https://api.openai.com/v1)
      OPENAI_MODEL      OpenAI model name (default: gpt-4o)
    """
    console = Console()
    verified_book_path = None
    if book_path:
        try:
            verified_book_path = verify_book_path(book_path)
        except click.ClickException as e:
            console.print(f"[red]{e.message}[/red]")
            return
    else:
        console.print(
            "[yellow]No book path provided. Using default LLM configuration.[/yellow]"
        )

    config = load_book_config(verified_book_path)
    model_name = getattr(config, "openai_model", "gpt-4o")
    api_base_url = getattr(config, "openai_url", "https://api.openai.com/v1")

    console.print(f"Using Model: [bold cyan]{model_name}[/bold cyan]")
    console.print(f"Using API Base URL: [bold cyan]{api_base_url}[/bold cyan]")

    console.print("Starting performance measurement...")

    console.print(
        f"Running {runs} iterations per benchmark for more reliable results..."
    )

    all_results = []
    with console.status("[bold green]Running benchmarks...") as status:
        for i, benchmark in enumerate(BENCHMARKS):
            status.update(
                f"Running benchmark {i+1}/{len(BENCHMARKS)}: {benchmark['name']} (0/{runs} runs)"
            )

            # Run multiple iterations for this benchmark
            benchmark_runs = []
            for run_num in range(runs):
                status.update(
                    f"Running benchmark {i+1}/{len(BENCHMARKS)}: {benchmark['name']} ({run_num+1}/{runs} runs)"
                )
                result = run_benchmark(verified_book_path, benchmark)
                if result.get("scores"):  # Only add if we got valid scores
                    benchmark_runs.append(result)

            # Average the scores across runs
            if benchmark_runs:
                averaged_result = average_benchmark_results(benchmark_runs)
                all_results.append(averaged_result)
            else:
                # If no valid runs, add empty result
                all_results.append(
                    {
                        "benchmark_id": benchmark.get("id", "unknown"),
                        "benchmark_name": benchmark.get("name", "Unknown Benchmark"),
                        "scores": {},
                    }
                )

    if update_golden_standards:
        save_golden_scores(model_name, all_results)
        console.print(
            f"[bold green]Golden standards updated successfully using model '{model_name}'.[/bold green]"
        )
        return

    console.print("Performance measurement finished.")
    golden_scores_data = load_golden_scores()
    golden_benchmarks = golden_scores_data.get("benchmarks", {})
    golden_model = golden_scores_data.get("model_name", "N/A")

    table = Table(
        title=f"LLM Performance Benchmark Results for '{model_name}' (vs. '{golden_model}') - {runs} runs averaged"
    )
    table.add_column("Benchmark", justify="left", style="cyan")
    table.add_column("ROUGE-1", justify="right")
    table.add_column("ROUGE-2", justify="right")
    table.add_column("ROUGE-L", justify="right")

    for result in all_results:
        scores = result["scores"]
        benchmark_id = result["benchmark_id"]
        golden_result = golden_benchmarks.get(benchmark_id, {})

        def format_score(metric_key):
            user_score = scores.get(metric_key, 0.0)
            golden_score = golden_result.get(metric_key, 0.0)
            diff = user_score - golden_score

            color = "green" if diff >= -0.05 else "red"
            sign = "+" if diff >= 0 else ""

            user_score_str = f"{user_score:.4f}"
            golden_score_str = f"(golden: {golden_score:.4f})"
            diff_str = f"[{color}]({sign}{diff:.4f})[/]"

            return Text.from_markup(
                f"{user_score_str}\n{golden_score_str}\n{diff_str}", justify="right"
            )

        table.add_row(
            result["benchmark_name"],
            format_score("rouge1"),
            format_score("rouge2"),
            format_score("rougeL"),
        )

    table.caption = f"Using API Base URL: {api_base_url}"
    console.print(table)
