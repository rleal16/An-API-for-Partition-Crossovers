# An API for Partition Crossovers

This repository contains the implementation of partition crossovers for the MaxSAT, NK Landscapes, and Traveling Salesman Problem, according to the API proposed in the Chapter 5 in [1].

For the particular case of the TSP, we implemented a version of GPX2 [3] according with the proposed API (this implementation *is not* complete).

In each folder, the recombination algorithm is implemented in `OptimalRecombination.py` and is based on the recombination operator in [2]. It is the same for all problems.

For each problem, the problem dependent implementation is in PX.py. The algorithm in `OptimalRecombination.py` calls the methods from this class.

# Code

To run the code, it is required:

- Python 3.7 or greater
- Networkx 2.6.2

## Exhaustive Recombination

Both implementation for MaxSAT and NK Landscapes were tested agains the algorithm in `ExhaustiveRecombination.py`, that searches for the set of optimal solutions from a recombination of two parents.

## MaxSAT

To run the partition crossover for the MaxSAT, execute the following command in the terminal along with the name (and path) of the instance file:

```bash
python main.py <instance>
```

The implementation supports file with the same forma as the weighted instances in [https://maxsat-evaluations.github.io](https://maxsat-evaluations.github.io/).

Two random parents are recombined.

## NK Landscapes

To run the partition crossover of the NK Landscapes, the number of sub-function, the number of variables for each function, and the total number of variables must be provided. To this end, run the following command on the terminal:

```bash
python main.py <num. of sub-function> <num. of vars per sub-function> <num. of variables>
```

An instance will be generated where each of the sub-functions has *exactly* the number of variables indicated.

Two random parents are then recombined.

## GPX2 for the Travelling Salesman Problem

<aside>
‼️ Still in development...

</aside>

### Compiling the code

In addition to the requirements aforementioned to run the code, this implementation requires Cython 0.29.14.

To compile de code, run the following in the terminal:

```bash
python setup.py build_ext --inplace
```

### Running the code

It is run through a test file, as follows:

```bash
python test.py
```

It uses the instance berlin52.tsp from the repository in [4].

The folder TestingData/ contains:

- 909 unique local optima sampled from multiple runs of an Iterated Local Search algorithm for the TSP (TestingData/berlin52_sampled_solutions.csv), where each parent is identified by a run and an id.
- The pairs of parents that were recombined (TestingData/berlin52_sampled_pairs.csv) with the original code of the GPX2 ([https://github.com/rtinos/gpx2](https://github.com/rtinos/gpx2)).
- The data of the resulting offspring (TestingData/berlin52_offspring_data.csv), where each offspring is identified by the run and id of both parents.
- The permutation of the resulting offspring (TestingData/berlin52_offspring.csv).

The code in `test.py` selects a pair of parents, determined manually in the variable `s_pair`, performs the recombination and compares it with the offspring for the indicated pair in TestingData/berlin52_offspring.csv

# References

[1] Rúben Leal. Developing Partition Crossovers for Combinatorial Optimisation Problems. Master’s Thesis, University of Coimbra, Portugal. 2021

[2] F. Chicano, G. Ochoa, D. Whitley, and R. Tinós. Quasi-Optimal Recombination Operator. In A. Liefooghe and L. Paquete, editors, Evolutionary Computation in Combinatorial Optimization, volume 11452, pages 131–146. Springer International Publishing, Cham, 2019. Series Title: Lecture Notes in Computer Science.

[3] R. Tinós, D. Whitley, and G. Ochoa. A New Generalized Partition Crossover for the Traveling Salesman Problem: Tunneling between Local Optima. Evolutionary Computation, 28(2):255–288, June 2020.

[4] TSPLIB. [http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html). Accessed: 2021-10-12
