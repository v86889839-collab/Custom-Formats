# -*- coding: utf-8 -*-
"""
custom_formats.py — Единый модуль для работы с пользовательскими форматами:
.luna, .unkn, .pyru, .lujit, .acf, .ctxt, .stxt

Совместимость: Python 3.9+
Зависимости: только стандартная библиотека.
"""

from __future__ import annotations

import os
import re
import json
import hashlib
import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Optional


# =====================================================================
# 1. .luna — лёгкий формат для программирования / конфигов
# =====================================================================

@dataclass
class LunaConfig:
    """Простой парсер .luna — ключ: значение, секции, списки."""
    data: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path) -> "LunaConfig":
        """Загрузить .luna файл."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Файл не найден: {p}")
        cfg = cls()
        current_section: Optional[str] = None

        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Секция: [section_name]
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].strip()
                cfg.data[current_section] = {}
                continue
            # key: value
            if ": " in line:
                key, _, value = line.partition(": ")
                key = key.strip()
                value = value.strip()
                # Список: [item1, item2, item3]
                if value.startswith("[") and value.endswith("]"):
                    value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
                # Число
                elif value.isdigit():
                    value = int(value)
                elif _is_float(value):
                    value = float(value)
                if current_section:
                    cfg.data[current_section][key] = value
                else:
                    cfg.data[key] = value
        return cfg

    def save(self, path: str | Path) -> None:
        """Сохранить .luna файл."""
        p = Path(path)
        lines: list[str] = []
        for key, value in self.data.items():
            if isinstance(value, dict):
                lines.append(f"[{key}]")
                for k, v in value.items():
                    lines.append(f"  {k}: {_format_value(v)}")
                lines.append("")
            else:
                lines.append(f"{key}: {_format_value(value)}")
        p.write_text("\n".join(lines), encoding="utf-8")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        return self.data.get(section, {}).get(key, default)


def _is_float(val: str) -> bool:
    try:
        float(val)
        return True
    except ValueError:
        return False


def _format_value(val: Any) -> str:
    if isinstance(val, list):
        return "[" + ", ".join(str(v) for v in val) + "]"
    return str(val)


# =====================================================================
# 2. .unkn — авто-определение языка и переименование
# =====================================================================

# Сигнатуры для определения языка по содержимому
_LANG_SIGNATURES: list[tuple[str, list[str]]] = [
    ("py", [r"^#!.*python", r"^\s*def\s+\w+\(", r"^\s*import\s+\w+", r"^\s*from\s+\w+\s+import"]),
    ("rs", [r"^\s*fn\s+\w+\(", r"^\s*use\s+\w+::", r"^\s*pub\s+(fn|struct|enum)\s+\w+"]),
    ("lua", [r"^\s*local\s+\w+\s*=", r"^\s*function\s+\w+\(", r"^\s*require\s*[\(\"]"]),
    ("js", [r"^\s*const\s+\w+\s*=", r"^\s*function\s+\w+\(", r"^\s*import\s+.*from\s+"]),
    ("c", [r"^\s*#include\s*<", r"^\s*int\s+main\s*\("]),
    ("cpp", [r"^\s*#include\s*<", r"^\s*std::", r"^\s*class\s+\w+\s*\{"]),
    ("go", [r"^\s*package\s+\w+", r"^\s*func\s+\w+\(", r"^\s*import\s+\("]),
    ("sh", [r"^#!/bin/(ba)?sh", r"^\s*echo\s+"]),
    ("java", [r"^\s*public\s+(class|static|void)\s+", r"^\s*import\s+java\."]),
]

# Приоритетный список расширений для LuaJIT
_LUAJIT_MARKERS = ["jit", "luajit", "ffi.cdef", "ffi.C"]


def detect_language(content: str) -> str:
    """Определить язык программирования по содержимому файла."""
    # Проверка LuaJIT
    for marker in _LUAJIT_MARKERS:
        if marker in content:
            return "lujit"

    # Проверка по сигнатурам
    for lang, patterns in _LANG_SIGNATURES:
        score = 0
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE):
                score += 1
        if score >= 2:
            return lang

    # Низкий порог: хотя бы 1 совпадение
    for lang, patterns in _LANG_SIGNATURES:
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE):
                return lang

    return "txt"


def process_unkn(path: str | Path, dry_run: bool = False) -> str:
    """
    Прочитать .unkn файл, определить язык, переименовать в подходящее расширение.
    Возвращает путь к новому файлу.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")

    content = p.read_text(encoding="utf-8", errors="replace")
    lang = detect_language(content)

    # Маппинг язык -> расширение
    ext_map = {
        "py": "py", "rs": "rs", "lua": "lua", "lujit": "lujit",
        "js": "js", "c": "c", "cpp": "cpp", "go": "go",
        "sh": "sh", "java": "java", "txt": "txt",
    }
    new_ext = ext_map.get(lang, "txt")
    new_path = p.with_suffix(f".{new_ext}")

    if dry_run:
        print(f"[DRY RUN] {p.name} -> {new_path.name} (язык: {lang})")
    else:
        p.rename(new_path)
        print(f"[OK] {p.name} -> {new_path.name} (язык: {lang})")

    return str(new_path)


