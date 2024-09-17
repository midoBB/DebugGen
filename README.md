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

## Neovim

If you're using Neovim, feel free to check out my configuration to make everything work seamlessly:

```lua
-- Inside your nvim-dap configuration

-- setup dap config by VsCode launch.json file
local vscode = require("dap.ext.vscode")
local json = require("plenary.json")
vscode.json_decode = function(str)
	local clean_str = json.json_strip_comments(str)
	clean_str = clean_str:gsub('"type"%s*:%s*"lldb"', '"type": "codelldb"')
	clean_str = clean_str:gsub('"type"%s*:%s*"debugpy"', '"type": "python"')
	clean_str = clean_str:gsub('"type"%s*:%s*"go"', '"type": "delve"')
	clean_str = clean_str:gsub('"type"%s*:%s*"chrome"', '"type": "pwa-chrome"')
    	clean_str = clean_str:gsub('"preLaunchTask"%s*:%s*"rust: cargo build"', '"preLaunchTask": "cargo build"')
	return vim.json.decode(clean_str)
end
vscode.load_launchjs(nil, {
	go = { "go" },
	python = { "py" },
	gdb = { "c", "cpp", "rust" },
	lldb = { "c", "cpp", "rust" },
	codelldb = { "c", "cpp", "rust" },
	cppdbg = { "c", "cpp", "rust" },
})
```

I also recommend using [nvim-dap-vscode-js](https://github.com/mxsdev/nvim-dap-vscode-js) to provide a working JS/TS debuggnig experience.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.
