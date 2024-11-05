#!/bin/sh
# LF Format

# Add local bin directory to PATH (required when not root user)
export PATH="$HOME/.local/bin:$PATH"

# Check if the required environment file is provided
if [ -z "$FASTAPI_ENV" ]; then
  echo "FASTAPI_ENV environment variables is required."
  exit 1
fi


# Check python requirements dependencies
echo "Checking python requirements dependencies..."
pip3 install -r requirements.txt




# Start the FastAPI server conditionally based on the environment file
echo "Starting FastAPI server..."
if [ "$FASTAPI_ENV" = "production" ]; then
  exec uvicorn main:app --host 0.0.0.0 --port 9000 --workers 4 --loop uvloop --http httptools --ws auto --lifespan on 
else
  exec uvicorn main:app --host 0.0.0.0 --port 9000 --workers 2 --reload --loop uvloop --http httptools --ws auto --lifespan on # --reload: reload the server when code changes 
fi

# Execute the command passed to the script
exec "$@"