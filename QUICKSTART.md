# Superdense Coding - Quick Start Guide

## Version 1.1 - All Bugs Fixed! ✓

A complete, **fully functional** implementation of quantum superdense coding demonstrating how to send 2 classical bits using only 1 qubit!

**Latest Updates:**
- ✅ Fixed bit ordering bug (01 and 10 now work correctly)
- ✅ Fixed UTF-8 encoding errors on Windows
- ✅ Fixed non-unitary matrix error in imperfect gates
- ✅ All test cases now passing with expected results

## Files Created

```
superdense/
├── venv/                            # Virtual environment (activated)
├── superdense_coding.py             # Main ideal implementation
├── superdense_noisy.py              # Noisy simulation
├── superdense_imperfect.py          # Imperfect gates simulation
├── analyze_results.py               # Analysis and comparison tools
├── run_all_scenarios.py             # Complete demonstration
├── requirements.txt                 # Dependencies
├── README.md                        # Full documentation
├── QUICKSTART.md                    # This file
└── superdense_coding_results.png    # Generated visualization
```

## Quick Commands

### 1. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Run Individual Scenarios

```bash
# Ideal (perfect) simulation - 100% success rate
python superdense_coding.py

# Noisy simulation - realistic quantum noise
python superdense_noisy.py

# Imperfect gates - calibration errors
python superdense_imperfect.py
```

### 3. Run Complete Demonstration

```bash
# Runs all scenarios and generates comprehensive analysis
python run_all_scenarios.py
```

### 4. Custom Analysis

```python
from superdense_coding import SuperdenseCoding

# Create instance
sdc = SuperdenseCoding()

# Run for specific input
counts = sdc.run_protocol('11', shots=2048)
print(f"Results: {counts}")

# Test all cases
results = sdc.test_all_cases(shots=1024)
sdc.print_summary(results)
sdc.visualize_results()
```

## Test Results

**ALL TESTS PASSED! ✓**

```
Input  Gates  Expected  Success Rate  Status
00     I      00        100.00%       [OK] Perfect
01     X      01        100.00%       [OK] Perfect
10     Z      10        100.00%       [OK] Perfect
11     ZX     11        100.00%       [OK] Perfect
```

## What Makes This Special?

### Quantum Advantage

- **Classical**: Need to send 2 bits to transmit 2 bits
- **Quantum**: Send 1 qubit to transmit 2 bits
- **Efficiency**: 2x information density!

### The Protocol

1. **Preparation**: Create Bell state (entangled pair)
2. **Encoding**: Alice applies one of four gates (I, X, Z, ZX)
3. **Transmission**: Alice sends 1 qubit to Bob
4. **Decoding**: Bob performs Bell measurement
5. **Result**: Bob recovers Alice's 2 classical bits perfectly!

## Circuit Diagram Example

```
For input '11':

      Bell State ┌───┐      Encode: 11 ┌───┐┌───┐ Decode      ┌───┐┌─┐
q_0: ─────░──────┤ H ├──■───────░──────┤ Z ├┤ X ├───░──────■──┤ H ├┤M├
          ░      └───┘┌─┴─┐     ░      └───┘└───┘   ░    ┌─┴─┐└┬─┬┘└╥┘
q_1: ─────░───────────┤ X ├─────░───────────────────░────┤ X ├─┤M├──╫─
          ░           └───┘     ░                   ░    └───┘ └╥┘  ║
c: 2/═══════════════════════════════════════════════════════════╩═══╩═
                                                                0   1
```

## Next Steps

### 1. Explore Noisy Scenarios

```python
from superdense_noisy import NoisySuperdenseCoding

# Test with different noise levels
for level in ['low', 'medium', 'high']:
    sdc = NoisySuperdenseCoding(noise_level=level)
    results = sdc.test_all_cases(shots=2048)
    sdc.print_summary(results)
```

### 2. Analyze Gate Errors

```python
from superdense_imperfect import ImperfectGateSuperdenseCoding
import numpy as np

# Test with 10° gate error
sdc = ImperfectGateSuperdenseCoding(gate_error_angle=np.radians(10))
results = sdc.test_all_cases(shots=2048)

# Compare different error angles
comparison = sdc.compare_gate_errors(bits='11',
                                      error_angles=[0, 5, 10, 15, 20])
```

### 3. Run on IBM Quantum Hardware

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save your IBM Quantum account (first time only)
QiskitRuntimeService.save_account(channel="ibm_quantum",
                                  token="YOUR_API_TOKEN")

# Then modify the simulator to use real backend
service = QiskitRuntimeService(channel="ibm_quantum")
backend = service.backend("ibm_brisbane")  # or other available backend
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Make sure virtual environment is activated
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Issue: Unicode/Encoding Errors

**Solution**: Already fixed! The scripts set UTF-8 encoding automatically.

### Issue: No display for plots

**Solution**: Plots are automatically saved as PNG files. Check your directory.

## Performance Notes

- **Ideal simulation**: 100% success rate (theoretical limit)
- **Noisy simulation**: 80-95% typical (realistic quantum noise)
- **Imperfect gates**: 75-90% typical (calibration errors)
- **IBM Hardware**: 60-85% typical (real quantum computer)

## Key Takeaways

1. ✓ Superdense coding achieves 2x classical communication efficiency
2. ✓ Uses quantum entanglement as a resource
3. ✓ Robust against moderate noise
4. ✓ Demonstrates genuine quantum advantage
5. ✓ Foundational protocol for quantum communication

## Questions?

- Check `README.md` for detailed documentation
- Review the code comments for implementation details
- Experiment with different parameters!

---

**Happy Quantum Computing!** 🚀

*Demonstrating quantum advantage through superdense coding*
