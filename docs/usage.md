# Usage Guide

This guide covers how to use OnHax effectively.

## Basic Usage

```python
from onhax.app import OnHaxApp

app = OnHaxApp()
result = app.generate_code("Create a simple Flask application")
app.save_generated_code(result, "app.py")
```

## Command Line Interface

OnHax can be used from the command line:

```bash
onhax generate "Create a React component"
```

## Advanced Features

### Custom Templates

### Configuration Options

### Integration with IDEs

For more examples, see the [examples directory](../examples/).

## Best Practices

1. Always review generated code
2. Use specific prompts
3. Follow security guidelines

## Troubleshooting

Common issues and their solutions are documented in our [troubleshooting guide](troubleshooting.md).
