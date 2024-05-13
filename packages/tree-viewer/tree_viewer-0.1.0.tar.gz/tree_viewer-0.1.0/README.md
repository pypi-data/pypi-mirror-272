# Tree Viewer

## Overview

This project provides a customizable tree of your current directory or project. The tool allows you to get a complete structure of your project with options to include hidden directories and exclude specific files or directories.

## Installation

```bash
pip install tree-viewer
```

then run:

```bash
tree-viewer
```

you will see your current directory tree in the console.

### Saving Directory Tree

If you want to save the results of your current directory tree, run:

```bash
tree-viewer --output file_name.txt
```

It will generate the results in the current directory `file_name.txt`.

### Include Hidden Directories

The `tree-viewer` tool now supports including hidden directories in the directory tree structure. Hidden directories are those whose names begin with a dot (`.`, such as `.git` or `.config`). By default, hidden directories are excluded from the tree structure.

To include hidden directories in the tree structure, use the `--hidden` flag:

```bash
tree-viewer --hidden
```

### Exclude Specific Directories and Files

The `tree-viewer` tool also allows you to exclude specific directories or files from the directory tree. This can be useful for omitting directories like `node_modules` or files such as `config.json` that you do not want to appear in the output.

To exclude specific directories or files, use the `--excludes` option followed by the names of the directories or files:

```bash
tree-viewer --excludes .git node_modules config.json
```

### Common Issues and Solutions

- **Installation Path:** Ensure that the Python packages installation path is included in your system's PATH environment variable.
- **Shell Restart:** You might need to restart your shell (like Bash) to recognize changes to the PATH environment variable.
- **Permissions:** Ensure that you have the necessary permissions to execute commands from the installed package.
- **Virtual Environment:** If using a virtual environment, make sure it is activated when you attempt to run the command.

## Example Directory Tree

```
project_directory/
📂 src/
│   📂 main/
│   │   📂 java/
│   │   │   📂 com/
│   │   │       📄 Main.java
│   │   📂 resources/
│   │   │   📂 config/
│   │   │       📄 application.properties
│   │   📂 webapp/
│   │       📄 index.html
│   📂 test/
│   │   📂 java/
│   │   │   📂 com/
│   │   │       📄 MainTest.java
│   │   │       📂 example/
│   │   │           📄 MainTest.java
│   │   📂 resources/
│   │       📂 test_config/
│   │           📄 test.properties
📂 docs/
│   📄 documentation.md
📄 README.md
📄 LICENSE
```

**Note:**
If you encounter any issues or have suggestions, please submit them here: [https://github.com/wiliancirillo/tree-viewer](https://github.com/wiliancirillo/tree-viewer).

**Credits**
This project, tree-viewer, is based on and inspired by the Custom Tree project developed by dragon-devs. Our tool extends the original functionality by providing additional features such as the ability to exclude specific files and directories from the tree output. We are grateful to the original authors and contributors of Custom Tree for their pioneering work which served as a foundation for further development in this tool.

For more details about the original project, please visit their GitHub repository: [https://github.com/dragon-devs/custom-tree](https://github.com/dragon-devs/custom-tree).
