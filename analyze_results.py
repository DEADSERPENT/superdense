"""
Superdense Coding Analysis and Comparison Module
=================================================
This module provides comprehensive analysis and visualization tools
for comparing different superdense coding scenarios.

Author: DEADSERPENT
Platform: Qiskit
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


class SuperdenseAnalyzer:
    """
    Analyzer for comparing ideal, noisy, and imperfect gate scenarios.
    """

    def __init__(self):
        """Initialize the analyzer."""
        self.scenarios = {}

    def add_scenario(self, name, results):
        """
        Add results from a scenario for comparison.

        Args:
            name: String name of the scenario (e.g., 'Ideal', 'Noisy', 'Imperfect')
            results: Dictionary of results from test_all_cases()
        """
        self.scenarios[name] = results

    def compare_success_rates(self, save_fig=True):
        """
        Create a comparison chart of success rates across scenarios.

        Args:
            save_fig: Whether to save the figure
        """
        if not self.scenarios:
            print("No scenarios to compare. Add scenarios first.")
            return

        all_bits = ['00', '01', '10', '11']
        scenario_names = list(self.scenarios.keys())
        n_scenarios = len(scenario_names)

        # Set up the figure
        fig, ax = plt.subplots(figsize=(12, 7))

        # Width of bars and positions
        bar_width = 0.2
        x_pos = np.arange(len(all_bits))

        # Color scheme
        colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']

        # Plot bars for each scenario
        for i, scenario_name in enumerate(scenario_names):
            success_rates = []
            for bits in all_bits:
                if bits in self.scenarios[scenario_name]:
                    rate = self.scenarios[scenario_name][bits]['success_rate']
                    success_rates.append(rate)
                else:
                    success_rates.append(0)

            offset = (i - n_scenarios / 2) * bar_width + bar_width / 2
            bars = ax.bar(x_pos + offset, success_rates, bar_width,
                         label=scenario_name, color=colors[i % len(colors)],
                         alpha=0.8, edgecolor='black', linewidth=1.5)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

        # Customize plot
        ax.set_xlabel('Input Bits', fontsize=14, fontweight='bold')
        ax.set_ylabel('Success Rate (%)', fontsize=14, fontweight='bold')
        ax.set_title('Superdense Coding: Success Rate Comparison',
                    fontsize=16, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(all_bits, fontsize=12)
        ax.set_ylim(0, 110)
        ax.legend(fontsize=11, loc='lower right')
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # Add reference line at 100%
        ax.axhline(y=100, color='green', linestyle='--', alpha=0.5, linewidth=2,
                  label='Perfect transmission')

        plt.tight_layout()

        if save_fig:
            plt.savefig('comparison_success_rates.png', dpi=300, bbox_inches='tight')
            print("\n✓ Success rate comparison saved as 'comparison_success_rates.png'")

        plt.show()

    def compare_fidelities(self, save_fig=True):
        """
        Create a heatmap comparing fidelities across scenarios and inputs.

        Args:
            save_fig: Whether to save the figure
        """
        if not self.scenarios:
            print("No scenarios to compare. Add scenarios first.")
            return

        all_bits = ['00', '01', '10', '11']
        scenario_names = list(self.scenarios.keys())

        # Prepare data matrix
        fidelity_matrix = []
        for scenario_name in scenario_names:
            row = []
            for bits in all_bits:
                if bits in self.scenarios[scenario_name]:
                    if 'fidelity' in self.scenarios[scenario_name][bits]:
                        fidelity = self.scenarios[scenario_name][bits]['fidelity']
                    else:
                        # Calculate from success rate
                        success_rate = self.scenarios[scenario_name][bits]['success_rate']
                        fidelity = success_rate / 100
                    row.append(fidelity)
                else:
                    row.append(0)
            fidelity_matrix.append(row)

        fidelity_matrix = np.array(fidelity_matrix)

        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(fidelity_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

        # Set ticks
        ax.set_xticks(np.arange(len(all_bits)))
        ax.set_yticks(np.arange(len(scenario_names)))
        ax.set_xticklabels(all_bits, fontsize=12)
        ax.set_yticklabels(scenario_names, fontsize=12)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Fidelity', fontsize=12, fontweight='bold')

        # Add text annotations
        for i in range(len(scenario_names)):
            for j in range(len(all_bits)):
                text = ax.text(j, i, f'{fidelity_matrix[i, j]:.3f}',
                             ha="center", va="center", color="black",
                             fontsize=11, fontweight='bold')

        ax.set_xlabel('Input Bits', fontsize=14, fontweight='bold')
        ax.set_ylabel('Scenario', fontsize=14, fontweight='bold')
        ax.set_title('Fidelity Heatmap Across Scenarios',
                    fontsize=16, fontweight='bold')

        plt.tight_layout()

        if save_fig:
            plt.savefig('comparison_fidelity_heatmap.png', dpi=300, bbox_inches='tight')
            print("\n✓ Fidelity heatmap saved as 'comparison_fidelity_heatmap.png'")

        plt.show()

    def create_quantum_advantage_chart(self, save_fig=True):
        """
        Visualize quantum advantage: 2 classical bits sent using 1 qubit.

        Args:
            save_fig: Whether to save the figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Classical communication
        ax1.text(0.5, 0.8, 'Classical Communication', ha='center', va='center',
                fontsize=16, fontweight='bold', transform=ax1.transAxes)

        # Alice
        alice_box = Rectangle((0.1, 0.5), 0.2, 0.2, facecolor='lightblue',
                              edgecolor='black', linewidth=2)
        ax1.add_patch(alice_box)
        ax1.text(0.2, 0.6, 'Alice', ha='center', va='center',
                fontsize=12, fontweight='bold')

        # Bob
        bob_box = Rectangle((0.7, 0.5), 0.2, 0.2, facecolor='lightcoral',
                           edgecolor='black', linewidth=2)
        ax1.add_patch(bob_box)
        ax1.text(0.8, 0.6, 'Bob', ha='center', va='center',
                fontsize=12, fontweight='bold')

        # Classical bits transmission
        ax1.annotate('', xy=(0.7, 0.62), xytext=(0.3, 0.62),
                    arrowprops=dict(arrowstyle='->', lw=3, color='black'))
        ax1.text(0.5, 0.67, '2 classical bits', ha='center',
                fontsize=11, fontweight='bold', color='red')

        ax1.text(0.5, 0.3, 'Need to send 2 bits\nto transmit 2 bits of info',
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        ax1.axis('off')

        # Quantum communication
        ax2.text(0.5, 0.8, 'Quantum Superdense Coding', ha='center', va='center',
                fontsize=16, fontweight='bold', transform=ax2.transAxes)

        # Alice
        alice_box2 = Rectangle((0.1, 0.5), 0.2, 0.2, facecolor='lightblue',
                               edgecolor='black', linewidth=2)
        ax2.add_patch(alice_box2)
        ax2.text(0.2, 0.6, 'Alice', ha='center', va='center',
                fontsize=12, fontweight='bold')

        # Bob
        bob_box2 = Rectangle((0.7, 0.5), 0.2, 0.2, facecolor='lightcoral',
                            edgecolor='black', linewidth=2)
        ax2.add_patch(bob_box2)
        ax2.text(0.8, 0.6, 'Bob', ha='center', va='center',
                fontsize=12, fontweight='bold')

        # Entanglement (before)
        ax2.plot([0.2, 0.8], [0.48, 0.48], 'g--', linewidth=2, alpha=0.5)
        ax2.text(0.5, 0.43, 'Shared entanglement', ha='center',
                fontsize=9, color='green', style='italic')

        # Qubit transmission
        ax2.annotate('', xy=(0.7, 0.62), xytext=(0.3, 0.62),
                    arrowprops=dict(arrowstyle='->', lw=3, color='purple'))
        ax2.text(0.5, 0.67, '1 qubit', ha='center',
                fontsize=11, fontweight='bold', color='purple')

        ax2.text(0.5, 0.3, 'Send 1 qubit\nto transmit 2 bits of info!\n✨ Quantum Advantage ✨',
                ha='center', va='center', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')

        fig.suptitle('Classical vs Quantum Communication Efficiency',
                    fontsize=18, fontweight='bold', y=0.98)

        plt.tight_layout()

        if save_fig:
            plt.savefig('quantum_advantage.png', dpi=300, bbox_inches='tight')
            print("\n✓ Quantum advantage chart saved as 'quantum_advantage.png'")

        plt.show()

    def generate_report(self):
        """
        Generate a comprehensive text report of all scenarios.
        """
        print("\n" + "=" * 80)
        print("COMPREHENSIVE SUPERDENSE CODING ANALYSIS REPORT")
        print("=" * 80)

        for scenario_name, results in self.scenarios.items():
            print(f"\n{'─' * 80}")
            print(f"Scenario: {scenario_name}")
            print(f"{'─' * 80}")

            total_success = 0
            total_tests = 0

            for bits in ['00', '01', '10', '11']:
                if bits in results:
                    success_rate = results[bits]['success_rate']
                    total_success += success_rate
                    total_tests += 1

                    print(f"  Input {bits}: {success_rate:.2f}% success")

            if total_tests > 0:
                avg_success = total_success / total_tests
                print(f"\n  Average Success Rate: {avg_success:.2f}%")

                if avg_success >= 98:
                    grade = "A+ (Excellent)"
                elif avg_success >= 90:
                    grade = "A (Very Good)"
                elif avg_success >= 80:
                    grade = "B (Good)"
                elif avg_success >= 70:
                    grade = "C (Fair)"
                else:
                    grade = "D (Poor)"

                print(f"  Overall Grade: {grade}")

        print("\n" + "=" * 80)
        print("QUANTUM ADVANTAGE SUMMARY")
        print("=" * 80)
        print("  Classical Communication: 2 bits needed for 2 bits of information")
        print("  Quantum Superdense Coding: 1 qubit needed for 2 bits of information")
        print("  Efficiency Gain: 2x (Double the information density!)")
        print("=" * 80 + "\n")


def main():
    """Main function for analysis demonstration."""
    print("\n" + "=" * 70)
    print("SUPERDENSE CODING - COMPREHENSIVE ANALYSIS")
    print("=" * 70)

    # Note: This is a standalone analysis module
    # To use it, run the individual scenario scripts first to generate data
    # Or integrate it with a comprehensive demo script

    print("\nThis module provides analysis and visualization tools.")
    print("Run the comprehensive demo script to see full analysis.\n")

    # Create sample visualization
    analyzer = SuperdenseAnalyzer()
    analyzer.create_quantum_advantage_chart(save_fig=True)

    print("\n✓ Analysis module ready for use!")


if __name__ == "__main__":
    main()
