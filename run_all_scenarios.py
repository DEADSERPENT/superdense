"""
Comprehensive Superdense Coding Demonstration
==============================================
This script runs all superdense coding scenarios and generates a complete analysis:
- Ideal (noiseless) simulation
- Noisy simulation with different noise levels
- Imperfect gates simulation
- Comprehensive comparison and analysis

Author: DEADSERPENT
Platform: Qiskit
"""

import sys
import io

# Fix Windows console encoding (do this FIRST, before importing other modules)
if sys.platform == 'win32' and not isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    except AttributeError:
        # Already wrapped or can't wrap
        pass

import numpy as np
from superdense_coding import SuperdenseCoding
from superdense_noisy import NoisySuperdenseCoding
from superdense_imperfect import ImperfectGateSuperdenseCoding
from analyze_results import SuperdenseAnalyzer


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")


def run_ideal_scenario(shots=1024):
    """
    Run the ideal (noiseless) superdense coding scenario.

    Args:
        shots: Number of measurement repetitions

    Returns:
        Dictionary of results
    """
    print_header("SCENARIO 1: IDEAL (NOISELESS) SUPERDENSE CODING")
    print("Simulating perfect quantum gates and qubits...")
    print("This represents the theoretical limit of the protocol.\n")
    print("(Circuit diagrams disabled to avoid encoding issues on Windows)\n")

    sdc = SuperdenseCoding()
    results = sdc.test_all_cases(shots=shots, draw_circuit=False)
    sdc.print_summary(results)
    sdc.visualize_results(save_fig=True)

    return results


def run_noisy_scenario(shots=2048):
    """
    Run the noisy superdense coding scenario.

    Args:
        shots: Number of measurement repetitions

    Returns:
        Dictionary of results for each noise level
    """
    print_header("SCENARIO 2: SUPERDENSE CODING WITH NOISE")
    print("Simulating realistic quantum noise including:")
    print("  • Depolarizing errors")
    print("  • Thermal relaxation (T1, T2 decay)")
    print("  • Gate errors\n")

    all_results = {}

    # Test different noise levels
    for noise_level in ['low', 'medium', 'high']:
        print(f"\n{'-' * 80}")
        print(f"Testing with {noise_level.upper()} noise level...")
        print(f"{'-' * 80}")

        noisy_sdc = NoisySuperdenseCoding(noise_level=noise_level)
        results = noisy_sdc.test_all_cases(shots=shots, draw_circuit=False)
        noisy_sdc.print_summary(results)

        if noise_level == 'medium':
            noisy_sdc.visualize_noisy_results(save_fig=True)

        all_results[noise_level] = results

    # Return medium noise results for comparison
    return all_results['medium']


def run_imperfect_gates_scenario(shots=2048):
    """
    Run the imperfect gates superdense coding scenario.

    Args:
        shots: Number of measurement repetitions

    Returns:
        Dictionary of results
    """
    print_header("SCENARIO 3: SUPERDENSE CODING WITH IMPERFECT GATES")
    print("Simulating systematic gate calibration errors:")
    print("  • Over/under-rotation in single-qubit gates")
    print("  • Amplitude damping")
    print("  • Coherent errors\n")

    gate_error = np.radians(5)  # 5 degree error
    imperfect_sdc = ImperfectGateSuperdenseCoding(gate_error_angle=gate_error)
    results = imperfect_sdc.test_all_cases(shots=shots, draw_circuit=False)
    imperfect_sdc.print_summary(results)
    imperfect_sdc.visualize_imperfect_results(save_fig=True)

    # Also show error angle comparison
    print(f"\n{'-' * 80}")
    print("Analyzing impact of different gate error magnitudes...")
    print(f"{'-' * 80}\n")

    comparison = imperfect_sdc.compare_gate_errors(
        bits='11',
        error_angles=[0, 1, 2, 5, 10, 15],
        shots=shots
    )
    imperfect_sdc.visualize_error_comparison(comparison, '11', save_fig=True)

    return results


def run_comprehensive_analysis(ideal_results, noisy_results, imperfect_results):
    """
    Run comprehensive comparison and analysis of all scenarios.

    Args:
        ideal_results: Results from ideal scenario
        noisy_results: Results from noisy scenario
        imperfect_results: Results from imperfect gates scenario
    """
    print_header("COMPREHENSIVE ANALYSIS AND COMPARISON")
    print("Comparing performance across all scenarios...\n")

    # Create analyzer
    analyzer = SuperdenseAnalyzer()

    # Add all scenarios
    analyzer.add_scenario('Ideal', ideal_results)
    analyzer.add_scenario('Noisy (Medium)', noisy_results)
    analyzer.add_scenario('Imperfect Gates (5°)', imperfect_results)

    # Generate visualizations
    print("Generating comparison visualizations...\n")
    analyzer.compare_success_rates(save_fig=True)
    analyzer.compare_fidelities(save_fig=True)
    analyzer.create_quantum_advantage_chart(save_fig=True)

    # Generate text report
    analyzer.generate_report()


