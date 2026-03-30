import sys


def score_analytics() -> None:
    print("=== Player Score Analytics ===")

    valid_scores = []

    for arg in sys.argv[1:]:
        try:
            score = int(arg)
            valid_scores.append(score)
        except ValueError:
            print(f"Invalid parameter: '{arg}'")

    if len(valid_scores) == 0:
        print("No scores provided. Usage: python3)"
              "(ft_score_analytics.py <score1> <score2>")
        return

    total_players = len(valid_scores)
    total_score = sum(valid_scores)
    average = total_score / total_players
    high_score = max(valid_scores)
    low_score = min(valid_scores)
    score_range = high_score - low_score

    print(f"Scores processed: {valid_scores}")
    print(f"Total players: {total_players}")
    print(f"Total score: {total_score}")
    print(f"Average score: {average}")
    print(f"High score: {high_score}")
    print(f"Low score: {low_score}")
    print(f"Score range: {score_range}")


if __name__ == "__main__":
    score_analytics()
