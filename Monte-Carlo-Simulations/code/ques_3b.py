# Problem 3b
def dp_initialize(tot_rounds):
    # Create a 2D list initialized with (0, 0) tuples
    dp = [[(0, 0) for _ in range(2 * tot_rounds + 3)] for _ in range(tot_rounds + 2)]
    
    return dp

def calc_prob(na,nb,prob,strat):
        payoff_matrix =     [[[nb/(na+nb), 0, na/(na+nb)],[7/10, 0, 3/10],[5/11, 0, 6/11]],
                        [[3/10, 0, 7/10],[1/3, 1/3, 1/3],[3/10, 1/2, 1/5]],
                        [[6/11, 0, 5/11],[1/5, 1/2, 3/10],[1/10, 4/5, 1/10]]]

        for j in range(3):
            prob[0] += payoff_matrix[strat][j][0]/3
            prob[1] += payoff_matrix[strat][j][2]/3
            prob[2] += payoff_matrix[strat][j][1]/3

def calc_exp(na,nb,strat):
        payoff_matrix =     [[[nb/(na+nb), 0, na/(na+nb)],[7/10, 0, 3/10],[5/11, 0, 6/11]],
                        [[3/10, 0, 7/10],[1/3, 1/3, 1/3],[3/10, 1/2, 1/5]],
                        [[6/11, 0, 5/11],[1/5, 1/2, 3/10],[1/10, 4/5, 1/10]]]
        
        t=0
        
        for i in range(3):
            t +=   payoff_matrix[strat][i][0]/3 + payoff_matrix[strat][i][1]/6
            
        return t


def calc(na,nb,tot_rounds,dp):
    
    
    
    n = tot_rounds + 2
    m = 2*tot_rounds + 3
    
    for j in range (m-2):
        ap = na + j/2
        bp = na + nb + tot_rounds - 1 -ap
        attack = (bp)/(ap+bp) + 127/330
        defense = 329/660
        if attack > defense:
            dp[1][j] = (0,attack)
        else:
            dp[1][j] = (2,defense)
    
    for i in range(2,n):
        for j in range(m-2):
            
                ap = na + j/2
                bp = na + nb + tot_rounds - 1 -ap
                
                alice_prob_attack = [0,0,0]
                calc_prob(ap,bp,alice_prob_attack,0)
                print("HELLOO")
                print(alice_prob_attack)
                attack = dp[i-1][j+2][1]*(alice_prob_attack[0]) + dp[i-1][j][1]*(alice_prob_attack[1]) + dp[i-1][j+1][1]*(alice_prob_attack[2]) + calc_exp(ap,bp,0)
                
                alice_prob_defence = [0,0,0]
                calc_prob(ap,bp,alice_prob_defence,2)
                
                defence = dp[i-1][j+2][1]*(alice_prob_defence[0]) + dp[i-1][j][1]*(alice_prob_defence[1]) + dp[i-1][j+1][1]*(alice_prob_defence[2]) + calc_exp(ap,bp,2)
                
                alice_prob_balanced = [0,0,0]
                calc_prob(ap,bp,alice_prob_balanced,1)
                
                balance = dp[i-1][j+2][1]*(alice_prob_balanced[0]) + dp[i-1][j][1]*(alice_prob_balanced[1]) + dp[i-1][j+1][1]*(alice_prob_balanced[2]) + calc_exp(ap,bp,1)
            
                ans = max(attack,balance,defence)
                
                if(ans == attack):
                    dp[i][j] = (0,attack)
                elif(ans == defence):
                    dp[i][j] = (2,defence)
                elif(ans == balance):
                    dp[i][j] = (1,balance)
                    
    return dp          
                

def optimal_strategy(na, nb, tot_rounds):
    """
    Calculate the optimal strategy for Alice maximize her points in the future rounds
    given the current score of Alice(na) and Bob(nb) and the total number of rounds left(tot_rounds).
    
    Returns: 
        0 : attack
        1 : balanced
        2 : defence
    """
    dp = dp_initialize(tot_rounds)
    ans =  calc(na,nb,tot_rounds,dp)
    for i in ans:
        print(i)
    return ans[tot_rounds+1][0]
    
print(optimal_strategy(1,1,3))