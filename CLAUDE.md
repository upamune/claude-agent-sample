# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a sample repository demonstrating the Claude Agent SDK (`claude-agent-sdk`), which enables building AI agents powered by Claude that can execute tasks using tools and MCP (Model Context Protocol) servers. The main application (`main.py`) is a Japanese-language interactive calculator agent showcasing system prompt design and custom tool integration.

## Development Commands

### Running the Application

```bash
uv run main.py
```

or

```bash
mise run agent
```

### Code Quality

```bash
# Format code with Ruff
mise run format

# Lint and auto-fix issues
mise run lint
```

## Architecture

### Core Components

1. **Main Application (`main.py`)**
   - Interactive calculator agent with Japanese UI using Rich library for display
   - Demonstrates system prompt design with XML tags for role, principles, boundaries, and tools
   - Uses MCP server pattern with `create_sdk_mcp_server()` for tool registration
   - Implements `ClaudeSDKClient` for streaming mode interactions

2. **SDK Interaction Patterns**
   - **Query Mode**: Simple one-off queries using `query()` function (see `examples/quick_start.py`)
   - **Streaming Mode**: Interactive sessions with `ClaudeSDKClient` for multi-turn conversations (see `examples/streaming_mode.py`)
   - **Agent Mode**: Custom agent definitions with specific prompts and tools (see `examples/agents.py`)

3. **Custom Tools and MCP**
   - Tools defined using `@tool` decorator with name, description, and input schema
   - Tools return dict with `content` array (type: text) and optional `is_error` flag
   - MCP servers created with `create_sdk_mcp_server()` for in-process tool execution
   - Tools referenced as `mcp__<server_name>__<tool_name>` in `allowed_tools`

### Key SDK Patterns

**Tool Definition:**
```python
@tool("tool_name", "Description", {"param": type})
async def tool_function(args: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "content": [{"type": "text", "text": "result"}],
        "is_error": False  # optional
    }
```

**MCP Server Creation:**
```python
server = create_sdk_mcp_server(
    name="server_name",
    version="1.0.0",
    tools=[tool_func1, tool_func2]
)

options = ClaudeAgentOptions(
    mcp_servers={"server_name": server},
    allowed_tools=["mcp__server_name__tool_name"],
    system_prompt="...",
    permission_mode="default"
)
```

**Streaming Client Usage:**
```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("user prompt")
    async for message in client.receive_response():
        # Handle AssistantMessage, UserMessage, ResultMessage
        pass
```

### System Prompt Design

The main application demonstrates effective system prompt structure using XML tags:
- `<role>`: Define agent's purpose and capabilities
- `<core_principles>`: Guiding principles for behavior
- `<boundaries>`: Clear limitations and out-of-scope requests
- `<tools_specification>`: Document available tools

This pattern helps maintain agent focus and provides clear boundaries.

### Documentation Structure

The `docs/` directory contains two types of documentation:
- `docs/claude/`: General Claude API best practices (prompt engineering, guardrails, etc.)
- `docs/claude-agent-sdk/`: SDK-specific documentation (sessions, MCP, custom tools, etc.)

## Dependencies

- Python 3.12+ required (specified in `pyproject.toml`)
- `claude-agent-sdk>=0.1.6`: Core SDK for building Claude agents
- `rich>=14.2.0`: Terminal UI library for formatted output
- Development tools managed via `mise`: uv for Python package management, Ruff for linting/formatting

## Utility Scripts

**fetch_doc.py**: Fetches web content and converts to markdown with frontmatter
- Uses PEP 723 inline script metadata (dependencies specified in script header)
- Executed with `uv run --script` shebang for self-contained execution
- Supports both direct text fetching and Jina Reader API for HTML conversion
