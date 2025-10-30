#🧠 IBM Quantum Cloud Demonstration

This repository contains the Python experiment used in our Quantum Computing and Cloud Services report.
It demonstrates how to execute a Bell-state circuit on both:

a local simulator (Aer), and

a real IBM Quantum hardware backend (with and without error mitigation).

The results include counts, probabilities, and a comparison plot between ideal and hardware executions.

🧩 Files Included
File	Description
QC_ibm_demo.py	Main Python script for running the Bell state experiment using IBM Quantum and Aer simulators.
⚙️ Setup Instructions

Follow these steps to replicate the experiment exactly as done in the report.

1. Install Python and Dependencies

Make sure you have Python 3.9+ installed.

Then open a terminal and run:

pip install qiskit qiskit-aer qiskit-ibm-runtime matplotlib

2. Create an IBM Quantum Account

Go to https://quantum.ibm.com

Sign up (it’s free).

Once logged in, click on your profile icon (top right) → Account.

Copy your API Token.
It will look like this:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

3. Save Your IBM Quantum API Key Locally

You can save your key in one of two ways:

Option 1 — Use Qiskit built-in command

Run this command in your terminal:

qiskit-ibm-runtime login --token YOUR_API_KEY

Option 2 — Set environment variable manually

If the above doesn’t work, you can manually set it:

set QISKIT_IBM_TOKEN=YOUR_API_KEY        # Windows
export QISKIT_IBM_TOKEN=YOUR_API_KEY     # macOS/Linux


Once you log in, your credentials are saved locally so you won’t have to log in again.

4. Run the Experiment

Run the script from the command line:

python QC_ibm_demo.py


This will:

Build and simulate the Bell-state circuit

Select an available IBM Quantum backend

Run the circuit on real hardware

Display results for:

Simulator (ideal)

Hardware (no mitigation)

Hardware (+ mitigation)

Generate a comparison plot

🧾 Expected Output (Example)
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

📊 Output Plot Example

A bar chart will be displayed comparing:

Simulator (ideal)

Hardware (without mitigation)

Hardware (with mitigation)

This visualization clearly shows how mitigation improves the results to approach the ideal Bell-state probabilities.

🧠 Notes

If you don’t have an IBM Quantum API key, only the simulator (Aer) part will work.

Hardware access may queue depending on IBM Quantum’s public device load.

If you’re using a university or research account, you can also run on premium devices with shorter queue times.
