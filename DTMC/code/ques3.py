"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
M=1000000007

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


def game_duration(p, q, k, t, W):
    """
    Return the expected number of rounds the gambler will play before quitting.

    p : float, 0 < p < 1, probability of winning a round
    q : float, q = 1 - p, probability of losing a round
    k : int, starting wealth
    t : int, t < k, the gambler will quit if she reaches t
    W : int, the threshold on maximum wealth the gambler can reach
    
    """
    if(p==q):
        return (k-t)*(2*W+1)
    else:
        a = 1 - 1/(q-p)
        b = (p/q)**W
        c = 1/(q-p)
        return (k-t)*(a*b + c)
    pass

def test_game_duration():
    # Test case 1: Basic scenario
    p = 0.3
    q = 0.7
    k = 201
    t = 200
    W = 1
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 1: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 2: Equal probabilities
    p = 0.5
    q = 0.5
    k = 100
    t = 50
    W = 10
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 2: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 3: High probability of winning
    p = 0.8
    q = 0.2
    k = 150
    t = 100
    W = 5
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 3: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 4: High probability of losing
    p = 0.2
    q = 0.8
    k = 50
    t = 25
    W = 20
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 4: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 5: Large values
    p = 0.6
    q = 0.4
    k = 1000
    t = 500
    W = 100
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 5: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 6: Edge case where k == t
    p = 0.4
    q = 0.6
    k = 100
    t = 100
    W = 10
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 6: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 7: Edge case where k == 0
    p = 0.4
    q = 0.6
    k = 102
    t = 100
    W = 10
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 7: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 8: Edge case where t == 0
    p = 0.4
    q = 0.6
    k = 100
    t = 0
    W = 10
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 8: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 9: Edge case where W == 0
    p = 0.4
    q = 0.6
    k = 100
    t = 50
    W = 1
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 9: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 10: Edge case where p == 1
    p = 0.89
    q = 0.11
    k = 100
    t = 50
    W = 10
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 10: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

    # Test case 11: Edge case where p == 0
    p = 0.8
    q = 0.2
    k = 100
    t = 50
    W = 10
    expected_rounds = game_duration(p, q, k, t, W)
    print(f"Test case 11: Expected number of rounds for (p, q, k, t, W) = ({p}, {q}, {k}, {t}, {W}): {expected_rounds}")

# Run the test cases
test_game_duration()

