import numpy as np

### HELLO!!!! #####

#Lognormal PDF original
def lognorm_pdf(x, mu = 0, vol = 1): 
    """
    Compute the probability density function (PDF) of the lognormal distribution.

    Parameters:
        x (float or array-like): The input values at which to compute the PDF.
        mu (float): The mean parameter of the lognormal distribution.
        vol (float): The standard deviation parameter of the lognormal distribution.

    Returns:
        float or array-like: The PDF values corresponding to the input values `x`.
    """
    pdf = 1 / (x * vol * np.sqrt(2 * np.pi)) * np.exp(-(np.log(x) - mu)**2 / (2 * vol**2))
    return pdf

