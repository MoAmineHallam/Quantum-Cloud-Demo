# Azure Quantum Bell-State Demonstration (Q#)

This repository contains the **Q# implementation** of a two-qubit Bell-state experiment executed using **Azure Quantum simulators**.  
It complements the IBM Quantum experiment, providing a hands-on comparison between **Q# (Azure)** and **Python/Qiskit (IBM Quantum)** for cloud-based quantum computing.

---

## Files Included

| File | Description |
|------|--------------|
| `[BellQSharp]/(BellQSharp/)` | Q# project folder containing the Bell-state operation and host C# driver. |

---
## Files
- Program.cs – C# host that runs the Q# operation.
- Operations.qs – Q# operation that prepares and measures the Bell state.
- BellQSharp.csproj – Project file with Q# SDK and dependencies.

## Setup Instructions

Follow these steps to replicate the Azure Q# experiment.

### 1. Prerequisites

.NET SDK: The project was originally created with .NET 6.0.
If you have the latest .NET (e.g., .NET 8.0/9.0), you may encounter build errors.
Solution: Install the .NET 6.0 SDK from https://dotnet.microsoft.com/en-us/download/dotnet/6.0

Q# Development Kit: Installed via NuGet (packages are already in the .csproj).
> dotnet tool install -g Microsoft.Quantum.IQSharp
> dotnet new --install Microsoft.Quantum.ProjectTemplates

### 2. Clone or Download the Project

Clone this repository and navigate to the Q# project folder:

> git clone https://github.com/MoAmineHallam/Quantum-Cloud-Demo.git
> cd Quantum-Cloud-Demo/BellQSharp

### 3. Run the Q# Bell-State Simulation

You can run the project using the Quantum simulator (local):

> dotnet run

Expected output (ideal Bell-state counts):

=== Simulator (QuantumSimulator) ===
Counts: {"00": 2048, "11": 2048}
Probabilities: {"00": 0.5, "01": 0.0, "10": 0.0, "11": 0.5}

!! No actual Azure subscription is required for local simulation.
If you have an Azure Quantum workspace, you can target real hardware later using the Q# Azure target.

### Notes

- The Q# project demonstrates the same quantum concept as the IBM Qiskit experiment: creating and measuring a two-qubit Bell state.

- Using Q# allows exploration of Microsoft’s quantum ecosystem and integrates naturally with C#/.NET.

- The output can be screenshotted and included in reports to illustrate expected results.


