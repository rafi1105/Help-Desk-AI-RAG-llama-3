# Backend Architecture: RAG-Enhanced University Help Desk Chatbot

## System Overview

This document provides a comprehensive architectural overview of the backend system for a **Retrieval-Augmented Generation (RAG)** chatbot designed for university help desk operations. The system integrates multiple AI/ML techniques including TF-IDF vectorization, cosine similarity matching, reinforcement learning from user feedback, and Large Language Model (LLM) generation.

---

## 1. High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    React Frontend                       │   │
│  │                    HTTP/JSON API Communication                           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │ REST API (JSON)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     Flask REST API Server                                │   │
│  │                                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │   │
│  │  │  /chat   │  │/feedback │  │ /health  │  │  /stats  │  │  /reset  │ │   │
│  │  │ POST     │  │ POST     │  │ GET      │  │ GET      │  │ POST     │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CORE PROCESSING LAYER                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │              IntegratedSearchSystem (Main Orchestrator)                  │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Query Processing Pipeline                     │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐│   │   │
│  │  │  │  Text    │→│  NLP     │→│ Department│→│ Multi-Strategy   ││   │   │
│  │  │  │Preprocess│  │Normalize │  │ Detection │  │ Search Engine    ││   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘│   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │                   Search Strategies (Parallel)                   │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │   │
│  │  │  │  TF-IDF      │  │  Keyword     │  │  Instruction-Response│  │   │   │
│  │  │  │  Cosine      │  │  Exact       │  │  Dataset Search      │  │   │   │
│  │  │  │  Similarity  │  │  Matching    │  │  (100K+ entries)      │  │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │   │   │
│  │  │  │  Question    │  │  Phrase      │  │  Department-Specific │  │   │   │
│  │  │  │  Variation   │  │  Matching    │  │  Boost/Penalty       │  │   │   │
│  │  │  │  Matching    │  │              │  │                      │  │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘  │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      CHATBOT ENHANCEMENT LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │           EnhancedOllamaChatbotV2 (RAG + RL + Feedback)                  │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    Enhancement Pipeline                           │  │   │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │  │   │
│  │  │  │ Language   │→│ RAG Context│→│ Disliked   │→│ Pattern    │ │  │   │
│  │  │  │ Enforcement│  │ Injection  │  │ Answer     │  │ Learning   │ │  │   │
│  │  │  │ (English)  │  │            │  │ Avoidance  │  │            │ │  │   │
│  │  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘ │  │   │
│  │  └──────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                         │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    Feedback Learning System                       │  │   │
│  │  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐ │  │   │
│  │  │  │ Positive       │  │ Negative       │  │ Response Pattern   │ │  │   │
│  │  │  │ Feedback       │  │ Feedback       │  │ Analysis           │ │  │   │
│  │  │  │ Reinforcement  │  │ Blocking       │  │ & Improvement      │ │  │   │
│  │  │  └────────────────┘  └────────────────┘  └────────────────────┘ │  │   │
│  │  └──────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬─────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        LLM INFERENCE LAYER                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                   Ollama Service (Port 11434)                            │   │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    LLaMA 3.2:1b/8b Model                          │  │   │
│  │  │  • Natural Language Understanding                                 │  │   │
│  │  │  • Context-Aware Response Generation                              │  │   │
│  │  │  • Dynamic System Prompt Enhancement                              │  │   │
│  │  └──────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DATA PERSISTENCE LAYER                                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ Dataset JSON  │  │ enhanced_     │  │ user_feedback │  │ disliked_     │   │
│  │ Files (10+)   │  │ ndata.json    │  │ _data.json    │  │ answers.json  │   │
│  │ ~30K entries  │  │               │  │               │  │               │   │
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘   │
│  ┌───────────────┐  ┌───────────────┐                                         │
│  │ learning_     │  │ blocked_      │                                         │
│  │ model.pkl     │  │ keywords.json │                                         │
│  └───────────────┘  └───────────────┘                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 API Gateway Layer (`rag_api_server.py`)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Flask REST API Server                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         CORS Configuration                               │   │
│  │  Allowed Origins: localhost:3000, 5173, 5174 (Frontend Dev Servers)     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                          API Endpoints                                   │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  POST /chat                                                              │   │
│  │  ├─ Input:  { "message": string }                                       │   │
│  │  ├─ Process: IntegratedSearchSystem.integrated_search()                 │   │
│  │  └─ Output: { "answer", "confidence", "method", "processing_time",      │   │
│  │              "source", "analyzed_items" }                               │   │
│  │                                                                          │   │
│  │  POST /feedback                                                          │   │
│  │  ├─ Input:  { "feedback": "like"|"dislike", "answer", "question" }     │   │
│  │  ├─ Process: record_feedback() → learning system update                 │   │
│  │  └─ Output: { "status", "message", "learning_stats" }                   │   │
│  │                                                                          │   │
│  │  GET /health                                                             │   │
│  │  ├─ Process: Check LLM, Search System, Chatbot availability            │   │
│  │  └─ Output: { "status", "llm_available", "search_system_available",    │   │
│  │              "enhanced_chatbot_available", "data_loaded" }              │   │
│  │                                                                          │   │
│  │  GET /stats                                                              │   │
│  │  ├─ Process: Aggregate learning statistics                              │   │
│  │  └─ Output: { "learning_stats", "data_stats", "feedback_count" }       │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    System Initialization                                 │   │
│  │  1. Load environment variables (.env)                                   │   │
│  │  2. Initialize NLTK resources (stopwords, wordnet)                      │   │
│  │  3. Load IntegratedSearchSystem with all datasets                       │   │
│  │  4. Initialize EnhancedOllamaChatbotV2                                  │   │
│  │  5. Connect to Ollama LLM service                                       │   │
│  │  6. Train ML models (TF-IDF, RandomForest)                              │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Integrated Search System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        IntegratedSearchSystem Class                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     DATA LOADING SUBSYSTEM                               │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  load_data()              → Load enhanced_ndata.json                    │   │
│  │                           → Load instruction-response pairs (30K+)      │   │
│  │                                                                          │   │
│  │  load_dataset_files()     → Load department-specific JSON files         │   │
│  │                           → Priority handling (CRITICAL > improved)     │   │
│  │                           → Skip deprecated files                       │   │
│  │                                                                          │   │
│  │  load_feedback_data()     → Load disliked_answers.json                  │   │
│  │                           → Load user_feedback_data.json                │   │
│  │                           → Load learning_model.pkl                     │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     NLP PREPROCESSING PIPELINE                           │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  preprocess(text)         → Lowercase conversion                        │   │
│  │                           → Special character removal                   │   │
│  │                           → WordNet lemmatization                       │   │
│  │                           → Stopword filtering                          │   │
│  │                                                                          │   │
│  │  _extract_keywords()      → Academic term extraction                    │   │
│  │                           → Department term extraction                  │   │
│  │                           → Facility term extraction                    │   │
│  │                                                                          │   │
│  │  _auto_categorize()       → fees_financial                              │   │
│  │                           → admission_requirements                      │   │
│  │                           → academic_programs                           │   │
│  │                           → contact_information                         │   │
│  │                           → campus_facilities                           │   │
│  │                           → scholarships_aid                            │   │
│  │                           → student_activities                          │   │
│  │                           → general_inquiry                             │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     ML MODEL TRAINING                                    │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  train_models()                                                          │   │
│  │  ├─ TF-IDF Vectorizer                                                   │   │
│  │  │  • ngram_range: (1, 3)                                               │   │
│  │  │  • max_features: 5000                                                │   │
│  │  │  • min_df: 1, max_df: 0.95                                           │   │
│  │  │                                                                       │   │
│  │  └─ RandomForest Classifier (Category Prediction)                       │   │
│  │     • n_estimators: 20                                                  │   │
│  │     • Sample size: min(1000, total_data)                                │   │
│  │     • Train/Test split: 80/20                                           │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                  MULTI-STRATEGY SEARCH ENGINE                            │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  integrated_search(user_input) → Main orchestrator                      │   │
│  │  │                                                                       │   │
│  │  ├─► search_json_data()                                                 │   │
│  │  │   ├─ Strategy 0: Exact/Near-Exact Match (Highest Priority)          │   │
│  │  │   │  • Normalized question comparison                                │   │
│  │  │   │  • Question variation matching                                   │   │
│  │  │   │  • Jaccard similarity calculation                                │   │
│  │  │   │                                                                   │   │
│  │  │   ├─ Strategy 1: TF-IDF Cosine Similarity (40% weight)              │   │
│  │  │   │  • Semantic vector matching                                      │   │
│  │  │   │                                                                   │   │
│  │  │   ├─ Strategy 2: Keyword Exact Matching (20% weight)                │   │
│  │  │   │  • Direct keyword overlap                                        │   │
│  │  │   │                                                                   │   │
│  │  │   ├─ Strategy 3: Question Variation Matching (10% weight)           │   │
│  │  │   │  • Pre-defined question variations                               │   │
│  │  │   │                                                                   │   │
│  │  │   ├─ Strategy 4: Phrase Matching (10% weight)                       │   │
│  │  │   │  • 2-gram and 3-gram matching                                    │   │
│  │  │   │                                                                   │   │
│  │  │   └─ Strategy 5: Department-Specific Boost (20% weight)             │   │
│  │  │      • +0.4 boost for matching department                            │   │
│  │  │      • -0.5 penalty for wrong department                             │   │
│  │  │                                                                       │   │
│  │  └─► search_instruction_responses()                                     │   │
│  │      ├─ Jaccard Similarity (40% weight)                                 │   │
│  │      ├─ Word Order Similarity (20% weight)                              │   │
│  │      ├─ Key Term Matching (25% weight)                                  │   │
│  │      └─ Exact Phrase Matching (15% weight)                              │   │
│  │                                                                          │   │
│  │  Score Aggregation:                                                      │   │
│  │  combined_score = (tfidf × 0.4) + (keyword × 0.2) +                     │   │
│  │                   (variation × 0.1) + (phrase × 0.1) +                  │   │
│  │                   (department × 0.2)                                     │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Enhanced Chatbot V2 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      EnhancedOllamaChatbotV2 Class                               │
│                  (RAG + Reinforcement Learning + Feedback)                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    CONFIGURATION PARAMETERS                              │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │  • ollama_url: http://localhost:11434                                   │   │
│  │  • model_name: llama3.2:1b                                              │   │
│  │  • temperature: 0.7                                                      │   │
│  │  • top_p: 0.9                                                            │   │
│  │  • max_tokens: 512                                                       │   │
│  │  • similarity_threshold: 0.7 (for disliked answer detection)            │   │
│  │  • timeout: 60 seconds                                                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    RESPONSE GENERATION PIPELINE                          │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  generate_response(user_question, rag_context)                          │   │
│  │  │                                                                       │   │
│  │  ├─► Step 1: Language Enforcement                                       │   │
│  │  │   • enforce_english_response()                                       │   │
│  │  │   • Reject non-English input patterns                                │   │
│  │  │                                                                       │   │
│  │  ├─► Step 2: System Prompt Enhancement                                  │   │
│  │  │   • enhance_system_prompt(rag_context)                               │   │
│  │  │   • Inject RAG context                                               │   │
│  │  │   • Add learned patterns                                             │   │
│  │  │   • Add disliked answer warnings                                     │   │
│  │  │                                                                       │   │
│  │  ├─► Step 3: LLM Generation                                             │   │
│  │  │   • POST to Ollama /api/generate                                     │   │
│  │  │   • Stream: false                                                    │   │
│  │  │                                                                       │   │
│  │  ├─► Step 4: Non-English Detection & Regeneration                       │   │
│  │  │   • _contains_non_english()                                          │   │
│  │  │   • _force_english_regeneration()                                    │   │
│  │  │   • _get_fallback_english_response()                                 │   │
│  │  │                                                                       │   │
│  │  ├─► Step 5: Disliked Answer Similarity Check                           │   │
│  │  │   • is_similar_to_disliked()                                         │   │
│  │  │   • Word overlap calculation                                         │   │
│  │  │   • Regeneration if similarity > 70%                                 │   │
│  │  │                                                                       │   │
│  │  ├─► Step 6: Fee Validation                                             │   │
│  │  │   • CSE: BDT 70,000/semester                                         │   │
│  │  │   • EEE: BDT 80,000/semester                                         │   │
│  │  │   • BBA: BDT 60,000/semester                                         │   │
│  │  │                                                                       │   │
│  │  └─► Step 7: Response Formatting                                        │   │
│  │      • _format_response_with_feedback()                                 │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    FEEDBACK LEARNING SYSTEM                              │   │
│  ├─────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                          │   │
│  │  Positive Feedback (Like):                                               │   │
│  │  ├─ _analyze_feedback_patterns()                                        │   │
│  │  ├─ Extract successful response patterns by category:                   │   │
│  │  │  • cse_fee, fees, admission, programs                                │   │
│  │  └─ Reinforce patterns in future prompts                                │   │
│  │                                                                          │   │
│  │  Negative Feedback (Dislike):                                            │   │
│  │  ├─ save_disliked_answer()                                              │   │
│  │  ├─ Add to blocked answers list                                         │   │
│  │  └─ Prevent similar responses (similarity > 70%)                        │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow Architecture

