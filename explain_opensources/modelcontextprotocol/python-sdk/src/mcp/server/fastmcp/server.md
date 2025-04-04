# FastMCP
- Answer the question "What exactly is the FastMCP server?"
- Analyse from the flow of the samples code aka "reversed analysis"

## __init__
### Arguments
- name
    - To name server (MCPServer)
    - To define property name of server
- instructions
    - To describe server (MCPServer)
    - To give more contexts for clients (LLMs understanding)
    - To define property instructions of server
- settings
    - To set up server (Settings)
    - To define lifespan of server
    - To warn when tools/resources/prompts are duplicated
    - To declare dependencies of server (install when building server)
    - To set log level of server
    - To configure host, port, log level of uvicorn (uvicorn.Config)
    - To form ASGI app
        - To define a route for handling SSE
        - To handle incoming messages from clients
        - To set debug mode of the app
### Instance attributes
- settings
    - Read settings above
- _mcp_server (private attribute)
    - To encapsulate the core functionality of the MCP server
    - To expose attributes via properties for user friendly access while keeping the low-level details encapsulated
    - To set up core MCP protocol handlers
    - To set request context
    - To run server using stdio transport
    - To handle sse messages
    - To create initialization options
- _tool_manager (private attribute)
    - To list/call/add tools
- _resource_manager (private attribute)
    - To list/get/add resources/templates
- _prompt_manager (private attribute)
    - To list/get/add prompts
- dependencies (private attribute)
    - To install dependencies (by uv)
### Method calls
- _setup_handlers
### Function calls
- configure_logging
    - Configure logging

## _setup_handlers
- responsible for registering high-level handler methods (defined in FastMCP) with the underlying MCPServer instance (self._mcp_server). These handlers define how the server responds to specific protocol operations, such as listing tools, calling tools, managing resources, and handling prompts
- Registers the self.list_tools method as the handler for the list tools operation in the MCPServer. When a client requests a list of tools, the list_tools method in FastMCP is invoked to generate the response.
### decorators
- The MCPServer class provides methods like list_tools, call_tool, etc., which return decorators or callable objects. These decorators are used to register the corresponding handler methods (self.list_tools, self.call_tool, etc.) in the MCPServer. Once registered, the MCPServer will invoke these handlers whenever a client sends a request for the corresponding operation
### Usages
- The _setup_handlers method is used to connect the high-level logic of the FastMCP class with the low-level protocol implementation in the MCPServer. Here are its primary use cases
- Protocol Handling:
    - Ensures that the FastMCP server can handle all core MCP protocol operations, such as managing tools, resources, and prompts.
- Custom Logic:
    - Allows developers to define custom logic for each operation by overriding the corresponding methods in the FastMCP class (e.g., list_tools, call_tool).
- Extensibility:
    - Makes it easy to extend the server's functionality by adding new handlers or modifying existing ones.
- Separation of Concerns:
    - Keeps the high-level logic (defined in FastMCP) separate from the low-level protocol implementation (handled by MCPServer).

## list_tools
- responsible for retrieving and returning a list of all tools registered with the server. Tools are functionalities or operations that the server can perform, and this method provides a way to expose them to clients in a structured format.
### Actions
- This is an asynchronous method, meaning it uses Python's async/await syntax to handle asynchronous operations without blocking the event loop
- The list_tools method of ToolManager retrieves a list of all registered tools. Each tool is likely represented by an object containing metadata about the tool (e.g., name, description, input schema)
- The method iterates over the list of tools returned by self._tool_manager.list_tools() and converts each tool into an MCPTool object

## call_tool
- execute a tool registered with the server by its name, passing the provided arguments
### Arguments
- name
    - name of tool to execute
- arguments
    - arguments to pass to the tool
### Actions
- retrieve the current request context. Ensures that the tool has access to the context during its execution.
- The call_tool method of the ToolManager (self._tool_manager) is invoked
- converts the result into a standardized format