def process_unkn_folder(
    folder: str | Path, dry_run: bool = False
) -> list[str]:
    """Обработать все .unkn файлы в папке."""
    f = Path(folder)
    results: list[str] = []
    for fpath in f.iterdir():
        if fpath.suffix == ".unkn":
            results.append(process_unkn(fpath, dry_run))
    return results


# =====================================================================
# 3. .pyru — слияние Python и Rust в одном файле
# =====================================================================

_PYRU_PYTHON_MARKER = "# === PYTHON ==="
_PYRU_RUST_MARKER = "# === RUST ==="
_PYRU_END_MARKER = "# === END ==="


def create_pyru(python_code: str, rust_code: str, path: str | Path) -> None:
    """Создать .pyru файл с секциями Python и Rust."""
    p = Path(path)
    content = f"""{_PYRU_PYTHON_MARKER}
{python_code}
{_PYRU_END_MARKER}
{_PYRU_RUST_MARKER}
{rust_code}
{_PYRU_END_MARKER}
"""
    p.write_text(content.strip() + "\n", encoding="utf-8")


def parse_pyru(path: str | Path) -> dict[str, str]:
    """
    Разобрать .pyru файл, вернуть {'python': code, 'rust': code}.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")

    content = p.read_text(encoding="utf-8")
    result: dict[str, str] = {"python": "", "rust": ""}

    current_block: Optional[str] = None
    block_lines: list[str] = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped == _PYRU_PYTHON_MARKER:
            current_block = "python"
            block_lines = []
            continue
        elif stripped == _PYRU_RUST_MARKER:
            if current_block:
                result[current_block] = "\n".join(block_lines).strip()
            current_block = "rust"
            block_lines = []
            continue
        elif stripped == _PYRU_END_MARKER:
            if current_block:
                result[current_block] = "\n".join(block_lines).strip()
            current_block = None
            block_lines = []
            continue

        if current_block:
            block_lines.append(line)

    # Если файл кончился без END-маркера
    if current_block and block_lines:
        result[current_block] = "\n".join(block_lines).strip()

    return result


def run_pyru(
    path: str | Path,
    python_executable: str = "python",
    rust_compiler: str = "rustc",
    temp_dir: str | Path = ".pyru_temp",
) -> dict[str, Any]:
    """
    Разобрать .pyru, скомпилировать Rust, запустить Python.
    Возвращает {'python_output': ..., 'rust_output': ..., 'rust_compiled': bool}.
    """
    parts = parse_pyru(path)
    result: dict[str, Any] = {"python_output": "", "rust_output": "", "rust_compiled": False}

    # Python
    if parts["python"]:
        proc = subprocess.run(
            [python_executable, "-c", parts["python"]],
            capture_output=True, text=True, timeout=30,
        )
        result["python_output"] = proc.stdout + proc.stderr

    # Rust
    if parts["rust"]:
        tmp = Path(temp_dir)
        tmp.mkdir(exist_ok=True)
        rs_file = tmp / "_pyru_rust.rs"
        rs_file.write_text(parts["rust"], encoding="utf-8")
        exe_file = tmp / "_pyru_rust"
        compile_proc = subprocess.run(
            [rust_compiler, "-o", str(exe_file), str(rs_file)],
            capture_output=True, text=True, timeout=60,
        )
        if compile_proc.returncode == 0:
            result["rust_compiled"] = True
            run_proc = subprocess.run(
                [str(exe_file)],
                capture_output=True, text=True, timeout=30,
            )
            result["rust_output"] = run_proc.stdout + run_proc.stderr
        else:
            result["rust_output"] = f"[Ошибка компиляции]\n{compile_proc.stderr}"

    return result


# =====================================================================
# 4. .lujit — запуск LuaJIT-файлов
# =====================================================================

def is_lujit_file(path: str | Path) -> bool:
    """Проверить, что файл имеет расширение .lujit."""
    return Path(path).suffix == ".lujit"


def run_lujit(
    path: str | Path,
    luajit_executable: str = "luajit",
    fallback_to_lua: bool = False,
    lua_executable: str = "lua",
) -> dict[str, Any]:
    """
    Запустить .lujit файл через LuaJIT.
    Если LuaJIT не найден, можно откатиться к обычному Lua.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")
    if not is_lujit_file(p):
        raise ValueError(f"Ожидался .lujit файл, получено: {p.suffix}")

    # Проверка доступности LuaJIT
    lujit_path = shutil.which(luajit_executable)
    if lujit_path:
        proc = subprocess.run(
            [lujit_path, str(p)],
            capture_output=True, text=True, timeout=60,
        )
        return {
            "runner": "luajit",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    elif fallback_to_lua:
        lua_path = shutil.which(lua_executable)
        if lua_path:
            proc = subprocess.run(
                [lua_path, str(p)],
                capture_output=True, text=True, timeout=60,
            )
            return {
                "runner": "lua (fallback)",
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "warning": "LuaJIT не найден, использован обычный Lua",
            }
    return {
        "runner": "none",
        "returncode": -1,
        "stdout": "",
        "stderr": "LuaJIT не найден в системе",
    }


def validate_lujit(path: str | Path) -> tuple[bool, str]:
    """
    Базовая проверка: нет ли в .lujit очевидно LuaJIT-специфичных
    конструкций, которые упадут на обычном Lua (для диагностики).
    """
    p = Path(path)
    content = p.read_text(encoding="utf-8", errors="replace")
    jit_features = []
    if "ffi." in content:
        jit_features.append("ffi")
    if "jit." in content:
        jit_features.append("jit")
    if "require('ffi')" in content or 'require("ffi")' in content:
        jit_features.append("require ffi")

    if jit_features:
        return True, f"Найдены LuaJIT-фичи: {', '.join(jit_features)}. Обычный Lua не подойдёт."
    return True, "LuaJIT-специфичных конструкций не найдено. Можно запустить и на обычном Lua."


# =====================================================================
# 5. .acf — манифест критического exe-файла
# =====================================================================

@dataclass
class AcfManifest:
    """Манифест для критического .exe файла."""
    exe_name: str
    version: str = "1.0.0"
    critical: bool = True
    description: str = ""
    expected_sha256: str = ""
    min_os_version: str = ""
    requires_admin: bool = False
    auto_restart: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "exe_name": self.exe_name,
            "version": self.version,
            "critical": self.critical,
            "description": self.description,
            "expected_sha256": self.expected_sha256,
            "min_os_version": self.min_os_version,
            "requires_admin": self.requires_admin,
            "auto_restart": self.auto_restart,
        }

    @classmethod
    def load(cls, path: str | Path) -> "AcfManifest":
        p = Path(path)
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(**data)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def verify_exe(self, exe_dir: str | Path) -> tuple[bool, str]:
        """
        Проверить существование .exe и совпадение хеша (если задан).
        """
        exe_path = Path(exe_dir) / self.exe_name
        if not exe_path.exists():
            return False, f"EXE не найден: {exe_path}"

        if self.expected_sha256:
            sha = hashlib.sha256(exe_path.read_bytes()).hexdigest()
            if sha != self.expected_sha256:
                return False, (
                    f"Хеш не совпадает!\n"
                    f"  Ожидался: {self.expected_sha256}\n"
                    f"  Получен:  {sha}"
                )
            return True, f"OK: хеш совпадает, файл критический: {self.critical}"

        return True, f"OK: файл найден, хеш не задан, критический: {self.critical}"


