# Auto-generate launch.json for VS Code / Neovim

This script automatically generates a `.vscode/launch.json` file for your project, based on the presence of certain marker files.

## Supported Project Types

- **Go:** `go.mod`
- **TypeScript/JavaScript (Vite):** `package.json`
- **Rust:** `Cargo.toml`
- **Python:** `.py` files with shebang or `__main__`

## How it Works

The script searches for these marker files in your project directory. Based on the markers found, it generates corresponding debug configurations for VS Code / Neovim.

## Usage

1.  **Download the latest release for your platform from the [Releases](https://github.com/midoBB/DebugGen/releases) page.**
2.  **Make it executable (if necessary):**
    ```bash
    chmod +x debuggen-linux  # For Linux
    chmod +x debuggen-macos  # For macOS
    ```
3.  **Run the executable:**
    ```bash
    ./debuggen-linux  # For Linux
    ./debuggen-macos  # For macOS
    ```

This will create a `.vscode/launch.json` file in your project root.

## Build

To build the executable yourself, run:

```bash
make build
```

The executable will be created in the `dist` directory.

## Features

-   Automatically detects project types based on marker files.
-   Generates debug configurations for Go, TypeScript/JavaScript, Rust, and Python.
-   Respects `.gitignore` to exclude files and directories from the search.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.
