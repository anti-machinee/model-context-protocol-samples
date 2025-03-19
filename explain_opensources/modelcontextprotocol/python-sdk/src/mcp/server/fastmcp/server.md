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
- _mcp_server
    - To encapsulate the core functionality of the MCP server
    - To expose attributes via properties for user friendly access while keeping the low-level details encapsulated
    - To set up core MCP protocol handlers
    - To set request context
    - To run server using stdio transport
    - To handle sse messages
    - To create initialization options
- _tool_manager
    - To list/call/add tools
- _resource_manager
    - To list/get/add resources/templates
- _prompt_manager
    - To list/get/add prompts
- dependencies
    - To install dependencies (by uv)
### Method calls
- _setup_handlers
    - Read _mcp_server above
        - list_tools
        - call_tool
        - list_resources
        - read_resource
        - list_prompts
        - get_prompt
        - list_list_resource_templatestools
### Function calls
- configure_logging
    - Configure logging

## property
- name
    - To provide public interface to retrieve name of MCPServer
- instructions
    - To provide public interface to retrieve instructions of MCPServer
## run

## name

## instructions

## 

# Settings

# Context
