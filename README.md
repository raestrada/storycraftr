[![GitHub Actions Status](https://github.com/raestrada/storycraftr/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/raestrada/storycraftr/actions)  
[![GitHub Actions Status](https://github.com/raestrada/storycraftr/actions/workflows/pytest.yml/badge.svg)](https://github.com/raestrada/storycraftr/actions)

# <img src="https://res.cloudinary.com/dyknhuvxt/image/upload/f_auto,q_auto/ofhhkf6f7bryfgvbxxwc" alt="StoryCraftr Logo" width="100" height="100"> StoryCraftr - Your AI-powered Book Creation Assistant 📚🤖

Welcome to [**StoryCraftr**](https://storycraftr.app), the open-source project designed to revolutionize how books are written. With the power of AI and a streamlined command-line interface (CLI), StoryCraftr helps you craft your story, manage worldbuilding, structure your book, and generate chapters — all while keeping you in full control.

---

## What's New? Discover AI Craftr 🌐

**[AI Craftr](https://aicraftr.app)** is now available as a powerful suite for AI-assisted writing, featuring specialized tools like **StoryCraftr** for novelists and **[PaperCraftr](https://papercraftr.app)** for researchers. Each tool is designed to simplify your writing process with unique features catered to different types of content. Explore **PaperCraftr** for structuring academic papers, or stay tuned as we add more tools to the AI Craftr suite, such as **LegalCraftr** for legal documents and **EduCraftr** for educational materials.

---

## Release Notes v0.8.0-alpha4

You can find the release notes for version `v0.8.0-alpha4` [here](https://github.com/raestrada/storycraftr/releases/tag/v0.7.-alpha3).

## Step 1: Install StoryCraftr

First, install **StoryCraftr** using [pipx](https://pypa.github.io/pipx/), a tool to help you install and run Python applications in isolated environments. It works on most platforms, including macOS, Linux, and Windows. Using `pipx` ensures that **StoryCraftr** runs in its own virtual environment, keeping your system's Python installation clean.

To install **StoryCraftr**, run the following command:

```bash
pipx install git+https://github.com/raestrada/storycraftr.git@v0.8.0-alpha4
```

### Important: Before using StoryCraftr, make sure to set your OpenAI API key:

Store the key in a text file located at `~/.storycraftr/openai_api_key.txt` for convenience.

```bash
mkdir -p ~/.storycraftr/
echo "your-openai-api-key" > ~/.storycraftr/openai_api_key.txt
```

## Quick Examples

Here are a few ways to get started with **StoryCraftr**:

### Initialize a new book project:

```bash
storycraftr init "La purga de los dioses" --primary-language "es" --alternate-languages "en" --author "Rodrigo Estrada" --genre "science fiction" --behavior "behavior.txt"
```

### Generate a general outline:

```bash
storycraftr outline general-outline "Summarize the overall plot of a dystopian science fiction where advanced technology, resembling magic, has led to the fall of humanity’s elite and the rise of a manipulative villain who seeks to destroy both the ruling class and the workers."
```

## 💬 Introducing Chat!!! – A Simple Yet Powerful Tool to Supercharge Your Conversations! 💥

Whether you're brainstorming ideas, refining your story, or just need a little creative spark, Chat!!! is here to help. It's a straightforward, easy-to-use feature that lets you dive deep into meaningful discussions, unlock new insights, and get your thoughts flowing effortlessly.

🚀 Sometimes, all you need is a little chat to get the gears turning! Try it out and watch your creativity soar!

![chat](https://res.cloudinary.com/dyknhuvxt/image/upload/v1729551304/chat-example_hdo9yu.png)

## Full Guide

For a complete guide, including more examples and instructions on how to fully leverage StoryCraftr, visit our **Getting Started** page:

👉 [**Getting Started with StoryCraftr**](https://storycraftr.app/getting_started.html) 👈

## Why StoryCraftr?

Writing a book is a journey that involves not only creativity but also structure, consistency, and planning. **StoryCraftr** is here to assist you with:

- **Worldbuilding**: Define the geography, history, cultures, and more.
- **Outline**: Generate a cohesive story outline, from character summaries to chapter synopses.
- **Chapters**: Automatically generate chapters, cover pages, and epilogues based on your ideas.

With StoryCraftr, you'll never feel stuck again. Let AI guide your creative process, generate ideas, and help you bring your world and characters to life.

## StoryCraftr Chat Feature 💬

The **StoryCraftr Chat** feature allows users to engage directly with an AI assistant, helping to brainstorm, refine, and improve your book in real time. The chat supports various commands for outlining, iterating, and world-building, making it a powerful tool for writers to create and enhance their stories interactively.

### Key Commands:

- **Iterate**: Refine character names, motivations, and even insert new chapters mid-book.  
  Example:

  ```bash
  !iterate insert-chapter 3 "Add a flashback between chapters 2 and 3."
  ```

- **Outline**: Generate the general plot, chapter summaries, or key plot points.  
  Example:

  ```bash
  !outline general-outline "Summarize the overall plot of a dystopian sci-fi novel."
  ```

- **Worldbuilding**: Build the world’s history, geography, and technology, or develop the magic system.  
  Example:

  ```bash
  !worldbuilding magic-system "Describe the 'magic' system based on advanced technology."
  ```

- **Chapters**: Write new chapters or adjust existing ones and generate cover text.  
  Example:
  
  ```bash
  !chapters chapter 1 "Write chapter 1 based on the synopsis."
  ```

You can start a chat session with the assistant using:

```bash
storycraftr chat --book-path /path/to/your/book
```

For help with available commands during the session, simply type:

```bash
help()
```

## VSCode Extension

We are excited to introduce the **StoryCraftr** VSCode extension, designed to seamlessly integrate the StoryCraftr CLI into your development environment. This extension allows you to interact with StoryCraftr directly from VSCode, offering powerful tools for novel writing and AI-assisted creativity.

### Key Features:

- **Auto-detection**: Automatically detects if `storycraftr.json` is present in the project root, ensuring the project is ready to use.
- **Integrated Chat**: Start interactive AI-powered chat sessions for brainstorming and refining your novel without leaving VSCode.
- **Simplified Setup**: If StoryCraftr or its dependencies (Python, pipx) are not installed, the extension assists you in setting them up.

### Installation:

You can install the StoryCraftr VSCode extension directly from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=StoryCraftr.storycraftr).

### Usage:

Once installed, the extension will:

1. Check if `storycraftr.json` exists in the root of your project.
2. If it exists, you can start interacting with StoryCraftr by launching a terminal with the `chat` command using:
   - **Command Palette**: Run `Start StoryCraftr Chat`.
3. If not installed, it will guide you through installing Python, pipx, and StoryCraftr to get started.

Explore more about the [StoryCraftr CLI](https://github.com/raestrada/storycraftr) and see how it can boost your storytelling workflow.

Let your creativity flow with the power of AI! ✨

## Contributing

We welcome contributions of all kinds! Whether you’re a developer, writer, or simply interested in improving the tool, you can help. Here’s how you can contribute:

1. **Fork the repository** and create your branch:

```bash
git checkout -b feature/YourFeature
```

2. **Make your changes**, ensuring all tests pass.

3. **Submit a pull request** detailing your changes.

Join us on this journey to create an amazing open-source tool for writers everywhere. Together, we can make StoryCraftr the go-to AI writing assistant! 💡
