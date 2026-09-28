# Custom File Formats Toolkit

A collection of custom file formats and Python parsers/generators for automation, Discord bots (e.g., ReBoot), and system utilities (e.g., LUnlocker).

This repo provides:

- Custom file format definitions (`.luna`, `.unkn`, `.pyru`, `.lujit`, `.acf`, `.ctxt`, `.stxt`, `.wip`, `.lock`, `.anim`, `.dep`, `.meta`, `.bake`, `.diff`, `.texb`, `.rule`, `.seed`, `.cfgx`, `.temp`, `.snap`, `.cache`, `.pref`, `.plan`, `.todo`, `.draft`, `.ref`, `.out`)
- Python generators to create test files for each format
- Reference parsers to read and process these formats
- Example usage for bot and system-level workflows

## Formats Overview

### Core Formats (with full parser support)

| Format | Purpose | Typical Use Case |
|--------|---------|------------------|
| `.luna` | Lightweight config format with sections | Bot configs (prefixes, roles, settings) |
| `.unkn` | Unknown-type placeholder; auto-detected and renamed | Dynamic code delivery, plugin system |
| `.pyru` | Hybrid Python/Rust script with section markers | Multi-language command modules |
| `.lujit` | LuaJIT-ready scripts | In-game logic, fast scripting for Roblox/bots |
| `.acf` | Application Critical Manifest (JSON) | Integrity checks, version control, admin flags |
| `.ctxt` | Critical Text with SHA-256 signature | Signed rules, moderation policies, verified configs |
| `.stxt` | Structured text commands | Bot command batching, moderation actions, point systems |

### Extended Formats (status, workflow, and asset management)

| Format | Purpose | Typical Use Case |
|--------|---------|------------------|
| `.wip` | Work In Progress marker | Unfinished scripts/models, renamed to final type when done |
| `.lock` | Locked file (no modifications) | Prevent edits to shared configs or critical assets |
| `.anim` | Animation keyframe data | Reusable animations across multiple models |
| `.dep` | Dependencies list | Track what a file needs to run (modules, models, assets) |
| `.meta` | Metadata sidecar file | Store hash, author, tags, creation date alongside main file |
| `.bake` | Pre-computed baked data | Cached lighting, navigation meshes, collision data |
| `.diff` | Difference / patch file | Ship only changed portions between file versions |
| `.texb` | Texture bundle | Pack diffuse, normal, roughness textures into one file |
| `.rule` | Validation rule definition | Define what counts as "valid" for a file or project |
| `.seed` | Generator input parameters | Procedural world/landscape/structure generation seeds |
| `.cfgx` | Extended config with nested structures | Complex configs with conditions, sections, logic |
| `.temp` | Temporary file | Short-lived working files, deleted after processing |
| `.snap` | Snapshot of current state | Capture files, settings, process state at a moment in time |
| `.cache` | Cached computation results | Avoid recomputing expensive operations |
| `.pref` | User preferences | Personal settings: theme, language, layout |
| `.plan` | Action plan (ordered steps) | Build pipelines, migration plans, release checklists |
| `.todo` | Task list linked to a plan | Granular checkboxes tied to a `.plan` file |
| `.draft` | Draft / rough sketch | Raw unfinished content, excluded from builds |
| `.ref` | Reference pointer to another file | Link between files without copying data |
| `.out` | Program output capture | Store stdout/stderr results for logging and review |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/v86889839-collab/custom-formatsV2.git
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
- `module.wip` — work-in-progress script placeholder
- `shared.lock` — locked file marker example
- `walk.anim` — sample animation keyframe data
- `module.dep` — dependencies list for a script
- `model.meta` — metadata sidecar for a model file
- `scene.bake` — pre-computed baked lighting data
- `v1_to_v2.diff` — difference/patch between two versions
- `textures.texb` — packed texture bundle
- `lint.rule` — validation rule definition
- `world.seed` — procedural generation seed parameters
- `advanced.cfgx` — extended config with nested sections
- `work.temp` — temporary working file
- `checkpoint.snap` — state snapshot
- `render.cache` — cached computation result
- `user.pref` — user preferences
- `release.plan` — ordered action plan
- `release.todo` — task list linked to release plan
- `notes.draft` — draft/rough sketch file
- `link_to_model.ref` — reference pointer
- `build.out` — captured program output

