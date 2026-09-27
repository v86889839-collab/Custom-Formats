# Custom File Formats Toolkit

A collection of custom file formats and Python parsers/generators for automation, Discord bots (e.g., ReBoot), and system utilities (e.g., LUnlocker).

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
| `.acf` | Application Critical Manifest (JSON) | Integrity checks, version control, admin flags |
| `.ctxt` | Critical Text with SHA-256 signature | Signed rules, moderation policies, verified configs |
| `.stxt` | Structured text commands | Bot command batching, moderation actions, point systems |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/v86889839-collab/custom-formats.git
cd custom-formats
```

### 2. Generate all test files at once

Run the unified generator to create one example file for each format:

```bash
python generators/gen_all.py
```

This will create the following files in the root directory:

- `config.luna` — sample bot configuration with sections
- `mystery.unkn` — random code snippet (Python/Rust/Lua) for auto-detection
- `hybrid.pyru` — mixed Python/Rust script with section markers
- `test.lujit` — LuaJIT-ready script for fast in-game logic
- `app.acf` — manifest with SHA-256, version, and admin flags
- `rules.ctxt` — signed moderation rules with SHA-256 header
- `actions.stxt` — batch of bot commands (e.g., `r!add-points`, `r!give-role`)

You can inspect these files directly or feed them into the reference parser.

### 3. Test the parsers

Use the reference parser module to inspect and validate the generated files:

```bash
python custom_formats.py
```

The script will:

- Detect and auto-rename `.unkn` files based on content markers (`def`, `fn main()`, `--`, etc.)
- Parse configs, manifests, signed texts, and command batches
- Print structured output to the console (as JSON-like dicts/lists)
- Show detection confidence and any warnings (e.g., missing signature, unknown language)

Example output snippet:

```text
✅ Detected language for mystery.unkn → .py
✅ Parsed config.luna: bot.name = ReBoot, bot.prefix = r!
✅ Verified rules.ctxt signature: VALID
✅ Parsed actions.stxt: 8 commands ready for execution
```

## Format Details & Practical Usage

### `.luna` – Lightweight Config with Sections

**Use case:** Discord bot configs (ReBoot), quick settings for utilities.
**Why it's useful:** Simple, human-readable, no external dependencies.

Example (`config.luna`):

```ini
[bot]
name = ReBoot
prefix = r!
version = 2.3.1

[roles]
mod = 123456789012345678
helper = 876543210987654321
trial = 112233445566778899

[settings]
max_users = 200
timeout_sec = 180
log_level = INFO
```

**How to use in code:**

```python
from custom_formats import LunaConfig

cfg = LunaConfig.load("config.luna")
bot_name = cfg.get("", "name")          # "ReBoot"
mod_role_id = cfg.get("roles", "mod")   # 123456789012345678
```

---

### `.unkn` – Auto-Detected Code Placeholder

**Use case:** Plugin system, user-submitted scripts, dynamic command modules.
**Workflow:**

1. Receive a `.unkn` file (e.g., from an admin upload).
2. Run the detector: it analyzes content markers.
3. Automatically renames to `.py`, `.rs`, or `.lua`.
4. Then process with the appropriate runtime.

**Example detection logic:**

- `fn main()` or `println!` → `.rs` (Rust)
- `def` or `import` → `.py` (Python)
- `--` comments or `function` → `.lua` (Lua)

**Integration tip for ReBoot:**
Create a command like `!auto-fix` that scans `uploads/` and runs the `.unkn` detector on all new files. This keeps your plugin folder clean and safe.

**Code example:**

```python
from custom_formats import process_unkn, process_unkn_folder

# Single file
process_unkn("mystery.unkn")    # → mystery.py

# Entire folder
process_unkn_folder("./uploads/")
```

---

### `.pyru` – Hybrid Python/Rust Script

**Use case:** Multi-language command modules where Python handles Discord API and Rust handles heavy computation or safety-critical logic.

Example (`hybrid.pyru`):

```text
# === PYTHON ===
def py_hello():
    print("Hello from Python")

