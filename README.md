[![GitHub Actions Status](https://github.com/raestrada/storycraftr/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/raestrada/storycraftr/actions)
[![GitHub Actions Status](https://github.com/raestrada/storycraftr/actions/workflows/pytest.yml/badge.svg)](https://github.com/raestrada/storycraftr/actions)

# <img src="https://res.cloudinary.com/dyknhuvxt/image/upload/f_auto,q_auto/ofhhkf6f7bryfgvbxxwc" alt="StoryCraftr Logo" width="100" height="100"> StoryCraftr - Your AI-powered Book Creation Assistant 📚🤖

Welcome to [**StoryCraftr**](https://storycraftr.app), the open-source project designed to revolutionize how books are written. With the power of AI and a streamlined command-line interface (CLI), StoryCraftr helps you craft your story, manage worldbuilding, structure your book, and generate chapters — all while keeping you in full control.

## Release Notes v0.1.0

You can find the release notes for version `v0.1.0` [here](https://github.com/raestrada/storycraftr/releases/tag/v0.1.0).

## Installation

You can install the current version of **StoryCraftr** via `pipx` using the following command:

```bash
pipx install git+https://github.com/raestrada/storycraftr.git@v0.1.0
```

### Important: Before using StoryCraftr, make sure to set your OpenAI API key:

```bash
export OPENAI_API_KEY=your-openai-api-key
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

## Full Guide

For a complete guide, including more examples and instructions on how to fully leverage StoryCraftr, visit our **Getting Started** page:

👉 [**Getting Started with StoryCraftr**](https://storycraftr.app/getting_started.html) 👈

## Why StoryCraftr?

Writing a book is a journey that involves not only creativity but also structure, consistency, and planning. **StoryCraftr** is here to assist you with:
- **Worldbuilding**: Define the geography, history, cultures, and more.
- **Outline**: Generate a cohesive story outline, from character summaries to chapter synopses.
- **Chapters**: Automatically generate chapters, cover pages, and epilogues based on your ideas.

With StoryCraftr, you'll never feel stuck again. Let AI guide your creative process, generate ideas, and help you bring your world and characters to life.

## Contributing

We welcome contributions of all kinds! Whether you’re a developer, writer, or simply interested in improving the tool, you can help. Here’s how you can contribute:

1. **Fork the repository** and create your branch:
```bash
git checkout -b feature/YourFeature
```

2. **Make your changes**, ensuring all tests pass.

3. **Submit a pull request** detailing your changes.

Join us on this journey to create an amazing open-source tool for writers everywhere. Together, we can make StoryCraftr the go-to AI writing assistant! 💡
