# StoryCraftr - Your AI-powered Book Creation Assistant 📚🤖

Welcome to **StoryCraftr**, the open-source project designed to revolutionize how books are written. With the power of AI and a streamlined command-line interface (CLI), StoryCraftr helps you craft your story, manage worldbuilding, structure your book, and generate chapters — all while keeping you in full control.

If you're passionate about writing, coding, or both, we invite you to collaborate with us on making StoryCraftr the ultimate AI writing assistant! 🚀

## Why StoryCraftr?

Writing a book is a journey that involves not only creativity but also structure, consistency, and planning. **StoryCraftr** is here to assist you with:
- **Worldbuilding**: Define the geography, history, cultures, and more.
- **Outline**: Generate a cohesive story outline, from character summaries to chapter synopses.
- **Chapters**: Automatically generate chapters, cover pages, and epilogues based on your ideas.

With StoryCraftr, you'll never feel stuck again. Let AI guide your creative process, generate ideas, and help you bring your world and characters to life.

## Key Features

- **AI-powered writing assistant**: Leverages OpenAI's GPT models to help you write everything from chapter summaries to detailed plot points.
- **Modular structure**: Each aspect of the book (outline, worldbuilding, chapters) is handled individually, allowing full customization.
- **Markdown-based**: All generated content is saved in Markdown, making it easy to integrate with any writing workflow.
- **Customizable prompts**: You control the prompts and direction the AI takes.

## Getting Started

### Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/) for managing dependencies
- OpenAI API key (stored in `.env` file)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/storycraftr.git
    cd storycraftr
    ```

2. **Install dependencies using Poetry**:
    ```bash
    poetry install
    ```

3. **Create a `.env` file** to store your OpenAI API key:
    ```bash
    touch .env
    echo "OPENAI_API_KEY=your-openai-api-key" >> .env
    ```

4. **Run the CLI**:
    ```bash
    poetry run storycraftr --help
    ```

## Usage

StoryCraftr allows you to create, update, and manage every aspect of your book through simple CLI commands. Here are some examples:

### Worldbuilding

```bash
poetry run storycraftr my-book worldbuilding geography "Describe the geography of a futuristic dystopia" en
```

### Outline

```bash
poetry run storycraftr my-book outline general_outline "Outline a sci-fi thriller where humanity battles AI overlords" en
```

### Chapters

```bash
poetry run storycraftr my-book chapters chapter "Write chapter one of a space opera" en 1
```

### Updating Knowledge

If you've made changes to your book's structure, you can update the agent's knowledge with:

```bash
poetry run storycraftr my-book update
```

## Contributing

We welcome contributions of all kinds! Whether you’re a developer, writer, or simply interested in improving the tool, you can help. Here’s how you can contribute:

1. **Fork the repository** and create your branch:
    ```bash
    git checkout -b feature/YourFeature
    ```

2. **Make your changes**, ensuring all tests pass.

3. **Submit a pull request** detailing your changes.

Join us on this journey to create an amazing open-source tool for writers everywhere. Together, we can make StoryCraftr the go-to AI writing assistant! 💡

## Roadmap

- Add support for multi-language generation
- Improve prompt customization and retrieval pipeline
- Integrate more AI tools for worldbuilding and narrative assistance
- Create a web-based UI for non-technical writers
- Optimize token management for large projects

## License

StoryCraftr is open-source and licensed under the MIT License. Feel free to fork, extend, and contribute to this project!

---

### Stay in Touch

- **Issues**: If you encounter any bugs or have feature requests, please [open an issue](https://github.com/your-repo/storycraftr/issues).
- **Contributions**: Check out our [contributing guidelines](CONTRIBUTING.md) for more details.
- **Social**: Follow us on Twitter for the latest updates and discussions: [@storycraftr](https://twitter.com/storycraftr)

---

Let’s build the future of writing, one chapter at a time! ✍️
# storycraftr
