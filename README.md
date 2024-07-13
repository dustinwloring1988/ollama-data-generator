# Ollama Dataset Generator

This project is a Python script that generates a dataset of instruction-response pairs using the Ollama API. It's designed to create diverse, high-quality datasets for training or fine-tuning language models.

## Features

- Generates instruction-response pairs across various categories
- Uses multithreading for efficient data generation
- Customizable number of samples, retries, and concurrency
- Saves output in JSONL format for easy processing
- Robust error handling and retry mechanism

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ollama-dataset-generator.git
   cd ollama-dataset-generator
   ```

2. Install the required packages:
   ```
   pip install requests
   ```

3. Ensure you have Ollama running locally on the default port (11434).

## Usage

1. Configure the script by modifying the following variables at the top of the file:
   - `NUM_SAMPLES`: Number of samples to generate (default: 10)
   - `MAX_RETRIES`: Maximum number of API request retries (default: 3)
   - `TIMEOUT`: Timeout for API requests in seconds (default: 60)
   - `NUM_THREADS`: Number of concurrent threads (default: 4)
   - `DATASET_FILENAME`: Name of the output file (default: "dataset.jsonl")

2. Run the script:
   ```
   python ollama-dataset-generator.py
   ```

3. The script will generate the specified number of samples and save them to the output file.

## Output Format

The generated dataset is saved in JSONL format, with each line containing a JSON object with the following structure:

```json
{
  "category": "Category of the instruction",
  "instruction": "The generated instruction",
  "response": "The response from the Ollama API"
}
```

## Customization

You can customize the generated instructions by modifying the `INSTRUCTION_TEMPLATES` list and the various topic lists (e.g., `TOPICS`, `MATH_PROBLEMS`, `CODING_TASKS`, etc.) in the script.

## Contributing

Contributions to improve the script or add new features are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is intended for research and development purposes. Ensure you comply with Ollama's terms of service and have the necessary permissions to use the generated data.
