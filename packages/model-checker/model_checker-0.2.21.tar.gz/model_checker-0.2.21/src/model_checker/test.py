from model_structure import *


"don't delete this file yet, I'll delete it once I'm done debugging"
################################
########## SETTINGS ############
################################

# length of bitvectors
N = 3

# print all Z3 constraints if a model is found
print_cons_bool = False

# print core unsatisfiable Z3 constraints if no model exists
print_unsat_core_bool = False

# present option to append output to file
save_bool = False

# use constraints to find models in stead of premises and conclusions
use_constraints_bool = False

################################
############ SYNTAX ############
################################

### SENTENCES ###

# 'A', 'B', 'C',... can be used for sentence letters

# Alternatively, 'RedBall', 'MarySings',... can be used for sentence letters.

# 'top' is a designated sentence for the trivial truth verified by everything and falsified by nothing.


### UNARY OPERATORS ###

# Negation: 'neg', e.g., 'neg A'.
# Necessity: 'Box', e.g., 'Box A'.
# Possibility: 'Diamond', e.g., 'Diamond RedBall'. 


### BINARY OPERATORS ###

# Conjunction: 'wedge', e.g., '(A wedge B)'
# Disjunction: 'vee', e.g., '(A vee B)'
# Conditional: 'rightarrow', e.g., '(A rightarrow B)'
# Biconditional: 'leftrightarrow', e.g., '(A leftrightarrow B)'
# Counterfactual: 'boxright', e.g., '(A boxright B)' where 'A' cannot include 'Box', 'Diamond', or 'boxright'.

# NOTE: parentheses must always be included for binary operators.


################################
########## ARGUMENTS ###########
################################

### INVALID ###

premises = ['\\top']
conclusions = ['A']

### VALID ###

premises = ['((A vee B) boxright C)']
conclusions = ['(A boxright C)']

# premises = ['(A \\boxright B)','((A \\wedge B) \\boxright C)']
# conclusions = ['(A \\boxright C)']

# premises = ['(A \\boxright (B \\wedge C))']
# conclusions = ['(A \\boxright B)']
# premises = ['((A \\vee B) \\boxright C)']
# conclusions = ['(A \\boxright C)']

premises = ['(A \\boxright B)','(B \\boxright C)']
conclusions = ['(A \\boxright C)']

premises = ['(A \\boxright ((B \\boxright C) \\wedge (D \\boxright E)))']
conclusions = ['C']

# premises = ['(A \\boxright (B \\boxright C))']
# conclusions = ['B']


mod = make_model_for(N)(premises, conclusions)
mod.solve()
mod.print_to(print_cons_bool, print_unsat_core_bool)
# for prop in mod.all_propositions:
#     mod.rec_print()
for cf_prop in mod.counterfactual_propositions:
    print((cf_prop['worlds cf true at'], cf_prop['worlds cf false at']))

for infix_sent in premises:
    prop = mod.find_proposition_object(infix_sent)
    print(prop)

prop_list = mod.find_propositions(premises+conclusions)
print(prop_list)