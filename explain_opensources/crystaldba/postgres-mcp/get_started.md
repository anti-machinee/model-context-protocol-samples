# Setup
- Package management
    - uv
    - pipx
    - Docker

# Pyproject
- Have hatchling for packaging and build the project
- Have entry points
- Sets the default scope for the asyncio event loop fixture to "function", ensuring each test gets its own event loop
- Support developers to install dependencies with single command for development
- Have code formatter, linter and type checker

# Docker
## Dockerfile
- Multi stage buildings
- Stage 1
    - Setup env for uv
    - Install build dependencies
- Stage 2
    - Install runtime dependencies
    - Expose port
    - Execute entry point
## Entrypoint
- Replace localhost in a string with the Docker host
- Replace localhost in database URI with Docker host
- Set arguments for SSE transport
- Execute the command with arguments
- Handle error

# Claude desktop
## uv
- Setup
```
{
    "mcpServers": {
        "postgres": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/mnt/c/Users/duong/opensources/crystaldba/postgres-mcp",
                "run",
                "postgres-mcp",
                "--access-mode=unrestricted",
                "DATABASE_URI=postgresql://myuser:mypassword@localhost:5432/mydatabase"
            ]
        }
    }
}
```
## pipx
## Docker