def print_protocol_explanation():
    """Print a detailed explanation of the superdense coding protocol."""
    print_header("SUPERDENSE CODING PROTOCOL EXPLANATION")

    print("What is Superdense Coding?")
    print("-" * 80)
    print("""
Superdense coding is a quantum communication protocol that demonstrates
quantum advantage over classical communication. It allows two parties
(Alice and Bob) to transmit 2 classical bits of information by sending
only 1 qubit, using pre-shared quantum entanglement.

Key Concept:
    Classical: Need 2 bits to send 2 bits of information
    Quantum:   Need 1 qubit to send 2 bits of information
    Advantage: 2x information density!

Protocol Steps:
───────────────
1. PREPARATION (Before communication)
   • Create a Bell state (maximally entangled pair)
   • Give one qubit to Alice, one to Bob

2. ENCODING (Alice's action)
   • Alice wants to send 2 classical bits to Bob
   • She applies one of four gates to her qubit:
     - '00' → I (Identity - do nothing)
     - '01' → X (Pauli-X gate)
     - '10' → Z (Pauli-Z gate)
     - '11' → ZX (Pauli-Z then Pauli-X)

3. TRANSMISSION
   • Alice sends her qubit to Bob
   • Only 1 qubit travels through the channel!

4. DECODING (Bob's action)
   • Bob performs a Bell measurement on both qubits
   • He applies CNOT and Hadamard gates
   • Measures both qubits

5. RESULT
   • Bob perfectly recovers Alice's 2 classical bits
   • Success!

Why does this work?
───────────────────
The key is ENTANGLEMENT. The two qubits are correlated in a special
quantum way. When Alice modifies her qubit, this affects the joint state
of both qubits. Even though only 1 qubit is sent, Bob can extract 2 bits
of information because of the pre-shared entanglement.

This is a genuine quantum advantage - there's no classical way to achieve
the same information density without sending 2 classical bits.
""")


def print_results_summary():
    """Print expected results summary."""
    print_header("EXPECTED RESULTS SUMMARY")

    print("+------------+--------------+-------------+--------------------------+")
    print("| Input Bits | Gates Applied|   Output    |         Results          |")
    print("+------------+--------------+-------------+--------------------------+")
    print("|     00     |      I       |     00      | Success in all cases     |")
    print("|     01     |      X       |     01      | High-fidelity recovery   |")
    print("|     10     |      Z       |     10      | Robust in simulation     |")
    print("|     11     |      ZX      |     11      | Some hardware noise      |")
    print("+------------+--------------+-------------+--------------------------+")

    print("\n  Ideal Case:           100% success rate (perfect transmission)")
    print("  Noisy Case:           80-95% success rate (realistic noise)")
    print("  Imperfect Gates:      75-90% success rate (calibration errors)")
    print()


def main():
    """Main function to run all demonstrations."""
    print("\n" + "+" + "=" * 78 + "+")
    print("|" + "SUPERDENSE CODING: COMPREHENSIVE DEMONSTRATION".center(78) + "|")
    print("|" + "Implementation of Quantum Communication Protocol".center(78) + "|")
    print("+" + "=" * 78 + "+")

    # Print protocol explanation
    print_protocol_explanation()

    # Print expected results
    print_results_summary()

    # Confirm to proceed
    print("This demonstration will:")
    print("  1. Run ideal (noiseless) simulations")
    print("  2. Run noisy simulations (low, medium, high noise)")
    print("  3. Run imperfect gate simulations")
    print("  4. Generate comprehensive analysis and visualizations")
    print("\nThis may take a few minutes to complete.")

    try:
        input("\nPress Enter to start the demonstration (or Ctrl+C to cancel)...")
    except KeyboardInterrupt:
        print("\n\nDemonstration cancelled.")
        return

    # Run all scenarios
    try:
        # Scenario 1: Ideal
        ideal_results = run_ideal_scenario(shots=1024)

        # Scenario 2: Noisy
        noisy_results = run_noisy_scenario(shots=2048)

        # Scenario 3: Imperfect Gates
        imperfect_results = run_imperfect_gates_scenario(shots=2048)

        # Comprehensive Analysis
        run_comprehensive_analysis(ideal_results, noisy_results, imperfect_results)

        # Final summary
        print_header("DEMONSTRATION COMPLETE")
        print("✓ All scenarios executed successfully!")
        print("✓ All visualizations generated and saved!")
        print("\nGenerated Files:")
        print("  • superdense_coding_results.png")
        print("  • superdense_noisy_medium.png")
        print("  • superdense_imperfect_5.0deg.png")
        print("  • gate_error_comparison_11.png")
        print("  • comparison_success_rates.png")
        print("  • comparison_fidelity_heatmap.png")
        print("  • quantum_advantage.png")
        print("\nThank you for exploring quantum superdense coding!")
        print("=" * 80 + "\n")

    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
