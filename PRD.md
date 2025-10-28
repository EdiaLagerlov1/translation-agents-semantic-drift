# Product Requirements Document (PRD)
## Multi-Agent Translation System with Semantic Drift Analysis

**Version:** 1.0
**Date:** October 2025
**Project:** Turing Machine Agents - L13
**Status:** Implemented

---

## 1. Executive Summary

The Multi-Agent Translation System is a research tool designed to measure semantic drift in machine translation chains. By passing sentences through multiple translation steps (English → French → Hebrew → English), the system quantifies how much meaning is lost or altered through the translation process using vectorial distance measurements.

---

## 2. Product Overview

### 2.1 Purpose
To empirically study and visualize semantic degradation in multi-step machine translation processes, providing insights into translation quality and meaning preservation across language boundaries.

### 2.2 Target Users
- Machine Learning Researchers
- Natural Language Processing (NLP) Students
- Translation Quality Analysts
- Linguistic Researchers
- Data Scientists studying language models

### 2.3 Key Value Proposition
Automated, quantifiable analysis of semantic drift with visual representations, enabling researchers to understand how meaning changes through translation chains without manual evaluation.

---

## 3. Goals & Objectives

### 3.1 Primary Goals
1. **Automate Translation Chain Analysis**: Execute 100+ translation iterations without manual intervention
2. **Quantify Semantic Drift**: Measure meaning preservation using sentence embeddings
3. **Visualize Results**: Generate intuitive graphs showing drift patterns over iterations
4. **Data Collection**: Save comprehensive datasets for further analysis

### 3.2 Success Metrics
- System successfully completes 100 iterations or stops at configurable threshold
- Generates accurate vectorial distance measurements (0-1 scale)
- Produces timestamped CSV files with all iteration data
- Creates publication-ready visualization graphs
- Executes with <1% error rate in translation calls

---

## 4. User Requirements

### 4.1 User Stories

**As a researcher, I want to:**
- Run multiple translation experiments without overwriting previous results
- Adjust the stopping threshold to control when experiments terminate
- Access raw data in CSV format for custom analysis
- See statistical summaries (mean, variance, min, max) automatically calculated
- View visual representations of semantic drift over time

**As a student, I want to:**
- Understand how translation quality degrades through multiple steps
- See concrete examples of input vs output sentences
- Access clear documentation for running experiments
- Modify parameters without deep code knowledge

**As a data analyst, I want to:**
- Export results to CSV for integration with other tools
- See unique filenames for each run to prevent data loss
- Access timestamp information for tracking experiment timing
- Compare multiple runs using saved graph files

---

## 5. Functional Requirements

### 5.1 Core Features

#### 5.1.1 Agent System
- **Agent 1**: English → French translation
- **Agent 2**: French → Hebrew translation
- **Agent 3**: Hebrew → English translation
- **Agent 4**: Orchestrator (sentence generation + chain coordination)

**Requirements:**
- Each agent must handle translation errors gracefully
- Rate limiting (0.5s delay) to prevent API throttling
- Truncated display output for readability (50 chars max)

#### 5.1.2 Sentence Generation
- Generate random 15-word English sentences
- Use diverse vocabulary pools:
  - 10+ subjects
  - 10+ verbs
  - 10+ objects
  - 10+ adjectives
  - 6+ connectors
  - 10+ extra phrases
- Ensure grammatical structure (subject-verb-object pattern)
- Generate exactly 15 words per sentence

#### 5.1.3 Vectorial Distance Calculation
- Use sentence-transformers library (all-MiniLM-L6-v2 model)
- Calculate cosine distance: `distance = 1 - cosine_similarity`
- Range: 0 (identical) to 1 (completely different)
- Store all distances in memory for statistics

#### 5.1.4 Iteration Control
- Run up to 100 iterations maximum
- Stop early if `distance > stopping_threshold`
- Display iteration number with each run
- Show clear stopping messages with reason

#### 5.1.5 Data Export
- **CSV Format**:
  - Columns: input_sentence, output_sentence, vectorial_distance
  - UTF-8 encoding
  - Header row included
  - Unique filename per run: `results_YYYYMMDD_HHMMSS.csv`

#### 5.1.6 Visualization
- **Graph Requirements**:
  - Size: 12x6 inches
  - Line plot of distances (blue)
  - Mean line (red dashed)
  - Variance shaded area (red, 20% opacity)
  - Grid overlay (30% opacity)
  - Title with statistics: Mean | Variance | Stopping Threshold
  - Legend with all elements
  - 300 DPI resolution
  - Unique filename per run: `distance_graph_YYYYMMDD_HHMMSS.png`

#### 5.1.7 Statistics Calculation
- Mean distance
- Variance
- Standard deviation
- Minimum distance
- Maximum distance
- Display to console and in graph title

### 5.2 Configuration

