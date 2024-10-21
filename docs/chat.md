# StoryCraftr Chat Feature Tutorial 💬✨

![chat](https://res.cloudinary.com/dyknhuvxt/image/upload/v1729551304/chat-example_hdo9yu.png)

## Getting Help in Chat

At any time, if you're unsure of what commands are available or how to use them, you can get help within the chat by typing:

```bash
help()
```

This will provide a list of available commands and their usage.

## Using Multi-word Prompts

When interacting with the StoryCraftr assistant, it's important to enclose multi-word inputs in quotes to ensure they are processed as a single cohesive prompt. For example:

```[You]: "Explain how Zevid manipulates the elite using their own biotechnology in the rebellion."```

This ensures that the assistant treats the entire input as one argument rather than splitting it into separate terms.

**Bonus!** The assistant is pre-loaded with the full StoryCraftr documentation, so you can ask it about any command or feature. For example, if you need help with a specific command:

```[You]: "Show me how to use the insert-chapter command and its parameters."```

This will provide you with clear guidance directly within the chat, ensuring you have everything you need to use StoryCraftr to its full potential!


## Overview

The **Chat** feature in **StoryCraftr** allows you to interact directly with the AI assistant to brainstorm ideas, refine content, or improve any aspect of your book in real time. The feature includes the ability to prompt specific commands related to story development, iterative refinement, and world-building, all from within the chat environment. This guide will help you get started with using the chat feature effectively.

## Getting Started with Chat

Before you can use the chat feature, ensure that you have **StoryCraftr** installed and that your book project is initialized. Once your project is ready, you can start a chat session with this command:

```bash
storycraftr chat --book-path /path/to/your/book
```

### Example:

```bash
storycraftr chat --book-path ~/projects/la-purga-de-los-dioses
```

Once the session starts, you’ll be able to type messages to the assistant and receive responses directly in your terminal.

## Available Commands within Chat

While in a chat session, you can use commands to quickly execute tasks that StoryCraftr supports, such as refining your outline, improving chapters, or updating your world-building. These commands provide flexibility, allowing you to iterate on various aspects of your novel without leaving the chat.

### Command Examples

You can trigger the following commands within the chat by typing the appropriate prompt.

### **Iterate**: Refining the Story Iteratively

The **Iterate** commands are designed to help you iteratively improve the book's content. You can refine specific aspects such as character names, motivations, or plot points.

- **Check character names**:

  ```bash
  !iterate check-names "Check character names for consistency."
  ```

- **Refine character motivation**:

  ```bash
  !iterate refine-motivation "Refine character motivation for Zevid."
  ```

- **Check consistency**:

  ```bash
  !iterate check-consistency "Ensure consistency of character arcs and motivations."
  ```

- **Insert a chapter**:

  ```bash
  !iterate insert-chapter 3 "Insert a chapter about Zevid's backstory between chapters 2 and 3."
  ```

### **Outline**: Outlining the Book

The **Outline** commands help you generate or refine various components of your book's outline, including character summaries, plot points, or the entire general outline.

- **General outline**:

  ```bash
  !outline general-outline "Summarize the overall plot of a dystopian sci-fi novel."
  ```

- **Plot points**:

  ```bash
  !outline plot-points "Identify key plot points in the story."
  ```

- **Character summary**:

  ```bash
  !outline character-summary "Summarize Zevid’s character."
  ```

- **Chapter synopsis**:

  ```bash
  !outline chapter-synopsis "Outline each chapter of a dystopian society."
  ```

### **Worldbuilding**: Building the World of Your Story

With **Worldbuilding** commands, you can flesh out various aspects of your story's world, such as the history, culture, and even the "magic" system (which could be advanced technology in disguise).

- **History**:

  ```bash
  !worldbuilding history "Describe the history of a dystopian world."
  ```

- **Geography**:

  ```bash
  !worldbuilding geography "Describe the geography of a dystopian society."
  ```

- **Culture**:

  ```bash
  !worldbuilding culture "Describe the culture of a society controlled by an elite class."
  ```

- **Technology**:

  ```bash
  !worldbuilding technology "Describe the advanced biotechnology mistaken for magic."
  ```

- **Magic system**:

  ```bash
  !worldbuilding magic-system "Describe the 'magic' system based on advanced technology."
  ```

### **Chapters**: Managing and Writing Specific Chapters

The **Chapters** commands focus on generating or improving specific chapters of your book. You can also create cover and back-cover text for your novel using this command group.

- **Generate a chapter**:

  ```bash
  !chapters chapter 1 "Write chapter 1 based on the synopsis provided."
  ```

- **Insert a chapter**:

  ```bash
  !chapters insert-chapter 5 "Insert a chapter revealing Zevid’s manipulation."
  ```

- **Generate cover text**:

  ```bash
  !chapters cover "Generate the cover text for the novel."
  ```

- **Generate back-cover text**:

  ```bash
  !chapters back-cover "Generate the back-cover text for the novel."
  ```

## Exiting the Chat

When you're ready to exit the chat, simply type:

```bash
exit()
```

This will end the chat session and return you to the terminal.

## Conclusion

The **StoryCraftr Chat** feature, combined with powerful commands like **Iterate**, **Outline**, **Worldbuilding**, and **Chapters**, provides you with everything you need to write your book efficiently. Whether you are refining existing content or generating new chapters, this feature allows you to enhance your creative process with ease.

---

Happy writing with **StoryCraftr** and its powerful chat feature! ✍️✨
