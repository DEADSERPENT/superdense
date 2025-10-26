# Superdense Coding Implementation

A comprehensive implementation of the quantum superdense coding protocol using Qiskit, demonstrating quantum advantage in communication by transmitting 2 classical bits using only 1 qubit.

## Abstract

Superdense coding is a foundational quantum communication protocol that allows the transmission of two classical bits of information by sending only one qubit, leveraging entanglement and quantum operations. This project implements superdense coding in multiple scenarios—ranging from ideal noiseless situations to those involving noise and imperfect gates—demonstrating the practical applicability and quantum advantage over classical methods.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Protocol Explanation](#protocol-explanation)
- [Results](#results)
- [Platform](#platform)
- [Author](#author)

## Features

- **Ideal Simulation**: Perfect quantum gates and qubits (100% fidelity)
- **Noisy Simulation**: Realistic quantum noise including:
  - Depolarizing errors
  - Thermal relaxation (T1, T2 decay)
  - Gate errors at low, medium, and high noise levels
- **Imperfect Gates**: Systematic calibration errors:
  - Over/under-rotation in single-qubit gates
  - Amplitude damping
  - Coherent errors
- **Comprehensive Analysis**:
  - Success rate comparison across scenarios
  - Fidelity heatmaps
  - Quantum advantage visualization
  - Detailed performance reports
- **Publication-Quality Visualizations**: All plots saved as high-resolution PNG files

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime numpy matplotlib
```

## Project Structure

```
superdense/
│
├── superdense_coding.py          # Ideal (noiseless) implementation
├── superdense_noisy.py            # Noisy simulation implementation
├── superdense_imperfect.py        # Imperfect gates implementation
├── analyze_results.py             # Analysis and comparison tools
├── run_all_scenarios.py           # Comprehensive demonstration script
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Usage

### Quick Start - Run All Scenarios

To run the complete demonstration with all scenarios:

```bash
python run_all_scenarios.py
```

This will:
1. Run ideal (noiseless) simulations
2. Run noisy simulations at low, medium, and high noise levels
3. Run imperfect gate simulations
4. Generate comprehensive analysis and visualizations
5. Save all plots as PNG files

### Individual Scenarios

#### Ideal (Noiseless) Simulation

```bash
python superdense_coding.py
```

Tests all four input cases (00, 01, 10, 11) with perfect quantum gates.

#### Noisy Simulation

```bash
python superdense_noisy.py
```

Tests the protocol under realistic noise conditions with depolarizing errors, thermal relaxation, and gate errors.

#### Imperfect Gates Simulation

```bash
python superdense_imperfect.py
```

Tests the protocol with systematic gate calibration errors and coherent errors.

### Using as a Module

You can also import and use the classes in your own scripts:

```python
from superdense_coding import SuperdenseCoding

# Create instance
sdc = SuperdenseCoding()

# Run protocol for specific input
counts = sdc.run_protocol('11', shots=1024)

# Test all cases
results = sdc.test_all_cases(shots=1024)

# Visualize
sdc.visualize_results(save_fig=True)
```

## Protocol Explanation

### What is Superdense Coding?

Superdense coding is a quantum communication protocol that demonstrates quantum advantage over classical communication. It allows two parties (Alice and Bob) to transmit 2 classical bits of information by sending only 1 qubit, using pre-shared quantum entanglement.

**Key Concept:**
- **Classical**: Need 2 bits to send 2 bits of information
- **Quantum**: Need 1 qubit to send 2 bits of information
- **Advantage**: 2x information density!

### Protocol Steps

1. **Preparation** (Before communication)
   - Create a Bell state (maximally entangled pair): |Φ+⟩ = (|00⟩ + |11⟩) / √2
   - Give one qubit to Alice, one to Bob

2. **Encoding** (Alice's action)
   - Alice wants to send 2 classical bits to Bob
   - She applies one of four gates to her qubit:
     - '00' → I (Identity - do nothing)
     - '01' → X (Pauli-X gate)
     - '10' → Z (Pauli-Z gate)
     - '11' → ZX (Pauli-Z then Pauli-X)

3. **Transmission**
   - Alice sends her qubit to Bob
   - Only 1 qubit travels through the channel!

4. **Decoding** (Bob's action)
   - Bob performs a Bell measurement on both qubits
   - He applies CNOT and Hadamard gates
   - Measures both qubits

5. **Result**
   - Bob perfectly recovers Alice's 2 classical bits

### Circuit Diagram

```
        ┌───┐      ┌─────────┐      ┌───┐┌─┐
q_0: ───┤ H ├──■───┤ Encode  ├──■───┤ H ├┤M├───
        └───┘┌─┴─┐ └─────────┘┌─┴─┐ └───┘└╥┘┌─┐
q_1: ────────┤ X ├─────────────┤ X ├───────╫─┤M├
             └───┘             └───┘       ║ └╥┘
c: 2/════════════════════════════════════╩══╩═
                                          0  1
```

### Why Does This Work?

The key is **entanglement**. The two qubits are correlated in a special quantum way. When Alice modifies her qubit, this affects the joint state of both qubits. Even though only 1 qubit is sent, Bob can extract 2 bits of information because of the pre-shared entanglement.

This is a genuine quantum advantage - there's no classical way to achieve the same information density without sending 2 classical bits.

## Results

### Expected Outcomes

| Input Bits | Gates Applied | Output | Results |
|------------|---------------|--------|---------|
| 00 | I | 00 | Success in all ideal cases |
| 01 | X | 01 | High-fidelity recovery |
| 10 | Z | 10 | Robust in simulation, some hardware noise |
| 11 | XZ | 11 | Occasional errors with hardware decoherence |

### Performance Summary

- **Ideal Case**: 100% success rate (perfect transmission)
- **Noisy Case**: 80-95% success rate depending on noise level
- **Imperfect Gates**: 75-90% success rate depending on gate error magnitude

### Generated Visualizations

The scripts generate the following visualizations:

1. `superdense_coding_results.png` - Results for ideal case
2. `superdense_noisy_medium.png` - Results for noisy simulation
3. `superdense_imperfect_5.0deg.png` - Results for imperfect gates
4. `gate_error_comparison_11.png` - Impact of gate error angle
5. `comparison_success_rates.png` - Success rates across all scenarios
6. `comparison_fidelity_heatmap.png` - Fidelity comparison heatmap
7. `quantum_advantage.png` - Classical vs quantum communication comparison

## Platform

- **Language**: Python 3.8+
- **Framework**: Qiskit (Terra, Aer, IBM-Q)
- **Libraries**: NumPy, Matplotlib
- **Execution**:
  - Qiskit Aer (statevector and qasm simulators)
  - Can be adapted for IBM Quantum hardware

## Advanced Usage

### Customizing Noise Parameters

```python
from superdense_noisy import NoisySuperdenseCoding

# Create with custom noise level
noisy_sdc = NoisySuperdenseCoding(noise_level='high')

# Run and analyze
results = noisy_sdc.test_all_cases(shots=4096)
noisy_sdc.visualize_noisy_results()
```

### Customizing Gate Errors

```python
from superdense_imperfect import ImperfectGateSuperdenseCoding
import numpy as np

# Create with custom gate error (10 degrees)
imperfect_sdc = ImperfectGateSuperdenseCoding(gate_error_angle=np.radians(10))

# Compare different error angles
comparison = imperfect_sdc.compare_gate_errors(
    bits='11',
    error_angles=[0, 2, 5, 10, 15, 20],
    shots=2048
)
```

### Comprehensive Analysis

```python
from analyze_results import SuperdenseAnalyzer

# Create analyzer
analyzer = SuperdenseAnalyzer()

# Add scenarios
analyzer.add_scenario('Ideal', ideal_results)
analyzer.add_scenario('Noisy', noisy_results)
analyzer.add_scenario('Imperfect', imperfect_results)

# Generate visualizations
analyzer.compare_success_rates()
analyzer.compare_fidelities()
analyzer.generate_report()
```

## Running on IBM Quantum Hardware

To run on real IBM Quantum hardware:

1. **Set up IBM Quantum account**:
   - Create account at https://quantum.ibm.com/
   - Get your API token

2. **Save credentials**:
```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save account (only need to do this once)
QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
```

3. **Modify the code** to use IBM backend:
```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Load account
service = QiskitRuntimeService(channel="ibm_quantum")

# Get backend
backend = service.backend("ibm_brisbane")  # or another available backend

# Run circuit
job = backend.run(qc, shots=1024)
result = job.result()
```

## Contributing

This is an educational project. Feel free to:
- Experiment with different noise models
- Add new analysis techniques
- Implement additional quantum communication protocols
- Optimize for specific hardware backends

## References

- Bennett, C. H., & Wiesner, S. J. (1992). Communication via one- and two-particle operators on Einstein-Podolsky-Rosen states. Physical Review Letters, 69(20), 2881.
- Qiskit Documentation: https://qiskit.org/documentation/
- IBM Quantum: https://quantum.ibm.com/

## License

This project is provided as-is for educational purposes.

## Author

**DEADSERPENT**

---

**Quantum Advantage in Action!** 🚀

*Demonstrating the power of quantum entanglement for efficient communication.*
