import random


def gen_player_achievements() -> set[str]:
    master_list = [
        'Crafting Genius', 'Strategist', 'World Savior', 'Speed Runner',
        'Survivor', 'Master Explorer', 'Treasure Hunter', 'Unstoppable',
        'First Steps', 'Collector Supreme', 'Untouchable', 'Sharp Mind',
        'Boss Slayer', 'Hidden Path Finder'
    ]
    num_achievements = random.randint(5, 10)
    chosen_achievements = random.sample(master_list, num_achievements)
    return set(chosen_achievements)


def achievement_tracker() -> None:
    print("=== Achievement Tracker System ===")

    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()

    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}\n")

    all_distinct = alice.union(bob, charlie, dylan)
    print(f"All distinct achievements: {all_distinct}\n")

    common = alice.intersection(bob, charlie, dylan)
    print(f"Common achievements: {common}\n")

    print(f"Only Alice has: {alice.difference(bob, charlie, dylan)}")
    print(f"Only Bob has: {bob.difference(alice, charlie, dylan)}")
    print(f"Only Charlie has: {charlie.difference(alice, bob, dylan)}")
    print(f"Only Dylan has: {dylan.difference(alice, bob, charlie)}\n")

    print(f"Alice is missing: {all_distinct.difference(alice)}")
    print(f"Bob is missing: {all_distinct.difference(bob)}")
    print(f"Charlie is missing: {all_distinct.difference(charlie)}")
    print(f"Dylan is missing: {all_distinct.difference(dylan)}")


if __name__ == "__main__":
    achievement_tracker()
