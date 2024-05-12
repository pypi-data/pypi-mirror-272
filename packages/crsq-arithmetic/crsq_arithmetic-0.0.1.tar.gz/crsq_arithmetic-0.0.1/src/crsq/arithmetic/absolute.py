""" Absolute Gates
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from qiskit.circuit.quantumcircuit import QubitSpecifier
from crsq.arithmetic.adder import scoadder_gate
import crsq.arithmetic.utils as ut

def absolute(qc: QuantumCircuit, ar: QuantumRegister, sb: QubitSpecifier,
             cr: QuantumRegister):
    """ Emit an absolute value circuit.

        Effect:
            [ar, cr=0, sb] -> [abs(ar), cr=0, sign_bit(sb)]

        :param qc: target circuit
        :param ar: operand (n bits)
        :param sb: sign bit (1 bit)
        :param cr: carry register (n-1 bits)
    """
    n = ut.bitsize(ar)
    cn = ut.bitsize(cr)
    if not (cn == n - 1):
        raise ValueError(f"Size mismatch ar[{n}], cr[{cn}]")
    qc.cx(ar[n-1], sb)
    for i in range(n):
        qc.cx(sb, ar[i])
    cogate = scoadder_gate(n, 1)
    qc.append(cogate.control(1), [sb, *ar, *cr])


def absolute_gate(n: int, label: str="abs") -> Gate:
    """ Create an absolute value gate.

        Usage:
            qc.append(absolute_gate(n), [a1...an, c1...cn-1, s])
        
        Effect:
            [a, s=0, c = 0] -> [abs(a), sign_bit(b), c=0]

        :param n: bit size of a
        :param label: label to put on the gate.
    """
    ar = QuantumRegister(n, name="a")
    cr = QuantumRegister(n-1, name="c")
    sr = QuantumRegister(1, name="sb")
    qc = QuantumCircuit(ar, sr, cr)
    absolute(qc, ar, sr[0], cr)
    return qc.to_gate(label=f"{label}({n})")
