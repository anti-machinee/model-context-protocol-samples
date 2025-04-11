# SseServerTransport
- It provides a bidirectional communication channel between clients and servers using HTTP, where:
    - Server → Client: Uses SSE (Server-Sent Events) to push messages
    - Client → Server: Uses standard HTTP POST requests

## Class private attributes
### _endpoint
- This is set during the initialization of the SseServerTransport instance.
- It is used to construct the session-specific URI that is sent to the client when an SSE connection is established.
### _read_stream_writers
- manages the communication channels between clients and the server. It's a dictionary that maps session UUIDs to their corresponding memory object send streams

## __init__
### Arguments
- endpoint
    - Read _endpoint above
### Instance private attributes
- _endpoint
    - Read _endpoint above
- _read_stream_writers
    - Read _read_stream_writers above
### why need _endpoint and _read_stream_writers are private
- to follow the principle of encapsulation and to protect the integrity of the class's internal state
- Encapsulation
    - Encapsulation is a core principle of object-oriented programming that ensures internal implementation details are hidden from external access. By marking _endpoint and _read_stream_writers as private:
    - These attributes are treated as internal details of the SseServerTransport class.
    - External code cannot directly modify or access them, ensuring that the class's behavior remains predictable and controlled.
- Preventing Accidental Modification
    - _endpoint
        - Purpose: Stores the base URL or path where clients should send POST messages.
        - Why Private: If external code could modify _endpoint, it could break the functionality of the transport by pointing clients to an invalid or incorrect URL. The _endpoint is set once during initialization and should remain immutable throughout the lifetime of the SseServerTransport instance.
    - _read_stream_writers
        - Purpose: Tracks active sessions and their associated communication streams.
        - Why Private: If external code could modify _read_stream_writers, it could Corrupt the mapping of session IDs to streams. Remove or overwrite active streams, breaking communication for existing sessions. Introduce invalid or unauthorized session mappings, leading to security vulnerabilities.
- Protecting Data Integrity
    - Both _endpoint and _read_stream_writers are critical to the functionality of the SseServerTransport class:
        - _endpoint ensures that clients know where to send their POST messages.
        - _read_stream_writers ensures that messages are routed to the correct session.
    - Making these attributes private ensures that:
        - Only the methods of SseServerTransport can modify or access them.
        - The class can enforce validation and proper usage through controlled methods like connect_sse and handle_post_message
- Security
    - _endpoint: If _endpoint were public, external code could potentially expose sensitive information or redirect clients to malicious endpoints.
    - _read_stream_writers: If _read_stream_writers were public, external code could:
        - Access or manipulate active session streams, potentially hijacking or disrupting communication.
        - Introduce unauthorized session mappings, leading to security breaches.
    - By keeping these attributes private, the SseServerTransport class ensures that only authorized methods can interact with them, reducing the risk of security vulnerabilities.
- Implementation Flexibility
    - Marking _endpoint and _read_stream_writers as private allows the internal implementation of the SseServerTransport class to change without affecting external code. For example:
        - The _read_stream_writers dictionary could be replaced with a more complex data structure (e.g., a database or cache) in the future.
        - The _endpoint could be dynamically generated or validated internally.
        - Since these attributes are private, external code does not rely on their specific implementation, making the class easier to maintain and extend

## connect_sse
- sets up a bidirectional communication channel between the server and the client, enabling the server to send real-time updates to the client while also allowing the client to send messages back to the server via a separate POST endpoint
- Handles Incoming GET Requests: It processes HTTP GET requests to establish an SSE connection.
- Sets Up Bidirectional Communication:
    - Server-to-Client: Uses SSE to send messages from the server to the client.
    - Client-to-Server: Uses a memory stream to receive messages from the client.
- Manages Sessions: Creates a unique session ID for each connection and tracks it in _read_stream_writers.
### Arguments
- scope
- receive
- send
### sse_writer
#### Actions
- Defines an asynchronous function to handle server-to-client communication:
    - Sends the session URI to the client as an initial event.
    - Continuously reads messages from write_stream_reader and sends them to the client via SSE.
### Actions
- Ensures that the incoming request is an HTTP request. Logs an error and raises a ValueError if the request type is invalid.
- read_stream and read_stream_writer:
    - Used for client-to-server communication.
    - Messages sent by the client are written to read_stream_writer and read from read_stream.
- write_stream and write_stream_reader:
    - Used for server-to-client communication.
    - Messages sent by the server are written to write_stream and read from write_stream_reader.
- Generates a unique session ID using uuid4. Constructs a session-specific URI for the client to send POST messages. Stores the read_stream_writer in _read_stream_writers with the session ID as the key.
- Creates an EventSourceResponse to handle the SSE connection. Starts the SSE response task in a task group. Yields the read_stream and write_stream to allow the calling code to interact with the streams.
### Why this code does not assign value to variables (var: type)
- Type Annotations Only
    - The variables are declared with type annotations to specify the expected types of the variables.
    - This is a feature of Python's type hinting system introduced in PEP 484.
    - These annotations do not assign values; they only provide information about the type of data the variables will hold.
- Code Clarity:
    They make it clear what type of data the variables are expected to hold.
    This improves readability and helps other developers understand the code.
- Static Type Checking:
    - Tools like mypy or IDEs like PyCharm and VS Code can use these annotations to catch type-related errors before runtime.
- Documentation:
    - Type annotations serve as inline documentation, making it easier to understand the purpose of the variables.

## handle_post_message
- Is an ASGI application that handles incoming POST requests from clients
- Receiving Client Messages: Processes POST requests containing client messages.
- Session Validation: Ensures that the message is associated with a valid session.
- Message Validation: Parses and validates the incoming JSON-RPC message.
- Routing Messages: Sends the validated message to the appropriate session's stream for further processing.
### Arguments
- scope
- receive
- send
### Actions
- Wraps the ASGI scope and receive in a Request object for easier handling.
- Extract and Validate session_id
- Check for an Active Session
- Read and Validate the Message Body
- Route the Message to the Session
