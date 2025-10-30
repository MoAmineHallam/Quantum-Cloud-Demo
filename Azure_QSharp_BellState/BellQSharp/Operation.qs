namespace BellQSharpFixed {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation BellState() : Result {
        using (qubits = Qubit[2]) {
            H(qubits[0]);      // Apply Hadamard to first qubit
            CNOT(qubits[0], qubits[1]); // Entangle qubits

            // Measure both qubits
            let res0 = M(qubits[0]);
            let res1 = M(qubits[1]);

            // Reset qubits before releasing
            if (res0 == One) { X(qubits[0]); }
            if (res1 == One) { X(qubits[1]); }

            // Return measurement as combined string
            if (res0 == res1) {
                return Zero; // 00 or 11
            } else {
                return One;  // 01 or 10 (should be rare ideally)
            }
        }
    }
}
