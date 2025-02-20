# Changelog

## [0.9.1-beta2] - 2024-11-01

### Added

- **OpenAI Model and URL Configuration**: Added support for specifying the OpenAI model and URL in the configuration file and during project initialization.
- **Supported LLMs Documentation**: Included documentation for various LLMs compatible with the OpenAI API, such as DeepSeek, Qwen, Gemini, Together AI, and DeepInfra.
- **Behavior File Enhancements**: Improved the behavior file to guide the AI's writing process more effectively, ensuring alignment with the writer's vision.
- **Interactive Chat Enhancements**: Enhanced the chat feature to support more dynamic interactions and command executions directly from the chat interface.

## [0.9.0-beta1] - 2024-10-30

### Added

- **Support for PaperCraftr**: Major refactor to extend support for PaperCraftr, a CLI aimed at academic paper writing. Users can now initialize paper projects with a dedicated structure, distinct from book projects, for enhanced productivity in academic writing.
- **Multiple Prompt Support**: Implemented multi-purpose prompts for both book and paper creation, allowing users to generate and refine content for different aspects such as research questions, contributions, and outlines.
- **Define Command Extensions**: Added new commands under the `define` group to generate key sections for papers, including defining research questions and contributions.
- **Contribution Generation**: Added the `define_contribution` command to generate or refine the main contribution of a paper, supporting improved clarity and focus for academic projects.

## [0.8.0-alpha4] - 2024-03-14

### Added

- **Interactive Chat with Commands**: Enhanced chat functionality now allows users to interact with StoryCraftr using direct command prompts, helping with outlining, world-building, and chapter writing.
- **Documentation-Driven Chat**: StoryCraftr's documentation is fully loaded into the system, allowing users to ask for help with commands directly from within the chat interface.
- **Improved User Interface**: New UI elements for an enhanced interactive experience. Chat commands and documentation queries are more intuitive.

![Chat Example](https://res.cloudinary.com/dyknhuvxt/image/upload/v1729551304/chat-example_hdo9yu.png)

## [0.6.1-alpha2] - 2024-02-29

### Added

- **VSCode Extension Alpha**: Launched an alpha version of the StoryCraftr extension for VSCode, which automatically detects the `storycraftr.json` file in the workspace and launches a terminal for interacting with the StoryCraftr CLI.

## [0.6.0-alpha1] - 2024-02-22

### Added

- **VSCode Terminal Chat**: Chat functionality embedded into the VSCode extension, allowing users to launch a terminal directly from VSCode and interact with StoryCraftr.

## [0.5.2-alpha1] - 2024-02-15

### Added

- **Multi-command Iteration**: New CLI functionality allowing iterative refinement of plot points, character motivations, and chapter structures.

## [0.5.0-alpha1] - 2024-02-01

### Added

- **Insert Chapter Command**: Users can now insert chapters between existing ones and automatically renumber subsequent chapters for seamless story progression.

## [0.4.0] - 2024-01-20

### Added

- **Story Iteration**: Introduced the ability to iterate over various aspects of your book, including refining character motivations and checking plot consistency.
- **Flashback Insertion**: Users can now insert flashback chapters that automatically adjust surrounding chapters.

## [0.3.0] - 2024-01-10

### Added

- **Outline Generation**: Generate detailed story outlines based on user-provided prompts.
- **World-Building**: New commands to generate history, geography, culture, and technology elements of your book’s world.

## [0.2.0] - 2023-12-15

### Added

- **Behavior Guidance**: A behavior file that helps guide the AI's understanding of the writing style, themes, and narrative focus of your novel.

## [0.1.0] - 2023-11-28

### Added

- **Initial Release**: Base functionalities including chapter writing, character summaries, and basic outline generation.

---

StoryCraftr has come a long way from simple chapter generation to enabling an entire AI-powered creative writing workflow. With interactive chats, rich command sets, and VSCode integration, it’s now easier than ever to bring your stories to life!
