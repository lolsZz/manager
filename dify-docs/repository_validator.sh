#!/bin/bash

REPO_PATH=$1

# Check if repository path is provided
if [ -z "$REPO_PATH" ]; then
    echo "Please provide repository path"
    exit 1
fi

# Validate git repository
if [ ! -d "$REPO_PATH/.git" ]; then
    echo "Not a valid git repository"
    exit 1
fi

# Check for key files
echo "Repository Structure Analysis:"
echo "----------------------------"
echo "Looking for key files and directories..."

# Common configuration files
CONFIG_FILES=("package.json" "requirements.txt" "Gemfile" "composer.json" "go.mod")
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$REPO_PATH/$file" ]; then
        echo "✓ Found $file"
    fi
done

# Check for documentation
if [ -d "$REPO_PATH/docs" ] || [ -f "$REPO_PATH/README.md" ]; then
    echo "✓ Documentation present"
fi

# Check for tests
if [ -d "$REPO_PATH/tests" ] || [ -d "$REPO_PATH/test" ]; then
    echo "✓ Test directory found"
fi

echo "Analysis complete"
