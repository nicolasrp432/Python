from ex0.creature import Creature
from ex0.factory import CreatureFactory
from ex1.capabilities import TransformCapability


class Shiftling(Creature, TransformCapability):
    """Criatura base transformadora. _transformed cambia el attack()."""

    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self._transformed:
            return "Shiftling performs a boosted strike!"
        return "Shiftling attacks normally."

    def transform(self) -> str:
        self._transformed = True
        return "Shiftling shifts into a sharper form!"

    def revert(self) -> str:
        self._transformed = False
        return "Shiftling returns to normal."


class Morphagon(Creature, TransformCapability):
    """Criatura evolucionada de la familia transformadora."""

    def __init__(self) -> None:
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self._transformed:
            return "Morphagon unleashes a devastating morph strike!"
        return "Morphagon attacks normally."

    def transform(self) -> str:
        self._transformed = True
        return "Morphagon morphs into a dragonic battle form!"

    def revert(self) -> str:
        self._transformed = False
        return "Morphagon stabilizes its form."


class TransformCreatureFactory(CreatureFactory):
    """Fábrica transformadora: Shiftling (base) y Morphagon (evolucionada)."""

    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