py_hello()
# === PYTHON END ===

# === RUST ===
fn main() {
    println!("Hello from Rust");
}
# === RUST END ===
```

**How to use:**

```python
from custom_formats import parse_pyru, create_pyru, run_pyru

# Parse sections
parts = parse_pyru("hybrid.pyru")
python_code = parts["python"]    # Python block as string
rust_code = parts["rust"]        # Rust block as string

# Create a new .pyru file
create_pyru("print('Hi')", 'fn main() { println!("Hi"); }', "new.pyru")

# Run both parts (requires python and rustc in PATH)
result = run_pyru("hybrid.pyru")
print(result["python_output"])
print(result["rust_output"])
```

---

### `.lujit` – LuaJIT-Ready Scripts

**Use case:** In-game logic, fast scripting for Roblox, lightweight bots.
**Tip:** Configure VS Code to treat `.lujit` as Lua for syntax highlighting:

```json
{
  "files.associations": {
    "*.lujit": "lua"
  }
}
```

Example (`test.lujit`):

```lua
-- .lujit file — Generated for LuaJIT testing
print("Starting .lujit script")

for i = 1, 5 do
    local val = math.random(1, 100)
    print("Iteration:", i, "Random value:", val)
end

local sum = 0
for j = 1, 1000 do
    sum = sum + j
end
print("Sum calculated:", sum)

print("End of .lujit script")
```

**How to use:**

```python
from custom_formats import validate_lujit, run_lujit

# Validate (checks for LuaJIT-specific constructs like ffi, jit)
valid, msg = validate_lujit("test.lujit")
print(f"Valid: {valid}, Message: {msg}")

# Run with fallback to standard Lua if LuaJIT is not installed
result = run_lujit("test.lujit", fallback_to_lua=True)
print(result["stdout"])
```

---

### `.acf` – Application Critical Manifest

**Use case:** Integrity checks for critical executables, version control, admin permission flags. Designed for LUnlocker and similar utilities.

Example (`app.acf`):

```json
{
  "file": "app.exe",
  "version": "1.2.3",
  "critical": true,
  "requires_admin": false,
  "description": "Critical module for LUnlocker core",
  "expected_sha256": "a1b2c3d4e5f6...",
  "allowed_os": ["Windows 10", "Windows 11"],
  "min_build": 19041
}
```

**How to use:**

```python
from custom_formats import create_acf, AcfManifest

# Create a manifest (auto-calculates SHA-256 of the target exe)
create_acf("app.exe", "app.exe", "app.acf", description="Critical module")

# Load and verify
manifest = AcfManifest.load("app.acf")
ok, msg = manifest.verify_exe(".")
print(f"Integrity check: {ok}, Details: {msg}")
```

**What it checks:**

- File exists at the expected path
- SHA-256 hash matches `expected_sha256`
- OS version meets `min_build` requirement
- Admin flag is respected if `requires_admin` is `true`

---

### `.ctxt` – Critical Text with SHA-256 Signature

**Use case:** Signed moderation rules, verified configurations, tamper-proof policies.

Example (`rules.ctxt`):

```text
SIGNATURE: a1b2c3d4e5f6...
Critical Level: high
Description: Server moderation rules

Правила модерации сервера ReBoot:
1. Запрещён спам и реклама.
2. Оскорбления запрещены.
3. Не используйте ботов для накрутки поинтов.
4. Администрация имеет право выдать бан без объяснения причин.
```

**How to use:**

```python
from custom_formats import save_ctxt, load_ctxt

# Save signed text
save_ctxt("rules.ctxt", "Правила модерации...", critical_level="high")

