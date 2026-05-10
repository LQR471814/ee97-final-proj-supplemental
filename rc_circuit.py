from sympy import symbols, Function, Eq, diff, dsolve

V, t = symbols("V t", real=True)
R, C = symbols("R C", real=True, positive=True)
V_C = Function("V_C")
ode = Eq(V_C(t) + R * C * diff(V_C(t), t), V)
sol = dsolve(ode)

print(sol)
