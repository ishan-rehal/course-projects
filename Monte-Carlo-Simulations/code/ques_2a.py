import numpy as np
import random    
class Alice:
    def __init__(self):
        self.past_play_styles = [1,1]
        self.results = [1,0]           
        self.opp_play_styles = [1,1]  
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round. Implement your strategy for 2a here.
         
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        bob_points = len(self.results) - self.points
        if self.results[-1] == 1:
            if(bob_points/len(self.results) > 6/11):
                return 0
            else:
                return 2
        elif self.results[-1] == 0.5:  #if bob played attack last time he will play defense so alice plays balanced
            return 0
        else:
            return 1    
            
        pass
        
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result
        pass

class Bob:
    def __init__(self):
        # Initialize numpy arrays to store Bob's past play styles, results, and opponent's play styles
        self.past_play_styles = [1,1]
        self.results = [0,1]       
        self.opp_play_styles = [1,1]  
        self.points = 1

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:  
            return 0
        
        
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Bob's knowledge after each round based on the observed results.
        
        Returns:
            None
        """ 
        self.past_play_styles.append(own_style)
        self.results.append(result)
        self.opp_play_styles.append(opp_style)
        self.points += result
 

def simulate_round(alice : Alice, bob : Bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    alice_strat = alice.play_move()
    bob_strat = bob.play_move()
    payoff_matrix[0][0][0] = bob.points/(alice.points+bob.points)
    payoff_matrix[0][0][2] = alice.points/(alice.points+bob.points)
    
    # Generate a random float between 0 and 1
    p = random.random()
    
    if(p<=payoff_matrix[alice_strat][bob_strat][0]):
        alice.observe_result(alice_strat,bob_strat,1)
        bob.observe_result(bob_strat,alice_strat,0)
    elif(p<=payoff_matrix[alice_strat][bob_strat][0]+payoff_matrix[alice_strat][bob_strat][1]):
        alice.observe_result(alice_strat,bob_strat,0.5)
        bob.observe_result(bob_strat,alice_strat,0.5)
    else:
        alice.observe_result(alice_strat,bob_strat,0)
        bob.observe_result(bob_strat,alice_strat,1)
    
    pass
    


def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    payoff_matrix = [
    # Row for Attack
        [
            [0,0,0],                             # Attack vs Attack
            (7/10, 0, 3/10),                        # Attack vs Balanced
            (5/11, 0, 6/11)                         # Attack vs Defence
        ],
        # Row for Balanced
        [
            (3/10, 0, 7/10),                        # Balanced vs Attack
            (1/3, 1/3, 1/3),                        # Balanced vs Balanced
            (3/10, 1/2, 1/5)                        # Balanced vs Defence
        ],
        # Row for Defence
        [
            (6/11, 0, 5/11),                        # Defence vs Attack
            (1/5, 1/2, 3/10),                       # Defence vs Balanced
            (1/10, 4/5, 1/10)                       # Defence vs Defence
        ]
    ]
    alice = Alice()
    bob = Bob()
    for i in range(num_rounds):
        simulate_round(alice,bob,payoff_matrix)
    print(alice.points,bob.points)
    pass
    
 

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=10**5)