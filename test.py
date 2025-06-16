import numpy as np
a = np.array([[1,0,0,0,0], [0,0,1,0,0], [0,0,0,0,1], [0,1,0,0,0], [0,0,0,1,0]], dtype = float)
# d = np.array([[3,0,0,0,0], [0,0,1,0,0], [0,0,0,0,5], [0,1,0,0,0], [0,0,0,1,0]], dtype = float)
# t = np.full((5,5), 0.2)
# print(a[0:2])
# b = np.sum(a[0:2], axis=0)/2
# print(b)
# b_stacked = np.stack([b,b], axis = 0)
# print(b_stacked)
# a[0:2] = b_stacked
# print(a[1])
# print((a+d)/2)
#
#
# a = [(1,2), (10,13)]
#
# import numpy as np
#
#
# def sinkhorn_normalize(P, max_iter=100, epsilon=1e-6):
#     """
#     Apply the Sinkhorn-Knopp algorithm to convert a matrix P
#     into a doubly stochastic matrix.
#
#     Parameters:
#         P (np.ndarray): Square (n x n) non-negative matrix.
#         max_iter (int): Maximum number of iterations.
#         epsilon (float): Convergence tolerance.
#
#     Returns:
#         np.ndarray: Doubly stochastic matrix.
#     """
#     P = np.array(P, dtype=np.float64)
#
#     if np.any(P < 0):
#         raise ValueError("Input matrix must be non-negative.")
#
#     # Avoid division by zero
#     #P += 1e-12
#
#     for _ in range(max_iter):
#         P_prev = P.copy()
#
#         # Row normalization
#         P /= P.sum(axis=1, keepdims=True)
#
#         # Column normalization
#         P /= P.sum(axis=0, keepdims=True)
#
#         # Check convergence
#         if np.allclose(P, P_prev, atol=epsilon):
#             break
#
#     return P
# print(t)
# print(np.size(t,0))
# t[1] = np.zeros(5)
# print(t)
# t[:,2] = np.zeros(5)
# t[1,2] = 1
# print(t)
# t = sinkhorn_normalize(t)
# print(t)
#
# for a,b in [(1,3), (4,2)]:
#     print(a,b)
from scipy.stats import truncnorm
a = {1: "l", 2:"o", 3:"v", 4:"e"}
print(a.keys())
