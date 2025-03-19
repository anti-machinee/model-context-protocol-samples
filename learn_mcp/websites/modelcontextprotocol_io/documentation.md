# Introduction
## Why MCP
- Plug LLMs into services
- Switch between LLMs providers and vendors
- Secure data within infrastructure
### General architecture
- Follow client-server architecture
- Host wants to access data via MCP
    - Claude desktop
    - IDEs
    - AI tools
- Client maintains 1 vs 1 connections with servers
- Server exposes capabilities via MCP 
    - Reference servers
    - 3rd party servers
    - Community servers
- Data sources
    - Files
    - Databases
    - Services
- Remote services are external and assessable via servers
    - API providers

# Quick start
## For server developers
- Problem
    - LLm can not fetch data
- User story
    - A server provides get alerts and get forecast. And connect server to Claude desktop
- Capabilities of MCP servers
    - Resources: TODO
    - Tools: TODO
    - Prompts: TODO
- Steps
    - Init project using uv
    - Init FastMCP server
    - Register tools to alerts and get forecast
    - Get alerts and get forecast having these formats
        - Form URLs refer from API documents
        - Form request
    - Form request
        - Refer to API documents to prepare header, body ... aka configuration
    - Post processing responses
        - None value is replaced by texts (manually catch)
    - Run server
- Others
    - When develop using Python, follow type hints and docstrings convention
- Test
    - Set up Claude desktop to embed the MCP client server
## For client developers
- Steps
    - Init project using uv
    - Init FastMCP client
    - Connect to server
        - Form parameters (command,encoding, error handler, env)
        - Enter async context
            - Form memory object receive stream
            - Form object send stream
        - Form and initialize session
            - Create client session using the stdio transport and adds it to the exist_stack for proper resource management
            - Initialize the session
        - List tools
            - Tool includes description, name
    - Init chat loops (while loop)
    - Process query
        - Form user message
        - Form tools
        - Initialize API call
        - Execute tool call
- Read more
    - Error handling (wrap in try except, handle connection issues)
    - Resource management (cleanup, close connection, handle disconnection)
    - Security (api storing, server response validation, )
## For claude desktop users
- Steps
    - Install Claude desktop
    - Config filesystem
- Troubleshooting

# Example servers
## Reference implementations
### Data and files systems
- Filesystem, postgresql, sqlite, google drive
### Development tools
- Git, github, gitlab, sentry
### Web and browser
- Brave search, fetch, puppeteer
### Productivity and communication
- Slack, googple maps, memory
### AI and specialized tools
- EverArt, Sequential thinking, AWS KB retrieval
## Official integrations
- Maintained by companies (Cloudflare, qdrant, search1api)
## Community integrations
- Maintained by community (docker, k8s, snowflake)
## Others
- Getting started
- Config Claude desktop

# Example clients
## Feature support matrix
- A table of report about a client whether it supports resources, prompts, tools, sampling, roots
## Client details
- Name clients and their features
## Adding MCP support to your application
- Encourage create PRs to MCP organization to build a MCP ecosystem

# Building MCP with LLMs
- Recommend how to use Claude to build MCP

# Debugging
## Debugging tools overview
- Can use these tools to debug MCP
    - MCP inspector
    - Claude desktop developer tools
    - Server logging
- Learn more some levels of debugging
## Debugging in Claude Desktop
- Can use these ways to debug MCP
    - Server status
    - Viewing log
     - Chrome DevTools
## Common issues
## Implementing logging
## Debugging workflow
## Best practices

# Inspector
- For test and debug
## Getting started
## Feature overview
## Best practices
## Next steps

# Core architecture
## Overview
- Client server architecture
    - Hosts
    - Clients
    - Servers
## Core components
    - Protocol layer (protocol, client, server)
    - Transport layer (stdio transport, HTTP/SSE transport)
    - Message type (requests, responses, errors, notifications)
## Connection lifecycle
    - Initialize
    - Message exchange
    - Termination
    - Error handling
## Error handling
## Security considerations

# Resources
## Overview
- File contents, database records, API responses, live system data, screenshots and images, log files and more
## Resource URIs
## Resource types
- Text sources
- Binary sources
## Resource discovery
- Direct resources
- Resource templates
## Reading resources
## Resource updates
- List changes
- Content changes
## Security considerations

# Prompts
## Prompt structure
## Discovering prompts
## Using prompts
## Dynamic prompts
### Embedded resource context
### Multi-step workflows
## Updates and changes
## Security considerations

# Tools
## Overview
- Discovery
- Invocation
- Flexibility
## Tool definition structure
## Implementing tools
## Example tool patterns
- System operations
- API integrations
- Data processing
## Security considerations
## Tool discovery and updates
## Error handling
## Testing tools

# Samping
## How sampling works
## Message format
## Request parameters
### Messages
### Model preferences
### System prompt
### Context inclusion
### Sampling parameters
## Response format
## Example request
## Human in the loop controls
- For prompts
- For completions
- For prompt
## Security considerations
## Common patterns
### Agentic workflows
### Context management
### Error handling
## Limitations

# Roots
## What are Roots?
## Why useroots?
## How Roots Work
## Common Use Cases

# Transports
## Message Format
- Request
- Response
- Notification
## Built-in Transport Types
- Standard Input/Output (stdio)
- Server-Sent Events (SSE)
##  Custom Transports
## Error Handling
## Security Considerations
## Debugging Transport

# References
- [1] https://modelcontextprotocol.io/introduction