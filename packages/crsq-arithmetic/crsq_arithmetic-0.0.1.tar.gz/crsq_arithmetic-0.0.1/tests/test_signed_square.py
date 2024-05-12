""" arithmetic operator test (signed square square)
"""
from qiskit import QuantumCircuit, QuantumRegister

import crsq.arithmetic as ari
import crsq.arithmetic.test_tools as test_tools


def build_square_with_values(aval, n: int, use_bit_gates, use_gate_version):
    """ build an n bit square gate circuit
        aval, bval : operands
        n : bit size of the register to use
    """
    ar = QuantumRegister(n, name='a')
    dr = QuantumRegister(n*2, name='d')
    cr1 = QuantumRegister(n, name='cr1')
    cr2 = QuantumRegister(n-1, name='cr2')
    qc = QuantumCircuit(ar, dr, cr1, cr2)

    ari.set_value(qc, ar, aval)

    if use_gate_version:
        qc.append(ari.signed_square_gate(n, use_gates=use_bit_gates), ar[:] + dr[:] + cr1[:] + cr2[:])
    else:
        ari.signed_square(qc, ar, dr, cr1, cr2, use_bit_gates)

    qc.save_statevector()
    return qc


def do_square(aval, n, use_bit_gates, use_gate_version):
    """ Test squaring two n bit signed integers
    """
    qc = build_square_with_values(aval, n, use_bit_gates, use_gate_version)

    m = n * 2  # bits for result
    astr = bin((1 << n) + aval)[-n:]
    dstr = bin((1 << m) + aval*aval)[-m:]
    cstr = "0"*(n+n-1)
    expected = cstr + dstr + astr

    exp_dict = { expected: 1 }
    test_tools.run_circuit_and_check(qc, exp_dict)


def test_signed_square():
    """ test square_gate for all possible 3bit inputs.
    """
    print("Signed int square gate test")
    for use_gate_version in [False, True]:
        for use_bit_gates in [False, True]:
            print(f" gate version: {use_gate_version}  bit gates: {use_bit_gates}")
            for n in [2,3,4]:
                s = 1 << n
                hs = 1 << n-1
                for a in range(s):
                    do_square(a-hs, n, use_bit_gates, use_gate_version)


if __name__ == '__main__':
    test_signed_square()
