from storycraftr.agents import create_message, get_thread
from rich.console import Console
from rich.progress import Progress

console = Console()

def summarize_content(assistant, original_prompt):
    """
    Summarizes the prompt or content to reduce input size, generating a new thread for the summary step.
    """
    thread = get_thread()  # Generar un nuevo thread
    content = f"Summarize the following prompt to make it more concise:\n\nPrompt:\n{original_prompt}"
    
    # Log de inicio
    console.print("[cyan]Summarizing the prompt...[/cyan]")
    
    # Enviar el mensaje a través del asistente y obtener la respuesta
    summary_response = create_message(
        thread_id=thread.id,
        content=content,
        assistant=assistant
    )
    
    if summary_response:
        console.print("[green]Summary completed successfully.[/green]")
        return summary_response
    else:
        console.print("[red]Error summarizing prompt.[/red]")
        return ""

def optimize_query_with_summary(assistant, summarized_prompt):
    """
    Uses the summarized prompt to optimize it for a better response, generating a new thread for optimization.
    """
    thread = get_thread()  # Generar un nuevo thread
    content = f"Using the following summarized prompt, optimize it for the best result:\n\nSummarized Prompt: {summarized_prompt}"
    
    # Log de inicio
    console.print("[cyan]Optimizing the summarized prompt...[/cyan]")
    
    # Enviar el mensaje a través del asistente
    optimized_response = create_message(
        thread_id=thread.id,
        content=content,
        assistant=assistant
    )
    
    if optimized_response:
        console.print("[green]Optimization completed successfully.[/green]")
        return optimized_response
    else:
        console.print("[red]Error optimizing the query.[/red]")
        return ""

def final_query(assistant, optimized_prompt):
    """
    Executes the final query with the optimized prompt, generating a new thread for the final query.
    """
    thread = get_thread()  # Generar un nuevo thread
    content = f"Answer the following query:\n\nQuery: {optimized_prompt}"

    # Log de inicio
    console.print("[cyan]Executing the final query...[/cyan]")
    
    final_response = create_message(
        thread_id=thread.id,
        content=content,
        assistant=assistant
    )
    
    if final_response:
        console.print("[green]Final query executed successfully.[/green]")
        return final_response
    else:
        console.print("[red]Error in the final query.[/red]")
        return ""

def handle_failed_prompt(assistant, original_prompt):
    """
    The complete process to optimize a failed prompt using heuristic steps. Each step generates its own thread.
    1. Summarize the original prompt.
    2. Optimize the summarized prompt.
    3. Execute the final query using the optimized prompt.
    """
    with Progress() as progress:
        task = progress.add_task("[yellow]Processing failed prompt...", total=3)

        # Step 1: Summarize the original prompt
        console.print("Step 1: Summarizing the original prompt...")
        summarized_prompt = summarize_content(assistant, original_prompt)
        progress.update(task, advance=1)

        # Step 2: Optimize the summarized prompt
        console.print("Step 2: Optimizing the summarized prompt...")
        optimized_prompt = optimize_query_with_summary(assistant, summarized_prompt)
        progress.update(task, advance=1)

        # Step 3: Execute the final query
        console.print("Step 3: Executing the final query...")
        final_response = final_query(assistant, optimized_prompt)
        progress.update(task, advance=1)

    return final_response

# Ejemplo de uso
if __name__ == "__main__":
    from storycraftr.agents import create_or_get_assistant

    assistant = create_or_get_assistant()  # Obtener o crear el asistente

    original_prompt = "What are the key points of this content related to X?"
    
    result = handle_failed_prompt(assistant, original_prompt)

    if result:
        console.print(f"[green]Final response received successfully![/green]")
        print(result)
    else:
        console.print(f"[red]Failed to process the prompt.[/red]")
