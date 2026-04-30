from abc import ABC, abstractmethod


class Creature(ABC):
    """Clase base abstracta para todas las criaturas del juego."""

    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.creature_type = creature_type

    @abstractmethod
    def attack(self) -> str:
        """Cada criatura concreta define su propio ataque."""
        ...

    def describe(self) -> str:
        """Método concreto: todas las criaturas se describen igual."""
        return f"{self.name} is a {self.creature_type} type Creature"
