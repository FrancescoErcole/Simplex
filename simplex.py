import numpy as np
import helpers as h

x = h.simplex(max=True,Z = [3,5])
x.add_constraint((1,0),4,op="<=")
x.add_constraint((0,2),12,op="<=")
x.add_constraint((3,2),18,op="<=")

# x = h.simplex(max=False,Z = [0.4,0.5])
# x.add_constraint((0.3,0.1),2.7,op="<=")
# x.add_constraint((0.5,0.5),6,op="=")
# x.add_constraint((0.6,0.4),6,op=">=")

# x = h.simplex(max=True,Z = [4,12])
# x.add_constraint((3,2),180,op="<=")
# x.add_constraint((1,2),100,op="<=")
# x.add_constraint((-2,2),40,op="<=")

x.solve()
# print(x.tableau)
