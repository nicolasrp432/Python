def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def count(day, limit):
        if day > limit:
            print("Harvest time!")
        else:
            print(f"Day {day}")
            count(day + 1, limit)
    count(1, days)