## list_resources
- responsible for retrieving and returning a list of all resources registered with the server. Resources are entities that the server manages, such as files, data, or other content that can be accessed by clients.
### Actions
- retrieves the resources from the ResourceManager and formats them into a standardized structure (MCPResource) before returning them.

## list_resource_templates
- expose all resource templates managed by the server to clients
### Actions
- retrieves a list of all registered resource templates. Each template is likely represented by an object containing metadata such as its URI template, name, and description

## read_resource
- etrieving and reading the content of a resource identified by its URI
### Arguments
- uri
    - URI of the resource to read
### Actions
- retrieve the resource object
- The read method is asynchronous, allowing the server to handle other tasks while waiting for the resource to be read
### Raise errors
- ResourceError
    - Can not find any resources

## list_prompts
- retrieving and returning a list of all prompts registered with the server
### Actions
- retrieves a list of all registered prompts. Each prompt is likely represented by an object containing metadata such as its name, description, and arguments
- returns a list of MCPPrompt objects, each representing a prompt managed by the server

## get_prompt
- retrieve a specific prompt by its name and render it using the provided arguments
### Arguments
- name
    - name of the prompt to retrieve
- arguments
    - arguments to pass to the prompt
### Actions
- dynamically generates the prompt based on its template and the provided arguments

## get_context
### Actions
- Get request context from the server
### Raise erros
- LookupError
    - When context is not found

## properties
- name
    - To provide public interface to retrieve name of MCPServer
- instructions
    - To provide public interface to retrieve instructions of MCPServer

## run
### Arguments
- transport
    - To define transport protocal (support stdio and sse)
### Actions
- Run asynchronous method in an event loop  
### Raise errors
- ValueError
    - When transport is not supported

## run_stdio_async
### Actions
- Handle asynchronous operations without blocking the event loop by using async and await
- stdio_server is context manager sets up the standard input and output streams for communication
- `async with` ensures the streams are properly opened and closed when the context is exited
- Provide 2 streams
    - read_stream: A stream for reading incoming data (from stdin)
    - write_stream: A stream for writing outgoing data (to stdout)
- Create initialization options from this server instance
- Run the low level server

## run_sse_async
### Actions
- Handle asynchronous operations without blocking the event loop by using async and await
- create a Starlette application that serves as the SSE server. This application defines the HTTP routes and endpoints for handling SSE connections and related functionality.
- A Uvicorn configuration object is created to configure the server
- A Uvicorn server instance is created using the configuration object.
- start the server and handle incoming HTTP requests. This method runs the server asynchronously, allowing it to handle multiple connections concurrently

## sse_app
- Responsible for creating and returning a Starlette application configured to handle Server-Sent Events (SSE) and related HTTP routes. This application is used when the server is run using the SSE transport, enabling real-time communication between the server and clients over HTTP.
### Actions
- Creates an instance of SseServerTransport, which is responsible for managing SSE connections and handling messages sent to the server. This object encapsulates the logic for managing SSE connections and provides methods for handling incoming and outgoing data streams.
- Defines an asynchronous function to handle incoming SSE requests
    - Uses sse.connect_sse to establish an SSE connection with the client
    - Opens two streams:
        - streams[0]: Input stream for receiving data from the client.
        - streams[1]: Output stream for sending data to the client.
    - This function acts as the endpoint for the SSE connection, enabling real-time communication between the server and the client
- Creates a Starlette application with the following configuration
    - Debug mode
    - Defines the HTTP routes for the application
    - Mounts the sse.handle_post_message sub-application at the message_path (e.g., "/messages/"). This handles HTTP POST requests for sending messages to the server

## tool
- is a decorator used to register functions as tools in the server. 
- Tools are server-side functions that can be invoked by clients. 
- This decorator allows developers to define tools with optional metadata (e.g., name, description) and provides seamless integration with the server's context for logging, progress reporting, and resource access
### Arguments
- name
    - name of tool
- description
    - description of tool
