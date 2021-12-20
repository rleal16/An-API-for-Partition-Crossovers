# An API for Partition Crossovers

This repository contains the implementation of partition crossovers for the MaxSAT and NK Landscapes, according to the API proposed in the Chapter 5 in [1].


# Code

In each folder, the recombination algorithm is implemented in `OptimalRecombination.py` and is based on the recombination operator in [2]. It is the same for all problems.

For each problem, the problem dependent implementation is in `PX.py`. The algorithm in `OptimalRecombination.py` calls methods from this class.

To run the code, it is required:

- Python 3.7 or greater
- Networkx 2.6.2

## Exhaustive Recombination

Both implementation for MaxSAT and NK Landscapes were tested against the algorithm in `ExhaustiveRecombination.py`, that searches for the set of optimal solutions from a recombination of two parents.

## MaxSAT

To run the partition crossover for the MaxSAT, execute the following command in the terminal along with the name (and path) of the instance file:

```bash
python main.py <instance>
```

The implementation supports file with the same format as the weighted instances in [https://maxsat-evaluations.github.io](https://maxsat-evaluations.github.io/).
Two random parents are recombined.

## NK Landscapes

To run the partition crossover of the NK Landscapes, the number of sub-function, the number of variables for each function, and the total number of variables must be provided. Execute the following command in the terminal:

```bash
python main.py <num. of sub-function> <num. of vars per sub-function> <num. of variables>
```

An instance will be generated where each of the sub-functions has *exactly* the number of variables indicated.
Two random parents are then recombined.

# References

[1] Rúben Leal. Developing Partition Crossovers for Combinatorial Optimisation Problems. Master’s Thesis, University of Coimbra, Portugal. 2021

[2] F. Chicano, G. Ochoa, D. Whitley, and R. Tinós. Quasi-Optimal Recombination Operator. In A. Liefooghe and L. Paquete, editors, Evolutionary Computation in Combinatorial Optimization, volume 11452, pages 131–146. Springer International Publishing, Cham, 2019. Series Title: Lecture Notes in Computer Science.
