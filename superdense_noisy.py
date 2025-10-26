"""
Superdense Coding with Noise
==============================
This module implements superdense coding in the presence of quantum noise,
simulating realistic quantum channels with decoherence and gate errors.

Author: DEADSERPENT
Platform: Qiskit
"""

import sys
import io

# Fix Windows console encoding (check if not already wrapped)
if sys.platform == 'win32' and not isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except (AttributeError, ValueError):
        pass  # Already wrapped or can't wrap

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, thermal_relaxation_error
import matplotlib.pyplot as plt
import numpy as np


class NoisySuperdenseCoding:
    """
    Superdense coding implementation with realistic noise models.

    This class simulates the protocol under various noise conditions including:
    - Depolarizing noise
    - Thermal relaxation (T1, T2)
    - Gate errors
    """

    def __init__(self, noise_level='low'):
        """
        Initialize the noisy superdense coding protocol.

        Args:
            noise_level: String indicating noise level ('low', 'medium', 'high')
        """
        self.noise_level = noise_level
        self.noise_model = self._create_noise_model(noise_level)
        self.simulator = AerSimulator(noise_model=self.noise_model)
        self.results = {}

    def _create_noise_model(self, level):
        """
        Create a noise model based on the specified level.

        Args:
            level: String indicating noise level ('low', 'medium', 'high')

        Returns:
            NoiseModel object
        """
        noise_model = NoiseModel()

        # Define noise parameters based on level
        noise_params = {
            'low': {
                'single_gate_error': 0.001,   # 0.1% error
                'two_gate_error': 0.01,       # 1% error
                'depolar_error': 0.002,       # 0.2% depolarizing
                't1': 50e-6,                   # 50 microseconds
                't2': 70e-6,                   # 70 microseconds
                'gate_time': 50e-9             # 50 nanoseconds
            },
            'medium': {
                'single_gate_error': 0.01,    # 1% error
                'two_gate_error': 0.05,       # 5% error
                'depolar_error': 0.02,        # 2% depolarizing
                't1': 30e-6,                   # 30 microseconds
                't2': 40e-6,                   # 40 microseconds
                'gate_time': 50e-9
            },
            'high': {
                'single_gate_error': 0.05,    # 5% error
                'two_gate_error': 0.15,       # 15% error
                'depolar_error': 0.05,        # 5% depolarizing
                't1': 10e-6,                   # 10 microseconds
                't2': 15e-6,                   # 15 microseconds
                'gate_time': 50e-9
            }
        }

        params = noise_params.get(level, noise_params['low'])

        # Single-qubit gate errors
        error_1q = depolarizing_error(params['single_gate_error'], 1)
        noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'z'])

        # Two-qubit gate errors
        error_2q = depolarizing_error(params['two_gate_error'], 2)
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

        # Thermal relaxation
        t1 = params['t1']
        t2 = params['t2']
        gate_time = params['gate_time']

        thermal_error = thermal_relaxation_error(t1, t2, gate_time)
        noise_model.add_all_qubit_quantum_error(thermal_error, ['h', 'x', 'z'])

        return noise_model

    def create_bell_state(self, qc, alice_qubit, bob_qubit):
        """Create a Bell state between Alice and Bob."""
        qc.h(alice_qubit)
        qc.cx(alice_qubit, bob_qubit)

    def alice_encode(self, qc, alice_qubit, bits):
        """Alice encodes 2 classical bits onto her qubit."""
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
        """Bob decodes the message."""
        qc.cx(alice_qubit, bob_qubit)
        qc.h(alice_qubit)
        # Fix bit ordering - Qiskit uses little-endian
        qc.measure(alice_qubit, classical_bits[1])
        qc.measure(bob_qubit, classical_bits[0])

    def run_protocol(self, bits, shots=2048, draw_circuit=True):
        """
        Run the superdense coding protocol with noise.

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
            print(f"\nCircuit for encoding '{bits}' (with {self.noise_level} noise):")
            print(qc.draw(output='text'))

        # Execute with noise
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

    def test_all_cases(self, shots=2048, draw_circuit=False):
        """
        Test all four possible input cases with noise.

        Args:
            shots: Number of measurement repetitions
            draw_circuit: Whether to draw circuit diagrams (default: False to avoid encoding issues)

        Returns:
            Dictionary containing results for all cases
        """
        all_bits = ['00', '01', '10', '11']
        results = {}

        print("=" * 70)
        print(f"SUPERDENSE CODING - NOISY SIMULATION ({self.noise_level.upper()} NOISE)")
        print("=" * 70)

        for bits in all_bits:
            print(f"\n{'-' * 70}")
            print(f"Testing input: {bits}")
            print(f"{'-' * 70}")

            counts = self.run_protocol(bits, shots=shots, draw_circuit=draw_circuit)

            # Calculate metrics
            expected_output = bits
            success_count = counts.get(expected_output, 0)
            success_rate = (success_count / shots) * 100

            # Calculate fidelity (simplified)
            fidelity = success_count / shots

            results[bits] = {
                'counts': counts,
                'success_rate': success_rate,
                'fidelity': fidelity,
                'expected': expected_output
            }

            print(f"\nResults:")
            print(f"  Expected output: {expected_output}")
            print(f"  Measurement counts: {counts}")
            print(f"  Success rate: {success_rate:.2f}%")
            print(f"  Fidelity: {fidelity:.4f}")

            if success_rate >= 95.0:
                print(f"  ✓ High fidelity despite noise")
            elif success_rate >= 80.0:
                print(f"  ⚠ Moderate noise impact")
            else:
                print(f"  ✗ Significant noise degradation")

        return results

    def compare_noise_levels(self, bits='00', shots=2048):
        """
        Compare performance across different noise levels.

        Args:
            bits: Which bits to test
            shots: Number of shots

        Returns:
            Dictionary with results for each noise level
        """
        noise_levels = ['low', 'medium', 'high']
        comparison = {}

        print("=" * 70)
        print(f"NOISE LEVEL COMPARISON - Input: {bits}")
        print("=" * 70)

        for level in noise_levels:
            print(f"\n{'─' * 70}")
            print(f"Noise Level: {level.upper()}")
            print(f"{'─' * 70}")

            # Create new instance with specified noise level
            noisy_sdc = NoisySuperdenseCoding(noise_level=level)
            counts = noisy_sdc.run_protocol(bits, shots=shots, draw_circuit=False)

            success_count = counts.get(bits, 0)
            success_rate = (success_count / shots) * 100

            comparison[level] = {
                'counts': counts,
                'success_rate': success_rate,
                'fidelity': success_count / shots
            }

            print(f"  Success rate: {success_rate:.2f}%")
            print(f"  Error rate: {100 - success_rate:.2f}%")

        return comparison

    def visualize_noisy_results(self, save_fig=True):
        """
        Visualize results from noisy simulations.

        Args:
            save_fig: Whether to save the figure
        """
        if not self.results:
            print("No results to visualize. Run the protocol first.")
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Superdense Coding with {self.noise_level.upper()} Noise',
                    fontsize=16, fontweight='bold')

        all_bits = ['00', '01', '10', '11']

        for idx, bits in enumerate(all_bits):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]

            if bits in self.results:
                counts = self.results[bits]['counts']

                # Sort outcomes for consistent display
                outcomes = sorted(counts.keys())
                values = [counts[outcome] for outcome in outcomes]
                colors = ['green' if outcome == bits else 'red' for outcome in outcomes]

                ax.bar(outcomes, values, color=colors, alpha=0.7, edgecolor='black')
                ax.set_xlabel('Measurement Outcome', fontsize=12)
                ax.set_ylabel('Counts', fontsize=12)
                ax.set_title(f'Input: {bits}', fontsize=14, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)

                # Add metrics
                success_count = counts.get(bits, 0)
                success_rate = (success_count / self.results[bits]['shots']) * 100
                error_rate = 100 - success_rate

                info_text = f'Success: {success_rate:.1f}%\nError: {error_rate:.1f}%'
                ax.text(0.5, 0.95, info_text,
                       transform=ax.transAxes, ha='center', va='top',
                       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
                       fontsize=10, fontweight='bold')

        plt.tight_layout()

        if save_fig:
            filename = f'superdense_noisy_{self.noise_level}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✓ Results visualization saved as '{filename}'")

        plt.show()

    def print_summary(self, results):
        """Print summary table of noisy results."""
        print(f"\n{'=' * 80}")
        print("NOISY SIMULATION SUMMARY")
        print(f"{'=' * 80}")
        print(f"{'Input':<10} {'Expected':<10} {'Success Rate':<15} {'Fidelity':<12} {'Status'}")
        print(f"{'─' * 80}")

        for bits in ['00', '01', '10', '11']:
            if bits in results:
                data = results[bits]
                success = data['success_rate']
                fidelity = data['fidelity']

                if success >= 95.0:
                    status = '✓ Excellent'
                elif success >= 80.0:
                    status = '⚠ Good'
                elif success >= 60.0:
                    status = '⚠ Fair'
                else:
                    status = '✗ Poor'

                print(f"{bits:<10} {data['expected']:<10} {success:>6.2f}%{'':<8} "
                      f"{fidelity:>6.4f}{'':<6} {status}")

        print(f"{'=' * 80}\n")


def main():
    """Main function for noisy superdense coding demonstration."""
    print("\n" + "=" * 70)
    print("SUPERDENSE CODING WITH NOISE - DEMONSTRATION")
    print("=" * 70)
    print("\nSimulating realistic quantum channels with:")
    print("  • Depolarizing noise")
    print("  • Thermal relaxation (T1, T2 decay)")
    print("  • Gate errors\n")

    # Test with medium noise
    print("\n[1] Testing with MEDIUM noise level...")
    noisy_sdc = NoisySuperdenseCoding(noise_level='medium')
    results = noisy_sdc.test_all_cases(shots=2048)
    noisy_sdc.print_summary(results)
    noisy_sdc.visualize_noisy_results(save_fig=True)

    # Compare noise levels
    print("\n[2] Comparing different noise levels...")
    comparison = noisy_sdc.compare_noise_levels(bits='11', shots=2048)

    print("\n✓ Noisy simulation demonstration completed!")


if __name__ == "__main__":
    main()
