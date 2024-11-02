import numpy as np
import random
import time  # Import the time module

class Alice:
    def __init__(self):
        self.past_play_styles = [1,1]
        self.results = [1,0]           
        self.opp_play_styles = [1,1]  
        self.points = 1

    def play_move(self):
        bob_points = len(self.results) - self.points
        if self.results[-1] == 1:
            if(bob_points / len(self.results) > 6 / 11):
                return 0
            else:
                return 2
        elif self.results[-1] == 0.5:
            return 0
        else:
            return 1

    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result

class Bob:
    def __init__(self):
        self.past_play_styles = [1,1]
        self.results = [0,1]
        self.opp_play_styles = [1,1]
        self.points = 1

    def play_move(self):
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:
            return 0

    def observe_result(self, own_style, opp_style, result):
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result

def simulate_round(alice: Alice, bob: Bob, payoff_matrix):
    alice_strat = alice.play_move()
    bob_strat = bob.play_move()
    payoff_matrix[0][0][0] = bob.points / (alice.points + bob.points)
    payoff_matrix[0][0][2] = alice.points / (alice.points + bob.points)
    
    p = random.random()

    if p <= payoff_matrix[alice_strat][bob_strat][0]:
        alice.observe_result(alice_strat, bob_strat, 1)
        bob.observe_result(bob_strat, alice_strat, 0)
    elif p <= payoff_matrix[alice_strat][bob_strat][0] + payoff_matrix[alice_strat][bob_strat][1]:
        alice.observe_result(alice_strat, bob_strat, 0.5)
        bob.observe_result(bob_strat, alice_strat, 0.5)
    else:
        alice.observe_result(alice_strat, bob_strat, 0)
        bob.observe_result(bob_strat, alice_strat, 1)

def estimate_tau(T):
    payoff_matrix = [
        [
            [0, 0, 0],
            [7 / 10, 0, 3 / 10],
            [5 / 11, 0, 6 / 11]
        ],
        [
            [3 / 10, 0, 7 / 10],
            [1 / 3, 1 / 3, 1 / 3],
            [3 / 10, 1 / 2, 1 / 5]
        ],
        [
            [6 / 11, 0, 5 / 11],
            [1 / 5, 1 / 2, 3 / 10],
            [1 / 10, 4 / 5, 1 / 10]
        ]
    ]
    
    i = 0
    mean = 0
    count = 0

    start_time = time.time()  # Record the start time
    
    while i < 10**5:
        alice = Alice()
        bob = Bob()
        alice_wins = 1
        while i < 10**5:
            if alice_wins == T:
                mean += len(alice.results)
                count += 1
                i += 1
                break
            simulate_round(alice, bob, payoff_matrix)
            if alice.results[-1] == 1:
                alice_wins += 1
            
            i += 1

    end_time = time.time()  # Record the end time

    elapsed_time = end_time - start_time  # Calculate total time taken
    # print(f"Estimated value of E[tau]: {mean / count}")
    # print(f"Total running time: {elapsed_time:.2f} seconds")  # Print the elapsed time
    
    return mean / count

# estimate_tau(29)