### 3.1 Query Processing Flow

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         QUERY PROCESSING PIPELINE                               │
└────────────────────────────────────────────────────────────────────────────────┘

User Query: "What is the CSE tuition fee?"
                    │
                    ▼
┌─────────────────────────────────────┐
│  1. API RECEPTION                   │
│  POST /chat { message: "..." }      │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  2. TEXT PREPROCESSING              │
│  • Lowercase: "what is the cse..."  │
│  • Lemmatize: "what be the cse..."  │
│  • Remove stopwords: "cse tuition"  │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  3. DEPARTMENT DETECTION            │
│  • Detected: "cse"                  │
│  • Category: "fees_financial"       │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  4. PARALLEL SEARCH EXECUTION                                                │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────────┐ │
│  │  JSON Dataset Search        │   │  Instruction-Response Search        │ │
│  │  • TF-IDF: 0.75            │   │  • Jaccard: 0.82                    │ │
│  │  • Keyword: 0.90           │   │  • Key Terms: 0.85                  │ │
│  │  • Department: +0.40       │   │  • Phrase: 0.70                     │ │
│  │  Combined: 0.85            │   │  Combined: 0.78                     │ │
│  └─────────────────────────────┘   └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  5. RESULT AGGREGATION              │
│  • Best Match: JSON Dataset (0.85)  │
│  • Answer: "BDT 70,000/semester"    │
│  • Source References: Top 3         │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  6. LLM ENHANCEMENT (if needed)     │
│  • RAG Context Injection            │
│  • Language Enforcement             │
│  • Fee Validation                   │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  7. RESPONSE DELIVERY               │
│  {                                  │
│    "answer": "CSE tuition fee...",  │
│    "confidence": 0.85,              │
│    "method": "multi_strategy",      │
│    "processing_time": 1.2s          │
│  }                                  │
└─────────────────────────────────────┘
```

### 3.2 Feedback Learning Flow

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                         FEEDBACK LEARNING PIPELINE                              │
└────────────────────────────────────────────────────────────────────────────────┘

User Action: 👍 Like / 👎 Dislike
                    │
                    ▼
┌─────────────────────────────────────┐
│  1. FEEDBACK RECEPTION              │
│  POST /feedback {                   │
│    feedback: "like" | "dislike",    │
│    answer: "...",                   │
│    question: "..."                  │
│  }                                  │
└─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  LIKE PATH      │     │  DISLIKE PATH   │
├─────────────────┤     ├─────────────────┤
│                 │     │                 │
│ • Extract       │     │ • Add to        │
│   patterns      │     │   blocked list  │
│                 │     │                 │
│ • Categorize    │     │ • Calculate     │
│   (cse_fee,     │     │   similarity    │
│   admission..)  │     │   threshold     │
│                 │     │                 │
│ • Reinforce     │     │ • Prevent       │
│   in prompt     │     │   future use    │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
┌─────────────────────────────────────┐
│  2. PERSISTENCE                     │
│  • user_feedback_data.json          │
│  • disliked_answers.json            │
│  • learning_model.pkl               │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  3. MODEL UPDATE                    │
│  • Retrain patterns                 │
│  • Update similarity thresholds     │
│  • Adjust confidence scores         │
└─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────┐
│  4. FUTURE RESPONSES IMPROVED       │
│  • Better pattern matching          │
│  • Avoided disliked responses       │
│  • Higher accuracy                  │
└─────────────────────────────────────┘
```