def create_acf(
    exe_name: str,
    exe_path: str | Path,
    output_path: str | Path,
    version: str = "1.0.0",
    description: str = "",
    requires_admin: bool = False,
    auto_restart: bool = False,
) -> AcfManifest:
    """Создать .acf манифест для exe-файла с автоподстановкой хеша."""
    exe = Path(exe_path)
    if not exe.exists():
        raise FileNotFoundError(f"EXE не найден: {exe}")
    sha = hashlib.sha256(exe.read_bytes()).hexdigest()

    manifest = AcfManifest(
        exe_name=exe_name,
        version=version,
        critical=True,
        description=description,
        expected_sha256=sha,
        requires_admin=requires_admin,
        auto_restart=auto_restart,
    )
    manifest.save(output_path)
    return manifest


# =====================================================================
# 6. .ctxt — Critical TXT, текстовый файл с проверкой целостности
# =====================================================================

_CTXT_SIGNATURE_LINE = "# CTXT-SIGNATURE: "


def save_ctxt(
    path: str | Path,
    content: str,
    critical_level: str = "high",
    description: str = "",
) -> None:
    """
    Сохранить .ctxt файл с SHA-256 подписью содержимого.
    Структура:
        # CTXT-CRITICAL: <level>
        # CTXT-DESC: <description>
        # CTXT-SIGNATURE: <sha256_hex>
        --- содержимое ---
    """
    sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    header = (
        f"# CTXT-CRITICAL: {critical_level}\n"
        f"# CTXT-DESC: {description}\n"
        f"{_CTXT_SIGNATURE_LINE}{sha}\n"
    )
    Path(path).write_text(header + content, encoding="utf-8")


