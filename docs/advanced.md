## Advanced Usage of StoryCraftr

StoryCraftr provides advanced features for users who want more control over how the tool interacts with their projects. This guide will walk you through these features, including multi-prompt responses, file backups, and the `reload-files` command.

### Multiple Prompts Feature

By default, StoryCraftr uses **multiple prompts** when generating or refining content. This feature allows for more detailed and comprehensive outputs by breaking the response into parts and requesting confirmation before continuing. If you prefer a single, uninterrupted response, you can disable this feature by editing the `storycraftr.json` configuration file.

In your `storycraftr.json` file:

```json
{
  "multiple_answer": false
}
```

With `multiple_answer` set to `false`, StoryCraftr will generate a single, complete response for any prompt, without dividing it into sections.

### Backup Files

StoryCraftr automatically creates backups of any files it modifies. These backup files have a `.back` extension and are created in the same directory as the original file. This feature ensures that you always have a copy of your previous work and can easily revert to a previous state if needed.

For example, if you run a command to generate or refine a chapter, StoryCraftr will create a backup of the current file before making any changes:

```
chapters/chapter_1.md
chapters/chapter_1.md.back
```

The backup file allows you to compare the before and after states or recover content if needed.

### Reload Files with `storycraftr reload-files`

The **`reload-files`** command is a powerful feature that allows you to synchronize your local content with the retrieval system used by StoryCraftr. This ensures that any recent changes you've made are correctly picked up by the assistant, enhancing its understanding of your story before you execute additional commands.

#### Example Usage:

```bash
storycraftr reload-files --book-path "path/to/your/book"
```

This command will:

- **Re-sync all content**: It updates the assistant's context to reflect any new or edited content in your project.
- **Overwrite current agent files**: All agent files will be overwritten, ensuring the latest versions are used for retrieval during prompts.

### When to Use `reload-files`

- **After Manual Edits**: If you've made manual changes to the markdown files within your book project, use `reload-files` to ensure these changes are understood by StoryCraftr before running new commands.
- **After Deleting Content**: If you delete any sections or chapters, running `reload-files` will help StoryCraftr adapt to the new structure of your project, avoiding references to content that no longer exists.

### Summary

- **Multiple Prompts**: Enabled by default, but can be turned off for a single-response output.
- **Backup Files**: Automatically generated with a `.back` extension for every modified file.
- **Reload Files**: Use `storycraftr reload-files` to update the assistant's context after making manual changes.

These advanced features provide greater control over your workflow and ensure that your project evolves smoothly and consistently.
