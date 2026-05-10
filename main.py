from sympy import lambdify, symbols, limit, E, oo, Eq, solve, latex, plot, nsolve
import numpy as np
import matplotlib.pyplot as plt


V_src = symbols("V_src", real=True)
tau = symbols("tau", real=True, positive=True)

D, T_cycle = symbols("D T_cycle", real=True, positive=True)
T_on = D * T_cycle
T_off = (1 - D) * T_cycle

A_on = E ** (-T_on / tau)
A_off = E ** (-T_off / tau)
A = A_off * A_on
B = A_off * V_src * (1 - A_on)

bound = symbols("n")
V_0 = 0
V_n = A**bound * V_0 + B * (1 - A**bound) / (1 - A)  # for A != 1

lim = limit(V_n / V_src, bound, oo)  # lim n -> infty [V_out/V_src]
eq = Eq(lim, D)

solution = solve(eq, D)  # turn equation into expr of D = ...
fn = solution[0]

# 20 microseconds
cycle_time = 20 * 1e-6
source_voltage = 5
constants = {T_cycle: cycle_time, V_src: source_voltage}
const_eq = eq.subs(constants)


def solve_bound(bound: float, guess: float):
    bound_eq = const_eq.subs({D: bound})
    expr = bound_eq.lhs - bound_eq.rhs
    print(expr)
    return nsolve(expr, tau, guess)


def smallest_tau(
    bound: float,
    min=-7,
    max=0,
    steps=100000,
    error_bound=0.01,
) -> np.float64:
    bound_eq = const_eq.subs({D: bound})
    expr = bound_eq.lhs - bound_eq.rhs
    f_num = lambdify(tau, expr, "numpy")
    # step tau from min -> max
    taus = np.logspace(min, max, steps)
    # how D responds to all those steps
    deltas = f_num(taus)
    # pick tau which minimize diff between target bound and D
    min_tau = taus[abs(deltas) < error_bound].min()
    return min_tau


def test_bound(bound: float):
    tau = smallest_tau(bound, error_bound=0.01)
    print(f"RC -> {bound}: tau = {tau}, delta < 0.01")


test_bound(0.95)

prec = 0.001
bounds = np.linspace(0 + prec, 1 - prec, num=20)
taus = [smallest_tau(bound) for bound in bounds]

plt.figure()
plt.plot(bounds, taus, marker="o")
plt.xlabel("Duty Cycle")
plt.ylabel("Time Constant (tau)")
plt.title("Minimum Time Constant for < 1% Error from Duty Cycle")
plt.grid()
plt.tight_layout()
plt.savefig("plot.png", dpi=200)


# for 0.95:
# C = 42 nF
# R = 1197.63 ohm
