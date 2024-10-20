# Getting Started with StoryCraftr 📚✨

**StoryCraftr** is a CLI tool designed to help you write your book using AI. Inspired by the writing techniques of [Brandon Sanderson's Laws of Magic and Writing](https://www.brandonsanderson.com/pages/writing-advice), this guide will walk you through creating a story from scratch. Whether you're outlining, building worlds, or writing chapters, StoryCraftr can assist you every step of the way.

Sanderson emphasizes strong **structure** and **rules for storytelling**, which we will follow throughout this guide. 

## Step 1: Install StoryCraftr

First, install **StoryCraftr** using [pipx](https://pypa.github.io/pipx/), a tool to help you install and run Python applications in isolated environments. It works on most platforms, including macOS, Linux, and Windows. Using `pipx` ensures that **StoryCraftr** runs in its own virtual environment, keeping your system's Python installation clean.

To install **StoryCraftr**, run the following command:

```bash
pipx install git+https://github.com/raestrada/storycraftr.git@v0.6.0-alpha2
```

### Important: Before running the `storycraftr` command

Store the key in a text file located at ~/.storycraftr/openai_api_key.txt for convenience.

```bash
mkdir -p ~/.storycraftr/
echo "your-openai-api-key" > ~/.storycraftr/openai_api_key.txt
```

Once installed and the API key is set, you can run the tool using the command `storycraftr`.


## Step 2: Initialize Your Book Project

In Sanderson's writing methodology, having a clear starting point and preparation is essential for consistency and flow. Let's create our science fiction novel titled **La Purga de los Dioses** by **Rodrigo Estrada**.

1. **Create the project**:  
    ```bash
    mkdir la-purga-de-los-dioses
    cd la-purga-de-los-dioses
    ```

2. **Create the behavior file**: In line with Sanderson's principle of **focusing on conflict** and **character development**, this behavior will guide our AI.  
    ```bash
    echo "Focus on character development and conflict resolution in a futuristic society." > behaviors/default.txt
    ```

3. **Initialize the book**: A clear definition of genre and structure aligns with Sanderson’s emphasis on creating consistent rules for your world and plot ([Sanderson's First Law](https://www.brandonsanderson.com/sandersons-first-law/)). We've added an optional parameter --reference-author. If you use it, the system will try to emulate the style of that author; if not, it will assume the style based on what you write.

    ```bash
    storycraftr init "The Purge of the Gods" --primary-language "en" --alternate-languages "es" --author "Rodrigo Estrada" --genre "science fiction" --behavior "behavior.txt"  --reference-author "Brandon Sanderson"
    ```
> **Note:** In the following commands, any modified files are always backed up with a *.back* extension.

## Step 3: Generate the Outline

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

## Step 4: Build Your World

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

## Step 5: Write Your Chapters

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

## Step 6: Publish Your Book

StoryCraftr supports publishing your book to PDF, making it easy to share your work. To generate a PDF, you'll need to have **Pandoc** and **XeLaTeX** installed on your system.

### Prerequisites

Make sure to install **Pandoc** and **XeLaTeX** before running the *publish* command. Here are minimalistic installation instructions:

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

## Step 7: Chat with Your Assistant

StoryCraftr now includes a command to chat directly with your AI assistant. This allows you to ask questions, brainstorm ideas, or request improvements to your book's content in an interactive session, all from the comfort of your terminal.

### How to Start a Chat

To start chatting with your assistant, make sure your book project is initialized and then run the following command:

```bash
storycraftr chat
```

Replace `"book_path"` with the actual name of your book. This will open an interactive session where you can type messages to your AI assistant. The responses will be formatted in Markdown, making it easy to read any formatted text, lists, or other structures returned by the assistant.

### Example Chat Session

Here's an example of how a typical chat might look:

![chat](https://res.cloudinary.com/dyknhuvxt/image/upload/v1729089264/chat_idxfgi.png)

In this session, you ask for ideas for the next chapter, and the assistant responds with a detailed outline formatted in Markdown.

#### How to Exit the Chat
You can exit the chat at any time by typing:

``` exit() ```

This will gracefully close the chat session and return you to your terminal.

## Learn More About Writing

The ideas in this tool are heavily inspired by [Brandon Sanderson’s Laws of Magic and Writing](https://www.brandonsanderson.com/the-law-of-writing). StoryCraftr is designed to help you implement these concepts while crafting well-structured stories with strong character arcs and consistent plot development.

---

Happy writing with **StoryCraftr**! ✍️
