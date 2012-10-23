# Write a function is_satisfied which takes as its input the number of
# variables, a Boolean formula and assignment of the variables and
# return True if the formula is satisfied by the assignment and False
# otherwise. The Boolean formula is expressed as followed.

# The number of variables is given as an integer num_variables
# (all variables are consecutively numbered from 1 to (num_variables)

# The Boolean formula will be represented as a list of list, clauses.
# Each inner list is a clause where the variable x_i is represented as
# i if it appears without a not, otherwise it is represented as -i

# For example, the Boolean Formula
# (x1 or x2 or not(x3)) and (x2 or not(x4)) and (not(x1) or x3 or x4)
# would translate into
#
#    num_variables = 4
#    clauses = [[1,2,-3],[2,-4],[-1,3,4]]


def is_satisfied(num_variables, clauses, assignment):
    for clause in clauses:
        for i in clause:
            a = assignment[i] if i > 0 else not assignment[-i]
            if a:
                break
        else:
            return False
    return True

def test():
    num_variables = 4
    clauses = [[1,2,-3],[2,-4],[-1,3,4]]
    assignment = [0,1,1,1,1]
    assert is_satisfied(num_variables, clauses, assignment)

    assignment = [0,1,0,1,1]
    assert not is_satisfied(num_variables, clauses, assignment)


test()
