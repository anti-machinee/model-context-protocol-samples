# BaseSession
## Usages
- Request/Response Handling:
    - Sends requests to the other party and waits for responses.
    - Links requests with their corresponding responses
- Notification Handling:
    - Sends one-way notifications that do not expect a response.
    - Processes incoming notifications.
- Progress Tracking:
    - Sends progress notifications for long-running tasks.
- Message Stream Management:
    - Manages incoming and outgoing message streams for asynchronous communication.
- Extensibility
    - Provides hooks (_received_request and _received_notification) for subclasses to handle specific requests and notifications

## Parent classes
- Generic 
    - These generic parameters allows the BaseSession class to be reused for both client and server implementations by specifying the appropriate types.

## Class private attributes
- _response_streams
    - Tracks response streams for requests that have been sent but not yet completed.
    - Maps a unique RequestId to a MemoryObjectSendStream that will receive the corresponding response (JSONRPCResponse) or error (JSONRPCError).
    - When a request is sent using send_request, a new response stream is created and stored in _response_streams with the request's ID
    - When a response or error is received, it is sent to the corresponding stream, allowing the send_request method to retrieve it.
- _request_id
    - Maintains a counter for generating unique IDs for outgoing requests.
    - Ensures that each request sent by the session has a unique identifier, which is used to link requests with their corresponding responses.
    - Incremented each time a new request is sent using send_request.
    -The current value is used as the RequestId for the outgoing request.
- _in_flight
    - Tracks requests that are currently being processed by the session.
    - Maps a RequestId to a RequestResponder object, which manages the lifecycle of the request (e.g., responding, canceling, or marking it as completed).
    - When a request is received, a RequestResponder is created and added to _in_flight.
    - When the request is completed (e.g., responded to or canceled), it is removed from _in_flight.

## __init__
### Arguments
- read_stream
    - A stream for receiving incoming messages (e.g., requests, notifications, or exceptions) from the other party (client or server)
- write_stream
    - A stream for sending outgoing messages (e.g., requests, notifications, or responses) to the other party.
- receive_request_type
    - Specifies the type of requests that the session will receive (e.g., ClientRequest or ServerRequest).
- receive_notification_type
    - Specifies the type of notifications that the session will receive (e.g., ClientNotification or ServerNotification)
- read_timeout_seconds
    - Specifies the timeout for reading messages from the read_stream. If None, reading will never time out.
### Instance private attributes
- _read_stream
    - read read_stream above
- _write_stream
    - read write_stream above
- _response_streams
    - Read _response_streams above
- _request_id
    - Read _response_streams above
- _receive_request_type/_receive_notification_type
    - Define the types of requests and notifications that the session will handle.
    - These types are used to validate incoming messages.
    - Incoming requests and notifications are validated against these types in _receive_loop
- _read_timeout_seconds
    - Specifies the timeout for reading messages from the read_stream.
    - If None, reading will never time out.
    - Used in send_request to enforce a timeout while waiting for a response.
_in_flight
    - Read _in_flight above
- _exit_stack
    - Manages cleanup of resources (e.g., closing streams) when the session is exited.
    - Ensures that all resources (e.g., streams) are properly closed when the session is no longer needed.
- _incoming_message_stream_writer/_incoming_message_stream_reader
    - A memory object stream for handling incoming messages (e.g., requests, notifications, or exceptions).
    - The writer is used to send messages into the stream, and the reader is used to consume them.
    - Messages are written to this stream in _receive_loop.\
    - Other parts of the session can read messages from this stream.
### Function calls
- push_async_callback
    - The purpose of this code is to ensure that the _incoming_message_stream_reader and _incoming_message_stream_writer are properly closed when the session is exited. This is part of resource management to prevent resource leaks and ensure that all streams are cleaned up when the session is no longer in use.
    - The _incoming_message_stream_writer and _incoming_message_stream_reader are created using anyio.create_memory_object_stream. These streams are used to handle incoming messages.
    - The aclose methods of the _incoming_message_stream_reader and _incoming_message_stream_writer are registered as cleanup callbacks using push_async_callback.
    - This ensures that when the session is exited (e.g., via __aexit__), these streams are closed automatically.
    - When the session is exited (e.g., using async with session:), the AsyncExitStack ensures that all registered cleanup callbacks are executed in reverse order, closing the streams.

