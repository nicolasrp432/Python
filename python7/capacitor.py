from ex0.factory import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


def test_healing_factory(factory: CreatureFactory) -> None:
    """Prueba una fábrica curativa: describe, ataca y cura."""
    print("Testing Creature with healing capability")
    for label, creature in [
        (" base:", factory.create_base()),
        (" evolved:", factory.create_evolved()),
    ]:
        print(label)
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, HealCapability):
            print(creature.heal())


def test_transform_factory(factory: CreatureFactory) -> None:
    """Prueba una fábrica transformadora: describe, ataca, transforma,
    ataca de nuevo y revierte."""
    print("Testing Creature with transform capability")
    for label, creature in [
        (" base:", factory.create_base()),
        (" evolved:", factory.create_evolved()),
    ]:
        print(label)
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())


if __name__ == "__main__":
    healing = HealingCreatureFactory()
    transform = TransformCreatureFactory()

    test_healing_factory(healing)
    print()
    test_transform_factory(transform)
