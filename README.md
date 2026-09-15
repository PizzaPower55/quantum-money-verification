# Quantum Money Verification & Multi-Verifier Analysis

[![Open In Colab](https://img.shields.io/badge/Open_In-Colab-orange.svg?logo=googlecolab)](https://colab.research.google.com/drive/1Fl_kGnm7378BJAjwvB2I8_Ya370VGmpv)

A quantum information theory project analyzing verification strategies, state collapse dynamics, and multi-verifier security bounds for noise-tolerant quantum money systems.

---

## Overview & Key Insights

* **Optimal Measurement Strategy:** Analyzes token verification across classical/quantum verifiers using intermediate basis measurements (e.g., Breidbart basis on the Bloch sphere).
* **Fidelity Bounds:** Demonstrates the $85.35\%$ per-verifier fidelity limit for single-qubit measurement strategies and models state degradation upon measurement.
* **Multi-Verifier Security:** Simulates multi-round/multi-verifier scenarios, verifying that passing $n$ independent verifiers without central authority knowledge decays exponentially according to security limits (bounded by $(3/4)^n$).

---

## Simulation & Architecture

The accompanying Python/Qiskit notebooks simulate:
1. **Quantum Token State Preparation:** Encodings using random conjugate bases.
2. **Sequential Measurement Attacks:** Impact of eavesdropping/cloning on token fidelity.
3. **Multi-Verifier Verification Matrix:** Passing probabilities across multiple verification nodes under noise.

---

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/PizzaPower55/quantum-money-verification.git
   cd quantum-money-verification
