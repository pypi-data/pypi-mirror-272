# datadrivenquadrature

Data Driven Quadrature is a Python package for quadrature-based integration point selection. In many applications, integrals over high-resolution integration axes are calculated repeatedly and can be extremely computationally expensive. This operation can be simplified by selecting integration points and corresponding weights that approximate the integral (Gaussian quadrature). The simulated annealing technique is modeled off the procedure described in [Buehler et al., 2010](https://www.sciencedirect.com/science/article/pii/S0022407309003197?casa_token=LfkPCegaA3YAAAAA:rxGp4oporQ6V5gfXS3BuL4HtASAduklHd9VkM5Kn2xQ_gpAiOJgD8A_G4TICkhiB6hZQQrFM) and applied again in [Czarnecki et al., 2023](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023MS003819) 

This package implements a linear-programing approach to this optimization problem with a simple user-interface. 

### Contents
- [Usage](#usage)
    - [Parameters and Functions](#parameters-and-functions)
        - [Optimization Function Parameters](#optimization-function-parameters)
        - [find_normalization_vector()](#find_normalization_vector)
        - [check_params()](#check_params)
        - [optimize()](#optimize)
        - [flatten_history()](#flatten_history)
    - [Installation](#installation)
        - [via Pypi](#via-pypi)
        - [via GitHub](#via-github)
- [Authors](#authors)
- [License](#license)
- [References](#references)

## Usage


Four functions are available for direct user usage:  <code>find_normalization_vector()</code>, <code>check_params()</code>, <code>optimize()</code>, <code>flatten_history()</code>. Functions, signatures, and descriptions are below. A full (and hopefully helpful) tutorial is included [here](https://github.com/LDEO-CREW/data-driven-quadrature/blob/main/examples/tutorial.ipynb) and a full example can be found [here](https://github.com/LDEO-CREW/data-driven-quadrature/blob/main/examples/example.ipynb). Note, due to the high volume of data, the example data is not included in this package.

### Parameters and Functions

All functions are docstring compatible and information can be printed using the <code>help()</code> function:

    import datadrivenquadrature as ddq

    help(ddq.optimize)

#### Optimization Function Parameters:

- <code>x</code>: An <code>xarray</code> dataset including all necessary data and integration axes
- <code>y_ref</code>: Precalculated reference integrals as a flat vector
- <code>C()</code>: Cost function using only CVXPY functions to return a CVXPY
- <code>M()</code>: Mapping function that returns a matrix of shape (number of integration points, number of integrals) from mapped values 
- <code>params</code>: A dictionary of parameters used in optimization:
    - <code>integration_list</code>: List of integration axes. Currently, only one integration axis is supported at a time (REQUIRED)
    - <code>n_points</code>: Number of integration points to use (REQUIRED)
    - <code>epochs</code>: Number of epochs to use in optimization (default=100)
    - <code>block_size</code>: Number of iterations within an epoch (default=50)
    - <code>success</code>: Number of successes required to move on from a block early (default=25)
    - <code>random_seed</code>: Random seed for optimization 
    - <code>verbose</code>: Verbosity level during optimization (default=1)
        - <code>verbose=0</code>: Do not print anything during optimization
        - <code>verbose=1</code>: Only print final summary after optimization
        - <code>verbose=2</code>: Print final and epoch summaries
        - <code>verbose=3</code>: Print all final, epoch, and block summaries
- <code>x_sup</code>: If any additional data needs to be supplied to the mapping function for any reason, it can be passed in through this OPTIONAL parameter


#### find_normalization_vector()

Returns a normalization vector for all given integration axes
    
    :param x: xarray dataframe containing integration axes
    :param integration_axes: list of integration axes in x
    :returns: list of normalization tuples (scale, offset) to normalize integration axes to [0, 1]
    
#### check_params()

Returns a normalization vector for all given integration axes
    
    :param x: xarray dataframe containing integration axes
    :param integration_axes: list of integration axes in x
    :returns: list of normalization tuples (scale, offset) to normalize integration axes to [0, 1]
    
#### optimize()

User-called function to check validity of inputs and determine optimal point set

    :param x: xarray dataset containing integration axes
    :param y_ref: numpy multi-dimensional array containing reference/target values
    :param C: cost function
    :param M: mapping function
    :param params: dictionary of user-defined parameters for optimization loop and integration axes
    :param x_sup: optional parameter passed to map function
    :returns: history object containing 'point_sets', 'weight_sets', 'cost', and 'temperature_history' and 'best' index of optimization

#### flatten_history()

Flattens history object returned by the optimization loop

    :param history: history dictionary returned from an optimization loop
    :returns: history dictionary with all multi-dimensional lists fully flattened
    
## Installation

### via PyPi

This package is on the <code>PyPi</code> directory so you can install it using:

```
pip install datadrivenquadrature
```

### via GitHub

If you would like to change any of the code in the package, you can directly download the package from the [repository](https://github.com/LDEO-CREW/data-driven-quadrature) and find all relevant functions in [<code>/datadrivenquarature/main.py</code>](https://github.com/LDEO-CREW/data-driven-quadrature/blob/main/datadrivenquadrature/main.py)

## Authors

- Neal Ma ([nmadev](https://github.com/nmadev))
- Paulina Czarnecki ([pczarnecki](https://github.com/pczarnecki))
- Robert Pincus ([RobertPincus](https://github.com/RobertPincus))

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LDEO-CREW/data-driven-quadrature/blob/main/LICENSE) file for details.

## References

[1] S.A. Buehler, V.O. John, A. Kottayil, M. Milz, P. Eriksson, Efficient radiative transfer simulations for a broadband infrared radiometer—Combining a weighted mean of representative frequencies approach with frequency selection by simulated annealing, Journal of Quantitative Spectroscopy and Radiative Transfer, Volume 111, Issue 4, 2010, Pages 602-615, ISSN 0022-4073, https://doi.org/10.1016/j.jqsrt.2009.10.018.

[2] Czarnecki, P., Polvani, L., & Pincus, R. (2023). Sparse, empirically optimized quadrature for broadband spectral integration. Journal of Advances in Modeling Earth Systems, 15, e2023MS003819. https://doi.org/10.1029/2023MS003819