"""
Multi-Agent Translation System with Vectorial Distance Analysis
Implements 4 agents that translate sentences through a chain and analyze semantic drift
"""

import random
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
import time
from datetime import datetime


class Agent1:
    """Agent 1: Translates English to French"""

    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='fr')

    def translate(self, sentence):
        """Translate English sentence to French"""
        try:
            result = self.translator.translate(sentence)
            print(f"Agent 1 (EN→FR): {sentence[:50]}... → {result[:50]}...")
            time.sleep(0.5)  # Rate limiting
            return result
        except Exception as e:
            print(f"Agent 1 Error: {e}")
            return sentence


class Agent2:
    """Agent 2: Translates French to Hebrew"""

    def __init__(self):
        self.translator = GoogleTranslator(source='fr', target='iw')

    def translate(self, sentence):
        """Translate French sentence to Hebrew"""
        try:
            result = self.translator.translate(sentence)
            print(f"Agent 2 (FR→HE): {sentence[:50]}... → {result[:50]}...")
            time.sleep(0.5)  # Rate limiting
            return result
        except Exception as e:
            print(f"Agent 2 Error: {e}")
            return sentence


class Agent3:
    """Agent 3: Translates Hebrew to English"""

    def __init__(self):
        self.translator = GoogleTranslator(source='iw', target='en')

    def translate(self, sentence):
        """Translate Hebrew sentence to English"""
        try:
            result = self.translator.translate(sentence)
            print(f"Agent 3 (HE→EN): {sentence[:50]}... → {result[:50]}...")
            time.sleep(0.5)  # Rate limiting
            return result
        except Exception as e:
            print(f"Agent 3 Error: {e}")
            return sentence


class Agent4:
    """Agent 4: Orchestrator - generates random sentence and runs through translation chain"""

    def __init__(self, agent1, agent2, agent3):
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent3 = agent3

        # Word pool for generating random sentences
        self.subjects = ["The cat", "A dog", "The scientist", "My friend", "The teacher",
                        "The artist", "A child", "The engineer", "The musician", "The writer"]
        self.verbs = ["runs", "jumps", "thinks", "creates", "explores", "discovers",
                     "builds", "writes", "plays", "teaches"]
        self.objects = ["in the garden", "through the forest", "about life", "beautiful art",
                       "new technologies", "hidden treasures", "amazing structures",
                       "wonderful stories", "sweet music", "important lessons"]
        self.adjectives = ["quickly", "carefully", "passionately", "enthusiastically",
                          "thoughtfully", "creatively", "diligently", "joyfully",
                          "peacefully", "energetically"]
        self.connectors = ["and", "while", "because", "although", "when", "as"]
        self.extra_phrases = ["every day", "in the morning", "with great care",
                             "for hours", "without stopping", "with friends",
                             "under the stars", "near the ocean", "in the city",
                             "around the world"]

    def generate_random_sentence(self):
        """Generate a random 15-word English sentence"""
        words = []

        # Start with subject-verb-object
        words.extend(random.choice(self.subjects).split())
        words.extend(random.choice(self.verbs).split())
        words.extend(random.choice(self.adjectives).split())
        words.extend(random.choice(self.objects).split())

        # Add connector and more content to reach 15 words
        while len(words) < 15:
            if len(words) < 13:
                words.append(random.choice(self.connectors))
                words.extend(random.choice(self.extra_phrases).split())
            else:
                # Fill remaining with adjectives or extra phrases
                remaining = 15 - len(words)
                filler = random.choice(self.extra_phrases).split()
                words.extend(filler[:remaining])

        # Ensure exactly 15 words
        sentence = ' '.join(words[:15])
        return sentence

    def process(self):
        """
        Generate random sentence and run through translation chain
        Returns: (input_sentence, output_sentence)
        """
        print("\n" + "="*80)
        # Generate random English sentence
        input_sentence = self.generate_random_sentence()
        print(f"INPUT: {input_sentence}")

        # Pass through translation chain
        french = self.agent1.translate(input_sentence)
        hebrew = self.agent2.translate(french)
        output_sentence = self.agent3.translate(hebrew)

        print(f"OUTPUT: {output_sentence}")
        print("="*80)

        return input_sentence, output_sentence


class VectorDistanceCalculator:
    """Calculate vectorial distance between sentences using sentence embeddings"""

    def __init__(self):
        print("Loading sentence transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully!")

    def calculate_distance(self, sentence1, sentence2):
        """Calculate cosine distance between two sentences"""
        # Get embeddings
        embedding1 = self.model.encode(sentence1)
        embedding2 = self.model.encode(sentence2)

        # Calculate cosine similarity
        cosine_similarity = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

        # Convert to distance (1 - similarity)
        distance = 1 - cosine_similarity

        return distance


