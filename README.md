# 🔥 FIRE Calculator - Singapore Edition

![Python Version](https://img.shields.io/badge/python-3.10%20-%203.14-blue)
[![CI](https://github.com/taneu/FIRE-Calculator-SG-edition/actions/workflows/ci.yml/badge.svg)](https://github.com/taneu/FIRE-Calculator-SG-edition/actions/workflows/ci.yml)

A professional-grade Financial Independence, Retire Early (FIRE) calculator tailored specifically for the Singaporean context. This tool goes beyond simple 4% rules by modeling CPF complexities, local housing loans, and tiered retirement phases.

## 🌟 Key Features

### 1. The Three-Phase Liquidity Runway
Retirement in Singapore isn't a single block. This engine models three distinct phases:
- **Phase 1: The Bridge (Retirement to Age 55):** Living exclusively on private savings/investments.
- **Phase 2: The Unlock (Age 55 to Payout):** Accessing CPF Ordinary Account (OA) and Special Account (SA) surpluses above the Full Retirement Sum (FRS).
- **Phase 3: CPF Life (Age 65/70+):** Lifetime monthly payouts providing a solid floor for late-stage retirement.

### 2. Intelligent Withdrawal Engine
The simulation uses a **Mathematically Optimal Withdrawal Strategy**:
- Automatically identifies all available cash sources.
- Post-55, it sorts accounts by yield and drains the **lowest-yielding accounts first** to maximize long-term portfolio growth.

### 3. Comprehensive CPF Modeling
- **Automatic FRS/RA Transfer:** Simulates the creation of the Retirement Account at age 55 by draining SA then OA.
- **CPF Life Estimation:** Calculates expected payouts with deferral bonuses (7% increase per year deferred beyond 65).
- **Investment Growth:** Distinguishes between liquid CPF (base rates) and invested CPF (custom market rates).

### 4. Liability Management
- **Housing:** Models HDB/Bank loans with specific start ages and tenures. Automatically uses CPF OA for mortgage servicing before touching cash.
- **Cars:** Models car loans and downpayments.

### 5. Professional Data Management
- **State Persistence:** Import and export your financial profile as JSON.
- **Reset to Defaults:** Quickly revert to "Typical Singaporean" statistical averages.

---

## 🏗 Project Structure

<!-- PROJECT_TREE_START -->
```text
.
├── .gitattributes
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── GEMINI.md
├── LICENSE
├── README.md
├── build.py
├── main.py
├── pyproject.toml
├── requirements-dev.in
├── requirements-dev.txt
├── requirements.in
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── constants.py
│   ├── defaults.py
│   ├── engine.py
│   ├── models.py
│   ├── plotting.py
│   ├── sidebar.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_defaults.py
│   ├── test_engine.py
│   ├── test_integration.py
│   ├── test_models.py
│   ├── test_plotting.py
│   ├── test_sidebar.py
│   └── test_utils.py
├── tools/
│   └── update_readme.py
└── uv.lock
```
<!-- PROJECT_TREE_END -->

---

## 🛠 Installation & Setup

This project uses `uv` for ultra-fast, reliable dependency management.

1. **Install uv**:
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone & Sync**:
   ```bash
   git clone https://github.com/taneu/FIRE-Calculator-SG-edition.git
   cd FIRE-Calculator-SG-edition
   uv sync --all-extras
   ```

3. **Run the Dashboard**:
   ```bash
   uv run streamlit run main.py
   ```

---

## 🧪 Testing & Quality
We maintain high engineering standards:
- **100% Logic Coverage:** All core simulation branches in `engine.py` are covered by automated tests.
- **Linting:** Strictly enforced Ruff configuration (Google-style docstrings).
- **CI/CD:** Automated testing across Python 3.10 - 3.15.

Run tests locally:
```bash
uv run pytest --cov=src
```

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
