import pyomo.environ as pyo
from raytracing import Raytracing
from transmitter import Transmitter
from main import list_of_receivers_creation
from main import wall_creation

def optimization_problem(discretization_level=5,threshold=70):
    """ finds minimum number of transmitter and their position to complete a minimum mean bit rate everywhere in a given area
    discretization_level: modulate the number of receivers placed in an area max 5, min 1, must be an integer
    threshold: minimum bit rate to complete
    """


    wall_list= wall_creation()
    dummy_object = Raytracing()
    dummy_object.wall_list = wall_list
    dummy_object.receiver_list = list_of_receivers_creation(dummy_object, 200, 110, 5)

    tx_loc = []     #Contains all possibilities of one transmitter placement over the considered area
    for i in range(len(dummy_object.receiver_list)):                              #for each possible receiver position, we create Raytracing() object
        tx_loc.append(Raytracing())                                               # which has one and only one transmitter at the positon of one receiver
        tx_loc[i].wall_list=wall_list
        own_transmitter = Transmitter(dummy_object.receiver_list[i].position, "half_wave")
        tx_loc[i].transmitter_list.append(own_transmitter)
        tx_loc[i].receiver_list= list_of_receivers_creation(tx_loc[i],200,110,discretization_level)

    bit_rate_distribution = []                                                   #list cotaining the bit rate distribution for each position of transmitter
    x,y = tx_loc[0].ray_bit_rate_distribution()[0], tx_loc[0].ray_bit_rate_distribution()[1]    #list of corresponding positions for each bit rate (same lists for all objects)
    for i in tx_loc:
        bit_rate_distribution.append(i.ray_bit_rate_distribution()[2])          #appending of bit rates

    #linear problem resolution
    model = pyo.AbstractModel()

    model.m = pyo.Param(within=pyo.NonNegativeIntegers)      #number of discretisation points (max index)
    model.n = pyo.Param(within=pyo.NonNegativeIntegers)

    model.I = pyo.RangeSet(1, model.m )         #indexes for parameters and variables
    model.J = pyo.RangeSet(1, model.n )

    def x_init(model, i, j):
        return bit_rate_distribution[i-1][j-1]

    def a_init(model,i):
        return 0

    model.x = pyo.Param(model.I, model.J, initialize=x_init)           #variables of the LP

    model.a = pyo.Var(model.I, domain=pyo.Binary, initialize=a_init)   #parameters of the LP

    def obj_expression(m):                          # definition of objective function
        return pyo.summation(m.a)

    model.OBJ = pyo.Objective(rule=obj_expression)   #setting of objective for pyo model (minimizes the expression by default)

    def ax_constraint_rule(m, j):                         #definition of constraints: minimum bit rate = 70 mb/s
        # return the expression for the constraint for i
        return sum(m.x[i,j] * m.a[i] for i in m.I) >= threshold

    model.AxbConstraint = pyo.Constraint(model.J, rule=ax_constraint_rule)

    model.m = len(bit_rate_distribution)
    model.n = len(bit_rate_distribution[0])

    instance = model.create_instance()            #assigning ConcretModel to abstract model
    opt = pyo.SolverFactory('glpk')               # solver used is glpk
    opt.solve(instance)

    results = opt.solve(instance, tee=True)       #display of solutions

    optimal_position=[]
    for i in range(len(bit_rate_distribution[0])):
        if pyo.value(instance.a[i+1]) :
            optimal_position.append(i)

    optimal_solution = Raytracing()
    optimal_solution.wall_list=wall_list
    optimal_solution.receiver_list=list_of_receivers_creation(optimal_solution,200,110,3)

    for i in optimal_position:
        optimal_solution.transmitter_list.extend(tx_loc[i].transmitter_list)
    optimal_solution.ray_power_distribution((0,0), 0, 'mean')

