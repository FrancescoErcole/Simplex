# Simplex
Simplex method implemented in Python, for 2 or 3 dimensions

# Instructions
This is the code to create the tableau object.

```
simplex(max=True,Z = [3,5])
```

During the inizialization, the parameters define respectively:
1) if the objective function must be maximized or minimized
2) the coefficient of the objective function (which constrains the number of variables in scope).

In the above example, the objective function:\
$Z = 3*x + 5*y$

1) During the creation of the simplex tableau object, the objective function is declared as "max" or "min"
x = h.simplex(max=True,Z = [3,5])
x.add_constraint((1,0),4,op="<=")
x.add_constraint((0,2),12,op="<=")
x.add_constraint((3,2),18,op="<=")
