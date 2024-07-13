import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Configuration
NUM_SAMPLES = 10  # Number of samples to generate, 1000 is default
MAX_RETRIES = 3
TIMEOUT = 60  # Timeout for API requests in seconds
NUM_THREADS = 4  # Number of concurrent threads

DATASET_FILENAME = "dataset.jsonl"

# List of instruction templates
INSTRUCTION_TEMPLATES = [
    # General knowledge and explanation
    "General Knowledge: Explain the concept of {topic} in simple terms.",
    "General Knowledge: What are the main differences between {topic1} and {topic2}?",
    "General Knowledge: Summarize the key points of {topic} in bullet points.",
    "General Knowledge: How does {topic} relate to {topic2}?",
    "General Knowledge: What are the potential future implications of {topic}?",

    # Math and logic
    "Math and Logic: Solve the following math problem: {math_problem}",
    "Math and Logic: Explain the step-by-step solution to this equation: {equation}",
    "Math and Logic: What is the logical fallacy in the following argument: {argument}",
    "Math and Logic: Describe the mathematical principle behind {math_concept}.",
    "Math and Logic: Create a word problem that involves {math_operation}.",

    # Programming and coding
    "Programming: Write a {programming_language} function to {coding_task}.",
    "Programming: Explain the time complexity of the following algorithm: {algorithm}",
    "Programming: Debug the following code snippet: {code_snippet}",
    "Programming: Implement a {data_structure} in {programming_language}.",
    "Programming: Optimize the following code for better performance: {code_to_optimize}",

    # Reasoning and problem-solving
    "Problem-Solving: Analyze the following scenario and provide a solution: {scenario}",
    "Problem-Solving: What are the pros and cons of {subject}?",
    "Problem-Solving: Develop a strategy to solve the following problem: {problem}",
    "Problem-Solving: Evaluate the strengths and weaknesses of {approach} in addressing {issue}.",
    "Problem-Solving: Propose an innovative solution to {real_world_problem}.",

    # Creative writing
    "Creative Writing: Write a short story about {character} in a {setting}.",
    "Creative Writing: Create a dialogue between {character1} and {character2} about {topic}.",
    "Creative Writing: Describe a day in the life of {character} living in {setting}.",
    "Creative Writing: Write a poem that incorporates the themes of {theme1} and {theme2}.",
    "Creative Writing: Craft an alternative ending to the story of {famous_story}.",

    # Task instructions
    "Task Instructions: Provide a step-by-step guide on how to {task}.",
    "Task Instructions: What are the best practices for {professional_task}?",
    "Task Instructions: Create a troubleshooting guide for common issues with {technology}.",
    "Task Instructions: Outline a training program for {skill}.",
    "Task Instructions: Design a project plan for implementing {project}.",

    # Analysis and research
    "Analysis: Conduct a SWOT analysis of {company_or_product}.",
    "Analysis: Compare and contrast the theories of {scientist1} and {scientist2}.",
    "Analysis: Analyze the impact of {event} on {field_of_study}.",
    "Analysis: What are the ethical implications of {technology_or_practice}?",
    "Analysis: Review the methodology of the following research study: {study_description}",
]

# Lists to fill in the templates
TOPICS = [
    "artificial intelligence", "quantum computing", "blockchain", "neural networks", 
    "machine learning", "cryptography", "data structures", "algorithms", "cybersecurity",
    "cloud computing", "Internet of Things", "augmented reality", "virtual reality",
    "5G technology", "autonomous vehicles", "renewable energy", "gene editing",
    "nanotechnology", "fusion energy", "space exploration", "climate change modeling",
    "quantum entanglement", "dark matter", "black holes", "string theory"
]

MATH_PROBLEMS = [
    "Find the derivative of f(x) = 3x^2 + 2x - 5",
    "Solve the system of equations: 2x + y = 7, 3x - 2y = 1",
    "Calculate the area under the curve y = x^2 from x = 0 to x = 3",
    "Find the eigenvalues of the matrix [[1, 2], [3, 4]]",
    "Prove that the square root of 2 is irrational"
]

