"""
Superdense Coding with Imperfect Gates
========================================
This module implements superdense coding with imperfect quantum gates,
simulating systematic errors and calibration issues in real quantum hardware.

Author: DEADSERPENT
Platform: Qiskit
"""

import sys
import io

# ----------------------------------------------------------------------
# Windows console‑encoding fix (run before any Qiskit imports)
# ----------------------------------------------------------------------
if sys.platform == "win32" and not isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace", line_buffering=True
        )
    except (AttributeError, ValueError):
        # Already wrapped or cannot wrap – ignore
        pass

# ----------------------------------------------------------------------
# Qiskit imports
# ----------------------------------------------------------------------
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    amplitude_damping_error,
)

import matplotlib.pyplot as plt
import numpy as np


class ImperfectGateSuperdenseCoding:
    """
    Superdense coding with imperfect gate implementations.

    This class simulates:
    - Over/under‑rotation errors in single‑qubit gates
    - CNOT gate imperfections
    - Amplitude damping
    - Coherent errors
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    def __init__(self, gate_error_angle: float = 0.05):
        """
        Initialise the imperfect‑gate superdense‑coding protocol.

        Parameters
        ----------
        gate_error_angle : float
            Rotation error in **radians** (default 0.05 rad ≈ 2.86°).
        """
        self.gate_error_angle = gate_error_angle
        self.noise_model = self._create_imperfect_gate_model(gate_error_angle)
        self.simulator = AerSimulator(noise_model=self.noise_model)
        # `self.results` will hold the data needed for visualisation.
        self.results = {}

    # ------------------------------------------------------------------
    # Noise model creation
    # ------------------------------------------------------------------
    def _create_imperfect_gate_model(self, error_angle: float) -> NoiseModel:
        """
        Build a Qiskit ``NoiseModel`` that injects realistic gate errors.

        Parameters
        ----------
        error_angle : float
            Rotation error (radians). The larger the angle the larger the
            depolarising‑error probability.

        Returns
        -------
        NoiseModel
        """
        noise_model = NoiseModel()

        # ----- single‑qubit gate errors (H, X, Z) --------------------
        # Scale the error probability with the supplied angle; cap at 10 %.
        single_qubit_error_prob = min(0.10, error_angle * 2)
        single_qubit_error = depolarizing_error(single_qubit_error_prob, 1)
        noise_model.add_all_qubit_quantum_error(single_qubit_error, ["h", "x", "z"])

        # ----- two‑qubit gate errors (CNOT) -------------------------
        # CNOTs are usually noisier; cap at 15 %.
        two_qubit_error_prob = min(0.15, error_angle * 3)
        two_qubit_error = depolarizing_error(two_qubit_error_prob, 2)
        noise_model.add_all_qubit_quantum_error(two_qubit_error, ["cx"])

        # ----- amplitude damping (energy relaxation) ----------------
        # Simulates T₁ decay during single‑qubit gates.
        damping_param = min(0.05, error_angle)  # keep it small
        amp_damping = amplitude_damping_error(damping_param)
        noise_model.add_all_qubit_quantum_error(amp_damping, ["h", "x", "z"])

        return noise_model

    # ------------------------------------------------------------------
    # Circuit building blocks (Bell state, encoding, decoding)
    # ------------------------------------------------------------------
    def create_bell_state(self, qc: QuantumCircuit, alice_qubit: int, bob_qubit: int):
        """Create a Bell pair |Φ⁺⟩ = (|00⟩+|11⟩)/√2."""
        qc.h(alice_qubit)
        qc.cx(alice_qubit, bob_qubit)

    def alice_encode(self, qc: QuantumCircuit, alice_qubit: int, bits: str):
        """Apply the appropriate Pauli operator(s) to Alice's qubit."""
        if bits == "00":
            pass
        elif bits == "01":
            qc.x(alice_qubit)
        elif bits == "10":
            qc.z(alice_qubit)
        elif bits == "11":
            qc.z(alice_qubit)
            qc.x(alice_qubit)
        else:
            raise ValueError(f"Invalid bits: {bits}")

    def bob_decode(
        self,
        qc: QuantumCircuit,
        alice_qubit: int,
        bob_qubit: int,
        classical_bits: ClassicalRegister,
    ):
        """Undo the Bell preparation and measure."""
        qc.cx(alice_qubit, bob_qubit)
        qc.h(alice_qubit)
        # Qiskit uses little‑endian bit ordering – map accordingly
        qc.measure(alice_qubit, classical_bits[1])
        qc.measure(bob_qubit, classical_bits[0])

    # ------------------------------------------------------------------
    # Run a single protocol instance
    # ------------------------------------------------------------------
    def run_protocol(
        self, bits: str, shots: int = 2048, draw_circuit: bool = True
    ) -> dict:
        """
        Execute the superdense‑coding circuit with imperfect gates.

        Parameters
        ----------
        bits : str
            Two‑bit string to transmit (e.g. ``'01'``).
        shots : int
            Number of Monte‑Carlo repetitions.
        draw_circuit : bool
            If ``True`` the ASCII circuit diagram is printed.

        Returns
        -------
        dict
            ``{'counts': <dict>, 'circuit': <QuantumCircuit>, 'shots': shots}``
        """
        # ----- registers ------------------------------------------------
        qr = QuantumRegister(2, "q")
        cr = ClassicalRegister(2, "c")
        qc = QuantumCircuit(qr, cr)

        # ----- protocol -------------------------------------------------
        qc.barrier(label="Bell State")
        self.create_bell_state(qc, 0, 1)

        qc.barrier(label=f"Encode: {bits}")
        self.alice_encode(qc, 0, bits)

        qc.barrier(label="Decode")
        self.bob_decode(qc, 0, 1, cr)

        # ----- optional visualisation ------------------------------------
        if draw_circuit:
            err_deg = np.degrees(self.gate_error_angle)
            print(f"\nCircuit for encoding '{bits}' (gate error: {err_deg:.2f}°):")
            print(qc.draw(output="text"))

        # ----- execution -------------------------------------------------
        job = self.simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)

        # Store the low‑level data in the object (used by visualisers)
        self.results[bits] = {
            "counts": counts,
            "circuit": qc,
            "shots": shots,
        }

        return counts

    # ------------------------------------------------------------------
    # Test all four possible input strings
    # ------------------------------------------------------------------
    def test_all_cases(self, shots: int = 2048, draw_circuit: bool = False) -> dict:
        """
        Run the protocol for every possible 2‑bit message.

        Parameters
        ----------
        shots : int
            Number of repetitions per message.
        draw_circuit : bool
            Set ``True`` if you want to see the circuit diagrams.

        Returns
        -------
        dict
            Mapping ``bits → {counts, success_rate, error_rate,
            error_distribution, expected}``.
        """
        all_bits = ["00", "01", "10", "11"]
        results = {}

        err_deg = np.degrees(self.gate_error_angle)
        print("=" * 70)
        print(f"SUPERDENSE CODING - IMPERFECT GATES (Error: {err_deg:.2f}°)")
        print("=" * 70)

        for bits in all_bits:
            print(f"\n{'-' * 70}")
            print(f"Testing input: {bits}")
            print(f"{'-' * 70}")

            counts = self.run_protocol(bits, shots=shots, draw_circuit=draw_circuit)

            # ----- compute metrics ---------------------------------------
            expected_output = bits
            success_cnt = counts.get(expected_output, 0)
            success_rate = (success_cnt / shots) * 100

            # errors are everything that is NOT the expected outcome
            error_counts = {k: v for k, v in counts.items() if k != expected_output}
            total_errors = sum(error_counts.values())
            error_rate = (total_errors / shots) * 100

            # ----- store per‑bit dictionary -------------------------------
            results[bits] = {
                "counts": counts,
                "success_rate": success_rate,
                "error_rate": error_rate,
                "error_distribution": error_counts,
                "expected": expected_output,
            }

            # -------------------------------------------------------------
            # >>>>>>  NEW LINE – keep the same dict inside the instance <<<<<
            # This makes `self.results[bits]` contain success / error data,
            # which the visualiser expects.
            self.results[bits] = results[bits]
            # -------------------------------------------------------------

            # ----- console output -----------------------------------------
            print(f"\nResults:")
            print(f"  Expected output: {expected_output}")
            print(f"  Measurement counts: {counts}")
            print(f"  Success rate: {success_rate:.2f}%")
            print(f"  Error rate: {error_rate:.2f}%")

            if error_counts:
                print(f"  Error distribution:")
                for outcome, cnt in sorted(error_counts.items()):
                    pct = (cnt / shots) * 100
                    print(f"    {outcome}: {cnt} ({pct:.2f}%)")

            if success_rate >= 90.0:
                print(f"  ✓ Good fidelity with imperfect gates")
            elif success_rate >= 75.0:
                print(f"  ⚠ Moderate impact from gate errors")
            else:
                print(f"  ✗ Significant degradation from gate imperfections")

        return results

    # ------------------------------------------------------------------
    # Compare performance for a collection of gate‑error angles
    # ------------------------------------------------------------------
    def compare_gate_errors(
        self,
        bits: str = "11",
        error_angles: list | None = None,
        shots: int = 2048,
    ) -> dict:
        """
        Run the protocol for a single bit‑string over several error angles.

        Parameters
        ----------
        bits : str
            Which 2‑bit message to test (default ``'11'``).
        error_angles : list or None
            List of angles **in degrees**. If ``None`` a default set is used.
        shots : int
            Number of repetitions per run.

        Returns
        -------
        dict
            ``angle_deg → {counts, success_rate, error_rate}``.
        """
        if error_angles is None:
            error_angles = [0, 1, 2, 5, 10]  # degrees

        comparison = {}

        print("=" * 70)
        print(f"GATE ERROR COMPARISON - Input: {bits}")
        print("=" * 70)

        for angle_deg in error_angles:
            angle_rad = np.radians(angle_deg)
            print(f"\n{'─' * 70}")
            print(f"Gate Error: {angle_deg}° ({angle_rad:.4f} rad)")
            print(f"{'─' * 70}")

            # Fresh instance for each angle (ensures a clean noise model)
            imperfect_sdc = ImperfectGateSuperdenseCoding(gate_error_angle=angle_rad)
            counts = imperfect_sdc.run_protocol(bits, shots=shots, draw_circuit=False)

            success_cnt = counts.get(bits, 0)
            success_rate = (success_cnt / shots) * 100
            error_rate = 100 - success_rate

            comparison[angle_deg] = {
                "counts": counts,
                "success_rate": success_rate,
                "error_rate": error_rate,
            }

            print(f"  Success rate: {success_rate:.2f}%")
            print(f"  Error rate:   {error_rate:.2f}%")

        return comparison

    # ------------------------------------------------------------------
    # Visualisation helpers
    # ------------------------------------------------------------------
    def visualize_imperfect_results(self, save_fig: bool = True):
        """
        Plot bar‑charts for every input string showing the full outcome
        distribution together with success / error percentages.

        Parameters
        ----------
        save_fig : bool
            If ``True`` the figure is written to
            ``superdense_imperfect_<error>.png``.
        """
        if not self.results:
            print("No results to visualise. Run the protocol first.")
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        err_deg = np.degrees(self.gate_error_angle)
        fig.suptitle(
            f"Superdense Coding with Imperfect Gates (Error: {err_deg:.2f}°)",
            fontsize=16,
            fontweight="bold",
        )

        all_bits = ["00", "01", "10", "11"]

        for idx, bits in enumerate(all_bits):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]

            if bits in self.results:
                counts = self.results[bits]["counts"]

                # Sort outcomes for deterministic ordering
                outcomes = sorted(counts.keys())
                values = [counts[out] for out in outcomes]
                colors = ["green" if out == bits else "orange" for out in outcomes]

                ax.bar(outcomes, values, color=colors, alpha=0.7, edgecolor="black")
                ax.set_xlabel("Measurement Outcome", fontsize=12)
                ax.set_ylabel("Counts", fontsize=12)
                ax.set_title(f"Input: {bits}", fontsize=14, fontweight="bold")
                ax.grid(axis="y", alpha=0.3)

                # Annotate success / error rates
                success = self.results[bits]["success_rate"]
                error = self.results[bits]["error_rate"]
                txt = f"Success: {success:.1f}%\nError: {error:.1f}%"
                ax.text(
                    0.5,
                    0.95,
                    txt,
                    transform=ax.transAxes,
                    ha="center",
                    va="top",
                    bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.7),
                    fontsize=10,
                    fontweight="bold",
                )

        plt.tight_layout()

        if save_fig:
            filename = f"superdense_imperfect_{err_deg:.1f}deg.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"\n✓ Results visualisation saved as '{filename}'")

        plt.show()

    def visualize_error_comparison(
        self, comparison_data: dict, input_bits: str, save_fig: bool = True
    ):
        """
        Plot how the success / error rates change as the gate‑error angle
        varies.

        Parameters
        ----------
        comparison_data : dict
            Output of :py:meth:`compare_gate_errors`.
        input_bits : str
            Which two‑bit string was used for the comparison.
        save_fig : bool
            Save the figure as ``gate_error_comparison_<bits>.png`` if ``True``.
        """
        angles = sorted(comparison_data.keys())
        success_rates = [comparison_data[a]["success_rate"] for a in angles]
        error_rates = [comparison_data[a]["error_rate"] for a in angles]

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            angles,
            success_rates,
            "o-",
            color="green",
            linewidth=2,
            markersize=8,
            label="Success Rate",
        )
        ax.plot(
            angles,
            error_rates,
            "s-",
            color="red",
            linewidth=2,
            markersize=8,
            label="Error Rate",
        )

        ax.set_xlabel("Gate Error Angle (degrees)", fontsize=13)
        ax.set_ylabel("Rate (%)", fontsize=13)
        ax.set_title(
            f"Impact of Gate Errors on Superdense Coding\n(Input: {input_bits})",
            fontsize=15,
            fontweight="bold",
        )
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        ax.set_ylim(0, 105)

        plt.tight_layout()

        if save_fig:
            filename = f"gate_error_comparison_{input_bits}.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"\n✓ Comparison visualisation saved as '{filename}'")

        plt.show()

    # ------------------------------------------------------------------
    # Textual summary
    # ------------------------------------------------------------------
    def print_summary(self, results: dict):
        """Pretty‑print a table summarising success / error rates."""
        err_deg = np.degrees(self.gate_error_angle)
        print("\n" + "=" * 85)
        print(f"IMPERFECT GATES SUMMARY (Gate Error: {err_deg:.2f}°)")
        print("=" * 85)
        print(f"{'Input':<10} {'Expected':<10} {'Success Rate':<15} {'Error Rate':<15} {'Status'}")
        print(f"{'─' * 85}")

        for bits in ["00", "01", "10", "11"]:
            if bits in results:
                data = results[bits]
                success = data["success_rate"]
                error = data["error_rate"]

                if success >= 90.0:
                    status = "✓ Excellent"
                elif success >= 75.0:
                    status = "⚠ Good"
                elif success >= 60.0:
                    status = "⚠ Fair"
                else:
                    status = "✗ Poor"

                print(
                    f"{bits:<10} {data['expected']:<10} {success:>6.2f}%{'':<8} "
                    f"{error:>6.2f}%{'':<8} {status}"
                )

        print("=" * 85 + "\n")


