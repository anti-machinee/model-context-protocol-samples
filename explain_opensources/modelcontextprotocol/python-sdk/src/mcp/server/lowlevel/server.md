# Server

## Parent class
- Generic
    - LifespanResultT

## __init__
### Arguments
- name
    - name of server
- version
    - version of server
- instructions
    - instructions for server used for LLM
- lifespan
    - A callable that defines the server's lifespan context manager
### Attributes
- request_handlers
    -  A dictionary mapping request types to their respective handlers. It includes a default handler for PingRequest.
- notification_handlers
    - A dictionary mapping notification types to their respective handlers
- notification_options
    - Stores options for notifications (e.g., whether prompts, resources, or tools have changed).

## Properties
### request_context
- provides access to the current request context for the server
- If called outside of a request context, this will raise a LookupError
## create_initialization_options
- generating an InitializationOptions object, which encapsulates the server's metadata, capabilities, and instructions. Here's a detailed breakdown of its logic
### Arguments
- notification_options
    - An optional NotificationOptions object that specifies which notifications (e.g., prompts, resources, tools) have changed
- experimental_capabilities
    - An optional dictionary of experimental capabilities that the server supports
### pkg_version
#### Arguments
- package
    - This function retrieves the version of a given Python package
### Actions
- The get_capabilities method generates a ServerCapabilities object based on the server's registered request handler
### Usages
- The create_initialization_options method is typically called during the server's initialization phase to generate the InitializationOptions object

## get_capabilities
### Arguments
- notification_options
    - Read above
- experimental_capabilities
    - Read above
### Actions
- checks whether specific request handlers are registered in self.request_handlers
    - prompt
    - resource
    - tool
    - logging
- If a handler exists, it creates the corresponding capability object.
### Usages
- dynamically generates a ServerCapabilities object based on the server's registered request handlers, notification options, and experimental capabilities. It ensures that the server's capabilities are accurately communicated to the client during initialization. This modular design allows the server to adapt its capabilities based on the registered handlers and configuration

## list_prompts
### decorator
#### Arguments
- func
    - The function to be decorated
#### Actions
- The handler function is registered in the self.request_handlers dictionary under the key types.ListPromptsRequest
### handler
#### Actions
- Calls the original handler function (func) to retrieve the list of prompts
- Wraps the result in a types.ListPromptsResult object.
- Returns the result as a types.ServerResult.
### Usages
- Logs the registration of the handler.
- Wraps the original handler function in a wrapper (handler) that formats the result as a types.ServerResult.
- Registers the wrapper in the self.request_handlers dictionary.

## get_prompt
- Same as previous methods

## list_resources
- Same as previous methods

## read_resource
### decorator
#### Arguments
- func
    - The function to be decorated
#### Actions
- The handler function is registered in the self.request_handlers dictionary under the key types.ReadResourceRequest
### handler
#### Actions
- Extracts the uri from the request parameters (req.params.uri).
- Calls the original handler function (func) with the uri to retrieve the resource contents.
### create_content
#### Actions
- Converts the resource content (data) into a structured format
### Usages
- Read above

## set_logging_level
- Same as previous methods

## subscribe_resource
- Same as previous methods

## unsubscribe_resource
- Same as previous methods

## list_tools
- Same as previous methods

## call_tool
- Same as previous methods
### Try except
- Handles errors gracefully by returning an error response if the tool invocation fails.

## progress_notification
- Same as previous methods

## completion
- Same as previous methods

## run
### Arguments
- read_stream
    - A stream for receiving messages from the client.
- write_stream
    - A stream for sending messages to the client.
- initialization_options
    - An InitializationOptions object containing server metadata, capabilities, and instructions
- raise_exceptions
    - A boolean flag that determines how exceptions are handled:
        - If True, exceptions are raised, causing the server to shut down (useful for debugging or testing).
        - If False, exceptions are returned as error messages to the client.
### Actions
- allows the server to manage resources or perform setup/teardown tasks during its lifecycle
- The session manages incoming and outgoing messages using the provided read_stream and write_stream
- The session.incoming_messages stream is iterated over to receive messages from the client.
    - For each message:
        - A new task is started using tg.start_soon to handle the message asynchronously by calling the _handle_message method.
