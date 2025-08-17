#!/usr/bin/env python3
"""
Entry point for running the Google Tasks MCP server.
"""

import sys
import argparse
from .server import gtasks_mcp


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Google Tasks MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport protocol to use (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to for HTTP/SSE transports (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to for HTTP/SSE transports (default: 8000)"
    )
    parser.add_argument(
        "--path",
        default="/mcp",
        help="Path for HTTP transport (default: /mcp)"
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Starting Google Tasks MCP Server")
    print(f"📡 Transport: {args.transport}")
    
    try:
        if args.transport == "stdio":
            print("📝 Using STDIO transport (for command-line tools)")
            gtasks_mcp.run(transport="stdio")
        elif args.transport == "http":
            print(f"🌐 Using HTTP transport at http://{args.host}:{args.port}{args.path}")
            gtasks_mcp.run(
                transport="http",
                host=args.host,
                port=args.port,
                path=args.path
            )
        elif args.transport == "sse":
            print(f"🔄 Using SSE transport at http://{args.host}:{args.port}")
            gtasks_mcp.run(
                transport="sse",
                host=args.host,
                port=args.port
            )
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
