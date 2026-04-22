# Gemini Project Insights - FIRE Calculator SG Edition

This file serves as a persistent knowledge base for the Gemini CLI agent. It contains architectural notes, project-specific conventions, and a record of significant technical evolutions to ensure consistency and efficiency in future interactions.

## 🚀 Project Overview
A professional Streamlit-based financial independence calculator tailored for the Singapore context (CPF, HDB, local tax).

## 🛠 Technical Stack
- **Language:** Python 3.10+
- **Environment Management:** `uv` (standardized on `pyproject.toml` and `uv.lock`)
- **UI Framework:** Streamlit
- **Linting/Formatting:** Ruff (Line length: 88, configured in `pyproject.toml`)
- **Testing:** Pytest with Coverage (High logic coverage mandate)
- **Build System:** PyInstaller (via `build.py`)

## 📋 Engineering Standards
- **Docstrings:** 100% Google-style docstring coverage for all modules and functions.
- **Testing:** 100% logic coverage for `src/engine.py` (core simulation). High coverage for utilities and defaults.
- **Line Length:** Strictly follow the 88-character limit.
- **Optimal Withdrawal:** Logic implemented in `engine.py` ensures lowest-yield accounts are drained first post-55.

## 🔄 CI/CD Workflow
The project uses a sophisticated GitHub Actions pipeline (`.github/workflows/ci.yml`):
1. **Multi-Version Testing:** Validates across Python 3.10 through 3.15-dev.
2. **Automated Documentation:** Updates the `README.md` file tree and version badges using `tools/update_readme.py`.
3. **Linting & Formatting:** Automatically fixes/formats code using Ruff.
4. **Build Verification:** Ensures `build.py` successfully packages the application.

## 📝 Recent Learnings & Evolution
- **[2026-04-22] UV Migration:** Transitioned from `requirements.txt` to `uv`.
- **[2026-04-22] CI Porting:** Ported high-standard CI from `Group-Balancer`.
- **[2026-04-22] Engineering Push:** 
    - Achieved 100% logic coverage for the simulation engine.
    - Standardized all docstrings to Google style.
    - Created comprehensive `README.md` with feature deep-dives.
    - Fixed floating-point comparison issues in tests using `pytest.approx`.
- **[2026-04-22] PowerShell Optimization:** Defaulting to Windows PowerShell; ensured command syntax (e.g., `;` instead of `&&`) is compatible to minimize reattempts and save tokens.

## ⚠️ Important Notes
- **RA Logic:** At age 55, the engine must simulate the RA transfer (SA first, then OA) before any withdrawals.
- **Car/House Logic:** Ensure loans are subtracted from the correct asset classes (OA for house, Cash for car).
- **Inflows:** Monthly top-ups must stop exactly at the `retire_age`.

## 🔄 Post-Change Workflow
After every significant change, the following workflow MUST be executed by the main orchestrator to maintain elite engineering standards. The order is designed to minimize redundant work (e.g., testing or documenting dead code).

1. **Adversarial Vetting**: Hunt for logical flaws, security risks, and edge cases.
2. **Architecture Check**: Verify no unintended architectural shifts or SOLID principle violations.
3. **Dead Code Elimination**: Identify and remove unused imports, variables, and unreachable logic. Always inform the user before removing.
4. **Testing & Coverage**: Run tests, fix failing tests, and ensure 100% logic coverage for core modules (especially `src/engine.py`).
5. **Compliance & Linting**: Enforce 100% Google-style docstring coverage and complete Ruff compliance (check, format, and autofix).
6. **Documentation Update**: Update `README.md`, `GEMINI.md`, and any other high-level documentation to reflect the latest state.
