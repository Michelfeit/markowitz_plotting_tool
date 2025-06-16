import numpy as np

# XOM - Exxon Mobile
# GM - General Motors
# EXTR - Extreme Networks
# UAL - United Airline Holdings Inc
# DAR - Darling Ingredients
# TZOO - Travelzoo

# numbers based on Research on Optimizing Pension Planning Allocations -> https://www.researchgate.net/figure/Covariance-table-for-different-stocks_tbl2_376887913


mean = np.array([0.0138, 0.0136, 0.0181, 0.0168, 0.0122, 0.0205])
sigma = np.array([0.0111, 0.0125, 0.0297, 0.0189, 0.0116, 0.0330])

cov = np.matrix([
    [sigma[0], 0.0054, 0.0081, 0.0083, 0.0039, 0.0100],
    [0.0054, sigma[1], 0.0111, 0.0093, 0.0066, 0.0118],
    [0.0081, 0.0111, sigma[2], 0.0142, 0.0063, 0.0107],
    [0.0083, 0.0093, 0.0142, sigma[3], 0.0067, 0.0137],
    [0.0039, 0.0066, 0.0063, 0.0067, sigma[4], 0.0081],
    [0.0100, 0.0118, 0.0107, 0.0137, 0.0081, sigma[5]]
])