## Properties
### incoming_messages
- Provide a unified interface for consuming incoming messages (requests, notifications, or exceptions) from the session.
- Allow asynchronous iteration over the stream of messages for processing
- Abstract the underlying _incoming_message_stream_reader, making it easier to interact with the session's message stream.

## __aenter__
- used to set up the session when it is entered using an async with statement.
### Actions
- Setting up a task group to manage asynchronous tasks within the session.
- Enters the task group context, allowing tasks to be started within the group.
- Starting the _receive_loop task, which continuously processes incoming messages from the read_stream
- Returning the session instance (self) so it can be used within the async with block

## __aexit__
- is part of the asynchronous context management protocol. It is used to clean up resources and gracefully shut down the session when it is exited using an async with statement
### Arguments
- exc_type/exc_val/exc_tb
    - Read anyio
### Actions
- Closes the AsyncExitStack, which manages the cleanup of resources registered during the session's lifecycle
- Cancels all tasks running in the task group.
    - Ensures that any ongoing tasks (e.g., the _receive_loop) are stopped when the session is exited.
- Exits the task group context, finalizing the cleanup of tasks.
    - Ensures that all tasks in the task group are properly cleaned up, even if an exception occurred during the session.

## send_request
### Arguments
- request
    - Represents the request to be sent to the other party
    - This is a structured object that contains the details of the request.
- result_type
    - Specifies the expected type of the response.
    - Used to validate and deserialize the response.
### Actions
- A unique request_id is generated for the request. This ID is used to link the request with its corresponding response.
- A memory object stream is created to handle the response for this specific request. The response_stream is stored in the _response_streams dictionary, keyed by the request_id.
- Cleanup callbacks are registered with the AsyncExitStack to ensure that the response stream is properly closed when the session is exited.
- The request is serialized into a JSON-RPC format and sent over the write_stream.
- The method waits for a response from the response_stream_reader. If a timeout occurs, an McpError is raised with a REQUEST_TIMEOUT error.
- If the response is a JSONRPCError, an McpError is raised with the error details. Otherwise, the response is validated and deserialized into the specified result_type, which is then returned.
### Raise errors
- If the response is not received within the specified timeout, an McpError is raised with a REQUEST_TIMEOUT error.

## send_notification
- send notifications, which are one-way messages that do not expect a response. Notifications are typically used to inform the other party about events or changes without requiring any acknowledgment or reply
### Arguments
- notification
    - Represents the notification to be sent.
    - This is a structured object that contains the details of the notification.
### Actions
- Serialize the Notification
- Send the Notification

## _send_response
- Sends a response (success or error) to a previously received request
- Ensures the response is formatted according to the JSON-RPC 2.0 specification.
### Arguments
- request_id
    - The unique identifier of the request for which the response is being sent. This ID links the response to the original request.
- response
    - The response to be sent.
### Actions
- Check the Response Type
- Handle Error Responses
- Handle Successful Responses

## _receive_loop
- is responsible for continuously processing incoming messages from the read_stream. It handles requests, notifications, responses, and exceptions, routing them appropriately for further processing
- 
### Actions
- Ensures that the read_stream, write_stream, and incoming_message_stream_writer are properly managed and closed when the loop exits.
- Continuously reads messages from the read_stream. Each message is processed based on its type.
- If the message is an exception, it is forwarded to the incoming_message_stream_writer for further handling
- Handling Requests
    - Validates the request using the receive_request_type.
    - Creates a RequestResponder to manage the request lifecycle.
    - Calls _received_request to allow subclasses to handle the request directly.
    - If the request is not completed, it is forwarded to the incoming_message_stream_writer.
- Handling Notifications
    - Validates the notification using the receive_notification_type.
    - Handles cancellation notifications by canceling the corresponding in-flight request.
    - Calls _received_notification to allow subclasses to handle the notification directly.
    - Forwards the notification to the incoming_message_stream_writer
- Handling Responses
    - Matches the response to its corresponding request using _response_streams.
    - Sends the response to the appropriate stream.
    - If the response ID is unknown, forwards an error to the incoming_message_stream_writer.

## _received_request
- Provides a hook for subclasses to handle requests directly.
- Enables custom request handling logic in derived classes.
### Arguments
- responder

## _received_notification
- Provides a hook for subclasses to handle notification directly.
- Enables custom request handling logic in derived classes.
### Arguments
- notification

## send_progress_notification
- Provides a hook for subclasses to handle notification directly.
- Enables custom request handling logic in derived classes.
### Arguments
- progress_token
- progress
- total
