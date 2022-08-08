

# Build an application object
app = None

# Run the Server using Uvicorn
from ebs.apiserver.core.server import run_server
run_server(app)