# Load and verify
data = load_ctxt("rules.ctxt")
print(f"Valid: {data['valid']}")        # True if signature matches
print(f"Content: {data['content']}")   # Text without header
print(f"Level: {data['critical_level']}")
```

**Verification logic:**

1. Read the `SIGNATURE:` line (first line).
2. Calculate SHA-256 of the remaining content.
3. Compare: if match → `valid: True`, if not → file was tampered with.

---

### `.stxt` – Structured Text Commands

**Use case:** Batch bot commands, moderation actions, point systems. Perfect for ReBoot automation.

Example (`actions.stxt`):

```text
# SCRIPT_TXT v1
# Auto-generated test file

COMMAND: r!add-points
TARGET: PBSTHelper
AMOUNT: 100

COMMAND: r!give-role
USER: @User123
ROLE: mod_role

COMMAND: r!mute
USER: @Spammer
DURATION: 24h
```

**How to use:**

```python
from custom_formats import parse_stxt, execute_stxt, create_stxt

# Parse commands
cmds = parse_stxt("actions.stxt")
for c in cmds:
    print(c.command, c.params)

# Execute via custom handler
def my_handler(command, params):
    print(f"Executing {command} with {params}")

execute_stxt("actions.stxt", handler=my_handler)

# Create a new .stxt file
create_stxt([
    {"command": "r!add-points", "TARGET": "PBSTHelper", "AMOUNT": "100"},
    {"command": "r!mute", "USER": "@Spammer", "DURATION": "24h"},
], "mod_actions.stxt")
```

**Parsing rules:**

- Lines starting with `#` are comments (ignored).
- `COMMAND:` starts a new command block.
- All subsequent `KEY: VALUE` lines are parameters of that command.
- Blank lines separate command blocks.

## Integration Guide

### For ReBoot (Discord Bot)

| Format | How to integrate |
|--------|-----------------|
| `.luna` | Load `config.luna` on bot startup to set prefix, roles, limits |
| `.unkn` | `!auto-fix` command scans `uploads/` and renames files by language |
| `.stxt` | `!run-script` command reads `.stxt` and executes commands in sequence |
| `.ctxt` | Load signed moderation rules on startup, reject if signature invalid |
| `.lujit` | Run in-game logic scripts via LuaJIT subprocess |
| `.pyru` | Advanced plugin modules with Python (bot API) + Rust (perf-critical) |

### For LUnlocker (System Utility)

| Format | How to integrate |
|--------|-----------------|
| `.acf` | Verify integrity of critical `.exe` files before launch |
| `.ctxt` | Load signed security policies, refuse to run if tampered |
| `.stxt` | Batch operations: clean → verify → restart service |
| `.unkn` | Analyze unknown files before execution |

## VS Code Setup

Add this to your `settings.json` for syntax highlighting:

```json
{
  "files.associations": {
    "*.luna": "ini",
    "*.lujit": "lua",
    "*.pyru": "python",
    "*.stxt": "plaintext",
    "*.ctxt": "plaintext",
    "*.acf": "json",
    "*.unkn": "plaintext"
  }
}
```

## Project Structure

```
custom-formats/
├── custom_formats.py        # Core parser module (all 7 formats)
├── generators/
│   ├── gen_all.py            # Run all generators at once
│   ├── gen_luna.py           # Generate config.luna
│   ├── gen_unkn.py           # Generate mystery.unkn
│   ├── gen_pyru.py           # Generate hybrid.pyru
│   ├── gen_lujit.py          # Generate test.lujit
│   ├── gen_acf.py            # Generate app.acf
│   ├── gen_ctxt.py           # Generate rules.ctxt
│   └── gen_stxt.py           # Generate actions.stxt
├── examples/
│   ├── config.luna
│   ├── mystery.unkn
│   ├── hybrid.pyru
│   ├── test.lujit
│   ├── app.acf
│   ├── rules.ctxt
│   └── actions.stxt
├── LICENSE
└── README.md
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Author

GitHub: [@v86889839-collab](https://github.com/v86889839-collab)
