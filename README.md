
<div align="center">

# OpenOperator

**An open-source vision-guided desktop automation framework that combines OCR, GUI interaction, natural language planning, and task execution.**

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()
[![Tests](https://img.shields.io/badge/Tests-47%2F47%20Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Development Status](https://img.shields.io/badge/Status-Active%20Development-orange.svg)]()

</div>

---


## 📖 About OpenOperator

OpenOperator is a powerful, locally-run desktop automation framework designed for Windows. It bridges the gap between natural language intent and physical desktop execution. By utilizing OCR for screen perception and intelligent plan compilation, OpenOperator can locate UI elements, focus windows, and interact with your desktop natively—all driven by human-readable commands.

## ✨ Features

OpenOperator is built on a modular architecture, breaking down autonomous execution into discrete, robust layers.

| Layer | Capabilities |
| :--- | :--- |
| **👁️ Perception** | Screenshot Engine, OCR Engine, Vision Text Detection, Fuzzy OCR Matching, Vision Guided Click Target Detection |
| **🕹️ Action** | Mouse Controller, Keyboard Controller, Window Controller, Window Focus Automation |
| **🧠 Planning** | Task Planner, Intent Parser, Plan Compiler, Intelligent Planner, Natural Language Planning |
| **⚙️ Execution** | Vision Actor, Vision Task Executor, Task Runner, Autonomous Task Execution |
| **✅ Verification**| Verification Engine, Screen State Validation, OCR Verification |
| **💻 Interface** | CLI Interface, Interactive Shell, Natural Language Commands |

## 🚀 Installation

**Prerequisites:**
* Windows Operating System
* Python 3.13+

1. Clone the repository:
   ```bash
   git clone https://github.com/trmxvibs/OpenOperator
   cd OpenOperator

```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\activate

```


3. Install the package and dependencies:
```bash
pip install -e .

```



## 💡 Usage

OpenOperator provides a persistent Interactive Shell (REPL) that allows you to chain natural language commands continuously.

### Starting the Interactive Shell

```bash
python src/openoperator/cli.py shell

```

### Example Commands

Once inside the interactive shell, you can issue direct, natural language commands:

**Step-by-step Execution:**

```text
OpenOperator > switch to Notepad
OpenOperator > click File
OpenOperator > type Hello World
OpenOperator > verify Hello

```

**Compound Natural Language Planning:**

```text
OpenOperator > open notepad and type hello world
OpenOperator > switch to chrome and click search and type OpenOperator
OpenOperator > open notepad and click file and verify file

```

## 🏗️ Architecture & Major Components

OpenOperator is structured to enforce separation of concerns between "seeing," "thinking," and "doing."

* **`ScreenshotEngine`**: Captures the current desktop state as PNG bytes.
* **`OCREngine`**: Extracts raw text from screenshots.
* **`VisionActor`**: Locates specific text coordinates on screen and executes precise mouse interactions.
* **`WindowController`**: Interfaces with the OS to find, focus, and manage desktop windows.
* **`VisionIntentParser`**: Analyzes natural language instructions and translates them into structured action intents.
* **`VisionPlanCompiler`**: Validates parsed intents and compiles them into a strictly typed execution graph.
* **`IntelligentPlanner`**: A higher-level abstraction combining both the Intent Parser and Plan Compiler.
* **`TaskRunner`**: Iterates through compiled plans and routes actions to specific hardware/OS controllers.
* **`VisionTaskExecutor`**: Orchestrates the end-to-end flow: Focus Window → Click Target → Type Text → Verify Result.
* **`InteractiveShell`**: The user-facing REPL interface for seamless natural language automation.

### Directory Structure

```text
OpenOperator/
├── docs/                 # Documentation and architecture designs
├── examples/             # Standalone demo scripts for specific components
├── src/
│   └── openoperator/
│       ├── action/       # Keyboard, Mouse, and Window controllers
│       ├── agent/        # Planners, Parsers, Compilers, and Task Runners
│       ├── core/         # Verification and Action Memory
│       ├── perception/   # OCR, Locators, and Screenshot engines
│       ├── cli.py        # Main CLI entry point
│       └── shell.py      # Interactive REPL shell
└── tests/                # Comprehensive unit testing suite

```

## 🧪 Testing

OpenOperator maintains a strict testing standard. Currently, **47/47 unit tests are passing**, ensuring the stability of the core engines, planners, controllers, and the interactive shell.

To run the test suite locally:

```bash
pytest tests/

```

## 🗺️ Roadmap

OpenOperator is actively under development. We are currently tracking the following major milestones:

* [ ] **Issue #28:** Action Memory Integration
* [ ] **Issue #29:** Context Aware Follow-up Commands
* [ ] **Issue #30:** Vision Retry Strategy
* [ ] **Issue #31:** Multi-Step Autonomous Task Execution
* [ ] **Issue #32:** Documentation and Examples Expansion

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

*Please ensure all tests pass (`pytest`) before submitting a pull request.*

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