You can inspect these files directly or feed them into the reference parser.

### 3. Test the parsers

Use the reference parser module to inspect and validate the generated files:

```bash
python custom_formatsV2.py
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

---

### `.wip` – Work In Progress

**Use case:** Mark files that are still being worked on. Once finished, rename to the final extension.

Example (`module.wip`):

```text
# WIP: anti_spam module
# Status: 60% complete
# TODO: Add rate limiting logic

def check_spam(message):
    pass  # not implemented yet
```

**How to use:**

```python
import os

# Rename when done
os.rename("module.wip", "module.py")
```

**Rules:**
- Files with `.wip` should not be executed or included in builds.
- When the work is complete, strip `.wip` to reveal the final extension.

---

### `.lock` – Locked File

**Use case:** Prevent modifications to shared or critical files. To unlock, simply rename (remove `.lock`).

Example (`shared_config.lock`):

```text
# This file is locked. Remove .lock extension to edit.
[bot]
prefix = r!
```

**How to use:**

```python
import os

# Unlock by renaming
os.rename("shared_config.lock", "shared_config.luna")

# Lock again after edits
os.rename("shared_config.luna", "shared_config.lock")
```

**Rules:**
- While `.lock` is present, the file should be treated as read-only.
- No automated process should modify a locked file.

---

### `.anim` – Animation Keyframe Data

**Use case:** Store animation keyframes separately from models for reuse across multiple objects.

Example (`walk.anim`):

```text
# ANIM v1
# Target: humanoid_rig
# Duration: 2.0s
# FPS: 30

FRAME 0:
  bone_root: pos(0,0,0) rot(0,0,0,1)

FRAME 15:
  bone_root: pos(0.5,0,0) rot(0,0.38,0,0.92)

FRAME 30:
  bone_root: pos(1,0,0) rot(0,0,0,1)
```

**How to use:**

```python
from pathlib import Path

content = Path("walk.anim").read_text(encoding="utf-8")
# Parse frames and apply to rig
```

---

### `.dep` – Dependencies List

**Use case:** Declare what a file needs to run: modules, models, textures, other assets.

Example (`module.dep`):

```text
# DEP v1
# File: module.pyru

python: numpy>=1.21, requests>=2.28
rust: serde, tokio
assets: models/character.rmodl, textures/skin.texb
```

**How to use:**

```python
from pathlib import Path

deps = Path("module.dep").read_text(encoding="utf-8")
# Parse and install/verify dependencies before running the parent file
```

---

### `.meta` – Metadata Sidecar

**Use case:** Store metadata alongside a main file: hash, author, tags, creation date.

Example (`model.meta`):

```json
{
  "file": "character.rmodl",
  "author": "v86889839",
  "created": "2025-03-15",
  "tags": ["character", "humanoid", "rigged"],
  "sha256": "a1b2c3d4e5f6...",
  "version": "1.0"
}
```

**How to use:**

```python
import json
from pathlib import Path

meta = json.loads(Path("model.meta").read_text(encoding="utf-8"))
print(f"Author: {meta['author']}, Tags: {meta['tags']}")
```

---

### `.bake` – Baked Data

**Use case:** Pre-computed data that doesn't need recalculation every launch: baked lighting, nav meshes, collision data.

Example (`scene.bake`):

```text
# BAKE v1
# Type: lightmap
# Source: scene.luna
# Resolution: 2048x2048

[entry_0]
position: 10,20,5
color: 255,240,200
intensity: 0.8

[entry_1]
position: -15,10,-5
color: 100,150,255
intensity: 0.5
```

**How to use:**

```python
from pathlib import Path

data = Path("scene.bake").read_text(encoding="utf-8")
# Parse entries and load into engine
```

---

### `.diff` – Difference / Patch File

**Use case:** Ship only the changed portions between file versions instead of the entire file.

Example (`v1_to_v2.diff`):

```text
# DIFF v1
# From: config_v1.luna
# To: config_v2.luna

[-] prefix: r!
[+] prefix: !

[-] max_users: 200
[+] max_users: 500
```

**How to use:**

```python
from pathlib import Path

