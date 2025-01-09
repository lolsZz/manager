# Project Installation Automation Framework

This framework provides a universal way to automate GitHub project installations by:

1. **Mapping Documentation to Code**: We parse setup documentation (like setup-instructions.md) and map each step to automated actions.

2. **Smart Command Translation**: Manual commands from docs are translated to cross-platform code:
   ```python
   # In docs: curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
   # Becomes:
   def install_nodejs(self):
       system_manager.install_nodejs()  # Handles all OS-specific details
   ```

3. **Dynamic Package Management**: Automatically detects and uses the right package manager:
   ```python
   class SystemPackageManager:
       def _detect_package_manager(self):
           if platform.system() == "Linux":
               if shutil.which("apt"): return "apt"
               elif shutil.which("dnf"): return "dnf"
           return "unknown"
   ```

## How It Works

1. **Parse Installation Docs**:
   ```python
   def parse_setup_docs(doc_path):
       """Extract installation steps from documentation."""
       steps = []
       with open(doc_path) as f:
           content = f.read()
           steps = extract_installation_steps(content)
       return steps
   ```

2. **Map Steps to Code**:
   ```python
   # project-definition.yaml defines the mapping:
   mappings:
     - doc_section: "Step 1: Install Dependencies"
       automated_by: "self.install_dependencies()"
   ```

3. **Generate Installation Class**:
   ```python
   def generate_installer(project_def):
       """Create a project-specific installer."""
       return type(
           f"{project_def['name']}Installer",
           (BaseInstaller,),
           {
               "install": generate_install_method(project_def),
               "verify": generate_verify_method(project_def)
           }
       )
   ```

## Example: Dify Installation

We map setup-instructions.md directly to code:

1. Prerequisites Section:
   ```markdown
   # In setup-instructions.md:
   ## Prerequisites
   - Git
   - Python 3
   - Node.js
   ```
   Becomes:
   ```python
   def check_prerequisites(self):
       required = ['git', 'python3', 'node']
       for cmd in required:
           if not shutil.which(cmd):
               raise RuntimeError(f"{cmd} missing")
   ```

2. Environment Setup:
   ```markdown
   # In docs:
   1. Clone repository
   2. Set up environment
   ```
   Becomes:
   ```python
   def setup_environment(self):
       self.clone_repository()
       self.configure_env()
       self.install_dependencies()
   ```

## Using for Other Projects

1. Create a project definition:
   ```yaml
   name: Your Project
   repository: github.com/user/project
   docs: docs/setup.md
   steps:
     - name: Install Dependencies
       commands: ["apt-get install xyz"]
     - name: Configure
       commands: ["./configure"]
   ```

2. Generate installer:
   ```python
   installer = ProjectInstaller.from_definition("project.yaml")
   installer.install()
   ```

This framework helps standardize and automate project installations, making complex setups easy and reliable.