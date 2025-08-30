# Getting Started with StoryCraftr 📚✨

**StoryCraftr** is a CLI tool designed to help you write your book using AI. Inspired by the writing techniques of [Brandon Sanderson's Laws of Magic and Writing](https://www.brandonsanderson.com/pages/writing-advice), this guide will walk you through creating a story from scratch. Whether you're outlining, building worlds, or writing chapters, StoryCraftr can assist you every step of the way.

Sanderson emphasizes strong **structure** and **rules for storytelling**, which we will follow throughout this guide.

## Step 1: Install StoryCraftr

First, install **StoryCraftr** using [pipx](https://pypa.github.io/pipx/), a tool to help you install and run Python applications in isolated environments. It works on most platforms, including macOS, Linux, and Windows. Using `pipx` ensures that **StoryCraftr** runs in its own virtual environment, keeping your system's Python installation clean.

To install **StoryCraftr**, run the following command:

```bash
pipx install git+https://github.com/raestrada/storycraftr.git@v0.10.1-beta4
```

### Important: Before running the `storycraftr` command

Store the key in a text file located at ~/.storycraftr/openai_api_key.txt for convenience.

```bash
mkdir -p ~/.storycraftr/
echo "your-openai-api-key" > ~/.storycraftr/openai_api_key.txt
```

Once installed and the API key is set, you can run the tool using the command `storycraftr`.

### New: Specify OpenAI Model and URL

StoryCraftr now allows you to specify the OpenAI model and URL, which can be any service that supports the OpenAI API with file search capabilities, such as DeepSeek or others. This is essential as StoryCraftr relies on file search for its functionality.

To configure the model and URL, add the following lines to your configuration file located at `~/.storycraftr/config.json`:

```json
{
  "openai_model": "your-preferred-model",
  "openai_url": "https://api.your-preferred-service.com"
}
```

Make sure to replace `"your-preferred-model"` with the model you want to use and `"https://api.your-preferred-service.com"` with the URL of the service that supports the OpenAI API with file search.

### Supported LLMs

Here are some examples of LLMs that are compatible with the OpenAI API:

1. **OpenAI GPT Series**:

   - Models: `gpt-3.5-turbo`, `gpt-4`
   - URL Base: `https://api.openai.com/v1/`
   - Documentation: [OpenAI API Models](https://beta.openai.com/docs/models)

2. **Azure OpenAI Service**:

   - Models: `gpt-3.5-turbo`, `gpt-4`
   - URL Base: Depends on the region and configuration.
   - Documentation: [Azure OpenAI Service](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)

3. **DeepSeek**:

   - Model: `DeepSeek-R1`
   - URL Base: `https://api.deepseek.com/v1/`
   - Documentation: [DeepSeek API Documentation](https://deepseek.com/docs)

4. **Qwen (Alibaba Cloud)**:

   - Models: `qwen-7b`, `qwen-13b`
   - URL Base: `https://dashscope.aliyuncs.com/`
   - Documentation: [DashScope API](https://dashscope.aliyuncs.com/docs)

5. **Gemini (Google AI)**:

   - Models: `gemini-1`, `gemini-1.5`
   - URL Base: `https://api.gemini.google.com/v1/`
   - Documentation: [Gemini API](https://gemini.google.com/docs)

6. **Together AI**:

   - Model: `together-gpt-neoxt-chat-20b`
   - URL Base: `https://api.together.ai/v1/`
   - Documentation: [Together AI API](https://together.ai/docs)

7. **DeepInfra**:
   - Model: `Qwen2.5-Coder-32B-Instruct`
   - URL Base: `https://api.deepinfra.com/v1/`
   - Documentation: [DeepInfra API](https://deepinfra.com/docs)

## Step 2: Create the Behavior File

The **behavior file** is a crucial component that guides the AI’s **writing process**. It represents the **vision** of the writer and defines the behavior the AI should follow when generating the story. This file goes beyond plot or character details—it sets the tone, style, and thematic focus of the book and is the foundation for how the AI approaches the entire writing process.

This file should communicate the **high-level ideas** you, the writer, want the AI to follow. It’s like a creative manifesto that tells the AI **how to write** the book, what kind of **voice** to use, and how to approach the content from an artistic and stylistic perspective. The behavior file is where you articulate your **vision for the project**, ensuring the AI writes in a way that aligns with your creative goals.

### What Should Go in the Behavior File?

In the behavior file, you can include a variety of elements to help guide the AI:

- **General Focus**: What’s the overarching idea or theme of the book?
- **Tone**: Should the story be light, dark, humorous, serious, etc.?
- **Style**: Are you aiming for an epic, descriptive tone or a concise, fast-paced narrative?
- **Character Approach**: Should the AI focus on detailed emotional arcs, or are you more interested in action-driven characters?
- **Length**: Is this a short novella or a longer novel? This will influence the pacing and depth.
- **Narrative Structure**: Do you want traditional three-act structures or something more experimental?

The **behavior file** provides the essential **guidelines** that will define the AI’s approach to everything it writes for your book. Here's an example:

```bash
echo "Write in a dark, introspective tone focusing on a morally ambiguous protagonist. The novel should explore themes of power, control, and manipulation in a futuristic society. The writing should reflect a complex character-driven narrative, emphasizing internal conflict and relationships. The pacing should allow for detailed worldbuilding, with the story unfolding gradually. Target length: 250-300 pages." > behaviors/default.txt
```

---

### Why the Behavior File Matters

Unlike the outline (which provides structure) or worldbuilding (which defines the setting), the behavior file **sets the framework for the creative approach**. It tells the AI **how to think like you**, making sure that each piece of content it generates fits within the story’s **artistic direction**. Without this file, the AI might not align with your intended tone or style, resulting in a disjointed narrative.

Think of the behavior file as your way of ensuring the AI “understands” your creative intentions as if it were a co-writer who knows the rules of the world you're building and the atmosphere you're aiming for.

---

### Example Behavior File for The Purge of the Gods

- **Title**: _The Purge of the Gods_
- **Genre**: Dystopian Science Fiction
- **Tone**: Dark, introspective, and morally ambiguous
- **Main Themes**: Power, control, manipulation, and societal decay
- **Narrative Focus**: The story should focus heavily on internal character conflicts and the moral consequences of actions. It’s a character-driven story with a gradual unfolding of a manipulative protagonist's plan.
- **Protagonist Approach**: The protagonist is morally gray, often manipulative, and should be presented with increasing ruthlessness. The AI should depict the world as hostile, unforgiving, and filled with complex characters who reflect this.
- **Pacing and Length**: The story should be mid-length (250-300 pages), with a gradual build-up of tension. Include detailed worldbuilding but keep the focus on character development and power dynamics.

---

### **Why is this Important?**

The behavior file serves as the **creative guide** for your story. It helps the AI maintain consistency in **style**, **tone**, and **focus** as it develops the novel. It ensures the AI's writing process is in harmony with your initial vision and remains aligned with your intended **narrative** and **thematic direction** throughout the writing process.

## Step 3: Initialize the Book

A clear definition of genre and structure aligns with Sanderson’s emphasis on creating consistent rules for your world and plot ([Sanderson's First Law](https://www.brandonsanderson.com/sandersons-first-law/)). We've added an optional parameter `--reference-author`. If you use it, the system will try to emulate the style of that author; if not, it will assume the style based on what you write.

```bash
storycraftr init "The Purge of the Gods" --primary-language "en" --alternate-languages "es" --author "Rodrigo Estrada" --genre "science fiction" --behavior "behavior.txt" --reference-author "Brandon Sanderson" --openai-model "gpt-4" --openai-url "https://api.openai.com/v1/"
cd "The Purge of the Gods"
```

> **Note:** In the following commands, any modified files are always backed up with a _.back_ extension.

## Step 4: Generate the Outline

According to Sanderson, **strong outlines** provide the scaffolding for a story, ensuring that it remains structured and engaging throughout. Let's build the outline for **La Purga de los Dioses**.

1. **General Outline**:

   ```bash
   storycraftr outline general-outline "Summarize the overall plot of a dystopian science fiction where advanced technology, resembling magic, has led to the fall of humanity’s elite and the rise of a manipulative villain who seeks to destroy both the ruling class and the workers."
   ```

2. **Character Summary**:

   ```bash
   storycraftr outline character-summary "Summarize the character of Zevid, a villainous mastermind who seeks to destroy both the ruling elite and the workers in a dystopian world where advanced technology mimics magic."
   ```

3. **Plot Points**:

   ```bash
   storycraftr outline plot-points "Identify the key plot points of a dystopian novel where a villain manipulates both the elite and the workers to achieve ultimate control in a world where advanced technology mimics magic."
   ```

4. **Chapter-by-Chapter Synopsis**:
   ```bash
   storycraftr outline chapter-synopsis "Outline each chapter of a dystopian society where an ancient elite class, ruling with advanced biotechnology that mimics magic, manipulates both workers and warriors. The protagonist, Zevid, aims to destroy both factions through manipulation, eventually leading to his own version of 'The Purge.'"
   ```

## Step 5: Build Your World

Sanderson’s [Laws of Magic](https://www.brandonsanderson.com/sandersons-first-law/) stress the importance of **rules** and **limitations** in a story's world. Here, we will develop a solid world for **La Purga de los Dioses**.

1. **History**:

   ```bash
   storycraftr worldbuilding history "Describe the history of a dystopian world where advanced biotechnology and nanotechnology are perceived as magic, leading to a society where an elite class rules and manipulates both workers and technology to maintain control."
   ```

2. **Geography**:

   ```bash
   storycraftr worldbuilding geography "Describe the geography of a dystopian world where advanced biotechnology and nanotechnology are seen as magic. Focus on how the elite families control key regions, and the remnants of the world that survived the Purge."
   ```

3. **Culture**:

   ```bash
   storycraftr worldbuilding culture "Describe the culture of a dystopian society where the elite use advanced biotechnology to maintain power, and the workers live under the illusion that this technology is magic. Focus on how the elite families have developed their own rituals, and how the workers perceive their rulers."
   ```

4. **Technology**:

   ```bash
   storycraftr worldbuilding technology "Describe the technology of a dystopian world where advanced biotechnology and nanotechnology are perceived as magic. Focus on the elite's use of this technology for immortality, enhanced abilities, and control over the workers, who are unaware of its true nature."
   ```

5. **Magic System**:
   ```bash
   storycraftr worldbuilding magic-system "Describe the magic system in a dystopian world where advanced biotechnology and nanotechnology are mistaken for magic. Explain how the elite families use this 'magic' to control the population, and how the workers have developed their own beliefs around it."
   ```

## Step 6: Write Your Chapters

With a well-outlined story and a detailed world, we can now generate the chapters of **La Purga de los Dioses**. Sanderson’s principles of **progression** and **consistent conflict resolution** will guide us as we write.

1. **Generate Chapter 1**:

   ```bash
   storycraftr chapters chapter 1 "Write Chapter 1 based on the synopsis provided: Zevid is in the final stages of his grand plan. As the rebellion rages outside, he prepares to infiltrate the Dark Tower, the center of the elites' control over biotechnology. The rebellion he orchestrated serves as a distraction while he pursues his true goal of seizing the power within the tower."
   ```

2. **Generate Chapter 2**:

   ```bash
   storycraftr chapters chapter 2 "Write Chapter 2 based on the synopsis provided: Zevid continues to manipulate the false hero leading the workers. While the workers believe they are liberating themselves from the elite, Zevid uses their blind trust to further his own ends."
   ```

3. **Generate the Cover**:

   ```bash
   storycraftr chapters cover "Generate a cover text for the novel 'The Purge of the Gods' where a villain manipulates both the elite and the workers in a dystopian world of advanced technology disguised as magic."
   ```

4. **Generate the Back Cover**:
   ```bash
   storycraftr chapters back-cover "Generate a back-cover text for 'The Purge of the Gods,' a dystopian novel where advanced biotechnology is seen as magic, and a cunning villain manipulates both the elite and the workers to achieve ultimate control."
   ```

## Step 7: Publish Your Book

StoryCraftr supports publishing your book to PDF, making it easy to share your work. To generate a PDF, you'll need to have **Pandoc** and **XeLaTeX** installed on your system.

### Prerequisites

Make sure to install **Pandoc** and **XeLaTeX** before running the _publish_ command. Here are minimalistic installation instructions:

- **macOS**:  
  Install using Homebrew:

  ```bash
  brew install pandoc
  brew install --cask mactex
  ```

- **Linux**:  
  Install using the package manager:

  ```bash
  sudo apt install pandoc texlive-xetex
  ```

- **Windows**:  
  Download and install Pandoc from [Pandoc's website](https://pandoc.org/installing.html) and [MiKTeX](https://miktex.org/download) for XeLaTeX support.

Once you have these dependencies installed, you can proceed to publish your book.

### 1. Generate PDF:

To generate a PDF of your book in the primary language, use the following command:

```bash
storycraftr publish pdf en
```

### 2. Generate PDF with Translation:

If you want to translate your book and generate the PDF in another language (e.g., Spanish), you can use the `--translate` option:

```bash
storycraftr publish pdf en --translate es
```

Once the process is complete, the PDF file will be available in your project folder, ready to be shared or printed.

## Step 8: Chat with Your Assistant

StoryCraftr now includes a command to chat directly with your AI assistant. This allows you to ask questions, brainstorm ideas, or request improvements to your book's content in an interactive session, all from the comfort of your terminal. **Even better, the chat has StoryCraftr's documentation embedded**, so you can ask for help with commands and parameters without leaving the chat!

### How to Start a Chat

To start chatting with your assistant, make sure your book project is initialized and then run the following command:

```bash
storycraftr chat
```

Replace `"book_path"` with the actual name of your book. This will open an interactive session where you can type messages to your AI assistant. The responses will be formatted in Markdown, making it easy to read any formatted text, lists, or other structures returned by the assistant.

### Example Chat Session

In this interactive chat, you can ask the assistant to help with both your book and StoryCraftr’s commands. Here are three examples:

1. **Asking about your book:**

   ```bash
   [You]: "Explain how Captain Blackmane uses deception to take control of the hidden pirate fleet."
   ```

   ```bash
   [Assistant]: "Captain Blackmane’s cunning involves luring rival pirate factions into a false alliance. He promises them access to the treasure they’ve long sought, only to reveal his true plan of betrayal, securing the fleet for himself."
   ```

2. **Running a command:**

   ```bash
   [You]: "Generate the character summary for Captain Blackmane."
   ```

   ```bash
   [Assistant]: "To generate a character summary for Captain Blackmane, use the following command:
   `storycraftr outline character-summary "Summarize Captain Blackmane, a ruthless pirate leader with a talent for deception."`"
   ```

3. **Executing any StoryCraftr command directly in the chat:**

   ```bash
   [You]: !iterate check-names "Check character names for consistency."
   ```

In this session, you can seamlessly combine book content with command generation and execution, streamlining your writing process and giving you real-time insights.

![chat](https://res.cloudinary.com/dyknhuvxt/image/upload/v1729551304/chat-example_hdo9yu.png)

You can ask the assistant for suggestions like chapter ideas, worldbuilding elements, or even help refining your story’s plot using StoryCraftr’s built-in tools.

### How to Exit the Chat

You can exit the chat at any time by typing:

```bash
exit()
```

This will gracefully close the chat session and return you to your terminal.

## Learn More About Writing

The ideas in this tool are heavily inspired by [Brandon Sanderson’s Laws of Magic and Writing](https://www.brandonsanderson.com/the-law-of-writing). StoryCraftr is designed to help you implement these concepts while crafting well-structured stories with strong character arcs and consistent plot development.

---

Happy writing with **StoryCraftr**! ✍️
