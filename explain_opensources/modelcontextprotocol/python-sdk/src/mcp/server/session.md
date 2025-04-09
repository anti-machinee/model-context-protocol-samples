# ServerSession

## Usages
- to manage communication between a server and a client in the Model Context Protocol (MCP) framework.
- facilitates the exchange of requests, notifications, and responses between the two parties

## Parent classes
### BaseSession
- Define the specific types of requests, notifications, and results that the session will handle. This ensures type safety, improves code clarity, and allows for custom behavior tailored to the server's role in the MCP framework.

## Class private attributes
- _initialized
    - Tracks the current initialization state of the session
    - This attribute is updated during the session's lifecycle to reflect its current state
    - ensure that certain operations (e.g., handling requests or notifications) are only performed after the session is fully initialized
- _client_params
    - contains information about the client's capabilities, preferences, or other initialization-related data.
    - is populated when the server processes an initialization request from the client
    - can be accessed later to customize server behavior based on the client's initialization parameters
    - After initialization is complete, the server can use _client_params to
        - Check client capabilities.
        - Customize responses or behavior based on the client's preferences.

## __init__
### Arguments
- read_stream
    - is the input stream that receives messages (e.g., requests or notifications) from the client
- write_stream
    - is the output stream used to send messages (e.g., responses or notifications) to the client
- init_options
    - Contains server-specific initialization options, such as capabilities, server name, version, and instructions
    - Used to customize the server's behavior during the initialization process.
### Instance private attributes
- _initialization_state
    - Tracks the current state of the session's initialization process
    - It is updated during the session lifecycle
        - It transitions to InitializationState.Initializing when the server begins processing an initialization request.
        - It transitions to InitializationState.Initialized when the client sends an "Initialized" notification.
    - It is used to enforce that certain operations (e.g., handling requests or notifications) are only allowed after the session is fully initialized.
- _init_options
    - Read init_options above

## Properties
### client_params
- provides read-only access to the private attribute _client_params, which stores the initialization parameters sent by the client during the session's initialization process
- It allows other parts of the code to retrieve the client's initialization parameters without directly accessing the private _client_params attribute.
- How to set
    - The _client_params attribute is updated during the session's initialization process, specifically in the _received_request method
    - When the server receives an initialization request from the client, the _client_params attribute is populated with the client's initialization parameters

## check_client_capability
### Usages
- This method checks if the client supports the capabilities specified in the capability parameter. It compares the requested capabilities against the client's capabilities, which are stored in the _client_params attribute
### Arguments
- capability
    - specifies the capabilities to check for
### Actions
- Get client capabilities from initialization params
- Return Value
    - True: If the client supports all the specified capabilities.
    - False: If any of the specified capabilities are not supported by the client.

## _received_request
### Usages
- handling incoming client requests
### Arguments
- responder
    - An instance of RequestResponder that encapsulates the client's request and provides methods to send a response back to the client.
### Actions
- Handle InitializeRequest
    - Update _initialization_state to Initializing
    - The client's initialization parameters (params) are stored in _client_params
    - A response is sent back to the client with:
        - The protocol version.
        - The server's capabilities (from self._init_options.capabilities).
        - Server information (name and version).
        - Instructions for the client.
- Handle others\
    - For any request other than InitializeRequest, the method checks if the session is fully initialized (InitializationState.Initialized).
    - If the session is not initialized, a RuntimeError is raised.
    - Ensures that no requests are processed before the session is properly initialized.

## _received_notification
### Usages
- handling incoming notifications from the client
- The _received_notification method processes notifications sent by the client. Notifications are one-way messages that do not require a response. This method ensures that:
    - The session's state is updated when the client sends an InitializedNotification.
    - No notifications are processed before the session is fully initialized
### Arguments
- notification
    - notification is an instance of Notification that encapsulates the client's notification
### Actions
- ensures that the method yields control to the event loop, avoiding potential issues with asynchronous execution
- If the notification is of type InitializedNotification, the session's state is updated to InitializationState.Initialized
- For any notification other than InitializedNotification, the method checks if the session is fully initialized
    - If the session is not initialized, a RuntimeError is raised, indicating that the notification was received prematurely.

## send_log_message
### Usages
- sending log message notifications to the client
### Arguments
- level
    - Represents the severity or type of the log message (e.g., INFO, WARNING, ERROR).
    - This allows the client to categorize and handle the log message appropriately.
- data
    - The actual content of the log message. This could be a string, structured data, or any other information the server wants to log
- logger
    - The name of the logger that generated the message. This is useful for identifying the source of the log message, especially in complex systems with multiple loggers.
### Actions
- Form data and send the notification to the client

## send_resource_updated
### Usages
- sending a notification to the client when a resource has been updated
- notify the client that a specific resource has been updated
### Arguments
- uri
    - Represents the URI (Uniform Resource Identifier) of the resource that has been updated
    - This allows the client to identify which resource has changed.
### Actions
- Form data and send the notification to the client

## create_message
### Usages
- send a request to the client to generate a message based on the provided input parameters. This is typically used in scenarios where the server needs the client to perform some form of text generation or sampling
### Arguments
- messages
    - A list of messages (e.g., conversation history or context) that the client will use as input for generating the response.
- max_tokens
    - The maximum number of tokens the client should generate in the response.
- system_prompt
    - A system-level prompt that provides additional context or instructions for the client.
- include_context
    - Specifies whether and how the client should include additional context in the response.
- temperature
    - Controls the randomness of the generated response. Higher values result in more random outputs, while lower values make the output more deterministic.
- stop_sequences
    - A list of sequences that, if encountered, will cause the client to stop generating further tokens.
- metadata
    - Additional metadata that can be passed to the client for processing.
- model_preferences
    - Specifies preferences for the model to be used by the client.
### Actions
- Form data and send the request to the client

## list_roots
### Usages
- request a list of "roots" from the client. Roots typically represent the top-level entities or resources managed by the client, such as directories, projects, or other hierarchical structures
### Actions
- Form data and send the request to the client

## send_ping
### Usages
- check the connectivity or responsiveness of the client. It sends a lightweight "ping" request and expects an empty result (types.EmptyResult) in response. This is typically used for health checks or to ensure that the client is still active and reachable.
### Actions
- Form data and send the request to the client

## send_progress_notification
### Usages
- notify the client about the progress of a specific task or operation. This allows the client to track the progress of long-running or asynchronous tasks.
### Arguments
- progress_token
    - A unique identifier for the task or operation whose progress is being reported. This allows the client to associate the progress update with the correct task.
- progress
    - The current progress of the task, typically represented as a percentage (e.g., 0.5 for 50%).
- total
    - The total value representing 100% progress. If provided, the client can calculate the percentage progress using 
### Actions
- Form data and send the request to the client

## send_resource_list_changed
### Usages
- notify the client that the list of resources managed by the server has been updated.
### Actions
- Form data and send the request to the client

## send_tool_list_changed
### Usages
- notify the client that the list of tools available on the server has been updated. This allows the client to refresh its view of the tool list or take other appropriate actions.
### Actions
- Form data and send the request to the client

## send_prompt_list_changed
### Usages
- notify the client that the list of prompts available on the server has been updated. This allows the client to refresh its view of the prompt list or take other appropriate actions.
### Actions
- Form data and send the request to the client