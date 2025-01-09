# OnHax: AI-Powered Code Generation Tool

OnHax is a command-line application that leverages the DeepSeek API to generate code based on user-provided prompts. It simplifies the process of code generation by allowing users to describe their requirements in natural language and receive corresponding code output.

This tool is designed for developers who want to quickly prototype ideas or get assistance with coding tasks. OnHax handles the interaction with the DeepSeek API, processes the response, and saves the generated code to a file, streamlining the workflow from concept to implementation.

## Repository Structure

- `__init__.py`: Marks the `onhax` directory as a Python package.
- `__main__.py`: Entry point for the application, handles command-line arguments.
- `app.py`: Contains the main `OnHaxApp` class that orchestrates the code generation process.
- `client.py`: Implements the `DeepSeekClient` for API communication.
- `config.py`: Manages configuration settings, including API credentials.

## Usage Instructions

### Installation

1. Ensure you have Python 3.6 or later installed.
2. Clone the repository:
   ```
   git clone <repository_url>
   cd onhax
   ```
3. Install the required dependencies:
   ```
   pip install requests
   ```

### Configuration

Set the DeepSeek API key as an environment variable:

```
export DEEPSEEK_API_KEY=your_api_key_here
```

### Getting Started

To generate code, run the following command:

```
python -m onhax "<your_prompt>" <output_file>
```

Replace `<your_prompt>` with a description of the code you want to generate, and `<output_file>` with the desired filename for the generated code.

Example:

```
python -m onhax "Create a Python function that calculates the Fibonacci sequence" fibonacci.py
```

This will generate the code and save it to `fibonacci.py`.

### Common Use Cases

1. Generate a basic data structure implementation:
   ```
   python -m onhax "Implement a binary search tree in Python" bst.py
   ```

2. Create a utility function:
   ```
   python -m onhax "Write a function to validate email addresses" email_validator.py
   ```

3. Generate a simple API endpoint:
   ```
   python -m onhax "Create a Flask route for user registration" user_registration.py
   ```

### Troubleshooting

1. API Key Not Configured
   - Problem: You receive a "DeepSeek API key not configured" error.
   - Solution: Ensure you've set the `DEEPSEEK_API_KEY` environment variable correctly.
   - Diagnostic steps:
     1. Check if the environment variable is set:
        ```
        echo $DEEPSEEK_API_KEY
        ```
     2. If it's not set or incorrect, set it again:
        ```
        export DEEPSEEK_API_KEY=your_correct_api_key
        ```

2. Network Connection Issues
   - Problem: The application fails to connect to the DeepSeek API.
   - Solution: Check your internet connection and firewall settings.
   - Diagnostic steps:
     1. Test your internet connection:
        ```
        ping api.deepseek.com
        ```
     2. If the ping fails, troubleshoot your network connection.
     3. If the ping succeeds but the application still fails, check if your firewall is blocking the connection.

### Debugging

To enable debug mode, set the `ONHAX_DEBUG` environment variable:

```
export ONHAX_DEBUG=1
```

This will increase the verbosity of the application's output, providing more detailed information about the API requests and responses.

Log files are stored in the user's home directory under `.onhax/logs/`. Ensure you have write permissions to this directory.

## Data Flow

The OnHax application follows a straightforward data flow for code generation:

1. User input (prompt) -> 2. OnHaxApp -> 3. DeepSeekClient -> 4. DeepSeek API -> 5. Response processing -> 6. File output

```
[User] -> (prompt) -> [OnHaxApp] -> [DeepSeekClient] -> [DeepSeek API]
                                                              |
[File] <- (generated code) <- [OnHaxApp] <- [DeepSeekClient] <-
```

1. The user provides a prompt describing the desired code.
2. The `OnHaxApp` instance processes the input and prepares the API request.
3. The `DeepSeekClient` sends the request to the DeepSeek API.
4. The API generates the code based on the prompt.
5. The `DeepSeekClient` receives the response and extracts the generated code.
6. The `OnHaxApp` saves the generated code to the specified output file.

Note: Ensure that your DeepSeek API key has sufficient permissions and quota for code generation requests.