EQUATIONS = [
    "3x^2 + 4x - 2 = 0",
    "log(x) + log(y) = 10",
    "sin(x) + cos(x) = 1",
    "e^x = 2x + 1",
    "|x - 3| + |y + 2| = 5"
]

MATH_CONCEPTS = [
    "Fourier transforms", "Euclidean algorithm", "Riemann hypothesis",
    "P vs NP problem", "Bayes' theorem", "Zeno's paradox", "Fibonacci sequence",
    "Euler's identity", "Monty Hall problem", "Traveling salesman problem"
]

MATH_OPERATIONS = [
    "integration by parts", "matrix multiplication", "complex number division",
    "solving differential equations", "finding limits", "vector calculus",
    "probability distributions", "statistical hypothesis testing"
]

PROGRAMMING_LANGUAGES = [
    "Python", "JavaScript", "Java", "C++", "Ruby", "Go", "Rust", "Swift",
    "Kotlin", "TypeScript", "Scala", "Haskell", "R", "MATLAB", "SQL"
]

CODING_TASKS = [
    "implement a binary search tree", "create a REST API", "build a web scraper",
    "develop a machine learning model", "implement a sorting algorithm",
    "create a multithreaded application", "build a simple blockchain",
    "implement a caching system", "create a file compression utility"
]

ALGORITHMS = [
    "quicksort", "Dijkstra's algorithm", "A* search", "k-means clustering",
    "pagerank", "naive Bayes classifier", "Bellman-Ford algorithm",
    "Fast Fourier Transform", "RSA encryption", "Kruskal's algorithm"
]

DATA_STRUCTURES = [
    "hash table", "red-black tree", "heap", "trie", "graph", "B-tree",
    "skip list", "bloom filter", "disjoint set", "segment tree"
]

SCENARIOS = [
    "A company facing a cybersecurity breach",
    "A city planning to implement a smart transportation system",
    "A hospital looking to optimize patient care with AI",
    "A country dealing with rising sea levels due to climate change",
    "A school system transitioning to remote learning"
]

REAL_WORLD_PROBLEMS = [
    "reducing plastic waste in oceans", "improving urban air quality",
    "ensuring fair and secure elections", "providing clean water in developing countries",
    "combating misinformation on social media", "reducing traffic congestion in cities"
]

CHARACTERS = [
    "a time traveler", "an AI researcher", "a quantum physicist", "a cybersecurity expert",
    "an environmental activist", "a space colonist", "a genetic engineer",
    "a virtual reality designer", "a robot ethics philosopher", "a data detective"
]

SETTINGS = [
    "a post-quantum cryptography world", "a Martian colony", "a zero-waste city",
    "a world run by artificial general intelligence", "an underwater research station",
    "a society where aging has been cured", "a matrix-like virtual reality",
    "a world after a global internet collapse", "a civilization powered entirely by fusion energy"
]

TASKS = [
    "set up a home automation system", "create a personal carbon footprint tracker",
    "build a basic machine learning model", "secure a home network against cyber threats",
    "write a smart contract for cryptocurrency transactions", "design an efficient algorithm for data processing",
    "develop a strategy for ethical AI implementation", "create a disaster recovery plan for a data center"
]

COMPANIES_OR_PRODUCTS = [
    "Tesla's self-driving technology", "Amazon's drone delivery service",
    "Google's quantum supremacy claim", "Apple's privacy-focused approach",
    "Microsoft's cloud computing platform", "SpaceX's Starlink satellite internet",
    "IBM's Watson AI system", "Facebook's cryptocurrency project"
]

SCIENTISTS = [
    "Albert Einstein", "Stephen Hawking", "Alan Turing", "Marie Curie",
    "Richard Feynman", "Ada Lovelace", "Nikola Tesla", "Grace Hopper",
    "Tim Berners-Lee", "Barbara McClintock"
]

TECHNOLOGIES_OR_PRACTICES = [
    "facial recognition in public spaces", "CRISPR gene editing",
    "autonomous weapons systems", "social media data collection",
    "predictive policing algorithms", "brain-computer interfaces",
    "deep fake technology", "mass surveillance systems"
]

