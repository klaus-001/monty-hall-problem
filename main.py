import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate(num_doors: int, switch: bool) -> bool:
    car_position = np.random.randint(0, num_doors)

    player_choice = np.random.randint(0, num_doors)

    # Determine the doors that can be opened by the host
    available_doors = set(range(num_doors)) - {player_choice, car_position}
    doors_opened_by_host = np.random.choice(list(available_doors), size=min(num_doors - 2, len(available_doors)), replace=False)

    remaining_doors = set(range(num_doors)) - {player_choice} - set(doors_opened_by_host)

    if switch:
        player_choice = remaining_doors.pop()

    return player_choice == car_position

def run_trials(num_doors: int, trials: int) -> tuple:
    switch_wins = sum(simulate(num_doors, switch=True) for _ in range(trials))
    stay_wins = sum(simulate(num_doors, switch=False) for _ in range(trials))

    print(f'\n    Switching won {switch_wins:5} out of {trials} '
          f'({(switch_wins / trials * 100):.2f}% of the time)')
    print(f'Not Switching won {stay_wins:5} out of {trials} '
          f'({(stay_wins / trials * 100):.2f}% of the time)')

    return stay_wins, switch_wins

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--doors', default=3, type=int, metavar='int',
                        help='number of doors offered to contestant')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')

    args = parser.parse_args()

    print(f'Simulating {args.trials} trials...')
    
    results = []

    door_configs = [3, 10, 10000]
    for num_doors in door_configs:
        stay_wins, switch_wins = run_trials(num_doors, args.trials)
        results.append({
            'num_doors': num_doors,
            'stay_wins': stay_wins,
            'switch_wins': switch_wins,
            'stay_win_percentage': (stay_wins / args.trials) * 100,
            'switch_win_percentage': (switch_wins / args.trials) * 100
        })

    df_results = pd.DataFrame(results)

    print(df_results)

    plt.figure(figsize=(10, 6))
    plt.plot(df_results['num_doors'], df_results['stay_win_percentage'], label='Stay Win %', marker='o', c='red')
    plt.plot(df_results['num_doors'], df_results['switch_win_percentage'], label='Switch Win %', marker='o', c='blue')

    plt.title('Monty Hall Problem: Stay vs Switch Win Percentage')
    plt.xlabel('Number of Doors')
    plt.ylabel('Winning Percentage (%)')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)

    plt.show()
    
if __name__ == '__main__':
    main()