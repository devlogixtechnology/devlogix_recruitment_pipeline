# Open-Source LLM Evaluation Engine

## Overview

This project implements the AI evaluation layer for the DevLogix recruitment pipeline.

The system reads a candidate CV in JSON format and evaluates it against a DevLogix Python Developer Job Description using the local Llama 3.2 model through Ollama.

The evaluator generates a score from 1–10 and an exactly 2-sentence summary while validating the output to reduce unsupported or hallucinated claims.

---

## Features

- Local Llama 3.2 inference using Ollama
- JSON CV evaluation against a Job Description
- 1–10 candidate scoring
- Exactly 2-sentence summary
- Strict JSON output validation
- CV grounding and unsupported-claim detection
- Automatic retry on validation failure
- Prompt-based evaluation criteria
- No external API key required
- Strong, medium, and weak candidate testing

---

## System Workflow

```text
Candidate CV (JSON)
          |
          v
DevLogix Job Description
          |
          v
     Prompt Builder
          |
          v
   Ollama / Llama 3.2
          |
          v
    JSON Evaluation
          |
          v
       Validator
      /         \
   Valid       Invalid
     |            |
     v            v
 Final Output    Retry
                   |
                   v
              Re-evaluation