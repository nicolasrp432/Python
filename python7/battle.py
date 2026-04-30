from ex0 import FlameFactory, AquaFactory
from ex0.factory import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    """Crea base y evolucionada, las describe y las hace atacar."""
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    """Enfrenta las criaturas base de dos fábricas distintas."""
    print("Testing battle")
    creature1 = factory1.create_base()
    creature2 = factory2.create_base()
    print(creature1.describe())
    print(" vs.")
    print(creature2.describe())
    print(" fight!")
    print(creature1.attack())
    print(creature2.attack())


if __name__ == "__main__":
    flame = FlameFactory()
    aqua = AquaFactory()

    test_factory(flame)
    print()
    test_factory(aqua)
    print()
    test_battle(flame, aqua)
