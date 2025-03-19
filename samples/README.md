# Guides

## Setup a server
### UV
```bash
uv init mcp_server_git
uv venv
uv sync
```

## Deploy a server
### Claude desktop
- Add to `claude_desktop_config.json`
    - Windows: `"C:\Users\duong\AppData\Roaming\Claude\claude_desktop_config.json"`
- Example
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/home/duongdq/workspace/projects/personal_projects/ai-foundation/model-context-protocol-samples/samples/local_related/mcp_servers/mcp_server_git",
                "run",
                "main.py"
            ]
        }
    }
}
```