# Integrate MCP with Copilot

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey tswdqwdqwd!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

## Overview

This project demonstrates how to integrate Model Context Protocol (MCP) with GitHub Copilot. The Mergington High School Activities API has been extended with an MCP server that allows Claude/Copilot to interact with school activities programmatically.

## MCP Integration

### What is MCP?

Model Context Protocol (MCP) is a standardized protocol that enables LLM applications (like GitHub Copilot) to interact with external tools and data sources through a consistent interface.

### How It Works

1. **MCP Server** (`src/mcp_server.py`) - Exposes activities API endpoints as tools
2. **Configuration** (`.mcp.json`) - Defines how Copilot connects to the MCP server
3. **Tools** - Three tools are available:
   - `list_activities` - Retrieve all activities
   - `signup_for_activity` - Register a student for an activity
   - `unregister_from_activity` - Unregister a student from an activity

### Getting Started with MCP

1. Start the FastAPI server:
   ```bash
   cd src
   python app.py
   ```

2. Configure your Claude/Copilot environment to use the MCP server defined in `.mcp.json`

3. Ask Copilot questions like:
   - "What activities are available at Mergington High School?"
   - "Sign up emma@mergington.edu for Chess Club"
   - "Which students are registered for Programming Class?"

---

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/tswdqwdqwd/skills-integrate-mcp-with-copilot/issues/1)

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

