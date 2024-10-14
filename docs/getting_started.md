# Getting Started with StoryCraftr 📚✨

**StoryCraftr** is a CLI tool designed to help you write your book using AI. Inspired by the writing techniques of [Brandon Sanderson's Laws of Magic and Writing](https://www.brandonsanderson.com/the-law-of-writing), this guide will walk you through creating a story from scratch. Whether you're outlining, building worlds, or writing chapters, StoryCraftr can assist you every step of the way.

Sanderson emphasizes strong **structure** and **rules for storytelling**, which we will follow throughout this guide. 

## Step 1: Install StoryCraftr

First, install **StoryCraftr** using Homebrew from the project's hosted tap:

```bash
brew install raestrada/tap/storycraftr
```

Once installed, you can run the tool using the command `storycraftr`.

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

3. **Initialize the book**: Clear **genre** and **structure** definition aligns with Sanderson’s emphasis on creating consistent rules for your world and plot ([Sanderson's First Law](https://www.brandonsanderson.com/sandersons-first-law/)).  
    ```bash
    storycraftr init "La Purga de los Dioses" --primary-language "es" --alternate-languages "en" --author "Rodrigo Estrada" --genre "science fiction" --behavior "default.txt"
    ```

## Step 3: Generate the Outline

According to Sanderson, **strong outlines** provide the scaffolding for a story, ensuring that it remains structured and engaging throughout. Let's build the outline for **La Purga de los Dioses**.

1. **Chapter-by-Chapter Synopsis**: This follows Sanderson's advice on **progressive complications**—setting up expectations and slowly building tension ([Sanderson's Second Law](https://www.brandonsanderson.com/sandersons-second-law/)).  
    ```bash
    storycraftr outline chapter_synopsis "Outline each chapter of a dystopian society where gods are purged from human memory." es
    ```

2. **Character Summary**: Strong characters are the core of a compelling story. This is consistent with Sanderson's approach to creating well-rounded characters and conflict ([Sanderson's First Law](https://www.brandonsanderson.com/sandersons-first-law/)).  
    ```bash
    storycraftr outline character_summary "Summarize the main characters of a story where humanity rebels against divine control." es
    ```

3. **General Outline**: A good general outline ensures that your story remains on course and your magic or technology systems are **consistent with the internal rules** ([Sanderson's First Law](https://www.brandonsanderson.com/sandersons-first-law/)).  
    ```bash
    storycraftr outline general_outline "Summarize the overall plot of a science fiction where gods no longer rule humanity." es
    ```

4. **Plot Points**: Identifying major plot points is crucial to creating meaningful **progression** and **revelation**, a principle Sanderson emphasizes in creating impactful stories ([Sanderson's Second Law](https://www.brandonsanderson.com/sandersons-second-law/)).  
    ```bash
    storycraftr outline plot_points "List the key plot points for a sci-fi rebellion against the gods." es
    ```

## Step 4: Build Your World

Sanderson’s [Laws of Magic](https://www.brandonsanderson.com/sandersons-first-law/) stress the importance of **rules** and **limitations** in a story's world. Here, we will develop a solid world for **La Purga de los Dioses**.

1. **Culture**: Establishing the cultural background of the world brings depth and richness to the setting, following Sanderson's idea that **limitations are more interesting than powers** ([Sanderson's Second Law](https://www.brandonsanderson.com/sandersons-second-law/)).  
    ```bash
    storycraftr worldbuilding culture "Describe the culture of a futuristic world where religion and faith have been outlawed." es
    ```

2. **Geography**: Geography plays a key role in worldbuilding, establishing settings that shape the characters and their journey, in line with Sanderson’s focus on **setting limitations** that challenge characters.  
    ```bash
    storycraftr worldbuilding geography "Describe the geography of a dystopian city controlled by technology after the fall of the gods." es
    ```

3. **History**: Sanderson advises **creating internal consistency** in your world's history to enrich the present and future of your story.  
    ```bash
    storycraftr worldbuilding history "Outline the history leading to the rebellion against the gods." es
    ```

4. **Magic System**: This will follow Sanderson’s **First Law**: "An author's ability to solve conflict with magic is directly proportional to how well the reader understands the magic." Defining rules early is crucial.  
    ```bash
    storycraftr worldbuilding magic_system "Describe the technology that replaced divine powers in the society." es
    ```

5. **Technology**: In line with Sanderson's advice on **restrictions**, the advanced technology in your world should have defined limits that drive the plot forward.  
    ```bash
    storycraftr worldbuilding technology "Describe the advanced technology that shapes everyday life in a post-divine world." es
    ```

## Step 5: Write Your Chapters

With a well-outlined story and a detailed world, we can now generate the chapters of **La Purga de los Dioses**. Sanderson’s principles of **progression** and **consistent conflict resolution** will guide us as we write.

1. **Generate the Cover**:  
    ```bash
    storycraftr chapters cover "Design a cover for a science fiction novel about the fall of the gods." es
    ```

2. **Generate the Back Cover**:  
    ```bash
    storycraftr chapters back_cover "Write a synopsis for the back cover of a sci-fi story where gods no longer exist." es
    ```

3. **Generate Chapter 1**: Starting strong with **character conflict** and **tension** is key to grabbing the reader’s attention.  
    ```bash
    storycraftr chapters chapter "Write the first chapter where the rebellion against the gods begins." es 1
    ```

4. **Continue writing additional chapters**: Follow Sanderson’s advice on **gradually increasing stakes** and building toward the climax.  
    ```bash
    storycraftr chapters chapter "Write the second chapter where the protagonist learns about the secret of the gods." es 2
    ```

5. **Generate the Epilogue**: Wrap up with **meaningful resolution** to tie together the themes and the characters' journey ([Sanderson's Third Law](https://www.brandonsanderson.com/sandersons-third-law/)).  
    ```bash
    storycraftr chapters epilogue "Write the epilogue where humanity starts rebuilding after the fall of the gods." es
    ```

## Step 6: Publish Your Book

StoryCraftr supports publishing your book to PDF, making it easy to share your work:

1. **Generate PDF**:  
    ```bash
    storycraftr publish pdf
    ```

## Step 7: Translate Your Book

If you initialized your book with alternate languages, you can translate the content automatically:

1. **Translate to Alternate Languages**:  
    ```bash
    storycraftr translate
    ```

## Learn More About Writing

The ideas in this tool are heavily inspired by [Brandon Sanderson’s Laws of Magic and Writing](https://www.brandonsanderson.com/the-law-of-writing). StoryCraftr is designed to help you implement these concepts while crafting well-structured stories with strong character arcs and consistent plot development.

---

Happy writing with **StoryCraftr**! ✍️
