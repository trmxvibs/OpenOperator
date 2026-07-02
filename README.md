<div align="center">

# OpenOperator

**An autonomous, open-source vision-guided desktop automation framework that combines LLM reasoning, OCR, GUI interaction, and intelligent task execution.**

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey.svg)]()
[![Tests](https://img.shields.io/badge/Tests-95%2F95%20Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Development Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)]()

</div>

---

## 📖 About OpenOperator

OpenOperator is a powerful, locally-run desktop automation framework. It bridges the gap between natural language intent and physical desktop execution. By utilizing LLM-based reasoning (supporting multi-lingual prompts like English and Hinglish), OCR for screen perception, persistent action memory, and an autonomous goal-oriented loop, OpenOperator can launch apps, locate UI elements, focus windows, and interact with your desktop natively.

## ✨ Features

OpenOperator is built on a modular architecture, breaking down autonomous execution into discrete, robust layers.

| Layer | Capabilities |
| :--- | :--- |
| **👁️ Perception** | Screenshot Engine, OCR Engine, Vision Text Detection, Fuzzy OCR Matching, Vision Retry Strategy |
| **🕹️ Action** | Cross-Platform Window Controllers (Win/Mac/Linux Factory), Mouse & Keyboard Controllers |
| **🧠 Planning** | Dual-Engine Intent Parser (LLM + Regex Fallback), Vision Plan Compiler (Safety & Optimization) |
| **⚙️ Execution** | Task Runner (Dynamic Delays & Smart Fallback), Vision Task Executor |
| **🔌 Plugins** | Pluggable Architecture, AppLauncher Plugin (Autonomous System App Startup) |
| **💾 Memory** | ActionMemoryManager, Persistent MemoryStorage (Auto-Save/Load) |
| **✅ Verification**| Verification Engine, Screen State Validation, OCR Verification |

## 🏗️ Architecture

OpenOperator enforces a strict separation of concerns between "seeing," "thinking," and "doing."

```text
OpenOperator Framework
│
├── Interface Layer
│   ├── Autonomous Agent Demo (End-to-End Showcase)
│   └── Interactive Shell (REPL)
│
├── Agent Layer (The Brain)
│   ├── Dual-Engine Intent Parser (LLM & Regex)
│   ├── Vision Plan Compiler (Safety Checks)
│   ├── Task Runner (Execution Router & Smart Launch)
│   └── Action Memory Manager (Session Context)
│
├── Action Layer (The Hands)
│   ├── Cross-Platform Factory (OS Controllers)
│   ├── Keyboard Controller (Type)
│   └── Mouse Controller (Click)
│
├── Perception Layer (The Eyes)
│   ├── Screenshot Engine (Capture)
│   └── OCR Engine (Extract Text)
│
└── Plugin & Storage Layer
    ├── Plugin Manager (AppLauncher, etc.)
    └── Memory Storage (Persistent JSON State)
```
# 🚀 Installation
Prerequisites:

Python 3.13+

Windows (Fully Supported) / macOS & Linux (Stubs Available)

1. Clone the repository:
```sh
git clone [https://github.com/trmxvibs/OpenOperator](https://github.com/trmxvibs/OpenOperator)
cd OpenOperator
```
2. Create and activate a virtual environment:

```Bash
python -m venv venv
.\venv\Scripts\activate
```
3. Install dependencies:
```Bash
pip install -e .
```
4. Setup Local LLM (Required for Advanced NLP & Hinglish):
OpenOperator supports local LLMs natively without API keys for maximum privacy.
Install Ollama
Pull the default model:

```Bash
ollama pull llama3
```
# 💡 Usage
End-to-End Autonomous Agent Demo
Run the ultimate showcase script that ties the Brain, Eyes, and Hands together. It supports English, Hindi, and Hinglish!

```Bash
python examples/autonomous_agent_demo.py
```
Example Commands:

`open Notepad and type hello world`

`notepad khol do aur hello type karo`
(Note: If the application is closed, the Agent will automatically use its Plugin system to launch it!)

Persistent Interactive Shell
Start the REPL to chain natural language commands continuously, leveraging persistent memory to infer context.

```Bash
python src/openoperator/cli.py shell
```
# 🧪 Testing
OpenOperator maintains a strict Test-Driven Development (TDD) standard. The suite guarantees the stability of the core engines, cross-platform architecture, LLM fallbacks, and the agent loop.

To run the test suite locally:

```Bash
pytest tests/
```
# 🗺️ Roadmap
OpenOperator is actively under development.

[x] Advanced Vision Retry Strategies: Implemented self-healing fallback loops if a target is not found.

[x] LLM Integration Layer: Transitioned from Regex-based NLP parsing to a dual-engine local LLM intent parser.

[x] Cross-Platform Support: Implemented Factory architecture with full Windows support and open stubs for macOS and Linux.

[x] Vision Plan Compiler: Added context safety, validation, and redundancy optimization.

[x] Plugin System: Built dynamic plugin manager (added AppLauncher).

[ ] Core Audit & Hardening: Refactoring and security audit (Issues #61, #63, #65).

[ ] Dynamic UI Parsing: Extracting structured JSON UI trees from raw OCR data.

# 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated!
(Specifically looking for contributors to help fill out the macOS Quartz and Linux X11/Wayland Window Controller stubs!)

# Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request (Ensure all pytest checks pass!)

# 📄 License
See LICENSE for more information.





















