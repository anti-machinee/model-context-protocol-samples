# Stdio
## What is Stdio transport?
- [1]
- [2]
## What are usages of Stdio transport in MCP?
- CLI-Based Tools
    - The method is ideal for running the server in a command-line interface (CLI) environment where the server interacts with other processes or tools via stdin and stdout
    - Example: A CLI tool that sends requests to the server and receives responses through pipes.
- Integration with Other Processes
    - The stdio transport can be used to integrate the server with other processes or systems that communicate using standard input/output streams
    - Example: A parent process spawns the server as a subprocess and communicates with it through pipes.
- Testing and Debugging
    - The stdio transport can be useful for testing or debugging the server in a controlled environment where input and output streams are simulated.
- Lightweight Communication
    - The stdio transport is lightweight and does not require setting up a network server (e.g., HTTP or SSE). This makes it suitable for scenarios where simplicity and minimal overhead are important.

# Server Sent Events
## What is Server Sent Events?
## What are usages of SSE transport in MCP?
- Real-Time Updates to Clients
    - SSE is ideal for scenarios where the server needs to push real-time updates to clients, such as notifications, progress updates, or streaming data.
    - Example: A client subscribes to an SSE endpoint to receive updates about the status of a long-running task.
- HTTP-Based Communication:
    - The SSE transport uses HTTP, making it suitable for web-based applications where clients (e.g., browsers) can easily connect to the server.
- Integration with Frontend Applications:
    - Frontend applications (e.g., React, Angular, or Vue.js) can use the SSE protocol to receive real-time updates from the server without requiring WebSockets or polling.
- Scalable Real-Time Communication:
    - SSE is lightweight and efficient for one-way communication from the server to the client, making it scalable for many clients.
- Customizable Server Behavior:
    - The self.sse_app() method allows developers to define custom routes and endpoints for handling SSE connections and related functionality.


# References
- [1] https://docs.mulesoft.com/mule-runtime/3.9/stdio-transport-reference
- [2] https://introcs.cs.princeton.edu/python/15inout/#:~:text=That%20is%2C%20the%20stdio%20module,standard%20input%20at%20any%20time.