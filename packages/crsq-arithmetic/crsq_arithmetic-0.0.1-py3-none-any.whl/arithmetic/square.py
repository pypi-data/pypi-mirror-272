""" Square product functions
"""
from qiskit.circuit import QuantumCircuit, QuantumRegister, Gate
from crsq.arithmetic.adder import signed_adder, signed_adder_gate, unsigned_adder, unsigned_adder_gate
import crsq.arithmetic.utils as ut


def unsigned_square(qc: QuantumCircuit, ar: QuantumRegister, dr: QuantumRegister,
                    cr1: QuantumRegister, cr2: QuantumRegister, use_gates: bool = False):
    """ Emit an unsigned square circuit.

        Effect:
            [ar, dr, cr1=0, cr2=0] -> [ar, ar*ar, cr1=0, cr2=0]
        
        :param qc: target circuit
        :param ar: operand (n bits)
        :param dr: product (2*n bits)
        :param cr1: carry for the multiplier (n-1 bits)
        :param cr2: carry for the internal adder (n-2 bits)
    """
    n = ut.bitsize(ar)
    if not (ut.bitsize(cr1) == n-1 and ut.bitsize(cr2) == n-2
            and ut.bitsize(dr) == n*2):
        raise ValueError(
            f"size mismatch: ar[{ut.bitsize(ar)}], " +
            f"cr1[{ut.bitsize(cr1)}], cr2[{ut.bitsize(cr2)}], dr[{ut.bitsize(dr)}]")
    if use_gates:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])
        for j in range(n - 3):
            for k in range(n - 1 - j):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
            qc.append(unsigned_adder_gate(n-j-1),
                      ut.register_range(cr1, 0, n-j-1)[:] + 
                      ut.register_range(dr, j*2+2, n-j)[:] +
                      ut.register_range(cr2, 0, n-j-2)[:])
            for k in range(n - 1 - j - 1, -1, -1):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
        j = n - 3
        qc.ccx(ar[j], ar[j+1], cr1[0])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.append(unsigned_adder_gate(3),
                  ut.register_range(cr1, 0, 3)[:] +
                  ut.register_range(dr, j*2+2, 4)[:] +
                  ut.register_range(cr2, 0, 2)[:])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j], ar[j+1], cr1[0])
    else:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])
        for j in range(n - 3):
            for k in range(n - 1 - j):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
            unsigned_adder(qc, ut.register_range(cr1, 0, n-j-1),
                        ut.register_range(dr, j*2+2, n-j),
                        ut.register_range(cr2, 0, n-j-2))
            for k in range(n - 1 - j - 1, -1, -1):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
        j = n - 3
        qc.ccx(ar[j], ar[j+1], cr1[0])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        unsigned_adder(qc, ut.register_range(cr1, 0, 3),
                    ut.register_range(dr, j*2+2, 4),
                    ut.register_range(cr2, 0, 2))
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j], ar[j+1], cr1[0])


