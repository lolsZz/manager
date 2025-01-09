# OnHax 🚀

AI-powered code generation and project automation tool.

## Overview

OnHax is a powerful tool that helps developers generate and manage code using AI. It leverages
the DeepSeek API to provide intelligent code generation capabilities while maintaining a clean
and maintainable codebase.

## Features

- AI-powered code generation
- Project structure automation
- Customizable templates
- Command-line interface
- Python API for integration
- Extensive configuration options

## Quick Start

```bash
# Install using pip
pip install onhax

# Or using uv (recommended)
uv pip install onhax
```

## Project Structure

```
onhax/
├── docs/              # Documentation
├── examples/          # Usage examples
├── onhax/            # Main package
│   ├── app.py        # Core application
│   ├── client.py     # API client
│   ├── config.py     # Configuration
│   └── installer/    # Installation utilities
├── tests/            # Test suite
├── .github/          # GitHub workflows
├── pyproject.toml    # Project configuration
└── README.md         # This file
```

## Development

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/onhax.git
   cd onhax
   ```

2. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

4. Run tests:

   ```bash
   pytest
   ```

## Documentation

For detailed documentation, see the [docs](docs/) directory:

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [API Reference](docs/api-reference.md)
- [Contributing Guide](CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Built with ❤️ using DeepSeek's powerful AI technology.

This repository contains a powerful coding assistant application that integrates with the DeepSeek API to process user conversations and generate structured JSON responses. Through an intuitive command-line interface, it can read local file contents, create new files, and apply diff edits to existing files in real time.

## Key Features

1. DeepSeek Client Configuration

   - Automatically configures an API client to use the DeepSeek service with a valid DEEPSEEK_API_KEY.
   - Connects to the DeepSeek endpoint specified in the environment variable to stream GPT-like completions.

2. Data Models
   - Leverages Pydantic for type-safe handling of file operations, including:
     • FileToCreate – describes files to be created or updated.  
     • FileToEdit – describes specific snippet replacements in an existing file.  
     • AssistantResponse – structures chat responses and potential file operations.  

3. System Prompt
   - A comprehensive system prompt (system_PROMPT) guides conversation, ensuring all replies strictly adhere to JSON output with optional file creations or edits.  

4. Helper Functions
   - read_local_file: Reads a target filesystem path and returns its content as a string.  
   - create_file: Creates or overwrites a file with provided content.  
   - show_diff_table: Presents proposed file changes in a rich, multi-line table.  
   - apply_diff_edit: Applies snippet-level modifications to existing files.  

5. "/add" Command
   - Users can type "/add path/to/file" to quickly read a file's content and insert it into the conversation as a system message.  
   - This allows the assistant to reference the file contents for further discussion, code generation, or diff proposals.  

6. Conversation Flow
   - Maintains a conversation_history list to track messages between user and assistant.  
   - Streams the assistant's replies via the DeepSeek API, parsing them as JSON to preserve both the textual response and the instructions for file modifications.  

7. Interactive Session
   - Run the script (for example: "python3 main.py") to start an interactive loop at your terminal.  
   - Enter your requests or code questions. Enter "/add path/to/file" to add file contents to the conversation.  
   - When the assistant suggests new or edited files, you can confirm changes directly in your local environment.  
   - Type "exit" or "quit" to end the session.  

## Getting Started

1. Prepare a .env file with your DeepSeek API key:
   DEEPSEEK_API_KEY=your_api_key_here

2. Install dependencies and run (choose one method):

   ### Using pip

   ```bash
   pip install -r requirements.txt
   python3 main.py
   ```

   ### Using uv (faster alternative)

   ```bash
   uv venv

   uv run main.py
   ```

3. Enjoy multi-line streaming responses, file read-ins with "/add path/to/file", and precise file edits when approved.

> **Note**: This is an experimental project developed by Skirano to test the new DeepSeek v3 API capabilities. It was developed as a rapid prototype and should be used accordingly.
