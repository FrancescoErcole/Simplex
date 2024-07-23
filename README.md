# Simplex
This script is a part of a didactical project, aim to help the teaching of the simplex method.
In this script, the focus is to show what happens during each iteration of this algorithm.\

# Instructions
A) The tableau object must be created.\
During the inizialization, the parameters define respectively:
- if the objective function must be maximized or minimized
- the coefficients of the objective function (which constrains the number of variables in scope). At most 3 variables can be used in the objective function (and constraints).

For example, if I want to maximize this objective function:\
$$Z = 3x + 5y$$

The code is:
```
tableau_obj = simplex(max=True,Z = [3,5])
```
B) We add the constraints.\
For each constraint we call a function with 3 parameters:
- A tuple of 2 or 3 numbers, which represents the coefficients of the variables in the LHS of the constraint.
- A number, which is the RHS value of the constraint
- The sign of the inequality (">=" or "<=") or the equal symbol ("=")

For example, if I want to add these two constraints:\
$$y <= 12$$\
$$3x + 2y <= 18$$

The code is:
```
tableau_obj.add_constraint((0,2),12,op="<=")
tableau_obj.add_constraint((3,2),18,op="<=")
```
C) When all the constraints have been added, solve it
```
tableau_obj.solve()
```
The result will be printed as a tableau element.
Results of each iteration are validated against a software available in this site: https://linprog.com/

# Test

## Test 1
$$Z = 3x + 5y$$\
$$x <= 4$$\
$$2y <= 12$$\
$$3x + 2y <= 18$$\
Code is:
```
x = h.simplex(max=True,Z = [3,5])
x.add_constraint((1,0),4,op="<=")
x.add_constraint((0,2),12,op="<=")
x.add_constraint((3,2),18,op="<=")
```

Results is validated and in agreement with software in source

# Source
- Theory of the siplex algorithm: https://math.libretexts.org/Bookshelves/Applied_Mathematics/Applied_Finite_Mathematics_(Sekhon_and_Bloom)/04%3A_Linear_Programming_The_Simplex_Method/4.02%3A_Maximization_By_The_Simplex_Method
- Site for validating the script: https://linprog.com/
