<div align="center">

# OpenOperator

**An open-source vision-guided desktop automation framework that combines OCR, GUI interaction, natural language planning, and autonomous task execution.**

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()
[![Tests](https://img.shields.io/badge/Tests-78%2F78%20Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Development Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)]()

</div>

---

## 📖 About OpenOperator

OpenOperator is a powerful, locally-run desktop automation framework designed for Windows. It bridges the gap between natural language intent and physical desktop execution. By utilizing OCR for screen perception, persistent action memory, and an autonomous goal-oriented loop, OpenOperator can locate UI elements, focus windows, and interact with your desktop natively—all driven by human-readable commands.

## ✨ Features

OpenOperator is built on a modular architecture, breaking down autonomous execution into discrete, robust layers.

| Layer | Capabilities |
| :--- | :--- |
| **👁️ Perception** | Screenshot Engine, OCR Engine, Vision Text Detection, Fuzzy OCR Matching, Vision Guided Click Target Detection |
| **🕹️ Action** | Mouse Controller, Keyboard Controller, Window Controller, Window Focus Automation |
| **🧠 Planning** | Task Planner, Intent Parser, Context-Aware Follow-Up Commands, Intelligent Planner, Natural Language Planning |
| **⚙️ Execution** | Vision Actor, Vision Task Executor, Task Runner, Goal-Oriented Agent Loop |
| **💾 Memory** | ActionMemoryManager, Persistent MemoryStorage (Auto-Save/Load) |
| **✅ Verification**| Verification Engine, Screen State Validation, OCR Verification |
| **💻 Interface** | CLI Interface, Interactive REPL Shell, Natural Language Commands |

## 🏗️ Architecture

OpenOperator enforces a strict separation of concerns between "seeing," "thinking," and "doing."

```python
OpenOperator Framework
│
├── Interface Layer
│   ├── Interactive Shell (REPL)
│   └── CLI (Demos & Execution)
│
├── Agent Layer (The Brain)
│   ├── Agent Loop (Goal-Oriented Execution)
│   ├── Vision Intent Parser (NLP & Context Inference)
│   ├── Task Runner (Execution Router)
│   └── Action Memory Manager (Session Context)
│
├── Action Layer (The Hands)
│   ├── Window Controller (Focus/Manage)
│   ├── Keyboard Controller (Type)
│   └── Mouse Controller / Vision Actor (Click)
│
├── Perception Layer (The Eyes)
│   ├── Screenshot Engine (Capture)
│   └── OCR Engine (Extract Text)
│
└── Storage Layer
    └── Memory Storage (Persistent JSON State)
```

# 🚀 Installation
Prerequisites:

Windows Operating System

Python 3.13+

## Clone the repository:

```Bash
git clone https://github.com/trmxvibs/OpenOperator
cd OpenOperator
```
## Create and activate a virtual environment (recommended):

```Bash
python -m venv venv
.\venv\Scripts\activate

```
## Install the package and dependencies:

```Bash
pip install -e .

```
# 💡 Usage
OpenOperator provides a persistent Interactive Shell (REPL) that allows you to chain natural language commands continuously, leveraging persistent memory to infer context.

Starting the Interactive Shell
```Bash
python src/openoperator/cli.py shell
```

## Integration Testing

OpenOperator includes real Windows integration tests.

Example:

pytest tests/integration/test_notepad_workflow.py -v

This test:

- Launches Notepad
- Focuses the window
- Types text
- Uses OCR verification
- Cleans up automatically

Requirements:

- Windows
- Tesseract OCR installed



## Example Commands
Once inside the interactive shell, you can issue direct, natural language commands. The agent remembers your last actions.

Context-Aware Follow-Up Execution:

```
OpenOperator > open Notepad
[*] Executing plan with 1 steps...
[+] Sequence completed successfully.

OpenOperator > type Hello World
[*] Executing plan with 2 steps... (Infers 'Notepad' from memory)
[+] Sequence completed successfully.

OpenOperator > click File
[*] Executing plan with 2 steps... (Infers 'Notepad' from memory)
[+] Sequence completed successfully.
Checking Persistent Memory:

```

## OpenOperator > memory
```
Current Session Memory
Last Window: Notepad
Last Click: File
Last Typed: Hello World
Goal-Oriented Multi-Step Planning:

OpenOperator > open notepad and type hello world
OpenOperator > switch to chrome and click search and type OpenOperator
```

# 🧪 Testing
OpenOperator maintains a strict Test-Driven Development (TDD) standard. Currently, 78/78 unit tests are passing, ensuring the stability of the core engines, memory systems, context-aware parsers, and the agent loop.

To run the test suite locally:

```Bash
pytest tests/
```

## 🗺️ Roadmap

- OpenOperator is actively under development. Upcoming milestones include:

[ ] Advanced Vision Retry Strategies: Implementing self-healing fallback loops if a target is not found.

[ ] LLM Integration Layer: Transitioning from Regex-based NLP parsing to a pluggable local/remote LLM intent parser.

[ ] Cross-Platform Support: Expanding Window and OS controllers to support macOS and Linux.

[ ] Dynamic UI Parsing: Extracting structured JSON UI trees from raw OCR data.

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

## Open a Pull Request

Please ensure all tests pass (pytest) before submitting a pull request.

## 📄 License
See LICENSE for more information.