### Decorator
- wraps the target function
- Registers the function as a tool using the add_tool method of the FastMCP class
- The add_tool method handles the logic for adding the tool to the server's internal registry
### Raise errors
- TypeError
    - if the user mistakenly applied the @tool decorator without calling it (e.g., @tool instead of @tool()).

## add_tool
- responsible for registering a function as a tool in the server
- Tools are server-side functions that can be invoked by clients.
- This method is typically used internally by the @tool decorator to add tools to the server's registry.
### Arguments
- fn
    - The function to register as a tool
- name
    - Optional name for the tool (defaults to function name)
- description
    - Optional description of what the tool does
### Actions
- add the tool to the server's internal registry.

## resource
- register a function as a resource in the server
- This decorator supports both static and template-based resources, allowing for flexible and dynamic resource management
### Arguments
- uri
    - The URI for the resource (e.g., "resource://my-resource" or "resource://{param}").
    - If the URI contains placeholders (e.g., {param}), the resource is treated as a template.
- name
    - The name of the resource
- description
    - A description of the resource
- mime_type
    - The MIME type of the resource content
### Decorator
- checks if the resource should be treated as a template
- If the resource is a template, the method validates that the URI parameters match the function parameters:
    - Extracts URI parameters using a regular expression (re.findall).
    - Compares URI parameters with function parameters using inspect.signature.
    - If there is a mismatch, a ValueError is raised.
    - Register as template by using resource manager
- Otherwise
    - register as regular resource by creating a object
    - Use class method to register resource (that acutally register resource by using resource manager)
### Raise errors
- TypeError
    - If the decorator is used incorrectly (e.g., @resource instead of @resource('uri')), a TypeError is raised with a helpful error message.
- ValueError
    - If the URI template parameters do not match the function parameters, a ValueError is raised.

## add_resource
### Arguments
- resource
### Actions
- Use resource manager to add resource

## prompt
- register a function as a prompt in the server
- Prompts are predefined templates or instructions that can be dynamically generated and returned to clients
- This decorator simplifies the process of defining prompts and integrates them into the server's prompt management system.
### Arguments
- name
    - The name of the prompt
- description
    - A description of the prompt
### Actions
- create a Prompt object from the function
- register the Prompt object with the server's prompt manager
### Raise errors
- TypeError
    - If the decorator is used incorrectly (e.g., @prompt instead of @prompt('name')), a TypeError is raised with a helpful error message.

## add_prompt
### Arguments
- prompt
    - A Prompt instance to be registered with the server
### Actions
- Use prompt manager to add prompt

# lifespan_wrapper
- a utility function that wraps a custom lifespan context manager for the server
- It ensures that the custom lifespan logic is properly integrated with the server's lifecycle, allowing developers to define custom startup and shutdown behavior for the server
## Arguments
- app
    - The FastMCP server instance for which the lifespan is being wrapped.
    - This allows the custom lifespan to access the server instance and its settings
- lifespan 
    - A callable that defines the custom lifespan logic.
    - It takes the FastMCP instance as input and returns an asynchronous context manager
## wrap
- The wrap function is an asynchronous context manager that integrates the custom lifespan with the MCPServer
- Executes the custom lifespan logic, passing the FastMCP instance (app) to it
- The context returned by the custom lifespan is yielded to the MCPServer
- Passes the lifespan's context to the MCPServer, allowing it to manage the server's lifecycle
## Usages
- Custom Lifespan Management
    - Developers can define custom startup and shutdown logic for the server using a lifespan context manager.
- Wrapping the Lifespan for MCPServer
    - The lifespan_wrapper function is used internally by the FastMCP class to wrap the custom lifespan and pass it to the MCPServer
- Managing Server Lifecycle
    - The lifespan_wrapper ensures that the custom lifespan logic is executed during the server's startup and shutdown phases.
    - Example:
        - During startup, the custom lifespan logic is executed before the server starts handling requests.
        - During shutdown, the custom lifespan logic is executed after the server stops handling requests.