def load_ctxt(path: str | Path) -> dict[str, Any]:
    """
    Загрузить .ctxt, проверить подпись.
    Возвращает {'valid': bool, 'content': str, 'critical_level': str, 'description': str}.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")

    raw = p.read_text(encoding="utf-8")
    lines = raw.splitlines()

    critical_level = "unknown"
    description = ""
    signature = ""
    content_start = 0

    for i, line in enumerate(lines):
        if line.startswith("# CTXT-CRITICAL:"):
            critical_level = line.split(":", 1)[1].strip()
        elif line.startswith("# CTXT-DESC:"):
            description = line.split(":", 1)[1].strip()
        elif line.startswith(_CTXT_SIGNATURE_LINE):
            signature = line[len(_CTXT_SIGNATURE_LINE):].strip()
        elif not line.startswith("#"):
            content_start = i
            break

    content = "\n".join(lines[content_start:])
    actual_sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
    valid = (actual_sha == signature) if signature else False

    return {
        "valid": valid,
        "content": content,
        "critical_level": critical_level,
        "description": description,
        "expected_sha256": signature,
        "actual_sha256": actual_sha,
    }


# =====================================================================
# 7. .stxt — Script TXT, последовательность команд
# =====================================================================

@dataclass
class StxtCommand:
    command: str
    params: dict[str, str] = field(default_factory=dict)

    def __repr__(self) -> str:
        params_str = ", ".join(f"{k}={v}" for k, v in self.params.items())
        return f"StxtCommand({self.command}, {params_str})"


def parse_stxt(path: str | Path) -> list[StxtCommand]:
    """
    Разобрать .stxt файл в список команд.
    Формат:
        # SCRIPT_TXT v1
        # Комментарии начинаются с #

        COMMAND: r!add-points
        TARGET: PBSTHelper
        AMOUNT: 100

        COMMAND: r!give-role
        USER: @User123
        ROLE: mod_role
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Файл не найден: {p}")

    commands: list[StxtCommand] = []
    current_cmd: Optional[StxtCommand] = None

    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        key, _, value = line.partition(": ")
        key = key.strip().upper()
        value = value.strip()

        if key == "COMMAND":
            if current_cmd:
                commands.append(current_cmd)
            current_cmd = StxtCommand(command=value)
        elif current_cmd:
            current_cmd.params[key] = value

    if current_cmd:
        commands.append(current_cmd)

    return commands


