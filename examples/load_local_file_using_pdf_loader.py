import logging
import os
from deepsearcher.offline_loading import load_from_local_files
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    # Step 1: Initialize configuration
    config = Configuration()
    config.set_provider_config("llm", "Ollama", {
        "model": "qwen2.5-30K:72b-instruct-q8_0",
        "base_url": "http://192.168.5.233:11434"
        })
    
    config.set_provider_config("embedding", "OllamaEmbedding", {
        "base_url": "http://192.168.5.233:11434",
        "model": "quentinz/bge-large-zh-v1.5:f32"
    })
    # Configure Vector Database (Milvus) and File Loader (PDFLoader)
    config.set_provider_config("vector_db", "Milvus", {"uri": "./milvus.db", "token": ""})
    config.set_provider_config("file_loader", "PDFLoader", {})

    # Apply the configuration
    init_config(config)

    # Step 2: Load data from a local file or directory into Milvus
    input_file = "./data/DM"  # Replace with your actual file path
    collection_name = "DM"
    collection_description = "Diffusion Model Documents"

    load_from_local_files(paths_or_directory=input_file, collection_name=collection_name, collection_description=collection_description)

    # Step 3: Query the loaded data
    question = "What is Diffusion Model?"  # Replace with your actual question
    result = query(question)


if __name__ == "__main__":
    main()
