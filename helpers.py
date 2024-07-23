import numpy as np

class simplex:
    max = None
    tableau = None
    n_var = 0
    variables=None
    basic_var= None

    def __init__(self, max = True, Z=[0,0,0]):
        if type(Z) is not list or len(Z) > 3:
            raise("Z must be a list of equal or less than 3 items")

        self.max = max

        self.n_var = len(Z)

        self.tableau = np.zeros((1, len(Z)))
        self.tableau[0] = Z
        if self.max:
            self.multiply_row(0,-1) # change sign obj function 
        self.tableau = np.pad(self.tableau, ((0,0), (0,1)))

        self.variables = []
        self.basic_var = []
        for _ in range(len(Z)):
            self.create_variable("x")


    def add_constraint(self,left_side,right_side,op=None):
        '''
            Each new constraint is implemented for the augmented form, 
            creating any slack or artificial variable if necessary
        '''
        if len(left_side) != self.n_var:
            raise("Constraint must have same number of dimension of problem")
        
        self.tableau = np.pad(self.tableau, ((0,1), (0,0)))
        self.tableau[-1][:self.n_var] = left_side
        self.tableau[-1][-1] = right_side

        if op == "<=" and right_side >= 0:
            self.append_column(1)
            s = self.create_variable("s")
            self.basic_var.append(s)
        elif op == "<=" and right_side < 0:
            # it flips sign for the row, then it treats op as ">="
            self.tableau[-1][:self.n_var]  = -1 * self.tableau[-1][:self.n_var]
            self.tableau[-1][-1] = -1 * self.tableau[-1][-1]

            self.append_column(1)
            self.create_variable("s")

            self.append_column(-1,add_to_Z=True)
            a = self.create_variable("a")
            self.basic_var.append(a)
        elif op == "=":
            self.append_column(1,add_to_Z=True)
            a = self.create_variable("a")
            self.basic_var.append(a)
        elif op == ">=":
            self.append_column(-1)
            self.create_variable("s")

            self.append_column(1,add_to_Z=True)
            a = self.create_variable("a")
            self.basic_var.append(a)
        else:
            raise("Only inequalities or equalities are admitted")

    def create_variable(self,type_var="x"):
        ''' 
        A new variable is created, with increasing index.
        It is added on the list of the other variables, and it is returned from the function,
        so it can be added to the pool of basic variables if wanted
        '''
        if type_var not in ("x","s","a"):
            raise("Variable can only be 'x','s'(slack) or 'a' (artificial)")
        idx = len([i[0] for i in self.variables if i[0] == type_var])
        new_var = type_var + str(idx+1)
        self.variables.append(new_var)
        return(new_var)

    def append_column(self, value, add_to_Z = False):
        # append a new column to the second to last column (the column before the "b" vector)
        # If add_to_Z is false, column is '[0 0 ... 0 value]' where "value" is in the last row of the tableau matrix
        # Otherwise, column is '[value 0 ... 0 value]', that is, in the objective function (as with artificial variables)
        self.tableau = np.insert(self.tableau, -1, 0, axis=1)
        self.tableau[-1][-2] = value
        if add_to_Z:
            self.tableau[0][-2] = value



    def solve(self):
        iter = 0
        # if there are artificial variables, obj function starts with only artificial variables
        has_artificial_variables = len([i for i in self.variables if i[0] == "a"]) > 0
        if has_artificial_variables:
            print("Start phase 1")
            original_Z = [i for i in self.tableau[0]]
            self.tableau[0][:self.n_var] = np.zeros((1, self.n_var))

            # before starting, make artificial variable "0" in obj function 
            # by subtracting from row 0 the rows with artificial variables
            for n,i in enumerate(self.variables):
                if i[0] == "a":
                    for m,j in enumerate(self.tableau[1:,n],1):
                        if j == 1:
                            self.tableau[0] -= self.tableau[m]
                            break
                            
        
        while  (self.tableau[0,:-1] < 0).any(): # keep going until no more coefficients in obj function is < 0
            print(f"Iteration: {iter}")
            col = np.argmin(self.tableau[0,:-1], axis=0)
            pivot_column = self.tableau[1:,col]

            # find pivot row
            min = float('inf')
            row = None
            b = self.tableau[1:, -1]
            for i in range(len(b)):
                v = pivot_column[i]
                if v <= 0:
                    continue
                
                ratio = b[i]/v

                if ratio < min:
                    min = ratio
                    row = i

            entering_variable = self.variables[col]
            leaving_variable = self.basic_var[row]
            print(f"Entering variable: {entering_variable}")
            print(f"Leaving variable: {leaving_variable}")

            self.basic_var.insert(row,entering_variable)
            self.basic_var.remove(leaving_variable)

            pivot_row = self.tableau[row+1]
            self.normalize_row(row+1,col)

            # make pivot column a null vector except with the pivoting element
            for i in range(len(self.tableau)):
                if i == row+1:
                    continue

                if self.tableau[i][col] > 0:
                    self.tableau[i] -= np.abs(self.tableau[i][col]) * self.tableau[row+1]
                else:
                    self.tableau[i] += np.abs(self.tableau[i][col]) * self.tableau[row+1]

            iter += 1
            print(self.tableau)

            if has_artificial_variables and not (self.tableau[0,:-1]< 0).any():
                # start phase 2
                # restore original obj function
                self.tableau[0] = original_Z

                # drop artificial variables columns from tableau
                artificial_var_idx = [n for n,i in enumerate(self.variables) if i[0] == "a"]
                rows = np.array(list(range(len(self.tableau))), dtype=np.intp)
                columns = np.array([i for i in range(len(self.tableau[0])) if i not in artificial_var_idx], dtype=np.intp)
                self.tableau = self.tableau[np.ix_(rows, columns)]

                # drop variables from list of variables
                self.variables = [i for i in self.variables if i[0] != "a"]

                has_artificial_variables = False

                # before starting, make basic variables as 0 in obj function
                for n,i in enumerate(self.variables):
                    if i in self.basic_var:
                        for m,j in enumerate(self.tableau[1:,n],1):
                            if j == 1:
                                self.tableau[0] -= self.tableau[0][n] * self.tableau[m]
                                break
                
    def multiply_row(self,row,value):
        self.tableau[row] *= value
        
    def normalize_row(self,row,col):
        '''
        Choose an element in a row. The row will be multiplied so that the chosen element will be 1 
        '''
        self.tableau[row] /= self.tableau[row][col] 

    def add_two_rows(self,row1,row2,value):
        self.tableau[row1] += value * self.tableau[row2]