diff = Path("v1_to_v2.diff").read_text(encoding="utf-8")
# Apply [-] removals and [+] additions to the source file
```

---

### `.texb` – Texture Bundle

**Use case:** Pack multiple related textures (diffuse, normal, roughness) into one file with metadata.

Example (`textures.texb`):

```text
# TEXB v1
# Material: wood_planks

[diffuse]
file: wood_diffuse.png
format: RGBA8
size: 1024x1024

[normal]
file: wood_normal.png
format: RGBA8
size: 1024x1024

[roughness]
file: wood_rough.png
format: R8
size: 1024x1024
```

**How to use:**

```python
from pathlib import Path

bundle = Path("textures.texb").read_text(encoding="utf-8")
# Parse sections and load each texture map
```

---

### `.rule` – Validation Rule

**Use case:** Define what counts as "valid" for a file or project. Used by linters and CI checks.

Example (`lint.rule`):

```text
# RULE v1
# Target: *.py, *.pyru

[forbidden]
- os.system
- subprocess.call with shell=True
- eval(
- exec(

[required]
- encoding="utf-8" in all read/write calls

[naming]
- snake_case for functions
- PascalCase for classes
```

**How to use:**

```python
from pathlib import Path

rules = Path("lint.rule").read_text(encoding="utf-8")
# Parse rules and validate target files against them
```

---

### `.seed` – Generator Input

**Use case:** Store parameters for procedural generation: worlds, landscapes, structures.

Example (`world.seed`):

```text
# SEED v1
# Generator: terrain_v2

seed: 42
biome: forest
size: 256x256
height_range: 0-64
noise_octaves: 6
noise_scale: 0.01
water_level: 32
```

**How to use:**

```python
from pathlib import Path

params = Path("world.seed").read_text(encoding="utf-8")
# Parse and feed into procedural generator
```

---

### `.cfgx` – Extended Config

**Use case:** Complex configs with nested structures, conditions, and logic. For advanced LUnlocker and ReBoot settings.

Example (`advanced.cfgx`):

```text
# CFGX v1

[mode: safe]
  scan_depth: shallow
  auto_quarantine: true
  notify_admin: true

[mode: aggressive]
  scan_depth: deep
  auto_quarantine: true
  auto_delete: true
  notify_admin: false

[condition: os_version < 10.0.19041]
  fallback_mode: safe
  warn: "OS too old for aggressive mode"
```

**How to use:**

```python
from pathlib import Path

cfg = Path("advanced.cfgx").read_text(encoding="utf-8")
# Parse sections, evaluate conditions, select active mode
```

---

### `.temp` – Temporary File

**Use case:** Short-lived working files created during processing. Should be deleted after use.

Example (`work.temp`):

```text
# TEMP — auto-generated, safe to delete
processing_id: 8a3f2b1c
step: 3/5
intermediate_hash: d4e5f6...
```

**How to use:**

```python
import os
from pathlib import Path

# Use during processing
Path("work.temp").write_text("intermediate data", encoding="utf-8")

# Clean up when done
os.remove("work.temp")
```

**Rules:**
- `.temp` files should never be committed to version control.
- Any tool finding a `.temp` file older than its session may safely delete it.

---

### `.snap` – State Snapshot

**Use case:** Capture a moment-in-time state of files, settings, or processes.

Example (`checkpoint.snap`):

```text
# SNAP v1
# Timestamp: 2025-03-15T14:30:00
# Reason: pre-update checkpoint

[files]
  config.luna: a1b2c3...
  rules.ctxt: d4e5f6...
  actions.stxt: g7h8i9...

[settings]
  mode: safe
  scan_depth: shallow
```

**How to use:**

```python
from pathlib import Path

snap = Path("checkpoint.snap").read_text(encoding="utf-8")
# Parse and compare against current state to detect changes
```

---

### `.cache` – Cached Computation Results

**Use case:** Store results of expensive operations to avoid recomputation.

Example (`render.cache`):

```text
# CACHE v1
# Computed: 2025-03-15T10:00:00
# Source: scene.bake
# TTL: 86400

result_hash: a1b2c3d4...
data_path: ./render_output/
frame_count: 300
```

**How to use:**

```python
from pathlib import Path
import time

cache = Path("render.cache").read_text(encoding="utf-8")
# Check TTL; if expired, recompute and overwrite
```

---

### `.pref` – User Preferences

**Use case:** Personal settings stored per-project: theme, language, layout.

Example (`user.pref`):

```text
# PREF v1

[ui]
theme: dark
language: ru
font_size: 14

[editor]
tab_size: 4
auto_save: true
format_on_save: true
```

**How to use:**

```python
from pathlib import Path

prefs = Path("user.pref").read_text(encoding="utf-8")
# Parse and apply to UI/editor settings
```

---

### `.plan` – Action Plan

**Use case:** Ordered sequence of steps for builds, migrations, releases.

Example (`release.plan`):

```text
# PLAN v1
# Title: Release 2.0
# Created: 2025-03-15

[steps]
1: Bump version in all .acf manifests
2: Run validation rules (.rule) on all scripts
3: Generate .snap checkpoint
4: Build all .pyru modules
5: Pack textures into .texb bundles
6: Compute SHA-256 for all critical files
7: Update .meta sidecars
8: Tag release in git
```

**How to use:**

```python
from pathlib import Path

plan = Path("release.plan").read_text(encoding="utf-8")
# Parse steps and execute in order
```

---

### `.todo` – Task List

**Use case:** Granular checklist linked to a `.plan` file.

Example (`release.todo`):

```text
# TODO v1
# Linked plan: release.plan

[ ] Bump version in app.acf
[ ] Bump version in core.acf
[x] Run lint.rule on all .py files
[ ] Generate checkpoint.snap
[ ] Build hybrid.pyru
[x] Pack textures.texb
```

**How to use:**

```python
from pathlib import Path

todo = Path("release.todo").read_text(encoding="utf-8")
# Parse checkbox states and update as tasks complete
```

---

### `.draft` – Draft / Rough Sketch

**Use case:** Raw unfinished content. Excluded from builds and execution.

Example (`notes.draft`):

```text
# DRAFT — do not build, do not execute

Ideas for v2.1:
- Add .autho chain for scripts: .unscr → .unscr.autho → .rscr
- Auto-generate .dep files from imports
- Integrate .rule checks into CI
```

**How to use:**

```python
from pathlib import Path

draft = Path("notes.draft").read_text(encoding="utf-8")
# Read for reference; never execute or include in builds
```

**Rules:**
- `.draft` files are always excluded from builds, packaging, and execution.
- They exist for brainstorming and reference only.

---

### `.ref` – Reference Pointer

**Use case:** Link to another file or resource without duplicating data.

Example (`link_to_model.ref`):

```text
# REF v1
type: file
path: ../assets/models/character.rmodl
description: Main character model for cutscene
```

**How to use:**

```python
from pathlib import Path

ref = Path("link_to_model.ref").read_text(encoding="utf-8")
# Parse path and resolve to the actual file
```

---

### `.out` – Program Output

**Use case:** Capture stdout/stderr output of a program run for logging and review.

Example (`build.out`):

```text
# OUT v1
# Program: build.py
# Exit code: 0
# Timestamp: 2025-03-15T14:45:00

Building module: anti_spam...
OK
Building module: points_system...
OK
Building module: role_manager...
OK
All modules built successfully.
```

**How to use:**

```python
from pathlib import Path

output = Path("build.out").read_text(encoding="utf-8")
# Parse header for exit code; archive or display output
```

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
| `.wip` | Mark new commands/plugins as work-in-progress until tested |
| `.lock` | Lock shared config files during live events to prevent accidental edits |
| `.rule` | Validate bot scripts against naming and security rules before deploy |
| `.plan` | Plan feature releases step by step |
| `.todo` | Track granular tasks tied to a plan |
| `.draft` | Brainstorm command ideas without polluting the active codebase |
| `.ref` | Link bot modules to shared assets without duplication |
| `.pref` | Per-server user preferences (theme, language) |

### For LUnlocker (System Utility)

| Format | How to integrate |
|--------|-----------------|
| `.acf` | Verify integrity of critical `.exe` files before launch |
| `.ctxt` | Load signed security policies, refuse to run if tampered |
| `.stxt` | Batch operations: clean → verify → restart service |
| `.unkn` | Analyze unknown files before execution |
| `.cfgx` | Advanced mode-based config (safe / aggressive / fallback) |
| `.snap` | Checkpoint before risky operations, rollback if needed |
| `.cache` | Cache scan results to speed up repeated runs |
| `.dep` | Verify all dependencies are present before launching a module |
| `.meta` | Track file provenance, hash, and version metadata |
| `.bake` | Store pre-computed data (lightmaps, nav meshes) |
| `.diff` | Apply incremental updates without re-downloading entire files |
| `.texb` | Pack and load texture bundles for UI assets |
| `.temp` | Scratch files during multi-step unlock processes |
| `.out` | Capture and archive program output for audit logs |
| `.seed` | Procedural generation parameters for test environments |
| `.anim` | Animation data for UI transitions |

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
    "*.unkn": "plaintext",
    "*.wip": "plaintext",
    "*.lock": "plaintext",
    "*.anim": "plaintext",
    "*.dep": "ini",
    "*.meta": "json",
    "*.bake": "ini",
    "*.diff": "plaintext",
    "*.texb": "ini",
    "*.rule": "ini",
    "*.seed": "ini",
    "*.cfgx": "ini",
    "*.temp": "plaintext",
    "*.snap": "ini",
    "*.cache": "ini",
    "*.pref": "ini",
    "*.plan": "plaintext",
    "*.todo": "plaintext",
    "*.draft": "plaintext",
    "*.ref": "plaintext",
    "*.out": "plaintext"
  }
}
```

## Project Structure

```
custom-formats/
├── custom_formats.py        # Core parser module (all formats)
├── generators/
│   ├── gen_all.py            # Run all generators at once
│   ├── gen_luna.py           # Generate config.luna
│   ├── gen_unkn.py           # Generate mystery.unkn
│   ├── gen_pyru.py           # Generate hybrid.pyru
│   ├── gen_lujit.py          # Generate test.lujit
│   ├── gen_acf.py            # Generate app.acf
│   ├── gen_ctxt.py           # Generate rules.ctxt
│   ├── gen_stxt.py           # Generate actions.stxt
│   ├── gen_wip.py            # Generate module.wip
│   ├── gen_lock.py           # Generate shared.lock
│   ├── gen_anim.py           # Generate walk.anim
│   ├── gen_dep.py            # Generate module.dep
│   ├── gen_meta.py           # Generate model.meta
│   ├── gen_bake.py           # Generate scene.bake
│   ├── gen_diff.py           # Generate v1_to_v2.diff
│   ├── gen_texb.py           # Generate textures.texb
│   ├── gen_rule.py           # Generate lint.rule
│   ├── gen_seed.py           # Generate world.seed
│   ├── gen_cfgx.py           # Generate advanced.cfgx
│   ├── gen_temp.py           # Generate work.temp
│   ├── gen_snap.py           # Generate checkpoint.snap
│   ├── gen_cache.py          # Generate render.cache
│   ├── gen_pref.py           # Generate user.pref
│   ├── gen_plan.py           # Generate release.plan
│   ├── gen_todo.py           # Generate release.todo
│   ├── gen_draft.py          # Generate notes.draft
│   ├── gen_ref.py            # Generate link_to_model.ref
│   └── gen_out.py            # Generate build.out
├── examples/
│   ├── config.luna
│   ├── mystery.unkn
│   ├── hybrid.pyru
│   ├── test.lujit
│   ├── app.acf
│   ├── rules.ctxt
│   ├── actions.stxt
│   ├── module.wip
│   ├── shared.lock
│   ├── walk.anim
│   ├── module.dep
│   ├── model.meta
│   ├── scene.bake
│   ├── v1_to_v2.diff
│   ├── textures.texb
│   ├── lint.rule
│   ├── world.seed
│   ├── advanced.cfgx
│   ├── work.temp
│   ├── checkpoint.snap
│   ├── render.cache
│   ├── user.pref
│   ├── release.plan
│   ├── release.todo
│   ├── notes.draft
│   ├── link_to_model.ref
│   └── build.out
├── LICENSE
└── README.md
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Author

GitHub: [@v86889839-collab](https://github.com/v86889839-collab)
