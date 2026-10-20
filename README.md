# Quantum Information & Multi-Verifier Security Simulator

An interactive Python application modeling **Wiesner's Quantum Money** protocol, state collapse dynamics, and multi-verifier security bounds under various adversarial attack strategies.

**Live App:** [View on Streamlit Cloud](https://quantum-money-verification.streamlit.app)

---

## Overview
Proposed by Stephen Wiesner in 1970, quantum money uses physical qubits rather than classical data, leveraging the **Quantum No-Cloning Theorem** to detect counterfeiting without relying on a central database. 

This project implements a full-stack simulation dashboard to analyze how quantum states degrade when subjected to sequential verification nodes under different threat models:
1. **Attacker 1 (Naive Random Guessing):** Blind guessing resulting in a 50% baseline efficiency.
2. **Attacker 2 (Standard Intermediate Measurement):** Projective measurements along standard computational axes (~74.3% limit).
3. **Attacker 3 (Optimal Breidbart Basis Attack):** Custom projection operators rotated by a 22.5° offset on the Bloch sphere to achieve the physical per-verifier ceiling of **85.35%** ($\frac{1 + 1/\sqrt{2}}{2}$).

---

## Repository Structure
* `app.py` — The interactive Streamlit frontend, featuring tabbed layouts, multi-node controls, and 3D Bloch sphere visualizations.
* `simulation.py` — The backend quantum simulation engine handling qubit preparation, secret bases, and probability decay calculations.
* `requirements.txt` — Project dependencies (`streamlit`, `numpy`, `matplotlib`).

---

## Running Locally

Clone the repository and run the application locally via Streamlit:

```bash
# Clone the repository
git clone [https://github.com/PizzaPower55/quantum-money-verification.git](https://github.com/PizzaPower55/quantum-money-verification.git)
cd quantum-money-verification

# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit app
streamlit run app.py
