# GITHUB CI/CD LEARNING LAB

Welcome to this CI/CD learning lab using **GitHub Actions**.

In this lab, I’ll use a Python project as an example (though the concepts can be adapted to other projects). The main goal is to learn how to write CI pipelines with GitHub Actions.

---

## Usage

In this example, we’ll work with a mini Fink broker (a very simplified version). The real Fink broker is available [here](https://github.com/astrolabsoftware/fink-broker). This repo is just a convenient way to have a Python project to experiment with, and it’s a good fit since I work on the Fink team—a project based on Apache Spark & Kafka. But you can ignore that; this repo is purely for learning how to create a GitHub Actions CI pipeline for a Python project.


### Setup

```bash
git clone https://github.com/machterMassi06/github-ci-cd-learning-lab
cd github-ci-cd-learning-lab
```

A virtual environment is recommended:

```bash
python -m venv venv
source venv/bin/activate
```

Run `generate_fake_data.py` to generate alerts in the `data/` folder (`data/alerts.json`):

```bash
export PYTHONPATH=.
python3 generate_fake_data.py
```

Run the main script (with or without applying science modules/filters):

```bash
python3 mini-fink-broker/main.py -h
```

Output:
```
usage: main.py [-h] --input INPUT [--science] [--filters FILTERS]

Fink mini pipeline

options:
  -h, --help         show this help message and exit
  --input INPUT      Path to input JSON file (of alerts)
  --science          Apply science modules or not
  --filters FILTERS  Comma-separated filters (e.g. filter_1,filter_2)
```

For example (applying all options):

```bash
python mini-fink-broker/main.py --input data/alerts.json --science --filters filter_1,filter_3
```

This command simply displays the DataFrame (df.show(20)) after applying the business logic. You could adapt it—for example, by adding ingestion to a database, Kafka topics, etc.
## Run Tests

If you want to add new features—whether in existing files or by creating new modules—you should test your functions using **doctests**. Use `tests/run_tests.py` to run the tests (including doctrings) with a Spark session if needed.

To manually run the tests, use the following commands:

```bash
chmod +x run_tests.sh
./run_tests.sh -h
```

Output:

```
Mini-Fink Test Runner
_______________________________

Usage:
  ./run_tests.sh                     Run all tests
  ./run_tests.sh --single_module X   Run a single module
  ./run_tests.sh --help              Show help

Examples:
  ./run_tests.sh
  ./run_tests.sh --single_module mini_fink_science.py
  ./run_tests.sh --single_module mini-fink-broker/mini_fink_science.py
```

---

## Let’s Talk About CI/CD Pipelines

I’ll cover this next...