#### 5.2.1 Configurable Parameters
- `stopping_threshold`: Float (default: 0.4)
  - Acceptable range: 0.0 - 1.0
  - Controls early stopping condition
  - Displayed in graph title

#### 5.2.2 Fixed Parameters
- `max_iterations`: 100
- `rate_limit_delay`: 0.5 seconds
- `sentence_length`: 15 words
- `embedding_model`: 'all-MiniLM-L6-v2'
- `graph_dpi`: 300

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Complete 100 iterations in < 10 minutes (with rate limiting)
- Model loading time < 30 seconds
- CSV write operations < 100ms per row
- Graph generation < 5 seconds

### 6.2 Reliability
- Handle network failures gracefully (fallback to original sentence)
- Prevent data loss through unique filenames
- Auto-create results directory if missing
- Validate sentence embeddings before distance calculation

### 6.3 Usability
- Single command execution: `python translation_agents.py`
- Clear console output with progress indicators
- Readable iteration markers and formatting
- Comprehensive README documentation

### 6.4 Maintainability
- Modular class-based architecture
- Clear docstrings for all functions
- Separation of concerns (translation, calculation, visualization)
- Type hints in function signatures

### 6.5 Portability
- Cross-platform (Windows, macOS, Linux)
- Python 3.8+ compatibility
- Standard package dependencies only
- No hardcoded file paths (relative paths only)

---

## 7. Technical Requirements

### 7.1 System Architecture

```
┌─────────────────────────────────────────────────┐
│                   Main Loop                      │
│  (Iteration Control & Orchestration)             │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼─────┐         ┌────▼──────┐
   │ Agent 4  │         │  Distance  │
   │Generator │         │Calculator  │
   └────┬─────┘         └────▲──────┘
        │                    │
    ┌───▼────┐          ┌───┴────┐
    │Agent 1 │──────►   │Results │
    │ EN→FR  │          │        │
    └───┬────┘          └───┬────┘
        │                   │
    ┌───▼────┐          ┌───▼────┐
    │Agent 2 │          │  CSV   │
    │ FR→HE  │          │ Export │
    └───┬────┘          └────────┘
        │
    ┌───▼────┐          ┌────────┐
    │Agent 3 │          │ Graph  │
    │ HE→EN  │          │  Gen   │
    └────────┘          └────────┘
```

### 7.2 Dependencies
- **deep-translator**: Google Translate API wrapper
- **sentence-transformers**: Sentence embedding models
- **numpy**: Numerical computations
- **matplotlib**: Visualization
- **torch**: PyTorch backend (auto-installed with sentence-transformers)

### 7.3 File Structure
```
Turing machine agents/
├── translation_agents.py    # Main system
├── test_agents.py           # Test script
├── requirements.txt         # Dependencies
├── README.md               # User documentation
├── PRD.md                  # This document
└── results/                # Output directory
    ├── results_*.csv       # Data files
    └── distance_graph_*.png # Visualizations
```

---

## 8. User Interface

### 8.1 Console Interface

**Startup Phase:**
```
Initializing Multi-Agent Translation System...
================================================================================
Loading sentence transformer model...
Model loaded successfully!

Results will be saved to: results/results_20251028_143022.csv
Graph will be saved to: results/distance_graph_20251028_143022.png

Starting translation loop...
Will run for 100 iterations or until vectorial distance > 0.4
================================================================================
```

**Iteration Phase:**
```
### ITERATION 1 ###
================================================================================
INPUT: The cat thinks quickly wonderful stories when with friends...
Agent 1 (EN→FR): The cat thinks quickly... → Le chat pense rapidement...
Agent 2 (FR→HE): Le chat pense rapidement... → החתול חושב במהירות...
Agent 3 (HE→EN): החתול חושב במהירות... → The cat quickly thinks...
OUTPUT: The cat quickly thinks of wonderful stories...
================================================================================
Vectorial Distance: 0.0778
```

**Completion Phase:**
```
================================================================================
Completed 35 iterations
================================================================================

Creating visualization...

Statistics:
  Mean Distance: 0.1234
  Variance: 0.0045
  Std Deviation: 0.0671
  Min Distance: 0.0234
  Max Distance: 0.3456

Graph saved to: results/distance_graph_20251028_143022.png

Results saved to:
  - CSV: results/results_20251028_143022.csv
  - Graph: results/distance_graph_20251028_143022.png

Execution complete!
```

### 8.2 Graph Interface
- X-axis: Iteration Index (0 to N)
- Y-axis: Vectorial Distance (0.0 to 1.0)
- Title: Multi-line with statistics
- Legend: Top-right or best position (auto)
- Color scheme: Blue (data), Red (statistics), White background

---

## 9. Data Requirements

