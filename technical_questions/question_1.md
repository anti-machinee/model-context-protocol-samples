# How to connect Claude desktop from Windows to MCP server in WSL
# Answer
- Configure claude_desktop_config.json in Windows
- Note
    - You may need absolute path of uv
```
{
    "mcpServers": {
        "weather": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/home/duongdq/workspace/projects/opensources/modelcontextprotocol/quickstart-resources/weather-server-python",
                "run",
                "weather.py"
            ]
        }
    }
}
```