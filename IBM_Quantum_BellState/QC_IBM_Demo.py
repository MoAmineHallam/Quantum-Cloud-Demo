# QC_ibm_demo.py
# ------------------------------------------------------------
# IBM Quantum cloud demo (up-to-date, Oct 2025)
# - Simulator (ideal) with Aer
# - Hardware (no mitigation)
# - Hardware (+ mitigation)
# Produces counts, probabilities, and a comparison plot.
# ------------------------------------------------------------

import math
import warnings
from collections import Counter

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit_aer.primitives import Sampler as AerSampler

import matplotlib.pyplot as plt


# ---------- Helpers ----------

def make_bell_circuit():
    """Two-qubit Bell state circuit with a single classical register."""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def primitive_counts(result, which=0):
    """
    Extract a dict of bitstring->shots from a Sampler(V2) PrimitiveResult,
    robust to minor API differences across recent versions.
    """
    # Newer helper (if present)
    if hasattr(result, "get_counts"):
        try:
            return dict(result.get_counts(which))
        except Exception:
            pass

    # V2 structure: result[which].data is a DataBin with registers -> BitArray
    pub = result[which]          # SamplerPubResult
    data_bin = pub.data          # DataBin
    # Get first classical register (e.g., "c")
    reg_names = list(getattr(data_bin, "keys", lambda: [])())
    if not reg_names:
        # Some versions let you access attributes directly without keys()
        # Fall back: try common default "c"
        if hasattr(data_bin, "c"):
            bitarray = data_bin.c
        else:
            raise RuntimeError("No classical registers found in the Sampler result.")
    else:
        bitarray = getattr(data_bin, reg_names[0])

    # BitArray exposes get_counts()
    if hasattr(bitarray, "get_counts"):
        return dict(bitarray.get_counts())

    # If all else fails, last-resort: try 'meas' key
    if hasattr(data_bin, "meas") and hasattr(data_bin.meas, "get_counts"):
        return dict(data_bin.meas.get_counts())

    raise RuntimeError("Could not extract counts from Sampler PrimitiveResult.")


def normalize_counts(counts):
    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}


def ensure_all_bitstrings(prob_map, nbits=2):
    """Ensure we have entries for 00..11 in consistent order."""
    keys = [format(i, f"0{nbits}b") for i in range(2**nbits)]
    return {k: float(prob_map.get(k, 0.0)) for k in keys}


def quasi_to_counts(quasi_dist, shots=4096, nbits=2):
    """
    Convert a QuasiDistribution-like mapping to integer counts for comparison.
    Assumes keys are bitstrings like '00', '11' or integers; rounds to nearest.
    """
    counts = Counter()
    for k, p in dict(quasi_dist).items():
        bit = format(k, f"0{nbits}b") if isinstance(k, int) else str(k)
        counts[bit] += int(round(p * shots))
    # Adjust for rounding drift
    drift = shots - sum(counts.values())
    if drift != 0:
        # Nudge the max-probability key to make totals match exactly
        if counts:
            max_k = max(counts, key=counts.get)
            counts[max_k] += drift
    return dict(counts)


def plot_comparison(probs_ideal, probs_hw_off, probs_hw_on, title_suffix=""):
    labels = ["00", "01", "10", "11"]
    ideal_vals = [probs_ideal.get(k, 0.0) for k in labels]
    off_vals   = [probs_hw_off.get(k, 0.0) for k in labels]
    on_vals    = [probs_hw_on.get(k, 0.0) for k in labels]

    x = range(len(labels))
    width = 0.25

    plt.figure()
    plt.bar([i - width for i in x], ideal_vals, width=width, label="Simulator (ideal)")
    plt.bar(x, off_vals, width=width, label="Hardware (off)")
    plt.bar([i + width for i in x], on_vals, width=width, label="Hardware (+mitig)")

    plt.xticks(list(x), labels)
    plt.ylim(0.0, 1.0)
    plt.ylabel("Probability")
    plt.title(f"Bell-State Results (IBM Cloud){(' — ' + title_suffix) if title_suffix else ''}")
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------- Main flow ----------

def main():
    warnings.filterwarnings("ignore")  # reduce noisy deprecation messages

    # 1) Build the circuit once
    qc = make_bell_circuit()

    # 2) Simulator (ideal) — zero queue time
    aer_sampler = AerSampler()
    shots = 4096
    sim_res = aer_sampler.run([qc], shots=shots).result()
    # Aer Sampler returns quasi distributions
    try:
        qd = sim_res.quasi_dists[0]
    except AttributeError:
        # Older shapes: fall back to first item
        qd = list(getattr(sim_res, "quasi_dists", [sim_res[0]]))[0]
    ideal_counts = quasi_to_counts(qd, shots=shots, nbits=2)
    ideal_probs = normalize_counts(ideal_counts)

    print("\n=== Simulator (ideal) ===")
    print("Counts:", ideal_counts)
    print("Probabilities:", ensure_all_bitstrings(ideal_probs))

    # 3) Hardware — connect via IBM Quantum Runtime
    service = QiskitRuntimeService()  # uses saved account or env var token
    backend = service.least_busy(min_num_qubits=2, simulator=False, operational=True)
    print("\n=== Selected hardware backend ===")
    print("Backend:", backend.name)
    # A few device facts for your report
    try:
        print("Qubits:", backend.num_qubits)  # may not exist on all client versions
    except Exception:
        pass
    try:
        ops_preview = list(backend.target.operations.keys())[:8]
        print("Basis operations (sample):", ops_preview, "…")
    except Exception:
        pass

    # ISA requirement: transpile to the backend Target
    tqc = transpile(qc, backend=backend, optimization_level=2)

    # 3A) Hardware (no mitigation)
    sampler_off = Sampler(mode=backend)
    res_off = sampler_off.run([tqc], shots=shots).result()
    hw_off_counts = primitive_counts(res_off, 0)
    hw_off_probs = normalize_counts(hw_off_counts)

    print("\n=== Hardware (no mitigation) ===")
    print("Counts:", hw_off_counts)
    print("Probabilities:", ensure_all_bitstrings(hw_off_probs))

    # 3B) Hardware (+ mitigation)
    sampler_on = Sampler(mode=backend)
    # Not all client versions expose the same options. Try gracefully:
    try:
        sampler_on.options.dynamical_decoupling.enable = True
    except Exception:
        pass
    try:
        sampler_on.options.resilience.measure_mitigation = True
    except Exception:
        pass

    res_on = sampler_on.run([tqc], shots=shots).result()
    hw_on_counts = primitive_counts(res_on, 0)
    hw_on_probs = normalize_counts(hw_on_counts)

    print("\n=== Hardware (+ mitigation) ===")
    print("Counts:", hw_on_counts)
    print("Probabilities:", ensure_all_bitstrings(hw_on_probs))

    # 4) Plot comparison (one figure for your report)
    plot_comparison(
        ensure_all_bitstrings(ideal_probs),
        ensure_all_bitstrings(hw_off_probs),
        ensure_all_bitstrings(hw_on_probs),
        title_suffix=backend.name,
    )


if __name__ == "__main__":
    main()
 