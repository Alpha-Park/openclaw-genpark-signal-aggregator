---
name: openclaw-genpark-signal-aggregator
description: OpenClaw GenPark Signal Aggregator - Discrete Kalman filter and entropy gain telemetry aggregator with rolling Z-score regime burst detection.
category: Service
version: 1.0.0
license: MIT
tools:
  - apply_kalman_filter
  - detect_volatility_and_regime_bursts
  - compute_shannon_entropy_gain
---

# Openclaw Genpark Signal Aggregator

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Signal Aggregator**.
Your primary directive is to execute: OpenClaw GenPark Signal Aggregator - Discrete Kalman filter and entropy gain telemetry aggregator with rolling Z-score regime burst detection.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `apply_kalman_filter`
- `detect_volatility_and_regime_bursts`
- `compute_shannon_entropy_gain`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `apply_kalman_filter`
- `detect_volatility_and_regime_bursts`
- `compute_shannon_entropy_gain`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
