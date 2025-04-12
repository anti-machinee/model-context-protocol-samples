# websocket_server
- is an asynchronous context manager that provides a WebSocket-based transport layer for the MCP (Model Context Protocol) framework. It facilitates bidirectional communication between a WebSocket client and server, enabling the exchange of JSON-RPC messages
- WebSocket Transport for MCP: Acts as an ASGI application for handling WebSocket connections. Suitable for use with ASGI frameworks like Starlette and servers like Hypercorn.
- Bidirectional Communication: Client → Server: Reads JSON-RPC messages sent by the client over the WebSocket connection. Server → Client: Sends JSON-RPC messages from the server to the client over the WebSocket connection.
- Stream Abstraction: Provides read_stream and write_stream for handling incoming and outgoing messages, abstracting away the low-level WebSocket operations.
## Arguments
- scope
- receive
- send
## Actions
- Accept the WebSocket Connection
    - Creates a WebSocket object using the ASGI scope, receive, and send callables. Accepts the WebSocket connection and sets the subprotocol to "mcp".
- Creates two pairs of in-memory streams:
    - read_stream and read_stream_writer:
        - Used for client-to-server communication.
        - Messages received from the WebSocket are written to read_stream_writer and read from read_stream.
    - write_stream and write_stream_reader:
        - Used for server-to-client communication.
        - Messages written to write_stream are read from write_stream_reader and sent to the WebSocket.
- Run Readers and Writers in a Task Group 
    - Starts the ws_reader and ws_writer coroutines in an AnyIO task group.
    - Yields read_stream and write_stream to the calling code, allowing it to interact with the streams.
## ws_reader
- Reads text messages from the WebSocket using websocket.iter_text().
- Parses each message as a JSON-RPC message using model_validate_json.
- Sends valid messages to read_stream_writer.
- Sends validation errors (e.g., invalid JSON) to read_stream_writer.
- Closes the WebSocket if the resource is closed.
## ws_writer
- Reads messages from write_stream_reader.
- Serializes each message to JSON using model_dump_json.
- Sends the serialized JSON to the WebSocket using websocket.send_text.
- Closes the WebSocket if the resource is closed.