---

## 4. Algorithm Details

### 4.1 Multi-Strategy Scoring Formula

```
                    COMBINED SCORE CALCULATION
═══════════════════════════════════════════════════════════════════════

For JSON Dataset Search:
────────────────────────────────────────────────────────────────────────
combined_score = (similarity_tfidf × 0.40) +
                 (keyword_match × 0.20) +
                 (variation_match × 0.10) +
                 (phrase_match × 0.10) +
                 (department_boost × 0.20)

Where:
• similarity_tfidf = cosine_similarity(TF-IDF(query), TF-IDF(document))
• keyword_match = |query_keywords ∩ doc_keywords| / |query_keywords|
• variation_match = max(jaccard(query, variation) for variation in variations)
• phrase_match = Σ(phrase_in_doc) × 0.15  for phrases length > 3
• department_boost = +0.4 if department matches, -0.5 if wrong department

────────────────────────────────────────────────────────────────────────

For Instruction-Response Search:
────────────────────────────────────────────────────────────────────────
combined_score = (jaccard × 0.40) +
                 (order_sim × 0.20) +
                 (key_term × 0.25) +
                 (phrase × 0.15)

Where:
• jaccard = |A ∩ B| / |A ∪ B|  (word sets)
• order_sim = Σ(1 - position_diff) × 0.1 / |input_words|
• key_term = matches / total_key_terms_in_input
• phrase = phrase_matches / total_phrases

═══════════════════════════════════════════════════════════════════════
```

