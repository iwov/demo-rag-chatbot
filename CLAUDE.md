# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This workspace contains multiple projects:
1. **starting-ragchatbot-codebase**: A RAG system for course materials using ChromaDB and Anthropic Claude
2. **index.html**: Interactive particle visualization demo
3. **rag-flow-diagram.html**: Animated diagram showing RAG system request flow

## RAG Chatbot System (starting-ragchatbot-codebase)

### Essential Commands

**IMPORTANT: Always use `uv` to run the server and manage dependencies. Never use `pip` directly.**

```bash
# Install dependencies (requires uv package manager)
cd starting-ragchatbot-codebase
uv sync

# Run the application
./run.sh
# OR manually:
cd backend && uv run uvicorn app:app --reload --port 8000

# Run any Python script
uv run python script.py

# Application URLs
# Web Interface: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Required Setup

Before running, create `.env` file in project root:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Architecture Overview

The RAG system follows a tool-based architecture where Claude AI decides when to search:

**Request Flow:**
1. **Frontend** (vanilla JS) → POST `/api/query` with user question
2. **FastAPI Backend** → Creates/retrieves session, delegates to RAG System
3. **RAG System** → Orchestrates between components:
   - **Session Manager**: Maintains conversation history (last 2 messages)
   - **AI Generator**: Calls Claude with available tools
4. **Claude AI** → Analyzes query, decides whether to use search tool
5. **Search Tool** → If invoked, performs semantic search:
   - Resolves course names semantically (partial matches work)
   - Queries ChromaDB with filters
6. **Vector Store** (ChromaDB) → Returns relevant chunks
7. **Claude AI** → Generates final response using search results
8. Response flows back through the chain to user

**Key Components:**
- **Document Processor** (`backend/document_processor.py`): 
  - Chunks documents into 800 chars with 100 char overlap
  - Sentence-based splitting to preserve semantic boundaries
  - Adds lesson context to first chunk of each lesson
  
- **Vector Store** (`backend/vector_store.py`):
  - Dual collections: course catalog (metadata) and course content (chunks)
  - Semantic course name resolution
  - Embeddings: all-MiniLM-L6-v2
  
- **AI Generator** (`backend/ai_generator.py`):
  - Claude Sonnet model (claude-sonnet-4-20250514)
  - Tool-calling capability for search integration
  - System prompt optimized for educational content

- **Search Tools** (`backend/search_tools.py`):
  - CourseSearchTool with smart course/lesson filtering
  - Tool manager for registration and execution
  - Source tracking for UI display

### Document Format

Course documents in `docs/` folder must follow this structure:
```
Course Title: [title]
Course Link: [url]
Course Instructor: [instructor]

Lesson 0: Introduction
Lesson Link: [lesson_url]
[lesson content...]

Lesson 1: Next Topic
[content...]
```

### Configuration

Key settings in `backend/config.py`:
- Chunk size: 800 characters
- Chunk overlap: 100 characters
- Max search results: 5
- Max conversation history: 2 messages
- ChromaDB path: `./chroma_db`

### Course Content

The system includes 4 comprehensive course scripts in `docs/`:
1. `course1_script.txt`: Building Towards Computer Use with Anthropic
2. `course2_script.txt`: MCP: Build Rich-Context AI Apps
3. `course3_script.txt`: Advanced Retrieval for AI with Chroma
4. `course4_script.txt`: Prompt Compression and Query Optimization

### Dependencies

Core dependencies (Python 3.13+):
- chromadb==1.0.15
- anthropic==0.58.2
- sentence-transformers==5.0.0
- fastapi==0.116.1
- uvicorn==0.35.0