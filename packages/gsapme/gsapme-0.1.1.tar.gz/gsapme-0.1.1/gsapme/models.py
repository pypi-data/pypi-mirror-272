# models.py
import numpy as np
import pandas as pd

def ishigami_mod(X):
    """
    Calculate the Ishigami function for a given set of inputs.

    Parameters:
    - X: A DataFrame or 2D array where each row is a set of inputs (X1, X2, X3, ...).
         Only the first three columns are used in the computation.

    Returns:
    - Y: The output of the Ishigami function for each input set.
    """
    # Ensure X is a DataFrame for easy columnwise operations
    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame(X)

    # Apply the Ishigami function component-wise
    Y1 = np.sin(X.iloc[:, 0])
    Y2 = 7 * np.sin(X.iloc[:, 1])**2 if X.shape[1] >= 2 else 0
    Y3 = 0.1 * X.iloc[:, 2]**4 * np.sin(X.iloc[:, 0]) if X.shape[1] >= 3 else 0
    Y = Y1 + Y2 + Y3

    return Y