### Usages
- Manages the server's lifecycle using a lifespan context.
- Creates a session to handle communication with the client.
- Processes incoming messages (requests or notifications) asynchronously.
- Handles exceptions gracefully, depending on the raise_exceptions flag.

## _handle_message
### Arguments
- message
    - The incoming message to be processed
- session
    - The ServerSession object managing communication with the client.
- lifespan_context
    - The context object for the server's lifespan, used to manage resources or state during the server's runtime.
- raise_exceptions
    - A boolean flag that determines how exceptions are handled:
        - If True, exceptions are raised, causing the server to shut down (useful for debugging or testing).
        - If False, exceptions are logged or returned as error messages to the client.
### Actions
- Captures any warnings that occur during message processing.
- These warnings are logged at the end of the method
- Uses a match statement to determine the type of the incoming message.
- If the message is a RequestResponder containing a ClientRequest:
    - The responder object is used to manage the request-response lifecycle.
    - The _handle_request method is called to process the request.
- If the message is a ClientNotification:
The _handle_notification method is called to process the notification.
- Iterates over any warnings captured during message processing.
Logs each warning with its category and message.
### Usages
- Identifies the type of the incoming message (request, notification, or exception).
- Dispatches the message to the appropriate handler (_handle_request or _handle_notification).
- Logs any warnings that occur during message processing.

## _handle_request
### Arguments
- message
    - A RequestResponder object that represents the client request and manages the request-response lifecycle.
- req
    - The actual request object sent by the client.
- session
    - The ServerSession object managing communication with the client.
- lifespan_context
    - The context object for the server's lifespan, used to manage resources or state during the server's runtime.
- raise_exceptions
    - A boolean flag that determines how exceptions are handled:
        - If True, exceptions are raised, causing the server to shut down (useful for debugging or testing).
        - If False, exceptions are caught and returned as error responses to the client.
### Actions
- Retrieves the handler function for the request type.
- Sets the global request_ctx variable to allow the handler to access request-specific information (e.g., request ID, metadata, session, lifespan context).
- Calls the handler function with the request object and awaits its response.
- Handle errors
### Usages
- Identifies the type of the request and dispatches it to the appropriate handler.
- Manages the request context using request_ctx.
- Handles errors gracefully, either by raising them or returning error responses.
- Sends the response back to the client.

## _handle_notification
### Arguments
- notify
    - The incoming notification object sent by the client.
    - Its type determines which handler will process it.
### Actions
- Retrieves the handler function for the notification type from the self.notification_handlers dictionary.
- Calls the handler function with the notification object and awaits its completion
- Handle errors
### Usages
- Identifies the type of the notification.
- Dispatches the notification to the appropriate handler.
- Logs any exceptions that occur during the processing of the notification.

## _ping_handler
### Arguments
- request
    - TODO
### Actions
- The server responds with an empty result ({}), indicating that it is operational.
### Usages
- Responds to a "ping" request from the client.
- Returns an empty result (EmptyResult) wrapped in a ServerResult.
- Is used for health checks or to verify that the server is running and responsive.

# lifespan
## Context manager
- The @asynccontextmanager decorator is used to define an asynchronous context manager.
- This allows the function to be used with async with statements.
## Arguments
- server
    - An instance of the Server class.
    - Represents the server whose lifecycle is being managed by this context manager.
## Actions
- The function yields an empty dictionary ({}) as the context object.
- This indicates that no specific resources or state are being managed by this default implementation.
## Usages
- Provides a mechanism to manage the server's lifecycle.
- Does nothing by default, yielding an empty context ({}).
- Can be overridden with custom logic to manage resources or perform setup/teardown tasks.

# NotificationOptions
## __init__
### Arguments
- prompts_changed
    - Bolean flag indicating whether prompts have changed
- resources_changed
    - Bolean flag indicating whether resources have changed
- tools_changed
    - Bolean flag indicating whether tools have changed
## Usages
- Encapsulates three boolean flags (prompts_changed, resources_changed, tools_changed).
Usages
- Is used during server initialization and capability generation to indicate changes.
Usages
- Provides a simple and structured way to manage state changes in the server's features
