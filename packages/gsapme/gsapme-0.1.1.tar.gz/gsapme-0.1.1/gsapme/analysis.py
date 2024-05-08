# analysis.py
import numpy as np
from itertools import combinations
import scipy.special
from .simulation import jointSim, condSim
from .models import ishigami_mod


def compute_variance_np(model, jointSim, Nv, covMat, pert=False):
    X_v = jointSim(Nv, covMat)  # Generate samples using the joint simulation function

    # Sequential execution of the model on generated samples
    Y = model(X_v)

    # Compute the variance of the model output, using ddof=1 for sample variance
    vy = np.var(Y, ddof=1)
    return vy, X_v


def conditional_elements_estimation_np(model, condSim, jointSim, No, Ni, d, vy, covMat):
    # Generate conditional samples
    condX = jointSim(No, covMat)

    # Initialize indices and combination weights
    indices = [None] * (d + 1)
    comb_weights = np.zeros(d)

    # Use NumPy to create combinations and store indices for each interaction level
    for j in range(1, d + 1):
        indices[j] = np.array(list(combinations(range(d), j))).T
        comb_weights[j-1] = 1 / scipy.special.comb(d - 1, j - 1)

    # Initialize storage for variance explained results, mirroring the structure of indices
    VEs = [None] * len(indices)

    # Estimate variance explained for each subset of variables
    for level in range(1, len(indices)):
        current_level_indices = indices[level]
        current_level_VEs = []  # Initialize an empty list to store VEs for the current level
        for subset in current_level_indices.T:
            VE = estim_VE_MC(condX, condSim, model, list(subset), Ni, vy, covMat)
            current_level_VEs.append(VE)
        VEs[level] = np.array(current_level_VEs)  # Store the VEs for the current level

    # Set the last element of VEs to 1, representing the total variance explained for the full model
    VEs[-1] = 1

    # Convert combination weights to a NumPy array for consistency
    comb_weights_array = np.array(comb_weights)

    # Return the estimated VEs, indices, and combination weights
    return VEs, indices, comb_weights_array


def estim_VE_MC(condX, condSim, model, subset, Ni, vy, covMat):
    condX = np.asarray(condX)
    No, d = condX.shape

    # Adjust subset indices to match the R function logic
    complement_subset = np.setdiff1d(np.arange(d), subset)

    varVec = np.zeros(No)
    for i in range(No):
        # Extract conditional values for each sample, ensuring xjc matches the expected shape
        xjc = condX[i, complement_subset]  # Direct indexing without further adjustment

        # Perform conditional simulation
        # Ensure the condSim function is designed to accept these parameters correctly
        X_ = condSim(Ni, subset, complement_subset, xjc, covMat)  # Adjusted order to match the function definition

        # Apply the model function
        Y_ = model(X_)
        varVec[i] = np.var(Y_, ddof=1)  # ddof=1 for sample variance

    return np.mean(varVec) / vy


def calculate_shapley_effects_np(d, indices, VEs, comb_weights):
    Shaps = np.zeros(d)
    for var_j in range(d):
        for ord in range(1, d + 1):  # Ensure ord starts from 1 for consistency with indices
            if VEs[ord] is None:
                continue

            # Correctly handle indexing to avoid deprecation warnings and errors
            idx_j = np.where(indices[ord] == var_j)[1] if ord < len(indices) else np.array([])
            idx_woj = np.where(np.all(indices[ord-1] != var_j, axis=0))[0] if ord-1 > 0 else np.array([])

            # Adjust effect calculation using np.take, ensuring indices are valid
            effect_incl_j = np.sum(np.take(VEs[ord], idx_j, axis=0)) if idx_j.size > 0 else 0
            effect_excl_j = np.sum(np.take(VEs[ord-1], idx_woj, axis=0)) if idx_woj.size > 0 else 0

            # Compute the total incremental effect and update Shapley values
            Shaps[var_j] += comb_weights[ord-1] * (effect_incl_j - effect_excl_j) if ord-1 < len(comb_weights) else 0

    Shaps /= d
    return Shaps
