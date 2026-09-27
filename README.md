# Custom File Formats Toolkit

A collection of custom file formats and Python parsers/generators for automation, Discord (e.g.), and system utilities (e.g., Rust).

This repo provides:
- Custom file format definitions (`.luna`, `.unkn`, `.pyru`, `.lujit`, `.acf`, `.ctxt`, `.stxt`)
- Python generators to create test files for each format
- Reference parsers to read and process these formats
- Example usage for bot and system-level workflows

## Formats Overview

| Format | Purpose | Typical Use Case |
|--------|---------|------------------|
| `.luna` | Lightweight config format with sections | Bot configs (prefixes, roles, settings) |
| `.unkn` | Unknown-type placeholder; auto-detected and renamed | Dynamic code delivery, plugin system |
| `.pyru` | Hybrid Python/Rust script with section markers | Multi-language command modules |
| `.lujit` | LuaJIT-ready scripts | In-game logic, fast scripting for Roblox/bots |
| `.acf` | Application Critical Manifest (JSON) | Integrity checks, version control, admin flags (for LUnlocker) |
| `.ctxt` | Critical Text with SHA-256 signature | Signed rules, moderation policies, verified configs |
| `.stxt` | Structured text commands | Bot command batching, moderation actions, point systems |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/v86889839-collab/custom-formats.git
cd custom-formats
