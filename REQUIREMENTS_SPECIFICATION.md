# Software Requirements Specification (SRS)
## RAG-Enhanced University Help Desk Chatbot System

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Project:** GreenBot - AI-Powered University Assistant

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [System Requirements](#4-system-requirements)
5. [Use Case Diagrams](#5-use-case-diagrams)
6. [Requirements Traceability Matrix](#6-requirements-traceability-matrix)

---

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements for the RAG-Enhanced University Help Desk Chatbot System. The system is designed to provide automated, accurate, and context-aware responses to university-related queries using Retrieval-Augmented Generation (RAG) technology combined with Large Language Models (LLM).

### 1.2 Scope

The system covers:
- Automated query handling for university information
- Multi-source information retrieval
- User feedback-based learning
- Real-time response generation
- Department-specific information accuracy

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|------------|
| **RAG** | Retrieval-Augmented Generation |
| **LLM** | Large Language Model |
| **TF-IDF** | Term Frequency-Inverse Document Frequency |
| **NLP** | Natural Language Processing |
| **RLHF** | Reinforcement Learning from Human Feedback |
| **API** | Application Programming Interface |
| **CORS** | Cross-Origin Resource Sharing |

### 1.4 Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Students | Primary Users | Get accurate university information |
| University Staff | Content Providers | Maintain accurate data |
| System Administrators | Operators | System maintenance and monitoring |
| Researchers | Analysts | System performance evaluation |

---

## 2. Functional Requirements

### 2.1 Query Processing Module

#### FR-001: Natural Language Query Input
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-001 |
| **Title** | Natural Language Query Input |
| **Description** | The system shall accept natural language queries in text format from users |
| **Priority** | High |
| **Input** | User text query (string, max 1000 characters) |
| **Output** | Processed query ready for search |
| **Acceptance Criteria** | System accepts and processes any valid text input within character limit |

#### FR-002: Text Preprocessing
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-002 |
| **Title** | Text Preprocessing Pipeline |
| **Description** | The system shall preprocess input text by: (1) Converting to lowercase, (2) Removing special characters, (3) Lemmatizing words, (4) Removing stopwords |
| **Priority** | High |
| **Input** | Raw text query |
| **Output** | Normalized, lemmatized text tokens |
| **Acceptance Criteria** | "What is the CSE fee?" → "cse fee" |

#### FR-003: Department Detection
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-003 |
| **Title** | Automatic Department Detection |
| **Description** | The system shall automatically detect the department context from user queries using keyword pattern matching |
| **Priority** | High |
| **Supported Departments** | CSE, EEE, BBA, Textile, Law, English, Journalism, Sociology |
| **Acceptance Criteria** | Query containing "electrical engineering" → Department: "EEE" |

#### FR-004: Query Categorization
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-004 |
| **Title** | Automatic Query Categorization |
| **Description** | The system shall categorize queries into predefined categories |
| **Priority** | Medium |
| **Categories** | fees_financial, admission_requirements, academic_programs, contact_information, campus_facilities, scholarships_aid, student_activities, general_inquiry |
| **Acceptance Criteria** | "tuition cost" → Category: "fees_financial" |

---

### 2.2 Information Retrieval Module

#### FR-005: TF-IDF Based Semantic Search
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-005 |
| **Title** | TF-IDF Cosine Similarity Search |
| **Description** | The system shall perform semantic search using TF-IDF vectorization and cosine similarity matching |
| **Priority** | High |
| **Parameters** | ngram_range: (1,3), max_features: 5000 |
| **Output** | Similarity scores (0.0 - 1.0) |
| **Acceptance Criteria** | Return top matches with confidence scores ≥ 0.25 |

#### FR-006: Exact Match Detection
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-006 |
| **Title** | Exact Question Matching |
| **Description** | The system shall detect exact or near-exact matches between user queries and database questions |
| **Priority** | High |
| **Methods** | Normalized string comparison, Jaccard similarity |
| **Acceptance Criteria** | Exact match returns confidence ≥ 0.98 |

#### FR-007: Keyword Matching
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-007 |
| **Title** | Keyword-Based Matching |
| **Description** | The system shall perform direct keyword overlap matching between queries and stored keywords |
| **Priority** | Medium |
| **Weight** | 20% of combined score |
| **Acceptance Criteria** | Returns boost for matching keywords |

#### FR-008: Question Variation Matching
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-008 |
| **Title** | Question Variation Support |
| **Description** | The system shall match queries against pre-defined question variations stored in the dataset |
| **Priority** | Medium |
| **Weight** | 10% of combined score |
| **Acceptance Criteria** | "CSE cost" matches variation of "CSE tuition fee" |

#### FR-009: Phrase Matching
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-009 |
| **Title** | N-gram Phrase Matching |
| **Description** | The system shall extract and match 2-gram and 3-gram phrases from queries |
| **Priority** | Medium |
| **Weight** | 10% of combined score |
| **Acceptance Criteria** | Phrases > 3 characters are matched |

#### FR-010: Department-Specific Scoring
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-010 |
| **Title** | Department-Aware Scoring |
| **Description** | The system shall apply scoring adjustments based on department context |
| **Priority** | High |
| **Boost** | +0.4 for matching department |
| **Penalty** | -0.5 for wrong department |
| **Acceptance Criteria** | CSE query returns CSE-specific answers, not EEE |

#### FR-011: Multi-Source Search
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-011 |
| **Title** | Parallel Multi-Source Search |
| **Description** | The system shall search across multiple data sources simultaneously: (1) JSON dataset, (2) Instruction-response pairs |
| **Priority** | High |
| **Sources** | enhanced_ndata.json, instruction-response dataset (30K+), department JSONs |
| **Acceptance Criteria** | All sources searched in parallel, best result selected |

#### FR-012: Source Reference Tracking
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-012 |
| **Title** | Answer Source Attribution |
| **Description** | The system shall track and return source references for answers |
| **Priority** | Medium |
| **Output** | Top 3 source references with confidence scores |
| **Acceptance Criteria** | Each answer includes source metadata |

---

### 2.3 Response Generation Module

#### FR-013: LLM Response Generation
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-013 |
| **Title** | LLM-Based Response Generation |
| **Description** | The system shall generate natural language responses using Ollama LLaMA model when RAG confidence is insufficient |
| **Priority** | High |
| **Model** | LLaMA 3.2 (1b/8b) |
| **Trigger** | When RAG confidence < 0.5 or complex query detected |
| **Acceptance Criteria** | Natural, coherent responses generated |

#### FR-014: RAG Context Injection
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-014 |
| **Title** | Context-Augmented Generation |
| **Description** | The system shall inject retrieved context into LLM prompts for accurate response generation |
| **Priority** | High |
| **Format** | System prompt + RAG context + User question |
| **Acceptance Criteria** | Responses utilize retrieved context accurately |

#### FR-015: English Language Enforcement
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-015 |
| **Title** | English-Only Response Generation |
| **Description** | The system shall ensure all responses are in English, detecting and regenerating non-English content |
| **Priority** | High |
| **Detection** | Unicode range checking (Bengali: 0980-09FF, Hindi: 0900-097F) |
| **Acceptance Criteria** | No non-English characters in final response |

#### FR-016: Fee Information Validation
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-016 |
| **Title** | Fee Accuracy Validation |
| **Description** | The system shall validate fee-related answers against known correct values |
| **Priority** | High |
| **Validation Rules** | CSE: 70,000 BDT, EEE: 80,000 BDT, BBA: 60,000 BDT |
| **Acceptance Criteria** | Warning logged if fee mismatch detected |

---

### 2.4 Feedback Learning Module

#### FR-017: User Feedback Collection
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-017 |
| **Title** | Like/Dislike Feedback Collection |
| **Description** | The system shall collect user feedback (like/dislike) for each response |
| **Priority** | High |
| **Input** | { feedback: "like"|"dislike", answer: string, question: string } |
| **Storage** | user_feedback_data.json |
| **Acceptance Criteria** | All feedback persisted with timestamp |

#### FR-018: Positive Feedback Reinforcement
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-018 |
| **Title** | Pattern Learning from Positive Feedback |
| **Description** | The system shall analyze liked responses to identify successful patterns by category |
| **Priority** | Medium |
| **Categories** | cse_fee, fees, admission, programs |
| **Acceptance Criteria** | Patterns extracted and stored for future use |

#### FR-019: Negative Feedback Blocking
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-019 |
| **Title** | Disliked Answer Blocking |
| **Description** | The system shall permanently block disliked answers from being repeated |
| **Priority** | High |
| **Storage** | disliked_answers.json |
| **Acceptance Criteria** | Disliked answers never repeated |

#### FR-020: Similarity-Based Answer Avoidance
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-020 |
| **Title** | Similar Answer Detection |
| **Description** | The system shall detect and avoid generating responses similar to disliked answers |
| **Priority** | High |
| **Threshold** | 70% word overlap similarity |
| **Action** | Regenerate with different prompt |
| **Acceptance Criteria** | No response > 70% similar to blocked answers |

#### FR-021: Learning Statistics Tracking
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-021 |
| **Title** | Feedback Statistics Aggregation |
| **Description** | The system shall track and report learning statistics |
| **Priority** | Medium |
| **Metrics** | total_feedback, likes, dislikes, blocked_answers, improved_responses |
| **Acceptance Criteria** | Statistics available via /stats endpoint |

---

### 2.5 API Module

#### FR-022: Chat Endpoint
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-022 |
| **Title** | Chat API Endpoint |
| **Description** | The system shall provide POST /chat endpoint for query submission |
| **Priority** | High |
| **Request** | { "message": string } |
| **Response** | { "answer", "confidence", "method", "processing_time", "source", "analyzed_items" } |
| **Acceptance Criteria** | Valid JSON response for all requests |

#### FR-023: Feedback Endpoint
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-023 |
| **Title** | Feedback API Endpoint |
| **Description** | The system shall provide POST /feedback endpoint for feedback submission |
| **Priority** | High |
| **Request** | { "feedback", "answer", "question" } |
| **Response** | { "status", "message", "learning_stats" } |
| **Acceptance Criteria** | Feedback processed and acknowledged |

#### FR-024: Health Check Endpoint
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-024 |
| **Title** | Health Check API Endpoint |
| **Description** | The system shall provide GET /health endpoint for system status |
| **Priority** | Medium |
| **Response** | { "status", "llm_available", "search_system_available", "data_loaded" } |
| **Acceptance Criteria** | Returns current system health status |

#### FR-025: Statistics Endpoint
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-025 |
| **Title** | Statistics API Endpoint |
| **Description** | The system shall provide GET /stats endpoint for analytics |
| **Priority** | Low |
| **Response** | { "learning_stats", "data_stats", "feedback_count" } |
| **Acceptance Criteria** | Returns aggregated statistics |

---

### 2.6 Data Management Module

#### FR-026: Dataset Loading
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-026 |
| **Title** | Multi-File Dataset Loading |
| **Description** | The system shall load and merge data from multiple JSON files |
| **Priority** | High |
| **Files** | enhanced_ndata.json, dataset/*.json, instruction-response.json |
| **Acceptance Criteria** | All valid JSON files loaded on startup |

#### FR-027: Priority-Based Data Loading
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-027 |
| **Title** | Priority File Handling |
| **Description** | The system shall prioritize CRITICAL and improved files over regular files |
| **Priority** | Medium |
| **Priority Levels** | CRITICAL (+0.2 boost), High (+0.1 boost), Normal (no boost) |
| **Acceptance Criteria** | Priority files override deprecated versions |

#### FR-028: Feedback Data Persistence
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-028 |
| **Title** | Feedback Data Storage |
| **Description** | The system shall persist all feedback data to JSON files |
| **Priority** | High |
| **Files** | user_feedback_data.json, disliked_answers.json |
| **Acceptance Criteria** | Data survives system restart |

#### FR-029: Model Serialization
| Attribute | Description |
|-----------|-------------|
| **ID** | FR-029 |
| **Title** | ML Model Persistence |
| **Description** | The system shall serialize and load trained ML models |
| **Priority** | Medium |
| **Format** | Pickle (.pkl) |
| **File** | learning_model.pkl |
| **Acceptance Criteria** | Models loaded on startup if available |

---

## 3. Non-Functional Requirements

### 3.1 Performance Requirements

#### NFR-001: Response Time
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-001 |
| **Title** | Query Response Time |
| **Description** | The system shall respond to queries within acceptable time limits |
| **Metric** | Response latency |
| **Target** | |
| | RAG-only: < 1 second |
| | With LLM: < 3 seconds |
| | 95th percentile: < 5 seconds |
| **Measurement** | processing_time field in response |

#### NFR-002: Throughput
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-002 |
| **Title** | System Throughput |
| **Description** | The system shall handle concurrent user requests |
| **Metric** | Requests per second |
| **Target** | Minimum 10 concurrent users |
| **Peak** | 50 concurrent users |

#### NFR-003: Startup Time
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-003 |
| **Title** | System Initialization Time |
| **Description** | The system shall initialize within acceptable time |
| **Metric** | Time from start to ready |
| **Target** | < 10 seconds |
| **Includes** | Data loading, model training, LLM connection |

#### NFR-004: Memory Usage
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-004 |
| **Title** | Memory Consumption |
| **Description** | The system shall operate within memory constraints |
| **Metric** | RAM usage |
| **Target** | < 2 GB (without LLM) |
| **With LLM** | < 8 GB (with LLaMA 3.2:8b) |

---

### 3.2 Reliability Requirements

#### NFR-005: Availability
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-005 |
| **Title** | System Availability |
| **Description** | The system shall maintain high availability |
| **Metric** | Uptime percentage |
| **Target** | 99% uptime during operational hours |
| **Calculation** | (Total time - Downtime) / Total time × 100 |

#### NFR-006: Fault Tolerance
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-006 |
| **Title** | Graceful Degradation |
| **Description** | The system shall continue operating with reduced functionality when components fail |
| **Scenarios** | |
| | LLM unavailable → Use RAG-only responses |
| | Dataset partially loaded → Use available data |
| | Feedback system down → Continue query processing |

#### NFR-007: Data Integrity
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-007 |
| **Title** | Data Consistency |
| **Description** | The system shall maintain data integrity across operations |
| **Requirements** | |
| | Atomic feedback writes |
| | JSON validation on load |
| | UTF-8 encoding enforcement |

#### NFR-008: Error Handling
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-008 |
| **Title** | Comprehensive Error Handling |
| **Description** | The system shall handle all errors gracefully |
| **Requirements** | |
| | No unhandled exceptions |
| | User-friendly error messages |
| | Detailed logging for debugging |

---

### 3.3 Accuracy Requirements

#### NFR-009: Answer Accuracy
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-009 |
| **Title** | Response Accuracy |
| **Description** | The system shall provide accurate answers based on retrieved data |
| **Metric** | Accuracy rate |
| **Target** | |
| | High confidence (≥0.85): 95% accuracy |
| | Medium confidence (≥0.50): 80% accuracy |
| | Low confidence (≥0.25): 60% accuracy |

#### NFR-010: Department Accuracy
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-010 |
| **Title** | Department-Specific Accuracy |
| **Description** | The system shall not mix information between departments |
| **Metric** | Cross-department error rate |
| **Target** | < 1% cross-department errors |
| **Validation** | Department detection + scoring penalties |

#### NFR-011: Fee Accuracy
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-011 |
| **Title** | Financial Information Accuracy |
| **Description** | The system shall provide exact fee amounts |
| **Metric** | Fee accuracy rate |
| **Target** | 100% accuracy for known fee values |
| **Validation** | Hardcoded fee validation rules |

#### NFR-012: Confidence Calibration
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-012 |
| **Title** | Confidence Score Reliability |
| **Description** | Confidence scores shall correlate with actual accuracy |
| **Metric** | Calibration error |
| **Target** | |
| | 0.9+ confidence → 90%+ correct |
| | 0.7-0.9 confidence → 70-90% correct |
| | 0.5-0.7 confidence → 50-70% correct |

---

### 3.4 Scalability Requirements

#### NFR-013: Data Scalability
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-013 |
| **Title** | Dataset Growth Support |
| **Description** | The system shall handle growing datasets |
| **Current** | 30,000+ entries |
| **Target** | Up to 100,000 entries |
| **Constraint** | Response time degradation < 20% |

#### NFR-014: Horizontal Scalability
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-014 |
| **Title** | Multi-Instance Support |
| **Description** | The system architecture shall support horizontal scaling |
| **Requirements** | |
| | Stateless API design |
| | Shared data storage |
| | Load balancer compatible |

---

### 3.5 Security Requirements

#### NFR-015: Input Validation
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-015 |
| **Title** | Input Sanitization |
| **Description** | The system shall validate and sanitize all user inputs |
| **Requirements** | |
| | Maximum input length: 1000 characters |
| | Special character handling |
| | Encoding validation (UTF-8) |

#### NFR-016: CORS Security
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-016 |
| **Title** | Cross-Origin Resource Sharing |
| **Description** | The system shall implement CORS restrictions |
| **Allowed Origins** | localhost:3000, localhost:5173, localhost:5174 |
| **Methods** | GET, POST, OPTIONS |

#### NFR-017: Error Information Disclosure
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-017 |
| **Title** | Safe Error Messages |
| **Description** | The system shall not expose sensitive information in error messages |
| **Requirements** | |
| | Generic user-facing errors |
| | Detailed internal logging |
| | No stack traces to users |

---

### 3.6 Usability Requirements

#### NFR-018: Response Clarity
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-018 |
| **Title** | Clear Response Format |
| **Description** | Responses shall be clear, structured, and easy to understand |
| **Requirements** | |
| | Plain English language |
| | Structured formatting (bullets, numbers) |
| | Specific amounts and dates |

#### NFR-019: Language Consistency
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-019 |
| **Title** | English Language Consistency |
| **Description** | All system outputs shall be in English |
| **Enforcement** | Automatic detection and regeneration |
| **Target** | 100% English responses |

#### NFR-020: Feedback Simplicity
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-020 |
| **Title** | Simple Feedback Mechanism |
| **Description** | Users shall be able to provide feedback with minimal effort |
| **Interface** | Single-click like/dislike buttons |
| **Response** | Immediate acknowledgment |

---

### 3.7 Maintainability Requirements

#### NFR-021: Code Modularity
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-021 |
| **Title** | Modular Architecture |
| **Description** | The system shall be organized into independent modules |
| **Modules** | |
| | API Layer (rag_api_server.py) |
| | Search System (IntegratedSearchSystem) |
| | Chatbot (EnhancedOllamaChatbotV2) |
| | Data Layer (JSON files) |

#### NFR-022: Configuration Management
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-022 |
| **Title** | External Configuration |
| **Description** | System parameters shall be configurable without code changes |
| **Methods** | |
| | Environment variables (.env) |
| | Configuration file (config.py) |
| | JSON configuration (lora_config.json) |

#### NFR-023: Logging
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-023 |
| **Title** | Comprehensive Logging |
| **Description** | The system shall log all significant events |
| **Levels** | INFO, WARNING, ERROR |
| **Content** | Timestamps, query info, confidence scores, errors |

#### NFR-024: Documentation
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-024 |
| **Title** | System Documentation |
| **Description** | The system shall be fully documented |
| **Documents** | |
| | Architecture documentation |
| | API documentation |
| | Setup guides |
| | Requirements specification |

---

### 3.8 Compatibility Requirements

#### NFR-025: Python Compatibility
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-025 |
| **Title** | Python Version Support |
| **Description** | The system shall be compatible with supported Python versions |
| **Supported** | Python 3.9, 3.10, 3.11, 3.12 |
| **Recommended** | Python 3.10+ |

#### NFR-026: Operating System Compatibility
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-026 |
| **Title** | OS Support |
| **Description** | The system shall run on major operating systems |
| **Supported** | Windows 10/11, Ubuntu 20.04+, macOS 12+ |

#### NFR-027: Browser Compatibility
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-027 |
| **Title** | Frontend Browser Support |
| **Description** | The frontend shall work on modern browsers |
| **Supported** | Chrome 90+, Firefox 90+, Safari 14+, Edge 90+ |

---

### 3.9 Portability Requirements

#### NFR-028: Containerization Support
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-028 |
| **Title** | Docker Compatibility |
| **Description** | The system shall be deployable via containers |
| **Requirements** | |
| | Dockerfile support |
| | Docker Compose configuration |
| | Volume mounting for data persistence |

#### NFR-029: Cloud Deployment
| Attribute | Description |
|-----------|-------------|
| **ID** | NFR-029 |
| **Title** | Cloud Platform Support |
| **Description** | The system shall be deployable on cloud platforms |
| **Platforms** | AWS, Azure, GCP, DigitalOcean |
| **Requirements** | Environment variable configuration |

---

## 4. System Requirements

### 4.1 Hardware Requirements

#### Minimum Requirements
| Component | Specification |
|-----------|---------------|
| **CPU** | 4 cores, 2.0 GHz |
| **RAM** | 8 GB |
| **Storage** | 10 GB SSD |
| **Network** | 100 Mbps |

#### Recommended Requirements
| Component | Specification |
|-----------|---------------|
| **CPU** | 8 cores, 3.0 GHz |
| **RAM** | 16 GB |
| **Storage** | 50 GB SSD |
| **GPU** | NVIDIA RTX 3060 (for faster LLM inference) |
| **Network** | 1 Gbps |

### 4.2 Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.10+ | Runtime |
| Flask | 2.0+ | Web framework |
| scikit-learn | 1.3+ | ML algorithms |
| NLTK | 3.8+ | NLP processing |
| Ollama | Latest | LLM inference |
| Node.js | 18+ | Frontend runtime |

---

## 5. Use Case Diagrams

### 5.1 Primary Use Cases

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USE CASE DIAGRAM                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│                              ┌─────────────┐                                    │
│                              │   System    │                                    │
│                              │  Boundary   │                                    │
│         ┌────────┐           │             │                                    │
│         │        │           │  ┌───────────────────────┐                      │
│         │  User  │──────────────│  UC-01: Ask Question  │                      │
│         │        │           │  └───────────────────────┘                      │
│         │        │           │             │                                    │
│         │        │           │  ┌───────────────────────┐                      │
│         │        │──────────────│  UC-02: View Answer   │                      │
│         │        │           │  └───────────────────────┘                      │
│         │        │           │             │                                    │
│         │        │           │  ┌───────────────────────┐                      │
│         │        │──────────────│  UC-03: Give Feedback │                      │
│         │        │           │  └───────────────────────┘                      │
│         │        │           │             │                                    │
│         │        │           │  ┌───────────────────────┐                      │
│         │        │──────────────│  UC-04: Start New Chat│                      │
│         └────────┘           │  └───────────────────────┘                      │
│                              │             │                                    │
│         ┌────────┐           │  ┌───────────────────────┐                      │
│         │        │           │  │  UC-05: Check Health  │                      │
│         │ Admin  │──────────────│                       │                      │
│         │        │           │  └───────────────────────┘                      │
│         │        │           │             │                                    │
│         │        │           │  ┌───────────────────────┐                      │
│         │        │──────────────│  UC-06: View Stats    │                      │
│         │        │           │  └───────────────────────┘                      │
│         │        │           │             │                                    │
│         │        │           │  ┌───────────────────────┐                      │
│         │        │──────────────│  UC-07: Update Dataset│                      │
│         └────────┘           │  └───────────────────────┘                      │
│                              │             │                                    │
│                              └─────────────┘                                    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Use Case Descriptions

| UC ID | Name | Actor | Description | Pre-condition | Post-condition |
|-------|------|-------|-------------|---------------|----------------|
| UC-01 | Ask Question | User | User submits a query about university | System is running | Query processed |
| UC-02 | View Answer | User | User views the chatbot response | Query submitted | Answer displayed |
| UC-03 | Give Feedback | User | User rates the answer | Answer received | Feedback recorded |
| UC-04 | Start New Chat | User | User starts a fresh conversation | System available | Chat history cleared |
| UC-05 | Check Health | Admin | Admin checks system status | API accessible | Status returned |
| UC-06 | View Stats | Admin | Admin views learning statistics | System running | Stats displayed |
| UC-07 | Update Dataset | Admin | Admin adds new Q&A data | File access | Data loaded |

---

## 6. Requirements Traceability Matrix

### 6.1 Functional Requirements to Components

| Requirement | Component | File |
|-------------|-----------|------|
| FR-001 to FR-004 | Query Processing | rag_api_server.py |
| FR-005 to FR-012 | Information Retrieval | IntegratedSearchSystem |
| FR-013 to FR-016 | Response Generation | enhanced_ollama_chatbot_v2.py |
| FR-017 to FR-021 | Feedback Learning | EnhancedOllamaChatbotV2 |
| FR-022 to FR-025 | API Module | rag_api_server.py |
| FR-026 to FR-029 | Data Management | JSON files, pickle |

### 6.2 Non-Functional Requirements to Design Decisions

| NFR | Design Decision |
|-----|-----------------|
| NFR-001 (Response Time) | Parallel search, exact match priority |
| NFR-009 (Accuracy) | Multi-strategy scoring, department boost |
| NFR-010 (Department Accuracy) | Department detection + penalty scoring |
| NFR-006 (Fault Tolerance) | Fallback chain: V2 → V1 → LLM → Static |
| NFR-015 (Input Validation) | Preprocessing pipeline, character limits |
| NFR-021 (Modularity) | Separate classes for Search, Chatbot, API |

---

## 7. Appendix

### 7.1 Glossary

| Term | Definition |
|------|------------|
| **Cosine Similarity** | Measure of similarity between two vectors |
| **Jaccard Similarity** | Intersection over union of two sets |
| **Lemmatization** | Reducing words to their base form |
| **N-gram** | Contiguous sequence of n items from text |
| **Stopwords** | Common words filtered from text processing |
| **Vectorization** | Converting text to numerical vectors |

### 7.2 References

1. Flask Documentation: https://flask.palletsprojects.com/
2. scikit-learn Documentation: https://scikit-learn.org/
3. NLTK Documentation: https://www.nltk.org/
4. Ollama Documentation: https://ollama.ai/
5. LangChain Documentation: https://python.langchain.com/

---

*Document prepared for research and development purposes.*  
*Last Updated: January 2026*
