# <img src="https://res.cloudinary.com/dyknhuvxt/image/upload/f_auto,q_auto/ofhhkf6f7bryfgvbxxwc" alt="StoryCraftr Logo" width="100" height="100"> StoryCraftr - Your AI-powered Book Creation Assistant 📚🤖

Welcome to [**StoryCraftr**](https://storycraftr.homepage.com), the open-source project designed to revolutionize how books are written. With the power of AI and a streamlined command-line interface (CLI), StoryCraftr helps you craft your story, manage worldbuilding, structure your book, and generate chapters — all while keeping you in full control.

_Coming soon!_ The first alpha version is on its way, but it's not quite usable yet. Stay tuned!

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

### Initialize a new book project

To initialize a new book project with custom configuration, use the `init` command. The `book_name` is required, and you can specify the primary language, alternate languages, author, genre, and behavior file.

#### Example:

````bash
poetry run storycraftr init "La purga de los dioses" --primary-language "es" --alternate-languages "en" --author "Rodrigo Estrada" --genre "science fiction" --behavior "default.txt"
````

This will create the project structure for the book "La purga de los dioses" with the specified configuration and behavior.

### Generate Worldbuilding Content

The `worldbuilding` group allows you to generate different aspects of the world, such as geography, history, culture, and more. Below is an example of generating geography details.

#### Example:

````bash
poetry run storycraftr worldbuilding geography "Describe the mountain range in the northern region"
````

This will generate the geography content based on the prompt provided.

### Updating Knowledge

If you've made changes to your book's structure, you can update the agent's knowledge with:

```bash
poetry run storycraftr update
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
