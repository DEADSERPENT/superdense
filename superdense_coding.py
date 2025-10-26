"""
Superdense Coding Implementation
==================================
This module implements the superdense coding protocol for transmitting 2 classical bits
using 1 qubit, leveraging quantum entanglement.

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
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np


class SuperdenseCoding:
    """
    Implementation of the superdense coding protocol.

    The protocol allows Alice to send 2 classical bits to Bob by transmitting
    only 1 qubit, using a pre-shared entangled pair.
    """

    def __init__(self):
        """Initialize the superdense coding protocol."""
        self.simulator = AerSimulator()
        self.results = {}

    def create_bell_state(self, qc, alice_qubit, bob_qubit):
        """
        Create a Bell state (maximally entangled state) between Alice and Bob.

        Args:
            qc: QuantumCircuit object
            alice_qubit: Alice's qubit index
            bob_qubit: Bob's qubit index

        Creates the state: |Φ+⟩ = (|00⟩ + |11⟩) / √2
        """
        qc.h(alice_qubit)
        qc.cx(alice_qubit, bob_qubit)

    def alice_encode(self, qc, alice_qubit, bits):
        """
        Alice encodes 2 classical bits onto her qubit.

        Args:
            qc: QuantumCircuit object
            alice_qubit: Alice's qubit index
            bits: String of 2 bits to encode (e.g., '00', '01', '10', '11')

        Encoding scheme:
            '00' -> I (Identity - do nothing)
            '01' -> X (Pauli-X gate)
            '10' -> Z (Pauli-Z gate)
            '11' -> ZX (Pauli-Z then Pauli-X)
        """
        if bits == '00':
            # Do nothing (Identity operation)
            pass
        elif bits == '01':
            # Apply X gate
            qc.x(alice_qubit)
        elif bits == '10':
            # Apply Z gate
            qc.z(alice_qubit)
        elif bits == '11':
            # Apply Z then X gate
            qc.z(alice_qubit)
            qc.x(alice_qubit)
        else:
            raise ValueError(f"Invalid bits: {bits}. Must be '00', '01', '10', or '11'")

    def bob_decode(self, qc, alice_qubit, bob_qubit, classical_bits):
        """
        Bob decodes the message by reversing the Bell state creation.

        Args:
            qc: QuantumCircuit object
            alice_qubit: Alice's qubit index
            bob_qubit: Bob's qubit index
            classical_bits: ClassicalRegister to store results
        """
        # Reverse the entanglement
        qc.cx(alice_qubit, bob_qubit)
        qc.h(alice_qubit)

        # Measure both qubits (note: Qiskit uses little-endian ordering)
        # Measure alice_qubit to bit 1 and bob_qubit to bit 0 to match expected output
        qc.measure(alice_qubit, classical_bits[1])
        qc.measure(bob_qubit, classical_bits[0])

    def run_protocol(self, bits, shots=1024, draw_circuit=True):
        """
        Run the complete superdense coding protocol.

        Args:
            bits: String of 2 bits to encode ('00', '01', '10', or '11')
            shots: Number of measurement repetitions
            draw_circuit: Whether to draw and display the circuit

        Returns:
            Dictionary containing the measurement results
        """
        # Create quantum and classical registers
        qr = QuantumRegister(2, 'q')
        cr = ClassicalRegister(2, 'c')
        qc = QuantumCircuit(qr, cr)

        # Step 1: Create entangled Bell pair
        qc.barrier(label='Bell State')
        self.create_bell_state(qc, 0, 1)

        # Step 2: Alice encodes her message
        qc.barrier(label=f'Encode: {bits}')
        self.alice_encode(qc, 0, bits)

        # Step 3: Bob decodes the message
        qc.barrier(label='Decode')
        self.bob_decode(qc, 0, 1, cr)

        # Draw circuit if requested
        if draw_circuit:
            print(f"\nCircuit for encoding '{bits}':")
            print(qc.draw(output='text'))

        # Execute the circuit
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

    def test_all_cases(self, shots=1024, draw_circuit=False):
        """
        Test all four possible input cases: 00, 01, 10, 11.

        Args:
            shots: Number of measurement repetitions per case
            draw_circuit: Whether to draw circuit diagrams (default: False to avoid encoding issues)

        Returns:
            Dictionary containing results for all cases
        """
        all_bits = ['00', '01', '10', '11']
        results = {}

        print("=" * 70)
        print("SUPERDENSE CODING - IDEAL CASE")
        print("=" * 70)

        for bits in all_bits:
            print(f"\n{'-' * 70}")
            print(f"Testing input: {bits}")
            print(f"{'-' * 70}")

            counts = self.run_protocol(bits, shots=shots, draw_circuit=draw_circuit)

            # Calculate success rate
            expected_output = bits
            success_count = counts.get(expected_output, 0)
            success_rate = (success_count / shots) * 100

            results[bits] = {
                'counts': counts,
                'success_rate': success_rate,
                'expected': expected_output
            }

            print(f"\nResults:")
            print(f"  Expected output: {expected_output}")
            print(f"  Measurement counts: {counts}")
            print(f"  Success rate: {success_rate:.2f}%")

            if success_rate == 100.0:
                print(f"  [OK] Perfect transmission!")
            elif success_rate >= 95.0:
                print(f"  [OK] High fidelity transmission")
            else:
                print(f"  [WARNING] Some errors detected")

        return results

    def visualize_results(self, save_fig=True):
        """
        Create visualizations of the results.

        Args:
            save_fig: Whether to save the figure to a file
        """
        if not self.results:
            print("No results to visualize. Run the protocol first.")
            return

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Superdense Coding Results - All Cases', fontsize=16, fontweight='bold')

        all_bits = ['00', '01', '10', '11']

        for idx, bits in enumerate(all_bits):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]

            if bits in self.results:
                counts = self.results[bits]['counts']

                # Create bar plot
                outcomes = list(counts.keys())
                values = list(counts.values())
                colors = ['green' if outcome == bits else 'red' for outcome in outcomes]

                ax.bar(outcomes, values, color=colors, alpha=0.7, edgecolor='black')
                ax.set_xlabel('Measurement Outcome', fontsize=12)
                ax.set_ylabel('Counts', fontsize=12)
                ax.set_title(f'Input: {bits}', fontsize=14, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)

                # Add success rate
                success_count = counts.get(bits, 0)
                success_rate = (success_count / self.results[bits]['shots']) * 100
                ax.text(0.5, 0.95, f'Success Rate: {success_rate:.1f}%',
                       transform=ax.transAxes, ha='center', va='top',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       fontsize=11, fontweight='bold')

        plt.tight_layout()

        if save_fig:
            plt.savefig('superdense_coding_results.png', dpi=300, bbox_inches='tight')
            print("\n[OK] Results visualization saved as 'superdense_coding_results.png'")

        plt.show()

    def print_summary(self, results):
        """
        Print a summary table of all results.

        Args:
            results: Dictionary of results from test_all_cases()
        """
        print(f"\n{'=' * 70}")
        print("SUMMARY TABLE")
        print(f"{'=' * 70}")
        print(f"{'Input':<10} {'Gates Applied':<15} {'Expected':<10} {'Success Rate':<15} {'Status'}")
        print(f"{'-' * 70}")

        gate_map = {
            '00': 'I',
            '01': 'X',
            '10': 'Z',
            '11': 'ZX'
        }

        for bits in ['00', '01', '10', '11']:
            if bits in results:
                data = results[bits]
                gates = gate_map[bits]
                success = data['success_rate']

                if success == 100.0:
                    status = '[OK] Perfect'
                elif success >= 95.0:
                    status = '[OK] Excellent'
                elif success >= 80.0:
                    status = '[WARN] Good'
                else:
                    status = '[ERROR] Poor'

                print(f"{bits:<10} {gates:<15} {data['expected']:<10} {success:>6.2f}%{'':<8} {status}")

        print(f"{'=' * 70}\n")


def main():
    """Main function to run the superdense coding demonstration."""
    print("\n" + "=" * 70)
    print("SUPERDENSE CODING PROTOCOL DEMONSTRATION")
    print("=" * 70)
    print("\nThis demonstrates quantum advantage in communication:")
    print("  * Classical: Need to send 2 bits to transmit 2 bits of information")
    print("  * Quantum (Superdense Coding): Send 1 qubit to transmit 2 bits!\n")

    # Create instance
    sdc = SuperdenseCoding()

    # Test all cases
    results = sdc.test_all_cases(shots=1024)

    # Print summary
    sdc.print_summary(results)

    # Visualize
    print("Generating visualization...")
    sdc.visualize_results(save_fig=True)

    print("\n[OK] Superdense coding demonstration completed successfully!")


if __name__ == "__main__":
    main()
