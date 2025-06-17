import numpy as np
from scipy.stats import truncnorm

def sinkhorn_normalize(P, max_iter=100, epsilon=1e-6):
    """
    Apply the Sinkhorn-Knopp algorithm to convert a matrix P
    into a doubly stochastic matrix.

    Parameters:
        P (np.ndarray): Square (n x n) non-negative matrix.
        max_iter (int): Maximum number of iterations.
        epsilon (float): Convergence tolerance.

    Returns:
        np.ndarray: Doubly stochastic matrix.
    """
    P = np.array(P, dtype=np.float64)

    if np.any(P < 0):
        raise ValueError("Input matrix must be non-negative.")

    # Avoid division by zero


    for _ in range(max_iter):
        P_prev = P.copy()

        # Row normalization
        P /= P.sum(axis=1, keepdims=True)

        # Column normalization
        P /= P.sum(axis=0, keepdims=True)

        # Check convergence
        if np.allclose(P, P_prev, atol=epsilon):
            break

    return P

def random_threshold(mean, std = 0.1):

    # Define bounds in standard normal units
    a, b = (0 - mean) / std, (1 - mean) / std

    # Sample
    value = truncnorm.rvs(a, b, loc=mean, scale=std)
    return value

def closest_turn_ID(list_IDs, ID_search):
    lo, hi = 0, len(list_IDs) - 1
    ans = None
    while lo < hi:
        mid = (lo+hi)//2
        if list_IDs[mid] >= ID_search:
            ans = mid
            hi = mid -1
        else:
            lo = mid + 1
    if ans != None:
        return list_IDs[ans]
    else:
        return ans

if __name__ == '__main__':
    list = [0,4,5,6]
    a = closest_turn_ID(list, 3)
    print(a)