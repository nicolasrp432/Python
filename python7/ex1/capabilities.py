from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Mixin abstracto de curación. No hereda de Creature."""

    @abstractmethod
    def heal(self) -> str:
        """Retorna el mensaje de curación de esta criatura."""
        ...


class TransformCapability(ABC):
    """Mixin abstracto de transformación con estado persistente."""

    def __init__(self) -> None:
        # _transformed indica si la criatura está transformada.
        # Afecta directamente al comportamiento de attack().
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        """Activa la transformación (_transformed = True)."""
        ...

    @abstractmethod
    def revert(self) -> str:
        """Revierte la transformación (_transformed = False)."""
        ...
