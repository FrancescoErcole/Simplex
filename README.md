# Simplex
This script is a part of a didactical project, aim to help the teaching of the simplex method.
In this script, the focus is to show what happens during each iteration of this algorithm.

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
The result will be printed as a tableau element.\
Results of each iteration are validated against a software available in this site: https://linprog.com/

# Test
All the following tests have been validated (and resulted in agreement) with software (see source).

## Test 1
$$max(Z = 3x + 5y)$$\
$$x <= 4$$\
$$2y <= 12$$\
$$3x + 2y <= 18$$\
Code:
```
x = h.simplex(max=True,Z = [3,5])
x.add_constraint((1,0),4,op="<=")
x.add_constraint((0,2),12,op="<=")
x.add_constraint((3,2),18,op="<=")
```

## Test 2
$$min(Z = 0.4x + 0.5y)$$\
$$0.3x + 0.1y <= 2.7$$\
$$0.5x + 0.5y = 6$$\
$$0.6x + 0.4y >= 6$$\
Code:
```
x = h.simplex(max=False,Z = [0.4,0.5])
x.add_constraint((0.3,0.1),2.7,op="<=")
x.add_constraint((0.5,0.5),6,op="=")
x.add_constraint((0.6,0.4),6,op=">=")
```

## Test 3
$$max(Z = 4x + 12y)$$\
$$3x + 2y <= 180$$\
$$x + 2y <= 100$$\
$$-2x + 2y <= 40$$\
Code:
```
x = h.simplex(max=True,Z = [4,12])
x.add_constraint((3,2),180,op="<=")
x.add_constraint((1,2),100,op="<=")
x.add_constraint((-2,2),40,op="<=")
```



# Source
- Theory of the simplex algorithm: https://math.libretexts.org/Bookshelves/Applied_Mathematics/Applied_Finite_Mathematics_(Sekhon_and_Bloom)/04%3A_Linear_Programming_The_Simplex_Method/4.02%3A_Maximization_By_The_Simplex_Method
- Introduction to Operations Research, 10th edition, K. Hiller, Gerald J. Lieberman
- Site used for the validation of the script: https://linprog.com/
