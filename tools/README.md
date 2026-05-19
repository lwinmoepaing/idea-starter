# tools/

Local dev tools + bootstrap scripts for the idea-to-MVP loop. Each subfolder is a standalone app or utility; run directly, not via a skill.

## Subfolders

| Folder      | What it is                                                                                          | How to run                                           |
| ----------- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `drawing/`  | React + Vite + TypeScript + tldraw v3 canvas — sketch UX, flowcharts, or just doodle full-viewport  | `cd tools/drawing && npm install && npm run dev`     |
| `scripts/`  | Bootstrap scripts. Currently `setup-mcp.sh` (clones + builds the `tldraw` MCP into `.mcp-servers/`) | `bash tools/scripts/setup-mcp.sh`                    |

## `drawing/` vs the `tldraw` MCP

`drawing/` is for **you** sketching by hand. The `tldraw` MCP (in `.mcp.json`) is for **Claude**, rendering shape JSON to a PNG headlessly — used by `business-canvas`. Same runtime, different entry points.
