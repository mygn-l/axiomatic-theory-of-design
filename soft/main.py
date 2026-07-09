from atdm import *

# Physics
particle = ATDM_Object("A", ("position", (0, 0, 0)), ("velocity", (0, 0, 0)))
earth = ATDM_Object("earth", ("g", 9.8))

nature = Nature_Prime(particle, earth)
environment = Environment(particle, nature)
print(environment.equals(earth))

gravitational_force = Actions(particle, environment)

# Physics 2
spring = ATDM_Object("Spring", ("k", 5), ("length", 1))
weight = ATDM_Object("Weight", ("force", 10))

nature = Nature_Prime(spring, weight)
environment = Environment(spring, nature)
print(environment.equals(weight))

compression = Actions(spring, environment)
push_on_weight = Responses(spring, environment)

# Chemistry
hydrogen1 = ATDM_Object("H1", ("proton", 1), ("neutron", 0), ("electron", 1))
hydrogen2 = ATDM_Object("H2", ("proton", 1), ("neutron", 0), ("electron", 1))
oxygen = ATDM_Object("O", ("proton", 8), ("neutron", 8), ("electron", 8))
water = oxygen.get_union("H2O", hydrogen1, hydrogen2)
lab = ATDM_Object("lab", ("temperature", 20))

covalent_bond1 = Relation(hydrogen1, oxygen).get_union("covalent_bond1", Relation(oxygen, hydrogen1))
covalent_bond2 = Relation(hydrogen2, oxygen).get_union("covalent_bond1", Relation(oxygen, hydrogen2))

nature = Nature_Prime(water, lab)
chem_environment = Environment(water, nature)
print(chem_environment.equals(lab))

heat = Actions(water, chem_environment)
vaporization = Responses(water, chem_environment)

# Chemistry 2
acid = ATDM_Object("Acid", ("pH", 3))
base = ATDM_Object("Base", ("pH", 10))
water = ATDM_Object("Water", ("pH", 7))
solution = water.get_union("solution", acid)
lab = ATDM_Object("lab", ("temperature", 20))

nature = Nature_Prime(solution, base, lab)
solution_environment = Environment(solution, nature)

addition_of_base = Actions(solution, solution_environment)
reaction_and_heat = Responses(solution, solution_environment)

# Biology
nucleus = ATDM_Object("Nucleus", ("function", "stores genetic information"))
cell_membrane = ATDM_Object("Cell Membrane", ("function", "regulates transport"))
cytoplasm = ATDM_Object("Cytoplasm", ("function", "intracellular matrix"))
mitochondria = ATDM_Object("Mitochondria", ("function", "ATP production"))
ribosome = ATDM_Object("Ribosome", ("function", "protein synthesis"))
golgi = ATDM_Object("Golgi", ("function", "packaging"))
cytoplasm.insert_child(mitochondria)
cytoplasm.insert_child(ribosome)
cytoplasm.insert_child(golgi)
cell = cytoplasm.get_union("Cell", nucleus, cell_membrane)

nature = Nature_Prime(cell)
nucleus_environment = Environment(nucleus, nature)

gene_regulation = Actions(nucleus, nucleus_environment)
gene_expression = Responses(nucleus, nucleus_environment)

# Biology 2
prey_population = ATDM_Object("Prey population", ("qty", 100))
predator_population = ATDM_Object("Predator population", ("qty", 5))
forest = ATDM_Object("Forest", ("area", 10000))

nature = Nature_Prime(prey_population, predator_population, forest)
prey_environment = Environment(prey_population, nature)

hunting = Actions(prey_population, prey_environment)
reproduction = Responses(prey_environment, prey_environment)

# History
renaissance_people = ATDM_Object("Renaissance people", ("description", "people living during renaissance times"))
greek_philosophy = ATDM_Object("Greek philosophy", ("description", "Classical Greek philosophy"))
natural_philosophy = ATDM_Object("Natural philosophy", ("description", "Old term for science"))

renaissance_cultural_sphere = Nature_Prime(renaissance_people, greek_philosophy, natural_philosophy)
people_environment = Environment(renaissance_people, renaissance_cultural_sphere)

greek_introduced = Actions(renaissance_people, people_environment)
scientific_revolution = Responses(renaissance_people, people_environment)

# Math
function = ATDM_Object("Function", ("definition", "relation where y is unique for a given x"))
kolmogorov_complexity = ATDM_Object("Kolmogorov Complexity", ("definition", "information content"))

nature = Nature_Prime(function, kolmogorov_complexity)
function_environment = Environment(function, nature)
print(function_environment.equals(kolmogorov_complexity))

K = Responses(function, function_environment)
inverse_K = Actions(function, function_environment)
