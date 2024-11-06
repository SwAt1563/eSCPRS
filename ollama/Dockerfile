FROM ollama/ollama:0.3.10

ENV APP_DIR=/ollama

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN chmod +x start_ollama.sh

# Expose the relevant ports 
EXPOSE 11434