def generate_prompt():
    template = random.choice(INSTRUCTION_TEMPLATES)
    category = template.split(":")[0].strip()  # Extract category from the template
    formatted_prompt = template.format(
        topic=random.choice(TOPICS),
        topic1=random.choice(TOPICS),
        topic2=random.choice(TOPICS),
        math_problem=random.choice(MATH_PROBLEMS),
        equation=random.choice(EQUATIONS),
        math_concept=random.choice(MATH_CONCEPTS),
        math_operation=random.choice(MATH_OPERATIONS),
        programming_language=random.choice(PROGRAMMING_LANGUAGES),
        coding_task=random.choice(CODING_TASKS),
        algorithm=random.choice(ALGORITHMS),
        data_structure=random.choice(DATA_STRUCTURES),
        scenario=random.choice(SCENARIOS),
        real_world_problem=random.choice(REAL_WORLD_PROBLEMS),
        character=random.choice(CHARACTERS),
        character1=random.choice(CHARACTERS),
        character2=random.choice(CHARACTERS),
        setting=random.choice(SETTINGS),
        task=random.choice(TASKS),
        company_or_product=random.choice(COMPANIES_OR_PRODUCTS),
        scientist1=random.choice(SCIENTISTS),
        scientist2=random.choice(SCIENTISTS),
        technology_or_practice=random.choice(TECHNOLOGIES_OR_PRACTICES),
        theme1=random.choice(TOPICS),
        theme2=random.choice(TOPICS),
        famous_story=f"'{random.choice(CHARACTERS)}' in {random.choice(SETTINGS)}",
        professional_task=random.choice(TASKS),
        technology=random.choice(TECHNOLOGIES_OR_PRACTICES),
        skill=random.choice(CODING_TASKS),
        project=f"a {random.choice(TECHNOLOGIES_OR_PRACTICES)} system",
        event=f"the discovery of {random.choice(TOPICS)}",
        field_of_study=random.choice(TOPICS),
        study_description=f"A study on the effects of {random.choice(TECHNOLOGIES_OR_PRACTICES)} on {random.choice(TOPICS)}",
        argument="All cats are animals. Some animals are black. Therefore, all cats are black.",
        subject=random.choice(TOPICS),
        problem=random.choice(REAL_WORLD_PROBLEMS),
        approach=f"using {random.choice(TECHNOLOGIES_OR_PRACTICES)}",
        issue=random.choice(REAL_WORLD_PROBLEMS),
        code_snippet="def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
        code_to_optimize="for i in range(len(list1)):\n    for j in range(len(list2)):\n        if list1[i] == list2[j]:\n            print(list1[i])"
    )
    return category, formatted_prompt

def query_ollama(prompt, retries=0):
    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llama3",  # Change this to the model you're using
            "prompt": prompt,
            "stream": False
        }, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        if retries < MAX_RETRIES:
            print(f"Error querying Ollama API: {e}. Retrying...")
            time.sleep(1)
            return query_ollama(prompt, retries + 1)
        else:
            print(f"Failed to query Ollama API after {MAX_RETRIES} attempts.")
            return None

def save_dataset(dataset, filename="ollama_dataset.jsonl"):
    with open(filename, "w", encoding="utf-8") as f:
        for sample in dataset:
            json.dump(sample, f, ensure_ascii=False)
            f.write("\n")
    print(f"Dataset saved to {filename}")

def generate_sample():
    category, instruction = generate_prompt()
    response = query_ollama(instruction)
    if response:
        return {
            "category": category,
            "instruction": instruction,
            "response": response
        }
    return None

def append_to_dataset(sample):
    with open(DATASET_FILENAME, "a", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False)
        f.write("\n")

def main():
    # Create or clear the dataset file
    with open(DATASET_FILENAME, "w", encoding="utf-8") as f:
        pass  # This creates an empty file or clears existing content

    samples_generated = 0
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        future_to_sample = {executor.submit(generate_sample): i for i in range(NUM_SAMPLES)}
        for future in as_completed(future_to_sample):
            sample = future.result()
            if sample:
                append_to_dataset(sample)
                samples_generated += 1
                print(f"Generated and saved sample {samples_generated}/{NUM_SAMPLES}")

    print(f"Dataset generation complete. Total samples: {samples_generated}")
    print(f"Dataset saved to {DATASET_FILENAME}")

if __name__ == "__main__":
    main()