### 4.2 Disliked Answer Similarity Detection

```
                    SIMILARITY DETECTION ALGORITHM
═══════════════════════════════════════════════════════════════════════

def is_similar_to_disliked(generated_answer, disliked_list):
    """
    Returns True if generated answer is too similar to any disliked answer
    """
    threshold = 0.70  # 70% similarity threshold
    
    for disliked in disliked_list:
        generated_words = set(generated_answer.lower().split())
        disliked_words = set(disliked['answer'].lower().split())
        
        overlap = len(generated_words ∩ disliked_words)
        similarity = overlap / max(len(generated_words), len(disliked_words))
        
        if similarity > threshold:
            return True, f"Too similar ({similarity:.0%})"
    
    return False, None

═══════════════════════════════════════════════════════════════════════
```

### 4.3 TF-IDF Vectorization Configuration

```
                    TF-IDF VECTORIZER PARAMETERS
═══════════════════════════════════════════════════════════════════════

TfidfVectorizer(
    ngram_range=(1, 3),    # Unigrams, bigrams, trigrams
    max_features=5000,     # Maximum vocabulary size
    min_df=1,              # Minimum document frequency
    max_df=0.95,           # Maximum document frequency (ignore common terms)
    sublinear_tf=False,    # Use raw term frequency
    norm='l2'              # L2 normalization
)

Feature Matrix Shape: (N_documents × 5000)

═══════════════════════════════════════════════════════════════════════
```