def unsigned_square_gate(n: int, label: str="usquare") -> Gate:
    """ Create an unsigned square gate.
        
        Usage:
            qc.append(unsigned_square_gate(n), [a1...an, d1...d2n, c11...c1n, c21...c2n])

        Effect:
            [a, d=0, c1=0, c2=0] -> [a, a*a, c1=0, c2=0]
        
        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    dr = QuantumRegister(2*n, "d")
    c1 = QuantumRegister(n-1, "c1")
    c2 = QuantumRegister(n-2, "c2")
    qc = QuantumCircuit(ar, dr, c1, c2)
    unsigned_square(qc, ar, dr, c1, c2)
    return qc.to_gate(label=f"{label}({n})")


def signed_square(qc: QuantumCircuit, ar: QuantumRegister, dr: QuantumRegister,
                  cr1: QuantumRegister, cr2: QuantumRegister, use_gates: bool = False):
    """ Emit a signed square circuit.

        Effect:
            [ar, dr, cr1=0, cr2=0] -> [ar, ar*ar, cr1=0, cr2=0]
        
        :param qc: target circuit
        :param ar: operand (n bits, n >= 2)
        :param dr: product (2*n bits)
        :param cr1: carry for the multiplier (n bits)
        :param cr2: carry for the internal adder (n-1 bits)
    """
    n = ut.bitsize(ar)
    if not (n >= 2 and ut.bitsize(cr1) == n and ut.bitsize(cr2) == n - 1
            and ut.bitsize(dr) == n*2):
        raise ValueError(
            f"size mismatch: ar[{ut.bitsize(ar)}], dr[{ut.bitsize(dr)}], " +
            f"cr1[{ut.bitsize(cr1)}], cr2[{ut.bitsize(cr2)}]")
    if n == 2:
        # special simple case.
        qc.cx(ar[0], dr[0])
        qc.cx(ar[1], dr[2])
        qc.ccx(ar[0], ar[1], dr[2])
        return

    if use_gates:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])

        if (n % 2) == 1:
            # insert one bit we want to add in a sparse
            # list of bits
            qc.x(dr[n])
        else:
            # The one bit we want to set is preoccupied.
            # Increment the bit taking care of the carry
            qc.cx(dr[n], dr[n+1])
            qc.x(dr[n])

        for j in range(n - 3):
            for k in range(n - 1 - j):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
            qc.x(cr1[n-j-2])
            qc.append(unsigned_adder_gate(n-j),
                      ut.register_range(cr1, 0, n-j)[:] +
                      ut.register_range(dr, j*2+2, n-j+1)[:] +
                      ut.register_range(cr2, 0, n-j-1)[:])
            qc.x(cr1[n-j-2])
            for k in range(n - 1 - j - 1, -1, -1):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
        j = n - 3
        qc.ccx(ar[j], ar[j+1], cr1[0])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.x(cr1[1])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.x(cr1[2])
        qc.append(signed_adder_gate(3),
                  ut.register_range(cr1, 0, 3)[:] +
                  ut.register_range(dr, j*2+2, 3)[:] +
                  ut.register_range(cr2, 0, 2)[:])
        qc.x(cr1[2])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.x(cr1[1])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j], ar[j+1], cr1[0])
    else:
        for k in range(n):
            qc.cx(ar[k], dr[k*2])

        if (n % 2) == 1:
            # insert one bit we want to add in a sparse
            # list of bits
            qc.x(dr[n])
        else:
            # The one bit we want to set is preoccupied.
            # Increment the bit taking care of the carry
            qc.cx(dr[n], dr[n+1])
            qc.x(dr[n])

        for j in range(n - 3):
            for k in range(n - 1 - j):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
            qc.x(cr1[n-j-2])
            unsigned_adder(qc, ut.register_range(cr1, 0, n-j),
                        ut.register_range(dr, j*2+2, n-j+1),
                        ut.register_range(cr2, 0, n-j-1))
            qc.x(cr1[n-j-2])
            for k in range(n - 1 - j - 1, -1, -1):
                qc.ccx(ar[j], ar[j+k+1], cr1[k])
        j = n - 3
        qc.ccx(ar[j], ar[j+1], cr1[0])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.x(cr1[1])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.x(cr1[2])
        signed_adder(qc, ut.register_range(cr1, 0, 3),
                    ut.register_range(dr, j*2+2, 3),
                    ut.register_range(cr2, 0, 2))
        qc.x(cr1[2])
        qc.ccx(ar[j+1], ar[j+2], cr1[2])
        qc.x(cr1[1])
        qc.ccx(ar[j], ar[j+2], cr1[1])
        qc.ccx(ar[j], ar[j+1], cr1[0])


def signed_square_gate(n: int, label: str="ssquare", use_gates=False) -> Gate:
    """ Create an signed square gate.
        
        Usage:
            qc.append(signed_square_gate(n), [a1...an, d1...d2n, c11...c1n, c21...c2n])

        Effect:
            [a, d=0, c1=0, c2=0] -> [a, a*a, c1=0, c2=0]
        
        :param n: bit size of a
        :param label: label to put on the gate
    """
    ar = QuantumRegister(n, name="a")
    dr = QuantumRegister(2*n, "d")
    c1 = QuantumRegister(n, "c1")
    c2 = QuantumRegister(n-1, "c2")
    qc = QuantumCircuit(ar, dr, c1, c2)
    signed_square(qc, ar, dr, c1, c2, use_gates=use_gates)
    return qc.to_gate(label=f"{label}({n})")
