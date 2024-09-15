#!/usr/bin/env python3
import json
import os
from typing import Dict, List

import toml
from gitignore_parser import parse_gitignore


def is_hidden(path):
    return os.path.basename(path).startswith(".")


def find_markers(marker: str, start_dir: str = ".") -> List[str]:
    matches = []

    gitignore = os.path.join(start_dir, ".gitignore")
    if os.path.exists(gitignore):
        ignore_matcher = parse_gitignore(gitignore)
    else:

        def ignore_matcher(f):
            return False

    for root, dirs, files in os.walk(start_dir, topdown=True):
        dirs[:] = [d for d in dirs if not is_hidden(d)]
        dirs[:] = [d for d in dirs if not ignore_matcher(
            os.path.join(root, d))]

        if marker in files and not ignore_matcher(os.path.join(root, marker)):
            matches.append(root)

    return matches


def find_python_main_files(start_dir: str = ".") -> List[str]:
    main_files = []

    gitignore = os.path.join(start_dir, ".gitignore")
    if os.path.exists(gitignore):
        ignore_matcher = parse_gitignore(gitignore)
    else:

        def ignore_matcher(f):
            return False

    for root, dirs, files in os.walk(start_dir, topdown=True):
        dirs[:] = [d for d in dirs if not is_hidden(d)]
        dirs[:] = [d for d in dirs if not ignore_matcher(
            os.path.join(root, d))]

        for file in files:
            if file.endswith(".py") and not ignore_matcher(os.path.join(root, file)):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    if (
                        content.startswith("#!/usr/bin/env python")
                        or content.startswith("#!/usr/bin/python")
                        or "__main__" in content
                    ):
                        main_files.append(file_path)

    return main_files


def generate_go_config(go_root: str) -> Dict:
    return {
        "name": f"Launch Go Package ({os.path.relpath(go_root)})",
        "type": "go",
        "request": "launch",
        "console": "integratedTerminal",
        "program": go_root,
    }


def generate_typescript_config(ts_root: str) -> Dict:
    return {
        "name": f"Launch Chrome ({os.path.relpath(ts_root)})",
        "request": "launch",
        "type": "chrome",
        "url": "http://localhost:5173",
        "webRoot": ts_root,
    }


def generate_python_config(file_path: str) -> Dict:
    venv_path = os.getenv("VIRTUAL_ENV") or os.getenv("CONDA_PREFIX")
    python_path = None
    if venv_path:
        if os.name == "nt":  # Windows
            python_path = os.path.join(venv_path, "Scripts", "python")
        else:  # Unix-like systems (Linux, macOS)
            python_path = os.path.join(venv_path, "bin", "python")
        # Ensure the python_path exists
        if not os.path.exists(python_path):
            python_path = None

    config = {
        "name": f"Python: {os.path.relpath(file_path)}",
        "type": "debugpy",
        "request": "launch",
        "program": file_path,
        "console": "integratedTerminal",
    }

    if python_path:
        config["pythonPath"] = os.path.relpath(python_path)

    return config


def generate_rust_configs(cargo_toml_path: str) -> List[Dict]:
    with open(cargo_toml_path, "r") as f:
        cargo_toml = toml.load(f)
    if "package" not in cargo_toml:
        return []
    package_name = cargo_toml["package"]["name"]
    bin_targets = cargo_toml.get("bin", [])
    configs = []
    if not bin_targets:
        # Assume it's a library or single binary project
        bin_name = package_name.replace("-", "_")
        configs.append(
            {
                "type": "lldb",
                "request": "launch",
                "name": f"Debug executable '{bin_name}'",
                "preLaunchTask": "rust: cargo build",
                "console": "integratedTerminal",
                "program": f"${{workspaceFolder}}/target/debug/{bin_name}",
                "args": [],
                "cwd": "${workspaceFolder}",
            }
        )
    else:
        # Multiple binary targets
        for target in bin_targets:
            bin_name = target["name"]
            configs.append(
                {
                    "type": "lldb",
                    "request": "launch",
                    "name": f"Debug executable '{bin_name}'",
                    "preLaunchTask": "rust: cargo build",
                    "console": "integratedTerminal",
                    "program": f"${{workspaceFolder}}/target/debug/{bin_name}",
                    "args": [],
                    "cwd": "${workspaceFolder}",
                }
            )
    return configs


def generate_launch_json():
    configurations = []

    go_roots = find_markers("go.mod")
    for go_root in go_roots:
        configurations.append(generate_go_config(go_root))

    ts_roots = find_markers("package.json")
    for ts_root in ts_roots:
        configurations.append(generate_typescript_config(ts_root))

    rust_roots = find_markers("Cargo.toml")
    for rust_root in rust_roots:
        configurations.extend(
            generate_rust_configs(os.path.join(rust_root, "Cargo.toml"))
        )

    python_main_files = find_python_main_files()
    for python_file in python_main_files:
        configurations.append(generate_python_config(python_file))

    if configurations:
        launch_json = {"version": "0.2.0", "configurations": configurations}

        os.makedirs(".vscode", exist_ok=True)
        with open(".vscode/launch.json", "w") as f:
            json.dump(launch_json, f, indent=4)

        print(f"Generated launch.json with {
              len(configurations)} configuration(s)")
    else:
        print("No supported project markers (go.mod, package.json, Cargo.toml) found")


if __name__ == "__main__":
    generate_launch_json()