### 9.1 CSV Schema
| Column            | Type  | Description                              | Range    |
|-------------------|-------|------------------------------------------|----------|
| input_sentence    | str   | Original English sentence                | 15 words |
| output_sentence   | str   | Final English sentence after chain       | Variable |
| vectorial_distance| float | Cosine distance between embeddings       | 0.0-1.0  |

### 9.2 Data Storage
- Location: `results/` directory
- Format: CSV (UTF-8)
- Retention: Permanent (no auto-deletion)
- Naming: Timestamped (prevents overwrites)

---

## 10. Testing Requirements

### 10.1 Unit Tests
- Agent translation functions
- Distance calculation accuracy
- Sentence generation (15-word validation)
- CSV writing/reading

### 10.2 Integration Tests
- Full translation chain (4 agents)
- End-to-end iteration loop
- File creation and naming
- Graph generation

### 10.3 Test Script
- `test_agents.py` provides single-iteration test
- Validates all systems operational
- Quick smoke test before full runs

---

## 11. Security & Privacy

### 11.1 Data Privacy
- No personal information processed
- Randomly generated sentences only
- No user input collection
- No external data transmission (except Google Translate API)

### 11.2 API Security
- Rate limiting implemented (0.5s delay)
- Error handling for API failures
- No API keys exposed (uses public endpoint)

---

## 12. Out of Scope

The following are explicitly **not** included in v1.0:
- ❌ GUI/Web interface
- ❌ Real-time translation monitoring
- ❌ Custom translation APIs (only Google Translate)
- ❌ Multi-user support
- ❌ Cloud deployment
- ❌ Database storage
- ❌ Advanced statistical analysis (beyond basic stats)
- ❌ Comparison between different translation chains
- ❌ Manual sentence input
- ❌ Translation chain customization (fixed EN→FR→HE→EN)

---

## 13. Future Enhancements (Roadmap)

### 13.1 Phase 2 Features
- **Custom Translation Chains**: Allow users to configure language sequences
- **Multiple Translation APIs**: Support DeepL, Microsoft Translator, etc.
- **Batch Processing**: Run multiple experiments in parallel
- **Advanced Statistics**: Correlation analysis, trend detection
- **Export Formats**: JSON, Excel, PDF reports

### 13.2 Phase 3 Features
- **Web Dashboard**: Real-time monitoring interface
- **Database Integration**: PostgreSQL/MongoDB for result storage
- **Comparative Analysis**: Compare different translation services
- **Machine Learning**: Predict semantic drift patterns
- **API Endpoint**: RESTful API for programmatic access

### 13.3 Phase 4 Features
- **Multi-language Support**: Extend to 20+ languages
- **Quality Scoring**: Automated translation quality assessment
- **A/B Testing**: Compare translation strategies
- **Enterprise Features**: Team collaboration, access control
- **Performance Optimization**: GPU acceleration, caching

---

## 14. Acceptance Criteria

The system is considered complete when:
- ✅ All 4 agents translate correctly
- ✅ 100 iterations complete without errors
- ✅ CSV files generate with proper formatting
- ✅ Graphs display all required elements
- ✅ Statistics calculate accurately
- ✅ Unique filenames prevent data loss
- ✅ Stopping threshold is configurable
- ✅ Documentation is comprehensive
- ✅ Test script validates functionality
- ✅ No data loss or corruption occurs

---

## 15. Dependencies & Constraints

### 15.1 Technical Dependencies
- Python 3.8 or higher
- Internet connection (for translations and model download)
- ~500MB disk space (for model storage)
- ~100MB RAM per run

### 15.2 External Services
- Google Translate API (free tier, rate-limited)
- Hugging Face model repository (for sentence-transformers)

### 15.3 Constraints
- Rate limiting: 2 requests/second maximum
- Model loading: One-time ~80MB download
- Translation quality: Dependent on Google Translate accuracy
- Language support: Limited to supported Google Translate languages

---

## 16. Glossary

| Term                  | Definition                                                    |
|-----------------------|---------------------------------------------------------------|
| **Agent**             | Autonomous component performing specific translation task     |
| **Vectorial Distance**| Cosine distance between sentence embeddings (0-1 scale)       |
| **Semantic Drift**    | Loss or change of meaning through translation processes       |
| **Sentence Embedding**| Vector representation of sentence meaning                     |
| **Stopping Threshold**| Maximum distance before experiment termination                |
| **Translation Chain** | Sequential translation through multiple languages             |
| **Iteration**         | Single complete cycle through all 4 agents                    |

---

## 17. Approval & Sign-off

| Role              | Name          | Date       | Signature |
|-------------------|---------------|------------|-----------|
| Product Owner     |               |            |           |
| Technical Lead    |               |            |           |
| QA Lead           |               |            |           |
| Stakeholder       |               |            |           |

---

## 18. Document History

| Version | Date       | Author | Changes                    |
|---------|------------|--------|----------------------------|
| 1.0     | 2025-10-28 | Claude | Initial PRD creation       |

---

**End of Document**
