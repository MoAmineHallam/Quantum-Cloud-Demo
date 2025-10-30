# 🧠 IBM Quantum Cloud Demonstration

This repository contains the Python experiment used in our **Quantum Computing and Cloud Services** report.  
It demonstrates how to execute a **Bell-state circuit** on both:
- a **local simulator (Aer)**, and  
- a **real IBM Quantum hardware backend** (with and without error mitigation).  

The results include **counts, probabilities**, and a **comparison plot** between ideal and hardware executions.

---

## 🧩 Files Included

| File | Description |
|------|--------------|
| `QC_ibm_demo.py` | Main Python script for running the Bell state experiment using IBM Quantum and Aer simulators. |

---

## ⚙️ Setup Instructions

Follow these steps to replicate the experiment exactly as done in the report.

### 1. Install Python and Dependencies

Make sure you have **Python 3.9+** installed.  

Then open a terminal and run: pip install qiskit qiskit-aer qiskit-ibm-runtime matplotlib

### 2. Create an IBM Quantum Account

Go to https://quantum.ibm.com

  1. Sign up (it’s free).

  2. Once logged in, click on your profile icon (top right) → Account.

  3. Copy your API Token. It will look something like this: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

### 3. Save Your IBM Quantum API Key Locally

You can save your key in one of two ways:

Option 1 — Using Qiskit command:

qiskit-ibm-runtime login --token YOUR_API_KEY

Option 2 — Set it manually as an environment variable

# Windows
set QISKIT_IBM_TOKEN=YOUR_API_KEY

# macOS/Linux
export QISKIT_IBM_TOKEN=YOUR_API_KEY

Once you log in, your credentials are stored locally — no need to log in again.

### 4. Run the Experiment

Execute the script in your terminal:

python QC_ibm_demo.py

This will:

  Build and simulate the Bell-state circuit

  Select an available IBM Quantum hardware backend

  Run on real hardware (with and without mitigation)

  Generate and display a comparison plot

  Example Output

  === Simulator (ideal) ===
Counts: {'00': 2048, '11': 2048}
Probabilities: {'00': 0.5, '01': 0.0, '10': 0.0, '11': 0.5}

=== Selected hardware backend ===
Backend: ibm_osaka
Qubits: 127
Basis operations (sample): ['cx', 'id', 'rz', 'sx', 'x', 'measure'] …

=== Hardware (no mitigation) ===
Counts: {'00': 1950, '11': 2100, '01': 20, '10': 26}

=== Hardware (+ mitigation) ===
Counts: {'00': 2020, '11': 2050, '01': 10, '10': 16}

### Result Visualization

Below is an example of the generated comparison plot between simulator and hardware runs:

<img width="556" height="417" alt="image" src="https://github.com/user-attachments/assets/269f6fe1-a403-43d2-a602-4391130bea77" />

Notes

If you don’t have an IBM Quantum API key, only the simulator (Aer) part will execute.

Hardware jobs may queue depending on the current IBM Quantum public device load.

For academic users, university or research accounts can unlock premium devices with reduced queue times.
