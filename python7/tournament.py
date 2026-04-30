from ex0 import FlameFactory, AquaFactory
from ex0.factory import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)
from ex2.strategy import BattleStrategy


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    """Enfrenta cada par de oponentes una vez.
    Si una estrategia es inválida, el torneo se aborta.
    """
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    # Creamos las criaturas base de cada fábrica una sola vez.
    creatures = [
        (fac.create_base(), strat)
        for fac, strat in opponents
    ]

    # Enfrentamos cada par exactamente una vez (i < j evita duplicados).
    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            creature_i, strategy_i = creatures[i]
            creature_j, strategy_j = creatures[j]

            print()
            print("* Battle *")
            print(creature_i.describe())
            print(" vs.")
            print(creature_j.describe())
            print(" now fight!")

            try:
                strategy_i.act(creature_i)
                strategy_j.act(creature_j)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    flame = FlameFactory()
    aqua = AquaFactory()
    healing = HealingCreatureFactory()
    transform = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    # Torneo 0: caso básico con dos oponentes compatibles con sus estrategias.
    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame, normal), (healing, defensive)])

    print()

    # Torneo 1: caso de error — Flameling no tiene TransformCapability,
    # por lo que AggressiveStrategy es inválida para él.
    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame, aggressive), (healing, defensive)])

    print()

    # Torneo 2: tres oponentes, cada uno con una estrategia diferente.
    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([(aqua, normal), (healing, defensive), (transform, aggressive)])
