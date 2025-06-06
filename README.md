# GSlicer

An automated testing tool for graph-processing systems via Graph-cutting. The codebase for the paper ***"Finding Logic Bugs in Graph-processing Systems via Graph-cutting"***

## 📰 Project Update

We plan to actively maintain GSlicer and extend support for more algorithms in NetworkX (see `/graphs/networks/algs`). We warmly welcome contributions—feel free to open a pull request if you’d like to be part of the project!


## 🚀 Quick Start

### 1. Environment Requirements

The code has been tested on a Linux (Ubuntu 22.04 LTS) workstation with Python 3.10. To set up the environment, follow these steps:

```bash
docker compose up
pip install neo4j
pip install networkx
pip install kuzu
pip install numpy
pip install pandas
```

### 2. Testing Graph-Processing Systems

- **Neo4j GDBMS**: To test Neo4j, simply run:
  ```bash
  python ./databases/neo4j/test.py
  ```

- **Neo4j-GDS (Graph Data Science Library)**: To test specific algorithms, navigate to the corresponding directory. For example, to test triangle counting:
  ```bash
  cd ./graphs/neo4j/algorithms/triangle_counting
  python triangle_counting.py
  ```

- **NetworkX**: To test using NetworkX, run:
  ```bash
  python ./graphs/networkx/entrance.py
  ```
  Note that for NetworkX, we do not provide instances for applying graph-cutting oracles other than those identified by Algorithm 1. Users may implement them and add to `./graphs/networkx/output.json` file before running the above command.
  You can get the basic `./graphs/networkx/output.json` file by reproducing the task coverage results (see below).

- **Kuzu**: To test using Kuzu, run:
  ```bash
  python ./graphs/kuzu/launcher.py
  ```

### Reproducing Task Coverage Results

To reproduce the task coverage results, run:
```bash
python ./graphs/networkx/sample.py
```

### Reproducing Code Coverage Results

To reproduce the code coverage results:
1. Manually compile **Kuzu v0.4.2** and install the **LCOV** tool.
   - See [Kuzu Developer Guide](https://docs.kuzudb.com/developer-guide/) and [LCOV Documentation](https://lcov.readthedocs.io/en/latest/).
   
2. Once Kuzu and LCOV are set up, run:
   ```bash
   python ./graphs/kuzu/launcher.py
   ```



## 🐛 Found Bugs

*To keep the double-blind rules, we have removed the original links for bug reports in the artifacts submission.*

1. **GSlicer** detected 39 unique and previously unknown bugs, of which 34 have been fixed and confirmed by developers. The overall bug information can be found in `./found-bugs/overall.csv`.

2. Triggering test cases for logic bugs can be found in `./found-bugs/cases`.
