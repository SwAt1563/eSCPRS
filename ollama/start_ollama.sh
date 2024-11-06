#!/bin/sh

# Directories for the new models
GEMMA_MODEL_DIR="/root/.ollama/models/manifests/registry.ollama.ai/library/gemma2"
LLAMA_MODEL_DIR="/root/.ollama/models/manifests/registry.ollama.ai/library/llama3.1"

# Function to check and download models if not present
download_model_if_not_present() {
    local model_dir=$1
    local model_name=$2

    if [ ! "$(ls -A "$model_dir")" ]; then
        echo "$model_name model not found, downloading..."
        ollama pull "$model_name"
        if [ $? -eq 0 ]; then
            echo "$model_name model downloaded successfully."
        else
            echo "Failed to download $model_name model."
            exit 1
        fi
    else
        echo "$model_name model already present, skipping download."
    fi
}

# Start the Ollama service
echo 'Starting Ollama service...'
ollama serve &
SERVICE_PID=$!

echo 'Waiting for Ollama service to start...'
sleep 30


# if OLLAMA_ENV=development download gemma2:2b model else download llama3.1 model
if [ "$OLLAMA_ENV" = "development" ]; then
    download_model_if_not_present "$GEMMA_MODEL_DIR" "gemma2:2b"
else
    download_model_if_not_present "$LLAMA_MODEL_DIR" "llama3.1"
fi


# Keep the container running
echo 'Keeping the container running...'
tail -f /dev/null