---

## 5. Dataset Architecture

### 5.1 Dataset File Structure

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATASET HIERARCHY                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  backend/                                                                        │
│  │                                                                               │
│  ├── enhanced_ndata.json          (Primary Q&A dataset)                         │
│  │   └── Format: [{ question, answer, keywords, categories, confidence }]       │
│  │                                                                               │
│  ├── green_university_30k_instruction_response.json  (30K+ entries)            │
│  │   └── Format: JSONL { instruction, output }                                  │
│  │                                                                               │
│  └── dataset/                     (Department-specific datasets)                │
│      │                                                                           │
│      ├── Fee_Summary_CRITICAL.json     ★ PRIORITY: Critical                    │
│      │   └── All department fee information                                     │
│      │                                                                           │
│      ├── CSE_improved.json             ★ PRIORITY: High                        │
│      │   └── Computer Science & Engineering                                     │
│      │                                                                           │
│      ├── EEE_improved.json             ★ PRIORITY: High                        │
│      │   └── Electrical & Electronic Engineering                                │
│      │                                                                           │
│      ├── BBA_improved.json             ★ PRIORITY: High                        │
│      │   └── Business Administration                                            │
│      │                                                                           │
│      ├── General_University_Info.json  ★ PRIORITY: High                        │
│      │   └── General information                                                │
│      │                                                                           │
│      ├── BA ENG.json                   ○ PRIORITY: Normal                      │
│      ├── Law.json                      ○ PRIORITY: Normal                      │
│      ├── Sociology.json                ○ PRIORITY: Normal                      │
│      ├── textile.json                  ○ PRIORITY: Normal                      │
│      └── Journalism and media...json   ○ PRIORITY: Normal                      │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Data Entry Schema

