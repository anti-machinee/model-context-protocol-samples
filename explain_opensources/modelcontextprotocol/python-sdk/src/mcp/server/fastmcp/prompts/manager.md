# PromptManager
- to manage and render prompts in the FastMCP framework. It provides functionality for adding, retrieving, listing, and rendering prompts

## __init_
- Using a dictionary provides efficient O(1) lookups for prompts by name.
- The warn_on_duplicate_prompts flag gives flexibility to control logging behavior, which is useful in different environments (e.g., development vs. production).
### Arguments
- warn_on_duplicate_prompts
    - Initializes the PromptManager with an empty dictionary (_prompts) to store prompts by their names.
### Instance attributes
- _prompts
- warn_on_duplicate_prompts
    - Allows enabling or disabling warnings for duplicate prompts using the warn_on_duplicate_prompts flag.

## get_prompt
- Retrieve a Prompt
### Arguments
- name
    - prompt name used in dictionary lookup
### Actions
- Retrieves a prompt by its name from the _prompts dictionary.
- Using dict.get() avoids raising a KeyError if the prompt is not found, making it safer to use.

## list_prompts
- Provides a way to enumerate all available prompts, which is useful for debugging, introspection, or displaying available options to users.
### Actions
- Returns a list of all registered prompts

## add_prompt
- Prevents accidental overwriting of existing prompts, which could lead to unexpected behavior.
- Logging warnings for duplicates helps developers identify potential issues during development.
- Returning the existing prompt ensures that the method is idempotent (i.e., calling it multiple times with the same prompt has no adverse effects)
### Arguments
- prompt
### Actions
- Adds a new prompt to the _prompts dictionary.
- If a prompt with the same name already exists:
    - Logs a warning (if warn_on_duplicate_prompts is enabled).
    - Returns the existing prompt instead of overwriting it.

## render_prompt
- rendering a specific prompt by its name, optionally using arguments provided by the caller
### Arguments
- name
    - prompt name
- arguments
    - making the method flexible for prompts that do not require additional arguments.
### Actions
- Get prompt by name
- Render prompt with arguments. Check base class for render method
