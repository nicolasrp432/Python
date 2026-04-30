from abc import ABC, abstractmethod

from ex0.creature import Creature


class CreatureFactory(ABC):
    """Fábrica abstracta: contrato para crear criaturas."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Crea la criatura base de esta familia."""
        ...

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Crea la criatura evolucionada de esta familia."""
        ...
