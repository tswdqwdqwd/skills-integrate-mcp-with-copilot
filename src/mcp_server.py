"""
MCP Server for Mergington High School Activities API

This server exposes the activities API endpoints as MCP tools
that can be used by Claude/Copilot.
"""

import json
import sys
from typing import Any

# MCP Tools available through this server
TOOLS = [
    {
        "name": "list_activities",
        "description": "Get all available activities with their details and current participant count",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "signup_for_activity",
        "description": "Sign up a student for an activity",
        "inputSchema": {
            "type": "object",
            "properties": {
                "activity_name": {
                    "type": "string",
                    "description": "The name of the activity to sign up for"
                },
                "email": {
                    "type": "string",
                    "description": "The student's email address"
                }
            },
            "required": ["activity_name", "email"]
        }
    },
    {
        "name": "unregister_from_activity",
        "description": "Unregister a student from an activity",
        "inputSchema": {
            "type": "object",
            "properties": {
                "activity_name": {
                    "type": "string",
                    "description": "The name of the activity to unregister from"
                },
                "email": {
                    "type": "string",
                    "description": "The student's email address"
                }
            },
            "required": ["activity_name", "email"]
        }
    }
]


def send_response(response: dict[str, Any]) -> None:
    """Send a JSON-RPC response"""
    print(json.dumps(response), file=sys.stdout, flush=True)


def handle_initialize(request: dict[str, Any]) -> None:
    """Handle initialization request"""
    response = {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "Mergington Activities Server",
                "version": "1.0.0"
            }
        }
    }
    send_response(response)


def handle_list_tools(request: dict[str, Any]) -> None:
    """Handle list tools request"""
    response = {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "result": {
            "tools": TOOLS
        }
    }
    send_response(response)


def handle_call_tool(request: dict[str, Any]) -> None:
    """Handle tool call request"""
    tool_name = request.get("params", {}).get("name")
    tool_input = request.get("params", {}).get("arguments", {})
    
    # Import app to access activities
    from src.app import activities

    result = None
    error = None

    try:
        if tool_name == "list_activities":
            result = activities

        elif tool_name == "signup_for_activity":
            activity_name = tool_input.get("activity_name")
            email = tool_input.get("email")

            if activity_name not in activities:
                error = f"Activity '{activity_name}' not found"
            elif email in activities[activity_name]["participants"]:
                error = f"Student {email} is already signed up for {activity_name}"
            else:
                activities[activity_name]["participants"].append(email)
                result = {
                    "success": True,
                    "message": f"Successfully signed up {email} for {activity_name}"
                }

        elif tool_name == "unregister_from_activity":
            activity_name = tool_input.get("activity_name")
            email = tool_input.get("email")

            if activity_name not in activities:
                error = f"Activity '{activity_name}' not found"
            elif email not in activities[activity_name]["participants"]:
                error = f"Student {email} is not signed up for {activity_name}"
            else:
                activities[activity_name]["participants"].remove(email)
                result = {
                    "success": True,
                    "message": f"Successfully unregistered {email} from {activity_name}"
                }
        else:
            error = f"Unknown tool: {tool_name}"

    except Exception as e:
        error = str(e)

    response = {
        "jsonrpc": "2.0",
        "id": request.get("id"),
    }

    if error:
        response["error"] = {
            "code": -32603,
            "message": error
        }
    else:
        response["result"] = {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }

    send_response(response)


def main():
    """Main MCP server loop"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")

            if method == "initialize":
                handle_initialize(request)
            elif method == "tools/list":
                handle_list_tools(request)
            elif method == "tools/call":
                handle_call_tool(request)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                send_response(response)

        except json.JSONDecodeError:
            print("Invalid JSON", file=sys.stderr)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
