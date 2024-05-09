import pytest

from PourPy import PourbaixDiagram, System, Database
from custom_database import species


@pytest.fixture
def chemical_system():
    db = Database.from_default(species)
    system = System()
    system.set_database(db)

    system.temperature = 298.15
    system.pressure = 1
    system.pHs = (5, 14)
    system.electrode_potentials = (-2, 2)
    system.reference_electrode = ("SHE",1.0)

    system.add_elements(["O","H","Fe","C"])
    system.set_aqueous_activity("Fe", 1e-5)
    system.set_aqueous_activity("C", 1e-3)


    reactions = ('2H|+1| + 2e|-1| -> H2',
                 'O2 + 4H|+1| + 4e|-1| -> 2H2O',
                 'Fe -> Fe|+2| + 2e|-1|',
                 'Fe|+2| -> Fe|+3| + e|-1|',
                 'Fe|+2| + 2H2O -> Fe(OH)2 + 2H|+1|',
                 '3Fe|+2| + 4H2O -> Fe3O4 + 8H|+1| + 2e|-1|',
                 'Fe + 2H2O -> Fe(OH)2 + 2H|+1| + 2e|-1|',
                 '3Fe(OH)2 -> Fe3O4 + 2H2O + 2H|+1| + 2e|-1|',
                 '2Fe3O4 + H2O -> 3Fe2O3 + 2H|+1| + 2e|-1|',
                 'Fe|+3| + 1.5H2O -> 0.5Fe2O3 + 3H|+1|',
                 'Fe|+2| + 1.5H2O -> 0.5Fe2O3 + 3H|+1| + e|-1|'
                 )

    system.add_reactions(reactions)


    return system

def test_unique_const(chemical_system: System):
    diagram = PourbaixDiagram(chemical_system)
    unique_const = diagram._get_unique_constitutents()

    correct_unique_const = ['Fe', 'Fe|+2|', 'Fe(OH)2', 'Fe3O4', 'Fe2O3']

    for constituent in unique_const.keys():
        assert constituent.formula in correct_unique_const

            
def test_intersection(chemical_system: System):
    diagram = PourbaixDiagram(chemical_system)
    unique_const = diagram._get_unique_constitutents()
    diagram._compute_intersections(unique_const)
    diagram._compute_boundary_lines(chemical_system)