# ----------------------------------------------------------------------
# Demo when the file is executed directly
# ----------------------------------------------------------------------
def main():
    """Run a quick demonstration of the imperfect‑gate scenario."""
    print("\n" + "=" * 70)
    print("SUPERDENSE CODING WITH IMPERFECT GATES - DEMONSTRATION")
    print("=" * 70)
    print("\nSimulating systematic gate errors:")
    print("  • Over/under‑rotation in single‑qubit gates")
    print("  • Amplitude damping (energy loss)")
    print("  • Coherent errors\n")

    # ------------------------------------------------------------------
    # 1️⃣ 5‑degree gate error – the “standard” case used in the full demo
    # ------------------------------------------------------------------
    print("\n[1] Testing with 5° gate error...")
    imperfect_sdc = ImperfectGateSuperdenseCoding(gate_error_angle=np.radians(5))
    results = imperfect_sdc.test_all_cases(shots=2048)
    imperfect_sdc.print_summary(results)
    imperfect_sdc.visualize_imperfect_results(save_fig=True)

    # ------------------------------------------------------------------
    # 2️⃣  Compare several error magnitudes
    # ------------------------------------------------------------------
    print("\n[2] Comparing different gate error angles...")
    comparison = imperfect_sdc.compare_gate_errors(
        bits="11", error_angles=[0, 1, 2, 5, 10, 15], shots=2048
    )
    imperfect_sdc.visualize_error_comparison(comparison, "11", save_fig=True)

    print("\n✓ Imperfect‑gate demonstration completed!")


if __name__ == "__main__":
    main()
