# API Reference

## OnHaxApp

Main application class for generating and managing code.

### OnHaxApp Methods

#### `__init__(config: Optional[Config] = None) -> None`

Initialize the OnHaxApp with configuration.

**Args:**

- `config`: Optional configuration instance. If not provided, a new one will be created.

#### `generate_code(prompt: str) -> str`

Generate code based on the provided prompt.

**Args:**

- `prompt`: The natural language prompt describing the code to generate.

**Returns:**

- The generated code as a string.

**Raises:**

- `ConnectionError`: If the API request fails.
- `ValueError`: If the prompt is empty or invalid.

#### `save_generated_code(code: str, filename: str) -> None`

Save generated code to a file.

**Args:**

- `code`: The code content to save.
- `filename`: The path where the code should be saved.

**Raises:**

- `OSError`: If there is an error writing to the file.
- `ValueError`: If code or filename is empty.

## Config

Configuration class for OnHax application.

### Attributes

- `api_key`: API key for authentication with DeepSeek.
- `model`: The model identifier to use for code generation.
- `max_tokens`: Maximum number of tokens in generated response.
- `temperature`: Sampling temperature for generation (0.0-1.0).

### Config Methods

#### `is_configured() -> bool`

Check if the configuration is complete and valid.

#### `validate() -> None`

Validate the configuration settings.

**Raises:**

- `ValueError`: If any configuration values are invalid.

## DeepSeekClient

Client for interacting with the DeepSeek API.

### DeepSeekClient Methods

#### `__init__(config: Config)`

Initialize the DeepSeek API client.

**Args:**

- `config`: Configuration instance containing API credentials.

**Raises:**

- `ValueError`: If the config is not properly configured.

#### `query(prompt: str) -> Dict[str, Any]`

Send a query to the DeepSeek API.

**Args:**

- `prompt`: The natural language prompt for code generation.

**Returns:**

- Response from the API containing generated code and metadata.

**Raises:**

- `ConnectionError`: If the API request fails.
- `ValueError`: If the prompt is empty or invalid.
- `RequestException`: If there is an error communicating with the API.

#### `validate_connection() -> bool`

Validate the API connection and credentials.

**Returns:**

- True if connection is valid, False otherwise.
