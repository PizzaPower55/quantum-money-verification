import numpy as np

rng = np.random.default_rng()

ZERO = np.array([1, 0], dtype=complex)
ONE = np.array([0, 1], dtype=complex)
PLUS = (ZERO + ONE) / np.sqrt(2)
MINUS = (ZERO - ONE) / np.sqrt(2)

def prepare_pair(b, c0, c1):
    z_states = (ZERO, ONE)
    x_states = (PLUS, MINUS)
    if b == 0:
        return z_states[c0].copy(), x_states[c1].copy()
    if b == 1:
        return x_states[c0].copy(), z_states[c1].copy()
    raise ValueError("b must be either 0 or 1")

Z_PROJ_0 = np.array([[1, 0], [0, 0]], dtype=complex)
Z_PROJ_1 = np.array([[0, 0], [0, 1]], dtype=complex)
X_PROJ_PLUS = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
X_PROJ_MINUS = 0.5 * np.array([[1, -1], [-1, 1]], dtype=complex)

def measure_qubit_in_place(qubit, proj_0, proj_1):
    prob_0 = float(np.real(np.vdot(qubit, proj_0 @ qubit)))
    prob_0 = np.clip(prob_0, 0.0, 1.0)
    outcome = 0 if rng.random() < prob_0 else 1
    projector = proj_0 if outcome == 0 else proj_1
    collapsed_state = projector @ qubit
    collapsed_norm = np.linalg.norm(collapsed_state)
    if collapsed_norm == 0:
        raise RuntimeError("Numerical error produced a zero collapsed state.")
    qubit[...] = collapsed_state / collapsed_norm
    return outcome

def run_attacker2_sim(secret, token):
    N = len(secret)
    count1, count2 = 0, 0
    
    # Verifier 1
    for i in range(N):
        b, c0, c1 = secret[i]
        rnd = rng.integers(0, 2)
        if rnd == 0:
            x0, x1 = measure_qubit_in_place(token[i][0], Z_PROJ_0, Z_PROJ_1), measure_qubit_in_place(token[i][1], Z_PROJ_0, Z_PROJ_1)
            if (b == 0 and x0 == c0) or (b == 1 and x1 == c1): count1 += 1
        else:
            x0, x1 = measure_qubit_in_place(token[i][0], X_PROJ_PLUS, X_PROJ_MINUS), measure_qubit_in_place(token[i][1], X_PROJ_PLUS, X_PROJ_MINUS)
            if (b == 0 and x1 == c1) or (b == 1 and x0 == c0): count1 += 1

    # Verifier 2 (Post-Collapse)
    for i in range(N):
        b, c0, c1 = secret[i]
        rnd = rng.integers(0, 2)
        if rnd == 0:
            x0, x1 = measure_qubit_in_place(token[i][0], Z_PROJ_0, Z_PROJ_1), measure_qubit_in_place(token[i][1], Z_PROJ_0, Z_PROJ_1)
            if (b == 0 and x0 == c0) or (b == 1 and x1 == c1): count2 += 1
        else:
            x0, x1 = measure_qubit_in_place(token[i][0], X_PROJ_PLUS, X_PROJ_MINUS), measure_qubit_in_place(token[i][1], X_PROJ_PLUS, X_PROJ_MINUS)
            if (b == 0 and x1 == c1) or (b == 1 and x0 == c0): count2 += 1
            
    return count1 / N, count2 / N