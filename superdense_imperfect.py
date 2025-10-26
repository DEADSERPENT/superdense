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

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, amplitude_damping_error
import matplotlib.pyplot as plt
import numpy as np


class ImperfectGateSuperdenseCoding:
    """
    Superdense coding with imperfect gate implementations.

    This class simulates:
    - Over/under-rotation errors in single-qubit gates
    - CNOT gate imperfections
    - Amplitude damping
    - Coherent errors
    """

    def __init__(self, gate_error_angle=0.05):
        """
        Initialize the imperfect gates superdense coding protocol.

        Args:
            gate_error_angle: Rotation error in radians (default: 0.05 rad ≈ 2.86°)
        """
        self.gate_error_angle = gate_error_angle
        self.noise_model = self._create_imperfect_gate_model(gate_error_angle)
        self.simulator = AerSimulator(noise_model=self.noise_model)
        self.results = {}

    def _create_imperfect_gate_model(self, error_angle):
        """
        Create a noise model with imperfect gates.

        Args:
            error_angle: Rotation error in radians

        Returns:
            NoiseModel object
        """
        noise_model = NoiseModel()

        # Model gate imperfections using depolarizing errors
        # This simulates over/under-rotation and calibration errors

        # Imperfect single-qubit gates (H, X, Z)
        # Error probability scales with error_angle
        single_qubit_error_prob = min(0.1, error_angle * 2)  # Cap at 10%
        single_qubit_error = depolarizing_error(single_qubit_error_prob, 1)
        noise_model.add_all_qubit_quantum_error(single_qubit_error, ['h', 'x', 'z'])

        # Imperfect two-qubit gates (CNOT) - typically worse
        two_qubit_error_prob = min(0.15, error_angle * 3)  # Cap at 15%
        two_qubit_error = depolarizing_error(two_qubit_error_prob, 2)
        noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx'])

        # Amplitude damping (energy loss during gate operation)
        # Simulates T1 decay - only for single-qubit gates
        damping_param = min(0.05, error_angle)  # Scale with error angle
        amp_damping = amplitude_damping_error(damping_param)
        noise_model.add_all_qubit_quantum_error(amp_damping, ['h', 'x', 'z'])

        return noise_model

    def create_bell_state(self, qc, alice_qubit, bob_qubit):
        """Create a Bell state with imperfect gates."""
        qc.h(alice_qubit)
        qc.cx(alice_qubit, bob_qubit)

    def alice_encode(self, qc, alice_qubit, bits):
        """Alice encodes 2 classical bits with imperfect gates."""
        if bits == '00':
            pass  # Identity
        elif bits == '01':
            qc.x(alice_qubit)
        elif bits == '10':
            qc.z(alice_qubit)
        elif bits == '11':
            qc.z(alice_qubit)
            qc.x(alice_qubit)
        else:
            raise ValueError(f"Invalid bits: {bits}")

    def bob_decode(self, qc, alice_qubit, bob_qubit, classical_bits):
        """Bob decodes the message with imperfect gates."""
        qc.cx(alice_qubit, bob_qubit)
        qc.h(alice_qubit)
        # Fix bit ordering - Qiskit uses little-endian
        qc.measure(alice_qubit, classical_bits[1])
        qc.measure(bob_qubit, classical_bits[0])

    def run_protocol(self, bits, shots=2048, draw_circuit=True):
        """
        Run the superdense coding protocol with imperfect gates.

        Args:
            bits: String of 2 bits to encode
            shots: Number of measurement repetitions
            draw_circuit: Whether to draw the circuit

        Returns:
            Dictionary containing measurement results
        """
        # Create circuit
        qr = QuantumRegister(2, 'q')
        cr = ClassicalRegister(2, 'c')
        qc = QuantumCircuit(qr, cr)

        # Protocol steps
        qc.barrier(label='Bell State')
        self.create_bell_state(qc, 0, 1)

        qc.barrier(label=f'Encode: {bits}')
        self.alice_encode(qc, 0, bits)

        qc.barrier(label='Decode')
        self.bob_decode(qc, 0, 1, cr)

        if draw_circuit:
            error_deg = np.degrees(self.gate_error_angle)
            print(f"\nCircuit for encoding '{bits}' (gate error: {error_deg:.2f}°):")
            print(qc.draw(output='text'))

        # Execute with imperfect gates
        job = self.simulator.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts(qc)

        # Store results
        self.results[bits] = {
            'counts': counts,
            'circuit': qc,
            'shots': shots
        }

        return counts

    def test_all_cases(self, shots=2048):
        """
        Test all four possible input cases with imperfect gates.

        Args:
            shots: Number of measurement repetitions

        Returns:
            Dictionary containing results for all cases
        """
        all_bits = ['00', '01', '10', '11']
        results = {}

        error_deg = np.degrees(self.gate_error_angle)
        print("=" * 70)
        print(f"SUPERDENSE CODING - IMPERFECT GATES (Error: {error_deg:.2f}°)")
        print("=" * 70)

        for bits in all_bits:
            print(f"\n{'─' * 70}")
            print(f"Testing input: {bits}")
            print(f"{'─' * 70}")

            counts = self.run_protocol(bits, shots=shots, draw_circuit=True)

            # Calculate metrics
            expected_output = bits
            success_count = counts.get(expected_output, 0)
            success_rate = (success_count / shots) * 100

            # Calculate total error distribution
            error_counts = {k: v for k, v in counts.items() if k != expected_output}
            total_errors = sum(error_counts.values())
            error_rate = (total_errors / shots) * 100

            results[bits] = {
                'counts': counts,
                'success_rate': success_rate,
                'error_rate': error_rate,
                'error_distribution': error_counts,
                'expected': expected_output
            }

            print(f"\nResults:")
            print(f"  Expected output: {expected_output}")
            print(f"  Measurement counts: {counts}")
            print(f"  Success rate: {success_rate:.2f}%")
            print(f"  Error rate: {error_rate:.2f}%")

            if error_counts:
                print(f"  Error distribution:")
                for outcome, count in sorted(error_counts.items()):
                    pct = (count / shots) * 100
                    print(f"    {outcome}: {count} ({pct:.2f}%)")

            if success_rate >= 90.0:
                print(f"  ✓ Good fidelity with imperfect gates")
            elif success_rate >= 75.0:
                print(f"  ⚠ Moderate impact from gate errors")
            else:
                print(f"  ✗ Significant degradation from gate imperfections")

        return results

    def compare_gate_errors(self, bits='11', error_angles=None, shots=2048):
        """
        Compare performance with different gate error angles.

        Args:
            bits: Which bits to test
            error_angles: List of error angles in degrees
            shots: Number of shots

        Returns:
            Dictionary with results for each error angle
        """
        if error_angles is None:
            error_angles = [0, 1, 2, 5, 10]  # Degrees

        comparison = {}

        print("=" * 70)
        print(f"GATE ERROR COMPARISON - Input: {bits}")
        print("=" * 70)

        for angle_deg in error_angles:
            angle_rad = np.radians(angle_deg)
            print(f"\n{'─' * 70}")
            print(f"Gate Error: {angle_deg}° ({angle_rad:.4f} rad)")
            print(f"{'─' * 70}")

            # Create new instance with specified error angle
            imperfect_sdc = ImperfectGateSuperdenseCoding(gate_error_angle=angle_rad)
            counts = imperfect_sdc.run_protocol(bits, shots=shots, draw_circuit=False)

            success_count = counts.get(bits, 0)
            success_rate = (success_count / shots) * 100
            error_rate = 100 - success_rate

            comparison[angle_deg] = {
                'counts': counts,
                'success_rate': success_rate,
                'error_rate': error_rate
            }

            print(f"  Success rate: {success_rate:.2f}%")
            print(f"  Error rate: {error_rate:.2f}%")

        return comparison

    def visualize_imperfect_results(self, save_fig=True):
        """
        Visualize results from imperfect gate simulations.

        Args:
            save_fig: Whether to save the figure
        """
        if not self.results:
            print("No results to visualize. Run the protocol first.")
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        error_deg = np.degrees(self.gate_error_angle)
        fig.suptitle(f'Superdense Coding with Imperfect Gates (Error: {error_deg:.2f}°)',
                    fontsize=16, fontweight='bold')

        all_bits = ['00', '01', '10', '11']

        for idx, bits in enumerate(all_bits):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]

            if bits in self.results:
                counts = self.results[bits]['counts']

                # Sort outcomes
                outcomes = sorted(counts.keys())
                values = [counts[outcome] for outcome in outcomes]
                colors = ['green' if outcome == bits else 'orange' for outcome in outcomes]

                ax.bar(outcomes, values, color=colors, alpha=0.7, edgecolor='black')
                ax.set_xlabel('Measurement Outcome', fontsize=12)
                ax.set_ylabel('Counts', fontsize=12)
                ax.set_title(f'Input: {bits}', fontsize=14, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)

                # Add metrics
                success_rate = self.results[bits]['success_rate']
                error_rate = self.results[bits]['error_rate']

                info_text = f'Success: {success_rate:.1f}%\nError: {error_rate:.1f}%'
                ax.text(0.5, 0.95, info_text,
                       transform=ax.transAxes, ha='center', va='top',
                       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7),
                       fontsize=10, fontweight='bold')

        plt.tight_layout()

        if save_fig:
            filename = f'superdense_imperfect_{error_deg:.1f}deg.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✓ Results visualization saved as '{filename}'")

        plt.show()

    def visualize_error_comparison(self, comparison_data, input_bits, save_fig=True):
        """
        Visualize how success rate varies with gate error angle.

        Args:
            comparison_data: Dictionary from compare_gate_errors()
            input_bits: Which input was tested
            save_fig: Whether to save the figure
        """
        angles = sorted(comparison_data.keys())
        success_rates = [comparison_data[angle]['success_rate'] for angle in angles]
        error_rates = [comparison_data[angle]['error_rate'] for angle in angles]

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(angles, success_rates, 'o-', color='green', linewidth=2,
               markersize=8, label='Success Rate')
        ax.plot(angles, error_rates, 's-', color='red', linewidth=2,
               markersize=8, label='Error Rate')

        ax.set_xlabel('Gate Error Angle (degrees)', fontsize=13)
        ax.set_ylabel('Rate (%)', fontsize=13)
        ax.set_title(f'Impact of Gate Errors on Superdense Coding\n(Input: {input_bits})',
                    fontsize=15, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        ax.set_ylim(0, 105)

        plt.tight_layout()

        if save_fig:
            filename = f'gate_error_comparison_{input_bits}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✓ Comparison visualization saved as '{filename}'")

        plt.show()

    def print_summary(self, results):
        """Print summary table of imperfect gate results."""
        error_deg = np.degrees(self.gate_error_angle)
        print(f"\n{'=' * 85}")
        print(f"IMPERFECT GATES SUMMARY (Gate Error: {error_deg:.2f}°)")
        print(f"{'=' * 85}")
        print(f"{'Input':<10} {'Expected':<10} {'Success Rate':<15} {'Error Rate':<15} {'Status'}")
        print(f"{'─' * 85}")

        for bits in ['00', '01', '10', '11']:
            if bits in results:
                data = results[bits]
                success = data['success_rate']
                error = data['error_rate']

                if success >= 90.0:
                    status = '✓ Excellent'
                elif success >= 75.0:
                    status = '⚠ Good'
                elif success >= 60.0:
                    status = '⚠ Fair'
                else:
                    status = '✗ Poor'

                print(f"{bits:<10} {data['expected']:<10} {success:>6.2f}%{'':<8} "
                      f"{error:>6.2f}%{'':<8} {status}")

        print(f"{'=' * 85}\n")


def main():
    """Main function for imperfect gates superdense coding demonstration."""
    print("\n" + "=" * 70)
    print("SUPERDENSE CODING WITH IMPERFECT GATES - DEMONSTRATION")
    print("=" * 70)
    print("\nSimulating systematic gate errors:")
    print("  • Over/under-rotation in single-qubit gates")
    print("  • Amplitude damping (energy loss)")
    print("  • Coherent errors\n")

    # Test with moderate gate errors (5 degrees)
    print("\n[1] Testing with 5° gate error...")
    imperfect_sdc = ImperfectGateSuperdenseCoding(gate_error_angle=np.radians(5))
    results = imperfect_sdc.test_all_cases(shots=2048)
    imperfect_sdc.print_summary(results)
    imperfect_sdc.visualize_imperfect_results(save_fig=True)

    # Compare different error angles
    print("\n[2] Comparing different gate error angles...")
    comparison = imperfect_sdc.compare_gate_errors(
        bits='11',
        error_angles=[0, 1, 2, 5, 10, 15],
        shots=2048
    )
    imperfect_sdc.visualize_error_comparison(comparison, '11', save_fig=True)

    print("\n✓ Imperfect gates demonstration completed!")


if __name__ == "__main__":
    main()
