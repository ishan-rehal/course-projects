def decimalToBinary(num, k_prec): 
    binary = ""  
    Integral = int(num)    
    fractional = num - Integral 
   
    while Integral:       
        rem = Integral % 2
        binary += str(rem)  
        Integral //= 2

    binary = binary[::-1]  
    binary += '.'

    while k_prec: 
        fractional *= 2
        fract_bit = int(fractional)  
        if fract_bit == 1:  
            fractional -= fract_bit  
            binary += '1'       
        else: 
            binary += '0'
        k_prec -= 1
        
    return binary 

# Memoization arrays
win_prob_memo = []
game_dur_memo = []

def initialize_memoization_win_prob(N):
    global win_prob_memo
    win_prob_memo = [-1 for _ in range(N)]

def initialize_memoization_game_dur(N):
    global game_dur_memo
    game_dur_memo = [-1 for _ in range(N)]


def win_probability(p, q, k, N):
    initialize_memoization_win_prob(N)
    return calc_win_prob(p,q,k,N)

def calc_win_prob(p,q,k,N):
    # Check if result is already computed
    if win_prob_memo[k] != -1:
        return win_prob_memo[k]
    
    # Base cases
    if k == 0:
        return 0
    if k == N:    
        return 1

    # Recursive computation with memoization
    if k < N / 2:
        result = p * win_probability(p, q, 2 * k, N)
    else:
        result = p + q * win_probability(p, q, 2 * k - N, N)
    
    # Store result in memoization array
    win_prob_memo[k] = result
    return result

def game_duration(p, q, k, N):
    initialize_memoization_game_dur(N)
    return calc_game_dur(p,q,k,N)

def calc_game_dur(p,q,k,N):
    # Check if result is already computed
    if game_dur_memo[k] != -1:
        return game_dur_memo[k]
    
    # Base cases
    if k == 0 or k == N:
        return 0

    # Recursive computation with memoization
    if k < N / 2:
        result = p * (1 + game_duration(p, q, 2 * k, N)) + q
    else:
        result = p + q * (1 + game_duration(p, q, 2 * k - N, N))
    
    # Store result in memoization array
    game_dur_memo[k] = result
    return result

if __name__ == "__main__":
    p = 0.3
    q = 0.7
    k = 10
    N = 2**20
    
    
    win_prob = win_probability(p, q, k, N)
    game_dur = game_duration(p, q, k, N)
    print(win_prob)
    print(game_dur)
    # print(decimalToBinary(0.259, 10))
    # print(decimalToBinary(game_dur, 10))