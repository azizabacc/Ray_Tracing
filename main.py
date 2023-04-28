from raytracing import Raytracing
from transmitter import Transmitter
from receiver import Receiver
from wall import Wall
import pyomo.environ as pyo


def list_of_receivers_creation(raytracing, len_x, len_y, n):
    """
    insertion of receivers in the room, along x-axis w/ 1 receiver every 1/len_x metres,
     along y-axis w/ 1 receiver every 1/len_y metres
    """

    x_min = x_max = y_min = y_max = 0
    for wall in raytracing.wall_list:
        if x_max < wall.point_list[0][0]:
            x_max = wall.point_list[0][0]
        if x_max < wall.point_list[1][0]:
            x_max = wall.point_list[1][0]
        if x_min > wall.point_list[0][0]:
            x_min = wall.point_list[0][0]
        if x_min > wall.point_list[1][0]:
            x_min = wall.point_list[1][0]
        if y_max < wall.point_list[0][1]:
            y_max = wall.point_list[0][1]
        if y_max < wall.point_list[1][1]:
            y_max = wall.point_list[1][1]
        if y_min > wall.point_list[0][1]:
            y_min = wall.point_list[0][1]
        if y_min > wall.point_list[1][1]:
            y_min = wall.point_list[1][1]

    len_x = len_x
    len_y = len_y
    receiver = []
    for i in range(x_min, len_x * (x_max - x_min), n * 200):
        for j in range(y_min, len_y * (y_max - y_min), n * 110):
            receiver.append(Receiver((x_min + (i+1) / len_x, y_min + (j+1) / len_y), "half_wave"))

    return receiver


def wall_creation():
    # building of room
    mur1 = Wall(0.5, [(0, 45), (0, 110)], "concrete")
    mur2 = Wall(0.5, [(0, 110), (35, 110), (165, 110), (200, 110)], "concrete")
    mur3 = Wall(0.5, [(200, 110), (200, 45)], "concrete")
    mur4 = Wall(0.5, [(0, 45), (10, 45), (190, 45), (200, 45)], "concrete")
    mur5 = Wall(0.5, [(190, 10), (190, 45)], "concrete")
    mur6 = Wall(0.5, [(10, 10), (35, 10)], "concrete")
    mur7 = Wall(0.5, [(165, 10), (190, 10)], "concrete")
    mur8 = Wall(0.5, [(10, 10), (10, 45)], "concrete")
    mur9 = Wall(0.5, [(35, 10), (35, 20), (35, 100), (35, 110)], "concrete")
    mur10 = Wall(0.5, [(35, 20), (90, 20), (110, 20), (165, 20)], "concrete")
    mur11 = Wall(0.5, [(35, 100), (95, 100), (105, 100), (165, 100)], "concrete")
    mur12 = Wall(0.5, [(165, 10), (165, 20), (165, 100), (165, 110)], "concrete")
    mur13 = Wall(0.5, [(85, 0), (115, 0)], "concrete")
    mur14 = Wall(0.5, [(85, 0), (85, 15)], "concrete")
    mur15 = Wall(0.5, [(85, 15), (90, 15), (110, 15), (115, 15)], "concrete")
    mur16 = Wall(0.5, [(90, 15), (90, 20)], "concrete")
    mur17 = Wall(0.5, [(110, 15), (110, 20)], "concrete")
    mur18 = Wall(0.5, [(115, 0), (115, 15)], "concrete")
    murint1 = Wall(0.5, [(10, 35), (13, 35), (15, 35), (35, 35)], "brick")
    murint2 = Wall(0.5, [(35, 20), (35, 35), (35, 45), (35, 80)], "brick")
    murint3 = Wall(0.5, [(10, 45), (13, 45), (15, 45), (35, 45), (110, 45), (140, 45), (165, 45), (185, 45), (187, 45),
                         (190, 45)], "brick")
    murint4 = Wall(0.5, [(90, 30), (110, 30)], "brick")
    murint5 = Wall(0.5, [(35, 60), (85, 60), (90, 60), (95, 60), (105, 60), (140, 60)], "brick")
    murint6 = Wall(0.5,
                   [(0, 80), (5, 80), (10, 80), (35, 80), (37, 80), (68, 80), (70, 80), (95, 80), (105, 80), (120, 80),
                    (125, 80), (175, 80)], "brick")
    murint7 = Wall(0.5, [(30, 80), (30, 95)], "brick")
    murint8 = Wall(0.5, [(75, 80), (75, 85), (75, 95), (75, 100)], "brick")
    murint9 = Wall(0.5, [(85, 60), (85, 70)], "brick")
    murint10 = Wall(0.5, [(90, 30), (90, 40), (90, 45), (90, 60)], "brick")
    murint11 = Wall(0.5, [(95, 60), (95, 80)], "brick")
    murint12 = Wall(0.5, [(105, 60), (105, 80)], "brick")
    murint13 = Wall(0.5, [(110, 30), (110, 40), (110, 45), (110, 52), (110, 54), (110, 60)], "brick")
    murint14 = Wall(0.5, [(110, 40), (140, 40)], "brick")
    murint15 = Wall(0.5, [(125, 80), (125, 85), (125, 95), (125, 100)], "brick")
    murint16 = Wall(0.5, [(140, 20), (140, 40), (140, 45), (140, 50), (140, 60), (140, 70)], "brick")
    murint17 = Wall(0.5, [(140, 50), (150, 50), (152, 50), (160, 50)], "brick")
    murint18 = Wall(0.5, [(165, 20), (165, 30), (165, 40), (165, 45)], "brick")
    murint19 = Wall(0.5, [(140, 70), (160, 70)], "brick")
    murint20 = Wall(0.5, [(160, 50), (160, 70)], "brick")
    murint21 = Wall(0.5, [(175, 45), (175, 80)], "brick")

    wall_list = [mur1, mur2, mur3, mur4, mur5, mur6, mur7, mur8, mur9, mur10, mur11, mur12, mur13, mur14, mur15, mur16,
                 mur17, mur18, murint1, murint2, murint3, murint4, murint5, murint6, murint7, murint8, murint9,
                 murint10, murint11, murint12, murint13, murint14, murint15, murint16, murint17, murint18, murint19,
                 murint20, murint21]
    return wall_list


