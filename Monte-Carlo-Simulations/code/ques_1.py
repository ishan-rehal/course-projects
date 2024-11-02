"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
from fractions import Fraction
M=1000000007
memo = {}
def mod_add(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a+b)%M

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M

def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))

# Problem 1a
def calc_prob(alice_wins, bob_wins):

    #  ans = calc_p(alice_wins-1,bob_wins-1,1,1)
    #  return mod_divide(ans.numerator,ans.denominator)
    
    dp=[[0 for i in range(bob_wins+1)] for j in range(alice_wins+1)]
    dp[0][0]=Fraction(0,1)
    dp[1][0]=Fraction(0,1)
    dp[0][1]=Fraction(0,1)
    dp[1][1]=Fraction(1,1)
    for a in range(1,alice_wins+1):
        for b in range(1,bob_wins+1):
            if(a==1 and b==1):
                continue
            if(a-1==0 and b>1):
                dp[a-1][b]=0
            if(b-1==0 and a>1):
                dp[a][b-1]=0
            pb = Fraction(a, a+b-1)
            pa = Fraction(b, a+b-1)
         
            dp[a][b] = pa*dp[a-1][b] + pb*dp[a][b-1]
    
    return mod_divide(dp[alice_wins][bob_wins].numerator,dp[alice_wins][bob_wins].denominator)
            

    
# Problem 1b (Expectation)      
def calc_expectation(t):
    """
    Returns:
        The expected value of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    # for i in range(1,t+1):
    #     for keys in memo:
    alice_wins = t
    bob_wins = t
    dp=[[0 for i in range(bob_wins+1)] for j in range(alice_wins+1)]
    dp[0][0]=Fraction(0,1)
    dp[1][0]=Fraction(0,1)
    dp[0][1]=Fraction(0,1)
    dp[1][1]=Fraction(1,1)
    for a in range(1,alice_wins+1):
        for b in range(1,bob_wins+1):
            if(a==1 and b==1):
                continue
            if(a-1==0 and b>1):
                dp[a-1][b]=0
            if(b-1==0 and a>1):
                dp[a][b-1]=0
            pb = Fraction(a, a+b-1)
            pa = Fraction(b, a+b-1)
         
            dp[a][b] = pa*dp[a-1][b] + pb*dp[a][b-1]
    
    
    mean = Fraction(0,1)
    for j in range(3,t+1):
        for i in range(j+1):
            if(i==0 or i==j):
                continue
            if(j-i>1):
                mean = mean + Fraction(i,j-1)*dp[j-i-1][i]
                
            if(i>1):
                mean = mean - Fraction(j-i,j-1)*dp[j-i][i-1]
                
            # print(j-i,i,mean)
                
    return mod_divide(mean.numerator,mean.denominator)
    pass

# Problem 1b (Variance)
def calc_variance(t):
    """
    Returns:
        The variance of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    alice_wins = t
    bob_wins = t
    dp=[[0 for i in range(bob_wins+1)] for j in range(alice_wins+1)]
    dp[0][0]=Fraction(0,1)
    dp[1][0]=Fraction(0,1)
    dp[0][1]=Fraction(0,1)
    dp[1][1]=Fraction(1,1)
    for a in range(1,alice_wins+1):
        for b in range(1,bob_wins+1):
            if(a==1 and b==1):
                continue
            if(a-1==0 and b>1):
                dp[a-1][b]=0
            if(b-1==0 and a>1):
                dp[a][b-1]=0
            pb = Fraction(a, a+b-1)
            pa = Fraction(b, a+b-1)
         
            dp[a][b] = pa*dp[a-1][b] + pb*dp[a][b-1]
    
    var = Fraction(0,1)
    j = 1
    for i in range(t,0,-2):
        if(i==t):
            continue
        var = var + dp[j][t-j]*Fraction(2*i*i,1)
        j=j+1
    return mod_divide(var.numerator,var.denominator)
    pass


# print(calc_variance(2))
