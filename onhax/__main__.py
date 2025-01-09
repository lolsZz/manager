"""Entry point for onhax project."""
import sys
from .app import OnHaxApp

def main():
    """Main entry point for the application."""
    if len(sys.argv) < 3:
        print("Usage: python -m onhax <prompt> <output_file>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        app = OnHaxApp()
        code = app.generate_code(prompt)
        app.save_generated_code(code, output_file)
        print(f"Generated code saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()