## What are usages of Callable and AbstractAsyncContextManager
- The Callable type hint specifies that the lifespan parameter must be a function that takes specific arguments and returns a certain type.
- Callable[[FastMCP], AbstractAsyncContextManager[LifespanResultT]] means:
    - The lifespan parameter must be a callable (function) that:
    - Takes a single argument of type FastMCP.
    - Returns an AbstractAsyncContextManager object that manages an asynchronous context with a generic type LifespanResultT (likely the result of some lifecycle-related operation).
- AbstractAsyncContextManager [from contextlib]:
    - An AbstractAsyncContextManager is part of Python's asynchronous context management system. It represents objects that can be used in async with blocks to manage asynchronous resources.
    - It means that the function is expected to return an asynchronous context manager that can yield a result of type LifespanResultT when used with async with

# _convert_to_content
- the result of a tool or resource is converted into a standardized format that can be sent to clients
## Arguments
- result
    - The result of a tool or resource operation
## Actions
- Converts various result types into a sequence of TextContent, ImageContent, or EmbeddedResource objects
- Supports mixed content by handling lists or tuples containing mixed content types
- Converts custom objects to JSON or string representations

# Settings
- defines the configuration settings for the server. 
- It uses Pydantic's BaseSettings to enable easy configuration via environment variables, .env files, or directly in code. 
- This class provides a structured way to manage server settings, including debugging, logging, HTTP configuration, and resource/tool/prompt management
## Parent classes
- BaseSettings
- Generic
## Attributes
- The Settings class centralizes all configuration options for the FastMCP server.
- It allows settings to be configured via:
    - Environment variables (with the prefix FASTMCP_).
    - A .env file.
    - Directly in code when initializing the FastMCP server.
- Server Settings
    - debug
    - log_level
    - http settings (host, port, sse_path, message_path)
    - warning duplicated tools/resources/prompts
    - dependencies
    - lifespan
        - A callable that defines a lifespan context manager for the server
        - A custom lifespan can be provided to manage server startup and shutdown logic

# Context
- used in various scenarios to provide access to the server's capabilities and request-specific metadata
- The Context class in the FastMCP server provides a structured interface for accessing request-specific data and server capabilities during the execution of tools, resources, or other server-side operations. It is injected into tool and resource functions when requested via type annotations, enabling developers to interact with the server's features such as logging, progress reporting, and resource access.
- The Context class is a utility wrapper around the RequestContext and FastMCP server. It simplifies access to common MCP server functionalities and enforces proper usage within the scope of a request. Its design promotes clean and modular tool and resource functions by abstracting away low-level details. 
## Parent classes
- BaseModel
- Generic
    - ServerSessionT
    - LifespanContextT
## Private attributes
- _request_context
    - Contain metadata and session information about the current request
- _fastmcp
    - Holds a reference to the FastMCP server instance.
## __init__
### Arguments
- request_context
    - Read _request_context above 
- fastmcp
    - Read _fastmcp above
- kwargs
## properties
### fastmcp
- Provide access to private attribute _fastmcp
### request_context
- Provide access to private attribute _request_context
### client_id
- Retrieves the client ID from the request metadata, if available
### request_id
- Retrieves the unique ID for the current request
### session
- Provides access to the underlying session object for advanced usage.
## report_progress
### Arguments
- progress
    - The current progress value
- total
    - The optional total value
### Actions
- Uses the progressToken from the request metadata to send a progress notification via the session
## read_resource
### Arguments
- uri
    - The URI of the resource to read
### Actions
- Reads a resource by its URI using the FastMCP server instance.
## log
### Arguments
- level
    - log level
- message
    - log message
- logger_name
    - The name of the logger to use
### Actions
- Sends a log message to the client at the specified log level
## debug/info/warning/error
### Arguments
- message
    - log message
### Actions
- Sends a debug/info/warning/error-level log message