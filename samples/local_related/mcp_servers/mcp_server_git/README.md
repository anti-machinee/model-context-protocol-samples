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

# Setup
## uv
```bash
uv init mcp_server_git
uv venv
uv sync
```
## pip
```bash
pip install mcp-server-git
```
## docker
```bash
docker build -t mcp-server-git .
```

# Deploy with Claude desktop
- Edit `claude_desktop_config.json`
    - Windows: `"C:\Users\duong\AppData\Roaming\Claude\claude_desktop_config.json"`
### Python command
- Should be compatible with set up server by pip
- This config uses python module (from package)
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/miniconda3/bin/python",
                "-m",
                "mcp_server_git"
            ]
        }
    }
}
```
### uvx command
- Should be compatible with set up server by pip
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
- This config uses python file (not from package)
- Lead to an error meaning the `uvx` is suitable to run package but not file
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uvx",
                "--directory",
                "/home/duongdq/workspace/projects/personal_projects/ai-foundation/model-context-protocol-samples/samples/local_related/mcp_servers/mcp_server_git/src/mcp_server_git",
                "run",
                "main.py"
            ]
        }
    }
}
# error
  × Failed to build `run==0.2`
  ├─▶ The build backend returned an error
  ╰─▶ Call to `setuptools.build_meta:__legacy__.build_wheel` failed (exit
      status: 1)

      [stderr]
      Traceback (most recent call last):
        File "<string>", line 14, in <module>
        File
      "/home/duongdq/.cache/uv/builds-v0/.tmptHJC1x/lib/python3.12/site-packages/setuptools/build_meta.py",
      line 334, in get_requires_for_build_wheel
          return self._get_build_requires(config_settings, requirements=[])
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File
      "/home/duongdq/.cache/uv/builds-v0/.tmptHJC1x/lib/python3.12/site-packages/setuptools/build_meta.py",
      line 304, in _get_build_requires
          self.run_setup()
        File
      "/home/duongdq/.cache/uv/builds-v0/.tmptHJC1x/lib/python3.12/site-packages/setuptools/build_meta.py",
      line 522, in run_setup
          super().run_setup(setup_script=setup_script)
        File
      "/home/duongdq/.cache/uv/builds-v0/.tmptHJC1x/lib/python3.12/site-packages/setuptools/build_meta.py",
      line 320, in run_setup
          exec(code, locals())
        File "<string>", line 12, in <module>
      NameError: name 'file' is not defined. Did you mean: 'filter'?

      hint: This usually indicates a problem with the package or the build
      environment.
  help: `uvx run main.py` invokes the `run` package. Did you mean `uvx
        main.py`?
```
### uv Command
- This config uses python file (not from package)
```json
{
    "mcpServers": {
        "git": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/home/duongdq/workspace/projects/personal_projects/ai-foundation/model-context-protocol-samples/samples/local_related/mcp_servers/mcp_server_git/src/mcp_server_git",
                "run",
                "main.py"
            ]
        }
    }
}
```
- This config uses python project (not from package)
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
                "mcp-server-git"
            ]
        }
    }
}
```
### docker command
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