def save_to_csv(input_sentence, output_sentence, distance, filepath='results/results.csv'):
    """Save results to CSV file"""
    file_exists = os.path.isfile(filepath)

    with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['input_sentence', 'output_sentence', 'vectorial_distance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'input_sentence': input_sentence,
            'output_sentence': output_sentence,
            'vectorial_distance': distance
        })


def create_visualization(distance_list, filepath='results/distance_graph.png', threshold=0.5):
    """Create and save visualization of vectorial distances"""
    # Calculate statistics
    mean_distance = np.mean(distance_list)
    variance = np.var(distance_list)

    # Create figure
    plt.figure(figsize=(12, 6))

    # Plot distances
    indices = list(range(len(distance_list)))
    plt.plot(indices, distance_list, 'b-', label='Vectorial Distance', linewidth=1.5)

    # Plot mean line
    plt.axhline(y=mean_distance, color='r', linestyle='--',
                label=f'Mean: {mean_distance:.4f}', linewidth=2)

    # Fill area for variance visualization
    plt.fill_between(indices,
                     mean_distance - np.sqrt(variance),
                     mean_distance + np.sqrt(variance),
                     alpha=0.2, color='red',
                     label=f'Variance: {variance:.4f}')

    plt.xlabel('Iteration Index', fontsize=12)
    plt.ylabel('Vectorial Distance', fontsize=12)
    plt.title('Vectorial Distance Analysis: Translation Chain Drift\n' +
              f'Mean: {mean_distance:.4f} | Variance: {variance:.4f} | Stopping Threshold: {threshold:.2f}', fontsize=14)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save figure
    plt.savefig(filepath, dpi=300)
    print(f"\nGraph saved to: {filepath}")

    # Display statistics
    print(f"\nStatistics:")
    print(f"  Mean Distance: {mean_distance:.4f}")
    print(f"  Variance: {variance:.4f}")
    print(f"  Std Deviation: {np.sqrt(variance):.4f}")
    print(f"  Min Distance: {min(distance_list):.4f}")
    print(f"  Max Distance: {max(distance_list):.4f}")


def main(stopping_threshold=0.4):
    """Main execution function

    Args:
        stopping_threshold (float): Distance threshold to stop the loop (default: 0.5)
    """
    print("Initializing Multi-Agent Translation System...")
    print("="*80)

    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Initialize agents
    agent1 = Agent1()
    agent2 = Agent2()
    agent3 = Agent3()
    agent4 = Agent4(agent1, agent2, agent3)

    # Initialize distance calculator
    distance_calculator = VectorDistanceCalculator()

    # Initialize results storage
    vectorial_distance_list = []

    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)

    # Create unique filenames with timestamp
    results_file = f'results/results_{timestamp}.csv'
    graph_file = f'results/distance_graph_{timestamp}.png'

    print(f"\nResults will be saved to: {results_file}")
    print(f"Graph will be saved to: {graph_file}")

    print("\nStarting translation loop...")
    print(f"Will run for 100 iterations or until vectorial distance > {stopping_threshold}")
    print("="*80)

    # Main loop
    iteration = 0
    max_iterations = 100

    while iteration < max_iterations:
        iteration += 1
        print(f"\n### ITERATION {iteration} ###")

        # Run Agent 4
        input_sentence, output_sentence = agent4.process()

        # Calculate vectorial distance
        distance = distance_calculator.calculate_distance(input_sentence, output_sentence)
        print(f"Vectorial Distance: {distance:.4f}")

        # Store distance
        vectorial_distance_list.append(distance)

        # Save to CSV
        save_to_csv(input_sentence, output_sentence, distance, results_file)

        # Check stopping condition
        if distance > stopping_threshold:
            print(f"\n{'='*80}")
            print(f"STOPPING: Vectorial distance ({distance:.4f}) exceeded threshold ({stopping_threshold})!")
            print(f"{'='*80}")
            break

    print(f"\n{'='*80}")
    print(f"Completed {iteration} iterations")
    print(f"{'='*80}")

    # Create visualization
    print("\nCreating visualization...")
    create_visualization(vectorial_distance_list, graph_file, stopping_threshold)

    print(f"\nResults saved to:")
    print(f"  - CSV: {results_file}")
    print(f"  - Graph: {graph_file}")
    print("\nExecution complete!")


if __name__ == "__main__":
    main()
