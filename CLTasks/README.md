# CLTasks - A Beautiful Task Manager CLI

✨ CLTasks is a simple yet powerful command-line task manager with a beautiful interface built using Python, Typer, and Rich.

![CLTasks Demo](https://via.placeholder.com/700x400?text=CLTasks+CLI+Demo)

## Features

- ✅ **Beautiful Interface**: Colorful, well-organized display with helpful visual elements
- 📝 **Task Management**: Add, list, complete, and delete tasks with ease
- 🎨 **Rich Text Support**: Color-coded output for better readability
- 🔍 **Task Details**: View detailed information about specific tasks
- ⚡ **Fast & Lightweight**: Minimal dependencies, quick to start

## Installation

```bash
# Install from the repository
pip install -e .

# Or, if you have the package on PyPI
pip install taskcli
```

## Usage

CLTasks provides several commands to manage your tasks:

### Adding Tasks

```bash
cltasks add "Buy groceries"
```

### Listing Tasks

```bash
# List incomplete tasks
cltasks list

# List all tasks (including completed ones)
cltasks list --all
```

### Completing Tasks

```bash
cltasks complete 1
```

### Viewing Task Details

```bash
cltasks show 1
```

### Deleting Tasks

```bash
# With confirmation prompt
cltasks delete 1

# Skip confirmation
cltasks delete 1 --force
```

### Help

```bash
# Show all available commands
cltasks --help

# Show detailed help with examples
cltasks help
```

## Development

CLTasks is built with:

- [Typer](https://typer.tiangolo.com/): For creating the CLI interface
- [Rich](https://rich.readthedocs.io/): For beautiful terminal formatting
- Python 3.9+: For modern language features

To set up for development:

```bash
# Clone the repository
git clone https://github.com/yourusername/cltasks.git
cd cltasks

# Install in development mode
pip install -e .
```

## Storage

CLTasks currently supports:
- Local file storage (default)
- CosmosDB storage (coming soon)

Tasks are stored in `~/.taskcli_tasks.json` by default.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
