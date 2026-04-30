from abc import ABC, abstractmethod

from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    """Se lanza cuando una estrategia se usa con criatura incompatible."""
    pass


class BattleStrategy(ABC):
    """Estrategia abstracta: qué hace una criatura durante el torneo."""

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """True si esta estrategia es compatible con la criatura."""
        ...

    @abstractmethod
    def act(self, creature: Creature) -> None:
        """Ejecuta las acciones de combate. Lanza InvalidStrategyError
        si la criatura no es compatible."""
        ...


class NormalStrategy(BattleStrategy):
    """Válida para cualquier criatura, solo ataca."""

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    """Transforma, ataca potenciado, revierte. Requiere TransformCapability."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}'"
                " for this aggressive strategy"
            )
        assert isinstance(creature, TransformCapability)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    """Ataca y luego se cura. Requiere HealCapability."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}'"
                " for this defensive strategy"
            )
        print(creature.attack())
        assert isinstance(creature, HealCapability)
        print(creature.heal())