```json
{
  "question": "What is the CSE tuition fee per semester?",
  "answer": "The CSE tuition fee is BDT 70,000 per semester.",
  "keywords": ["cse", "tuition", "fee", "semester", "cost"],
  "categories": ["fees_financial", "academic_programs"],
  "confidence_score": 1.0,
  "question_variations": [
    "How much does CSE cost?",
    "CSE semester fee",
    "Computer science tuition"
  ],
  "department": "cse",
  "priority": "critical",
  "source": "dataset_CSE_improved.json"
}
```

---

## 6. Performance Metrics

### 6.1 System Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Startup Time** | 5-10 seconds | Includes model loading |
| **Response Time (RAG only)** | < 1 second | Without LLM generation |
| **Response Time (with LLM)** | 1-3 seconds | With Ollama LLaMA 3.2 |
| **Dataset Size** | 30K+ entries | Across all JSON files |
| **TF-IDF Features** | 5,000 | Maximum vocabulary |
| **Memory Usage** | ~500MB-1GB | Depends on model size |

### 6.2 Accuracy Metrics

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ACCURACY CALCULATION                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Confidence Score Thresholds:                                                    │
│  ├─ Exact Match:        ≥ 0.98  (Direct question match)                        │
│  ├─ High Confidence:    ≥ 0.85  (Strong semantic match)                        │
│  ├─ Medium Confidence:  ≥ 0.50  (Partial match)                                │
│  └─ Low Confidence:     ≥ 0.25  (Weak match, needs LLM)                        │
│                                                                                  │
│  Department-Specific Accuracy:                                                   │
│  ├─ Correct Department:     +40% boost                                          │
│  └─ Wrong Department:       -50% penalty                                        │
│                                                                                  │
│  Fee Validation:                                                                 │
│  ├─ CSE:     70,000 BDT/semester  ✓                                            │
│  ├─ EEE:     80,000 BDT/semester  ✓                                            │
│  ├─ BBA:     60,000 BDT/semester  ✓                                            │
│  ├─ Textile: 65,000 BDT/semester  ✓                                            │
│  └─ Law:     55,000 BDT/semester  ✓                                            │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Technology Stack

