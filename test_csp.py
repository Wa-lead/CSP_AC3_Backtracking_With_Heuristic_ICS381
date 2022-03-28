if __name__ == "__main__":    
    from csp import *
    
    # tests 1: australia map
    variables = set(['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T'])
    colors = set(['red', 'green', 'blue'])
    adjacency = {'WA': ['NT', 'SA'],
                 'NT': ['WA', 'SA', 'Q'],
                 'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
                 'Q': ['NT', 'SA', 'NSW'],
                 'NSW': ['Q', 'SA', 'V'],
                 'V': ['SA', 'NSW'], 
                 'T': []}
    graphcolorcsp = GraphColorCSP(variables, colors, adjacency)
    
    print(graphcolorcsp.diff_satisfied('WA', 'green', 'SA', 'green')) # False
    print(graphcolorcsp.diff_satisfied('WA', 'green', 'SA', 'red'))   # True
    print(graphcolorcsp.diff_satisfied('WA', 'green', 'T', 'green'))  # True
    print('_______________________________________________________________________')
    
    # test 2: check is_goal and partial       
    complete_inconsistent_assignment = {'WA': 'red', 'NT': 'red', 'SA': 'blue', 
                                        'Q': 'blue', 'NSW': 'green', 'V': 'green', 'T': 'green'}
    complete_consistent_assignment = {'WA': 'red', 'NT': 'green', 'SA': 'blue', 
                                      'Q': 'red', 'NSW': 'green', 'V': 'red', 'T': 'green'}
    print(graphcolorcsp.is_goal(complete_inconsistent_assignment)) # False
    print(graphcolorcsp.is_goal(complete_consistent_assignment)) # True
    print('_______________________________________________________________________')
    
    partial_inconsistent_assignment = {'NT': 'blue', 'SA': 'blue', 'T': 'green'}
    partial_consistent_assignment = {'WA': 'red', 'NT': 'green', 'T': 'green'}
    print(graphcolorcsp.check_partial_assignment(partial_inconsistent_assignment)) # False
    print(graphcolorcsp.check_partial_assignment(partial_consistent_assignment)) # True
    print('_______________________________________________________________________')
    
    # tests 3: run ac3 on graphcolorcsp; 
    is_consistent, updated_domains = ac3(graphcolorcsp)
    print(is_consistent, updated_domains) # should return true and not reduce the domain
    # run ac3 from example in slide 45 to 48
    # we just assigned Q = green
    # ac3 should detect inconsistency
    print('Testing AC3 with inconsistenct example:')
    assignment = {'Q': 'green', 'WA': 'red'}
    current_domains = {'WA': ['red'], 'NT': ['green', 'blue'], 'Q': ['green'],
                       'NSW': ['red', 'blue'], 'V': ['red', 'green', 'blue'], 
                       'SA': ['green', 'blue'], 'T': ['red', 'green', 'blue']}
    
    arcs_queue = [(n, 'Q') for n in graphcolorcsp.adjacency['Q'] if n not in assignment]
    is_consistent, reduced_domains = ac3(graphcolorcsp, arcs_queue=arcs_queue, current_domains=current_domains, assignment=assignment)
    print(is_consistent, reduced_domains) # False, update domains
    # note there are multiple variables whose domain can go to zero, and so which one your ac3 implementation detects first 
    # will effect what result your algorithm will spit out. the autograder will just check the True/False output. 
    print('_______________________________________________________________________')
    
    # tests 4: run backtracking search; for my implementation I used MRV+Degree+LCV+AC3. 
    #          for your implementation you might get different complete consistent assignment which is okay.
    #          the autograder will just check that the assignment is complete and consistent;
    #          in case there is no possible solution, the autograder will check None.
    import time
    start_time = time.time()
    sol_assignment = backtracking(graphcolorcsp)
    end_time = time.time()
    is_complete_and_consistent = graphcolorcsp.is_goal(sol_assignment)
    print('Sol: {}'.format(sol_assignment))
    print('Is sol complete and consistent: {}'.format(is_complete_and_consistent))
    print('Time taken: {} sec'.format(end_time - start_time))
    print('_______________________________________________________________________')