def stationary_distribution(p, q, r, N):
    """
    Return a list of size N+1 containing the stationary distribution of the Markov chain.
    
    p : array of size N+1, 0 < p[i] < 1, probability of price increase
    q : array of size N+1, 0 < q[i] < 1, probability of price decrease
    r : array of size N+1, r[i] = 1 - p[i] - q[i], probability of price remaining the same
    N : int, the maximum price of the stock
    """
    result = 1
    ans = 1
    for i in range(0, N):
        result = result * p[i]/q[i+1]
        ans+=result
    
    pi = [0 for _ in range(N+1)]
    
    pi[0] = 1/(ans)
    
    for i in range(1, N+1):
        pi[i] = pi[i-1] * (p[i-1]/q[i])
    return pi
    pass

def expected_wealth(p, q, r, N):
    """
    Return the expected wealth of the gambler in the long run.

    p : array of size N+1, 0 < p[i] < 1, probability of price increase
    q : array of size N+1, 0 < q[i] < 1, probability of price decrease
    r : array of size N+1, r[i] = 1 - p[i] - q[i], probability of price remaining the same
    N : int, the maximum price of the stock
    """
    result = 1
    ans = 1
    for i in range(0, N):
        result = result * p[i]/q[i+1]
        ans+=result
    
    pi = [0 for _ in range(N+1)]
    
    pi[0] = 1/(ans)
    
    for i in range(1, N+1):
        pi[i] = pi[i-1] * (p[i-1]/q[i])
        
    ans = 0
    
    for i in range(0, N+1):
        ans += pi[i] * i
    
    return ans
    
    
def expected_time(p, q, r, N, a, b):
    """
    Return the expected time for the price to reach b starting from a.

    p : array of size N+1, 0 < p[i] < 1, probability of price increase
    q : array of size N+1, 0 < q[i] < 1, probability of price decrease
    r : array of size N+1, r[i] = 1 - p[i] - q[i], probability of price remaining the same
    N : int, the maximum price of the stock
    a : int, the starting price
    b : int, the target price
    """
    if(b==0):
        return 0
    coeff = [(None, None) for _ in range(N+1)]
    coeff[0] = (1, 0)
    coeff[1] = ((1-r[0])/p[0], -1/p[0])
    for i in range(2, N+1):
        coeff[i] = ((coeff[i-1][0]*(1-r[i-1]) - q[i-1]*coeff[i-2][0])/p[i-1] , (coeff[i-1][1]*(1-r[i-1]) - q[i-1]*coeff[i-2][1] - 1)/p[i-1])
    
    ans = 0
    E_0 = -1*(coeff[b-1][1]*(1-r[b-1]) - q[b-1]*coeff[b-2][1] - 1)/(coeff[b-1][0]*(1-r[b-1]) - q[b-1]*coeff[b-2][0])
    
    ans = coeff[a][0]*E_0 + coeff[a][1]
    
    return ans
    pass

if __name__ == "__main__":
    p = [0.5, 0.25, 0.125, 0.125, 0]
    q = [0, 0.25, 0.25, 0.5, 0.5]
    r = [0.5, 0.5, 0.625, 0.375, 0.5]
    N = 4
    a = 2
    b = 2
    print(stationary_distribution(p, q, r, N))
    print(expected_wealth(p, q, r, N))
    print(expected_time(p,q,r,N,a,b))
    pass