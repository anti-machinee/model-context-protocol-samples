# Check list
- [x] Setup
    - [x] uv
    - [x] pip
    - [x] docker
- [x] Deploy with Claude desktop
    - [x] Python command
        - [x] with Python module
    - [x] uvx command
        - [x] with Python package
        - [x] with Python file -> error
    - [x] uv command
        - [x] with Python file
    - [x] docker command
        - [x] with Python project
- [] Deploy with Zed
- [x] Debug
    - [x] Log
    - [x] Inspector
- [x] Test
    - [x] Pytest

# Setup project
## uv
```bash
uv init mcp-server-git
uv venv
uv sync
```

# Deploy with Claude desktop
- Edit `claude_desktop_config.json`
    - Windows: `"C:\Users\duong\AppData\Roaming\Claude\claude_desktop_config.json"`

# Python command
- Setup
```bash
pip install mcp-server-git
```
- This config uses python module (from package)
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/miniconda3/bin/python",
                "-m",
                "mcp-server-git"
            ]
        }
    }
}
```

# uvx command
- Setup
```bash
pip install mcp-server-git
```
- This config uses python package (not from file)
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uvx",
                "mcp-server-git"
            ]
        }
    }
}
```

# uv Command
- This config uses python file (not from package)
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/home/duongdq/workspace/projects/personal_projects/ai-foundation/model-context-protocol-samples/samples/mcp_servers/mcp-server-git/src/mcp-server-git",
                "run",
                "main.py"
            ]
        }
    }
}
```
- This config uses python project (not from package). See issue ISSUE1
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/home/duongdq/workspace/projects/personal_projects/ai-foundation/model-context-protocol-samples/samples/mcp_servers/mcp-server-git",
                "run",
                "mcp-server-git"
            ]
        }
    }
}
```

# docker command
- Setup
```bash
docker build -t mcp-server-git .
```
- Same as use uv to run python project
```json
{
    "mcpServers": {
        "git": {
            "command": "docker",
            "args": [
                "run",
                "--rm",
                "-i",
                "--mount",
                "type=bind,src=C:\\Users\\duong\\workspace,dst=/mnt/c/Users/duong/workspace",
                "mcp-server-git"
            ]
        }
    }
}
```

# Debug
## Log
- Window: `C:\Users\duong\AppData\Roaming\Claude\logs\mcp-server-git.log`
## Inspector
### uvx
```bash
npx @modelcontextprotocol/inspector uvx mcp-server-git
```
### uv
```bash
npx @modelcontextprotocol/inspector uv run mcp-server-git
```

# Test
## Pytest
```bash
pytest
```

# References
- [1] https://github.com/modelcontextprotocol/servers/tree/main/src/git
