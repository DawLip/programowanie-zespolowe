from app import create_app  # Import your Flask app factory
from pdoc import cli
import sys

# 1. Create Flask app
app = create_app()

# 2. Set up application context
with app.app_context():
    # 3. Mock command line arguments for pdoc
    sys.argv = [
        "pdoc",  # Program name (required)
        "--html",  # Generate HTML output
        "--output-dir", "./docs",  # Output directory
        "--force",  # Overwrite existing files
        "app"  # Module to document (your Flask app package)
    ]
    
    # 4. Generate documentation
    cli.main()