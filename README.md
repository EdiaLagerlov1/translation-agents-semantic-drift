# Multi-Agent Translation System with Vectorial Distance Analysis

## Overview
This project implements a 4-agent translation system that demonstrates semantic drift through a chain of translations (English → French → Hebrew → English). It calculates vectorial distances between input and output sentences to measure how much meaning is lost or changed through the translation chain.

## Architecture

### Agent 1: English → French Translator
Takes an English sentence and translates it to French using Google Translate.

### Agent 2: French → Hebrew Translator
Takes a French sentence and translates it to Hebrew using Google Translate.

### Agent 3: Hebrew → English Translator
Takes a Hebrew sentence and translates it back to English using Google Translate.

### Agent 4: Orchestrator
- Generates random 15-word English sentences
- Coordinates the translation chain through Agents 1, 2, and 3
- Returns both the original input and final output sentences

## Features

✅ **Translation Chain**: EN → FR → HE → EN
✅ **Vectorial Distance Calculation**: Uses sentence embeddings (sentence-transformers) to measure semantic similarity
✅ **CSV Logging**: Saves all input/output sentences and distances to `results/results.csv`
✅ **Visualization**: Generates graphs showing distance evolution with mean and variance
✅ **Smart Stopping**: Runs for 100 iterations OR until distance > 0.5

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Full System
```bash
python translation_agents.py
```

This will:
- Run up to 100 iterations (or until vectorial distance > 0.5)
- Save results to `results/results_TIMESTAMP.csv`
- Generate visualization graph at `results/distance_graph_TIMESTAMP.png`
- Display statistics (mean, variance, min, max distances)

**Custom Stopping Threshold:**

You can customize the stopping threshold by modifying the `main()` call in the script:
```python
if __name__ == "__main__":
    main(stopping_threshold=0.7)  # Use 0.7 instead of default 0.5
```

### Run Quick Test
```bash
python test_agents.py
```

This runs a single iteration to verify all systems are working correctly.

## Output Files

### results/results_TIMESTAMP.csv
Contains three columns:
- `input_sentence`: Original randomly generated English sentence
- `output_sentence`: Final English sentence after translation chain
- `vectorial_distance`: Cosine distance between input and output (0 = identical, 1 = completely different)

Each run creates a new CSV file with a unique timestamp (format: YYYYMMDD_HHMMSS).

### results/distance_graph_TIMESTAMP.png
Visualization showing:
- Line plot of vectorial distances by iteration
- Mean distance (red dashed line)
- Variance visualization (shaded area)
- Stopping threshold value
- Statistics summary in title

Each run creates a new graph file with a unique timestamp (format: YYYYMMDD_HHMMSS).

## How It Works

### 1. Sentence Generation
Agent 4 creates random 15-word English sentences using a vocabulary of subjects, verbs, objects, adjectives, and connectors.

### 2. Translation Chain
```
English sentence
    ↓ (Agent 1)
French sentence
    ↓ (Agent 2)
Hebrew sentence
    ↓ (Agent 3)
English sentence (output)
```

### 3. Vectorial Distance Calculation
- Uses the `sentence-transformers` library with the 'all-MiniLM-L6-v2' model
- Generates embeddings for both input and output sentences
- Calculates cosine distance: `distance = 1 - cosine_similarity`
- Distance ranges from 0 (identical meaning) to 1 (completely different)

### 4. Results Analysis
- Tracks all distances in a list
- Calculates mean and variance
- Generates visualization
- Saves comprehensive CSV log

## Example Output

```
### ITERATION 1 ###
================================================================================
INPUT: The cat thinks quickly wonderful stories when with friends when in the city in the
Agent 1 (EN→FR): The cat thinks quickly wonderful stories when with... → Le chat pense rapidement à des histoires merveille...
Agent 2 (FR→HE): Le chat pense rapidement à des histoires merveille... → החתול חושב במהירות על סיפורים נפלאים כשהוא עם חברי...
Agent 3 (HE→EN): החתול חושב במהירות על סיפורים נפלאים כשהוא עם חברי... → The cat quickly thinks of wonderful stories when h...
OUTPUT: The cat quickly thinks of wonderful stories when he is with friends, when he is in town.
================================================================================
Vectorial Distance: 0.0778
```

## Statistics Example

```
Starting translation loop...
Will run for 100 iterations or until vectorial distance > 0.5

Statistics:
  Mean Distance: 0.1234
  Variance: 0.0045
  Std Deviation: 0.0671
  Min Distance: 0.0234
  Max Distance: 0.3456
```

The graph title will display: `Mean: 0.1234 | Variance: 0.0045 | Stopping Threshold: 0.50`

## Dependencies

- `deep-translator`: Google Translate API wrapper
- `sentence-transformers`: Sentence embedding models
- `numpy`: Numerical computations
- `matplotlib`: Data visualization
- `torch`: PyTorch backend for transformers

## Notes

- Translation API has rate limiting (0.5s delay between calls)
- First run downloads the sentence-transformers model (~80MB)
- Results folder is created automatically if it doesn't exist
- Each run creates unique timestamped files (no overwriting of previous results)

## Stopping Conditions

The system stops when:
1. 100 iterations are completed, OR
2. Vectorial distance exceeds the stopping threshold (default: 0.5, configurable)

The stopping threshold is displayed in the graph title alongside mean and variance statistics.

## Author

Turing Machine Agents Project - L13