def create_stxt(
    commands: list[dict[str, Any]],
    path: str | Path,
    version: str = "v1",
) -> None:
    """
    Создать .stxt файл из списка команд.
    commands: [{"command": "r!add-points", "TARGET": "user", "AMOUNT": "100"}, ...]
    """
    lines = [f"# SCRIPT_TXT {version}", "# Автогенерировано custom_formats.py", ""]

    for cmd in commands:
        command = cmd.pop("command")
        lines.append(f"COMMAND: {command}")
        for key, value in cmd.items():
            lines.append(f"{key}: {value}")
        lines.append("")

    Path(path).write_text("\n".join(lines), encoding="utf-8")


def execute_stxt(
    path: str | Path,
    handler: Any = None,
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    """
    Выполнить команды из .stxt файла.
    handler — callable(command: str, params: dict) -> Any.
    Если handler не задан, просто печатает команды.
    Возвращает список результатов.
    """
    commands = parse_stxt(path)
    results: list[dict[str, Any]] = []

    for cmd in commands:
        if dry_run:
            print(f"[DRY RUN] {cmd.command} | {cmd.params}")
            results.append({"command": cmd.command, "status": "dry_run", "params": cmd.params})
            continue

        if handler:
            try:
                result = handler(cmd.command, cmd.params)
                results.append({"command": cmd.command, "status": "ok", "result": result})
            except Exception as e:
                results.append({"command": cmd.command, "status": "error", "error": str(e)})
        else:
            print(f"{cmd.command} | {cmd.params}")
            results.append({"command": cmd.command, "status": "printed", "params": cmd.params})

    return results


# =====================================================================
# Единая точка входа: формат → обработчик
# =====================================================================

FORMAT_REGISTRY: dict[str, str] = {
    ".luna":  "LunaConfig.load() — загрузка конфига",
    ".unkn":  "process_unkn() — авто-определение и переименование",
    ".pyru":  "parse_pyru() / run_pyru() — слияние Python + Rust",
    ".lujit": "run_lujit() / validate_lujit() — запуск LuaJIT",
    ".acf":   "AcfManifest.load() / verify_exe() — манифест критического exe",
    ".ctxt":  "load_ctxt() / save_ctxt() — критический текст с подписью",
    ".stxt":  "parse_stxt() / execute_stxt() — скриптовые команды",
}


def print_formats() -> None:
    """Вывести список всех поддерживаемых форматов."""
    print("=" * 60)
    print(" Custom Formats — поддерживаемые расширения")
    print("=" * 60)
    for ext, desc in FORMAT_REGISTRY.items():
        print(f"  {ext:8s} — {desc}")
    print("=" * 60)


# =====================================================================
# Быстрый тест всех форматов (демо)
# =====================================================================

if __name__ == "__main__":
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="custom_formats_"))
    print(f"Тестовая папка: {tmp}\n")

    # --- .luna ---
    print(">>> .luna")
    luna_file = tmp / "config.luna"
    Path(luna_file).write_text(
        "# Конфиг бота\n"
        "bot_name: ReBoot\n"
        "prefix: r!\n"
        "[roles]\n"
        "  mod: 123456789\n"
        "  admin: 987654321\n"
        "[features]\n"
        "  enabled: true\n", encoding="utf-8")
    cfg = LunaConfig.load(luna_file)
    print(f"  bot_name = {cfg.get('', 'bot_name')}")
    print(f"  mod role = {cfg.get('roles', 'mod')}")
    print(f"  raw data = {cfg.data}\n")

    # --- .unkn ---
    print(">>> .unkn")
    unkn_file = tmp / "mystery.unkn"
    Path(unkn_file).write_text(
        "def hello():\n"
        "    print('hello')\n"
        "import os\n", encoding="utf-8")
    new_path = process_unkn(unkn_file, dry_run=True)
    print(f"  Результат: {new_path}\n")

    # --- .pyru ---
    print(">>> .pyru")
    pyru_file = tmp / "hybrid.pyru"
    create_pyru(
        python_code="print('Hello from Python')",
        rust_code='fn main() { println!("Hello from Rust"); }',
        path=pyru_file,
    )
    parts = parse_pyru(pyru_file)
    print(f"  Python block:\n{parts['python']}")
    print(f"  Rust block:\n{parts['rust']}\n")

    # --- .lujit ---
    print(">>> .lujit")
    lujit_file = tmp / "test.lujit"
    Path(lujit_file).write_text(
        'print("LuaJIT test")\n'
        'local ffi = require("ffi")\n', encoding="utf-8")
    valid, msg = validate_lujit(lujit_file)
    print(f"  Валидация: {valid}, {msg}")
    result = run_lujit(lujit_file, fallback_to_lua=True)
    print(f"  Runner: {result['runner']}, rc: {result['returncode']}")
    if result.get("stdout"):
        print(f"  stdout: {result['stdout']}")
    if result.get("stderr"):
        print(f"  stderr: {result['stderr']}")
    print()

    # --- .acf ---
    print(">>> .acf")
    fake_exe = tmp / "critical_app.exe"
    Path(fake_exe).write_bytes(b"\x4d\x5a\x90\x00")  # MZ header
    acf_file = tmp / "critical_app.acf"
    manifest = create_acf(
        exe_name="critical_app.exe",
        exe_path=fake_exe,
        output_path=acf_file,
        description="Критический компонент LUnlocker",
        requires_admin=True,
    )
    ok, msg = manifest.verify_exe(tmp)
    print(f"  Verify: {ok}, {msg}\n")

    # --- .ctxt ---
    print(">>> .ctxt")
    ctxt_file = tmp / "rules.ctxt"
    save_ctxt(
        ctxt_file,
        content="Правила модерации:\n1. Бан за спам\n2. Мут за флуд",
        critical_level="high",
        description="Правила модерации сервера",
    )
    ctxt_data = load_ctxt(ctxt_file)
    print(f"  Валиден: {ctxt_data['valid']}")
    print(f"  Уровень: {ctxt_data['critical_level']}")
    print(f"  Содержимое: {ctxt_data['content'][:40]}...\n")

    # --- .stxt ---
    print(">>> .stxt")
    stxt_file = tmp / "actions.stxt"
    create_stxt(
        [
            {"command": "r!add-points", "TARGET": "PBSTHelper", "AMOUNT": "100"},
            {"command": "r!give-role", "USER": "@User123", "ROLE": "mod_role"},
        ],
        stxt_file,
    )
    cmds = parse_stxt(stxt_file)
    for c in cmds:
        print(f"  {c}")
    print()
    results = execute_stxt(stxt_file, dry_run=True)
    print(f"  Dry run: {len(results)} команд\n")

    print(">>> Все форматы проверены!")
    print_formats()
