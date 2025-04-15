# Prompt
- represents a template for prompts that can be rendered with parameters
- It encapsulates the logic for defining, validating, and rendering prompts

## Class attributes
- name
    - The name of the prompt, used to identify it.
- description
    - An optional description of what the prompt does.
- arguments
    - A list of PromptArgument objects, each representing an argument that can be passed to the prompt.
- fn
    - A callable function that defines the behavior of the prompt.

## from function
- a factory method that creates a Prompt instance from a callable function. It encapsulates the logic for extracting metadata from the function and converting it into a structured Prompt object. 
### Arguments
- cls
- fn
- name
- description
### Actions
- The method uses TypeAdapter(fn).json_schema() to extract the function's parameter schema. This ensures that the function is properly typed and provides metadata about its parameters.
- Convert Parameters to PromptArgument
- wraps the callable to ensure that it adheres to its type annotations. This guarantees that the function is called with valid arguments.
- The Prompt instance is returned.
### Explaination of solution
- Dynamic Prompt Creation:
    - The from_function method allows developers to dynamically create prompts from existing functions. This reduces boilerplate code and makes it easier to integrate prompts into the system.
- Type Safety
    - By using TypeAdapter and validate_call, the method ensures that the function's parameters and return types are properly validated. This prevents runtime errors caused by invalid arguments or return values.
- Support for Metadata:
    - The method extracts metadata (e.g., parameter descriptions, required fields) from the function's schema. This makes the resulting Prompt object self-documenting and easier to use.
- Reusability:
    - By wrapping existing functions, the method promotes reusability. Developers can define prompts using standard Python functions without needing to manually create Prompt objects.
- Flexibility:
    - The method supports both synchronous and asynchronous functions, making it adaptable to various use cases.
- Consistency:
    - The method enforces a consistent structure for all prompts, ensuring that they adhere to the same interface and validation rules.

## render
- rendering a prompt by executing its associated function (fn) with the provided arguments and converting the result into a list of Message objects
### Arguments
- arguments
### Actions
- Validation of Required Arguments:
    - Ensures that the Prompt is executed with all necessary inputs, preventing runtime errors caused by missing arguments.
Provides clear error messages to help developers or users identify and fix issues.
- Support for Asynchronous Functions:
    - By checking if the result is a coroutine and awaiting it, the method supports both synchronous and asynchronous prompt functions. This makes the system flexible and suitable for various use cases (e.g., API calls, database queries).
- Normalization of Results:
    - Wrapping non-list results in a list ensures that the method always processes a consistent data structure. This simplifies downstream logic and reduces edge cases.
- Flexible Result Handling:
    - The method supports multiple result types (e.g., Message, dictionary, string, or JSON-serializable objects). This flexibility allows prompt functions to return outputs in the most convenient format for their implementation.
- Error Handling During Conversion:
    - By validating and converting each item in the result, the method ensures that the final output is always a list of valid Message objects.
    - Clear error messages help identify issues with specific items in the result.
- Encapsulation of Rendering Logic:
    - The render method encapsulates all the logic for executing the prompt function, validating inputs, and converting outputs. This keeps the Prompt class self-contained and easy to use.
- Type Safety and Validation:
    - The use of Pydantic models (Message, TextContent, etc.) ensures that all inputs and outputs are properly validated, reducing the likelihood of runtime errors

# Message/UserMessage/AssistantMessage
- define the structure and behavior of messages exchanged between users and assistants in the context of prompts
## Explaination of solution
- Inheritance for Code Reuse:
    - The UserMessage and AssistantMessage classes inherit from the Message base class to avoid duplicating common attributes and behavior.
    - This ensures that any changes to the shared logic (e.g., handling content) only need to be made in one place.
- Role-Specific Behavior:
    - The role attribute is overridden in UserMessage and AssistantMessage to enforce role-specific behavior. This ensures that each message type is clearly associated with its sender.
- Automatic Content Normalization:
    - The Message class constructor automatically converts string content into a TextContent object. This simplifies the handling of message content by ensuring it is always in a consistent format.
- Type Safety with Literal and CONTENT_TYPES:
    - The use of Literal for the role attribute ensures that only valid roles ("user" or "assistant") can be assigned.
    - The CONTENT_TYPES type alias enforces that the content attribute is one of the predefined types (TextContent, ImageContent, or EmbeddedResource).
- Extensibility:
    - The design allows for easy extension. For example, additional message types (e.g., SystemMessage) can be added by inheriting from the Message class and overriding the role attribute.
- Integration with Pydantic:
    - By inheriting from BaseModel, the classes benefit from Pydantic's validation and serialization features. This ensures that messages are always valid and can be easily converted to/from JSON.
- Separation of Concerns:
    - The Message class handles shared logic, while UserMessage and AssistantMessage focus on role-specific behavior. This separation makes the code easier to understand and maintain

# PromptArgument
- Encapsulation of Argument Metadata:
    - The PromptArgument class encapsulates all metadata related to a single argument, such as its name, description, and whether it is required. This makes the arguments self-contained and easy to manage.
- Type Safety:
    - This prevents invalid data from being passed to prompts.
- Optional Description:
    - The description field is optional, allowing developers to provide additional context for arguments without making it mandatory. This balances flexibility and usability.
- Default Value for required:
    - The required field defaults to False, making arguments optional by default. This reduces the need for explicit configuration unless an argument is mandatory.
- Integration with Prompts:
    - The PromptArgument class is designed to work seamlessly with the Prompt class. For example:
    -The from_function method in Prompt converts function parameters into PromptArgument instances.
    - The render method validates required arguments using the required field.
- Documentation and Schema Generation:
    - The use of Field descriptions ensures that the class is self-documenting. This is particularly useful for generating API documentation or schemas.

# message_validator
- Validation and Parsing:
    - Ensures that raw data (e.g., dictionaries) can be safely converted into UserMessage or AssistantMessage objects.
    - Centralizes validation logic, reducing duplication and ensuring consistency.
- Flexibility:
    - Allows the system to handle various input formats (e.g., raw dictionaries, JSON) while maintaining strict type safety.
- Error Handling:
    - If the input data is invalid, the TypeAdapter raises clear validation errors, making debugging easier.

# SyncPromptResult
- Flexibility in Return Types:
    - Allows prompt functions to return results in the most convenient format for their implementation.
    - Supports single values (e.g., a string or Message) as well as sequences, making it easy to handle both simple and complex outputs.
- Standardization:
    - Although multiple formats are allowed, the render method in the Prompt class normalizes all results into a list of Message objects. This ensures consistency in how results are processed.

# PromptResult
- Support for Asynchronous Workflows:
    - Many modern applications involve asynchronous operations (e.g., API calls, database queries). By supporting Awaitable results, PromptResult ensures compatibility with these workflows.
- Backward Compatibility:
    - By including SyncPromptResult, the system remains compatible with synchronous prompt functions, allowing developers to choose the approach that best suits their needs.
- Ease of Integration:
    - The unified type alias simplifies type annotations and ensures that all prompt functions adhere to a consistent interface.