raytracing = Raytracing()

# building of Wall_list
wall_list = wall_creation()
raytracing.wall_list = wall_list

# ADD the transmitter in the area
transmitter = Transmitter((100, 65), "half_wave")
raytracing.transmitter_list.append(transmitter)

# ADD the receivers in the area
raytracing.receiver_list = list_of_receivers_creation(raytracing, 200, 110, 5)

# RAYTRACING
raytracing.ray_power_distribution((0.005, 50.00909090909091), 1, "multipath")


def optimization_problem(discretisation_level=10, threshold=70):
    """ finds minimum number of transmitter and their position to complete a minimum mean bit rate everywhere in a given area
    discretization_level: modulate the number of receivers placed in an area max 5, min 1, must be an integer
    threshold: minimum bit rate to complete
    """

    wall_list = wall_creation()
    dummy_object = Raytracing()
    dummy_object.wall_list = wall_list
    dummy_object.receiver_list = list_of_receivers_creation(dummy_object, 200, 110, discretisation_level)

    tx_loc = []  # Contains all possibilities of one transmitter placement over the considered area
    for i in range(len(dummy_object.receiver_list)):  # for each possible receiver position, we create Raytracing() object
        tx_loc.append(Raytracing())  # which has one and only one transmitter at the positon of one receiver
        tx_loc[i].wall_list = wall_list
        own_transmitter = Transmitter(dummy_object.receiver_list[i].position, "half_wave")
        tx_loc[i].transmitter_list.append(own_transmitter)
        tx_loc[i].receiver_list = list_of_receivers_creation(tx_loc[i], 200, 110, discretisation_level)

    bit_rate_distribution = []  # list containing the bit rate distribution for each position of transmitter
    x, y = tx_loc[0].ray_bit_rate_distribution()[0], tx_loc[0].ray_bit_rate_distribution()[1]  # list of corresponding positions for each bit rate (same lists for all objects)
    for i in tx_loc:
        bit_rate_distribution.append(i.ray_bit_rate_distribution()[2])  # appending of bit rates

    # linear problem resolution
    model = pyo.AbstractModel()

    model.m = pyo.Param(within=pyo.NonNegativeIntegers)  # number of discretisation points (max index)
    model.n = pyo.Param(within=pyo.NonNegativeIntegers)

    model.I = pyo.RangeSet(1, model.m)  # indexes for parameters and variables
    model.J = pyo.RangeSet(1, model.n)

    def x_init(model, i, j):
        return bit_rate_distribution[i - 1][j - 1]

    def a_init(model, i):
        return 0

    model.x = pyo.Param(model.I, model.J, initialize=x_init)  # variables of the LP

    model.a = pyo.Var(model.I, domain=pyo.Binary, initialize=a_init)  # parameters of the LP

    def obj_expression(m):  # definition of objective function
        return pyo.summation(m.a)

    model.OBJ = pyo.Objective(rule=obj_expression)  # setting of objective for pyo model (minimizes the expression by default)

    def ax_constraint_rule(m, j):  # definition of constraints: minimum bit rate = 70 mb/s
        # return the expression for the constraint for i
        return sum(m.x[i, j] * m.a[i] for i in m.I) >= threshold

    model.AxbConstraint = pyo.Constraint(model.J, rule=ax_constraint_rule)

    model.m = len(bit_rate_distribution)
    model.n = len(bit_rate_distribution[0])

    print('starting LP solving')
    instance = model.create_instance()  # assigning ConcretModel to abstract model
    opt = pyo.SolverFactory('glpk')  # solver used is glpk
    opt.solve(instance)
    results = opt.solve(instance, tee=True)

    optimal_position = []
    for i in range(len(bit_rate_distribution[0])):  # gathering coefficient ==1 => put a TX at the place denoted by the coefficient
        if pyo.value(instance.a[i + 1]):
            optimal_position.append(i)

    optimal_solution = Raytracing()  # creating a display of the optimal solution
    optimal_solution.wall_list = wall_list
    optimal_solution.receiver_list = list_of_receivers_creation(optimal_solution, 200, 110, 1)


    for i in optimal_position:
        optimal_solution.transmitter_list.extend(tx_loc[i].transmitter_list)

    optimal_solution.ray_power_distribution((0, 0), 0, 'mean')


# Optimization problem :
optimization_problem(10, 70)
