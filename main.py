import numpy as np
import src

x = src.simplex(max=True,Z = [3,5])
x.add_constraint((1,0),4,op="<=")
x.add_constraint((0,2),12,op="<=")
x.add_constraint((3,2),18,op="<=")

x.solve()