### 7.1 Backend Technologies

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           TECHNOLOGY STACK                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Framework Layer:                                                                │
│  ├─ Flask 2.x                    REST API framework                             │
│  ├─ Flask-CORS                   Cross-origin resource sharing                  │
│  └─ python-dotenv                Environment configuration                      │
│                                                                                  │
│  ML/NLP Layer:                                                                   │
│  ├─ scikit-learn                 TF-IDF, Cosine Similarity, RandomForest       │
│  ├─ NLTK                         Tokenization, Lemmatization, Stopwords        │
│  └─ numpy                        Numerical operations                           │
│                                                                                  │
│  LLM Layer:                                                                      │
│  ├─ LangChain                    LLM orchestration                              │
│  ├─ Ollama                       Local LLM inference                            │
│  └─ LLaMA 3.2 (1b/8b)           Base language model                            │
│                                                                                  │
│  Data Layer:                                                                     │
│  ├─ JSON                         Primary data format                            │
│  ├─ Pickle                       Model serialization                            │
│  └─ UTF-8 Encoding               Unicode support                                │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Dependencies (requirements.txt)

```
flask>=2.0.0
flask-cors>=4.0.0
langchain>=0.1.0
langchain-community>=0.0.10
scikit-learn>=1.3.0
nltk>=3.8.0
numpy>=1.24.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## 8. Security Considerations

### 8.1 Implemented Security Features

- ✅ CORS configuration (whitelist-based)
- ✅ Input validation
- ✅ Error handling with safe fallbacks
- ✅ Environment variable configuration
- ✅ Non-English content filtering

### 8.2 Recommended Enhancements

- ⬜ API key authentication
- ⬜ Rate limiting
- ⬜ Input sanitization (SQL injection, XSS)
- ⬜ HTTPS/TLS encryption
- ⬜ Request logging and monitoring
- ⬜ User session management

---

## 9. Scalability Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      SCALABILITY CONSIDERATIONS                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  Current Architecture (Single Instance):                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Flask Server → IntegratedSearch → Ollama (Local)                       │   │
│  │  Capacity: ~10-50 concurrent users                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  Scaled Architecture (Recommended):                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                          Load Balancer                                   │   │
│  │                               │                                          │   │
│  │          ┌────────────────────┼────────────────────┐                    │   │
│  │          ▼                    ▼                    ▼                    │   │
│  │     Flask #1             Flask #2             Flask #3                  │   │
│  │          │                    │                    │                    │   │
│  │          └────────────────────┼────────────────────┘                    │   │
│  │                               ▼                                          │   │
│  │                      Redis Cache Layer                                   │   │
│  │                               │                                          │   │
│  │          ┌────────────────────┼────────────────────┐                    │   │
│  │          ▼                    ▼                    ▼                    │   │
│  │     Ollama #1            Ollama #2            Ollama #3                 │   │
│  │                                                                          │   │
│  │  Capacity: ~500-1000 concurrent users                                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. File Reference

| File | Purpose | Lines |
|------|---------|-------|
| [rag_api_server.py](backend/rag_api_server.py) | Main API server with IntegratedSearchSystem | ~1600 |
| [enhanced_ollama_chatbot_v2.py](backend/enhanced_ollama_chatbot_v2.py) | Advanced chatbot with RAG+RL+Feedback | ~660 |
| [enhanced_ollama_chatbot.py](backend/enhanced_ollama_chatbot.py) | V1 chatbot with feedback learning | ~290 |
| [config.py](backend/config.py) | Configuration settings | ~10 |
| [enhanced_ndata.json](backend/enhanced_ndata.json) | Primary Q&A dataset | Variable |
| [user_feedback_data.json](backend/user_feedback_data.json) | User feedback storage | Variable |
| [disliked_answers.json](backend/disliked_answers.json) | Blocked answers list | Variable |

---

## 11. Research Paper Integration Points

This architecture supports the following research contributions:

1. **Multi-Strategy Information Retrieval**: Novel combination of TF-IDF, keyword matching, and phrase detection
2. **Reinforcement Learning from Human Feedback (RLHF)**: Like/dislike feedback loop for continuous improvement
3. **Domain-Specific RAG**: Department-aware retrieval with boost/penalty scoring
4. **Hybrid Search Architecture**: Parallel search across multiple data sources
5. **Answer Quality Control**: Disliked answer detection and regeneration mechanism

---

*Document Version: 1.0 | Last Updated: January 2026*
