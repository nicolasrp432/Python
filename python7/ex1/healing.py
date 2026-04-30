from ex0.creature import Creature
from ex0.factory import CreatureFactory
from ex1.capabilities import HealCapability


class Sproutling(Creature, HealCapability):
    """Criatura base curativa. Hereda de Creature y HealCapability."""

    def __init__(self) -> None:
        # Llamamos explícitamente a Creature.__init__ porque con
        # herencia múltiple super() sigue el MRO y puede no
        # inicializar lo que esperamos.
        Creature.__init__(self, "Sproutling", "Grass")

    def attack(self) -> str:
        return "Sproutling uses Vine Whip!"

    def heal(self) -> str:
        return "Sproutling heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    """Criatura evolucionada de la familia curativa."""

    def __init__(self) -> None:
        Creature.__init__(self, "Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        return "Bloomelle uses Petal Dance!"

    def heal(self) -> str:
        return "Bloomelle heals itself and others for a large amount"


class HealingCreatureFactory(CreatureFactory):
    """Fábrica curativa: Sproutling (base) y Bloomelle (evolucionada)."""

    def create_base(self) -> Creature:
        return Sproutling()

    def create_evolved(self) -> Creature:
        return Bloomelle()
