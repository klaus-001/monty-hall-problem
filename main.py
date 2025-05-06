import argparse
import random
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

def simulate(num_doors: int, switch: bool, verbose: bool) -> bool:
    winning_door = random.randint(1, num_doors)
    if verbose:
        print(f'The prize is behind door {winning_door}.')

    choice = random.randint(1, num_doors)
    if verbose:
        print(f'Contestant chooses door {choice}.')

    closed_doors: List[int] = list(range(1, num_doors + 1))

    # Host opens doors
    while len(closed_doors) > 2:
        door_to_open = random.choice(closed_doors)
        if door_to_open in (winning_door, choice):
            continue
        closed_doors.remove(door_to_open)
        if verbose:
            print(f'The host opens door {door_to_open}.')

    assert len(closed_doors) == 2

    if switch:
        available_doors = [door for door in closed_doors if door != choice]
        previous_choice = choice
        choice = available_doors[0]
        if verbose:
            print(f'Contestant switches from door {previous_choice} to {choice}.')
    else:
        if verbose:
            print('Contestant does not switch doors.')

    won = (choice == winning_door)
    if verbose:
        print('Contestant WON' if won else 'Contestant LOST', end='\n\n')

    return won

def run_trials(num_doors: int, trials: int, verbose: bool) -> None:
    win_count_if_switch = sum(simulate(num_doors, switch=True, verbose=verbose) for _ in range(trials))
    win_count_no_switch = sum(simulate(num_doors, switch=False, verbose=verbose) for _ in range(trials))

    print(f'    Switching won {win_count_if_switch:5} out of {trials} '
          f'({(win_count_if_switch / trials * 100):.2f}% of the time)')
    print(f'Not Switching won {win_count_no_switch:5} out of {trials} '
          f'({(win_count_no_switch / trials * 100):.2f}% of the time)')
    
    return win_count_no_switch, win_count_if_switch

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--doors', default=3, type=int, metavar='int',
                        help='number of doors offered to contestant')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', action='store_true',
                        help='display the results of each trial')

    args = parser.parse_args()
    print(f'Simulating {args.trials} trials...')
    # run_trials(args.doors, args.trials, args.verbose)
    
    results = []

    door_configs = [3, 10, 1000]
    for num_doors in door_configs:
        stay_wins, switch_wins = run_trials(num_doors, args.trials, args.verbose)
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
    plt.plot(df_results['num_doors'], df_results['stay_win_percentage'], label='Stay Win %', marker='o')
    plt.plot(df_results['num_doors'], df_results['switch_win_percentage'], label='Switch Win %', marker='o')

    plt.title('Monty Hall Problem: Stay vs Switch Win Percentage')
    plt.xlabel('Number of Doors')
    plt.ylabel('Winning Percentage (%)')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)

    plt.show()

if __name__ == '__main__':
    main()