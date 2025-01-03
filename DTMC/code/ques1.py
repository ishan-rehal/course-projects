def win_probability(p, q, k, N):
    """
    Return the probability of winning a game of chance.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    N : int, maximum wealth
    """
    if(p==q):
        return k/N
    else:
        return (1 - (q/p)**k)/(1-(q/p)**N)
    pass

def limit_win_probability(p, q, k):
    """
    Return the probability of winning when the maximum wealth is infinity.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    """
    if(q<p):
        return 1 - (q/p)**k
    else:
        return 0
    pass

def game_duration(p, q, k, N):
    """
    Return the expected number of rounds to either win or get ruined.
    
    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    """
    if(p==q):
        return N*k - k**2
    else:
        a = N/(p-q)
        b = (1 - (q/p)**k)/(1-(q/p)**N)
        c = k/(p-q)
        return a*b-c
    pass

if __name__ == "__main__":
    (p,q,k,N)=(0,1,9,21)
    print(win_probability(p, q, k, N))
    print(limit_win_probability(p, q, k))
    print(game_duration(p, q, k, N))