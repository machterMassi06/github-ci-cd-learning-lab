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

# Let’s Talk About CI/CD Pipelines with GitHub Actions

## Introduction: Why Automate with GitHub Actions?
GitHub Actions pipelines automate **build, test, and deployment** processes for every defined Git event (e.g., push to a specific branch, pull request, merge).

**Key Point:**

While developers can (and should!) run tests locally using scripts before pushing or creating a pull request, GitHub Actions ensures your code integrates smoothly if it passes the CI pipeline.
In this project, we’ll explore the basics of how these pipelines work and cover key definitions and best practices.

---

## 1. Definitions

**GitHub Actions** is a GitHub tool that provides a powerful platform for setting up CI/CD pipelines.
- A **pipeline (workflow)** is an automated procedure linked to a Git repository.

---

## 2. How a Pipeline (Workflow) Works

- A pipeline consists of **one or more jobs**. By default, jobs run in parallel.
- You can define dependencies between jobs (using `needs` or stages).
- A **job** is made up of **steps**. Each step is an action or command.
- A job is executed by a **runner** , a virtual machine provided by GitHub ; free :-) .
- The pipeline is triggered by **events** (e.g., push, pull request, release).

---

## 3. Key Concepts

| Concept               | Description                                                                                     | Example                                                                                     |
|-----------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Job**               | Unit of work in a workflow; runs in a dedicated environment; can be parallel or sequential.     | `job: test`                                                                                 |
| **Steps**             | Sequential actions within a job (using Marketplace actions or custom commands).                | `step: pip install -r requirements.txt`                                                    |
| **Checkout**          | Action that clones the repository into the workflow environment.                              | `uses: actions/checkout@v4`                                                                |
| **Events/Conditions** | Expressions controlling job execution based on events (push, pull requests) or branches.       | `on: push: branches: [main]`                                                                |
| **Marketplace**       | Catalog of reusable actions developed by the community.                                        | [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)                     |

---

## 4. Creating Workflows

To create a workflow:
1. Create a **.github/workflows** directory in your repository.
2. Add workflow files in **YAML format** to this directory.

---

## 5. Managing Artifacts

**Artifacts** are files or directories generated by a job. They can be archived and shared between jobs in the same workflow.
- Use the **upload-artifact** action to archive artifacts.
- Use the **download-artifact** action to retrieve them in other jobs.

**Example:**
```yaml
- name: Upload test reports
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: reports/
```

---

## 6. Matrices

**Matrices** allow you to run the same job in parallel with different configurations (e.g., multiple Python versions).
This is useful for testing your application across different language versions, operating systems, or dependencies.

**Example:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
```

---

## 7. Full Example: Python Project Workflow

```yaml
name: Python CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest --cov=./ --cov-report=xml
      - name: Upload coverage
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: coverage.xml
```

---

## 8. Resources

- **Detailed Workflow Guide:** [Stéphane Robert’s Blog](https://blog.stephane-robert.info/docs/pipeline-cicd/github/)
- **Official GitHub Actions Documentation:** [GitHub Docs](https://docs.github.com/en/actions)
- **Workflow Examples:** [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)

---

# CI/CD Pipeline in This Project

In the `.github/workflows` directory, I’ve defined the following workflows to automate code quality checks and enforcement:

---

## **1. PEP8 Linter (`linter.yml`)**
 **File:** `.github/workflows/linter.yml`

### **Purpose**
This workflow ensures **all Python files comply with PEP8**, the official Python style guide.
It runs **automatically** in the following cases:
- On every **push** to the `main` branch.
- On every **pull request** targeting `main`.

### **What It Does**
1. Installs **Ruff** (a fast Python linter/formatter).
2. Checks PEP8 compliance 
3. **Fails the job** if violations are detected (e.g., unsorted imports, incorrect spacing, long lines).

---

### **What to Do If the Workflow Fails**
If the `linter` job fails, some Python files violate PEP8 rules.
**To fix the issues:**

1. Run locally:
   ```bash
   ruff check --fix --preview .
   ```
   - This **automatically fixes** most issues (e.g., import sorting, spacing).
   - Check changes with `git diff`.

2. Commit and push the fixes:
   ```bash
   git add .
   git commit -m "Fix PEP8 issues with Ruff"
   git push
   ```

3. The workflow should now **pass** .


---

## **2. Dependency Management (`dependabot.yml`)**

**File:** `.github/dependabot.yml`

### **What is it?**

Dependabot is a tool provided by GitHub to help you keep your project dependencies secure and up to date.

It automatically:

* detects vulnerable dependencies,
* suggests updates,
* and creates pull requests to fix or upgrade them.

Dependabot helps reduce security risks and ensures your project uses maintained and compatible versions of its dependencies.

For more details, see the official guide:
[dependabot-quickstart-guide](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart-guide)

---

### **What Dependabot does in this project**

1. **Monitors dependencies**
   
   It checks dependencies from:

   * Python (`pip`)
   * GitHub Actions

   All checks are performed from the root directory of the project.

2. **Runs on a schedule**

   * Executes checks **weekly**
   * Can ignore specific dependencies (e.g. `pyspark`) to avoid breaking changes

3. **Automates updates**

   * Creates pull requests automatically when updates are available
   * Limits the number of open PRs
   * Uses standardized commit prefixes:

     * `chore` for Python dependencies
     * `ci` for GitHub Actions
   * Adds relevant GitHub labels to each PR

---

Voici une section README propre et cohérente avec ce que tu fais 👇

---

## **3. Continuous Integration – Run Tests (`ci.yml`)**

**File:** `.github/workflows/ci.yml`

### **What is it?**

Continuous Integration (CI) is a development practice that automatically runs tests whenever code is pushed or a pull request is opened.

In this project, GitHub Actions is used to ensure that all modules are working correctly and remain compatible across different Python versions.

---

### **What this CI does**

1. **Triggers automatically**

   * On every push to the `main` branch
   * On every pull request targeting `main`

2. **Tests multiple Python versions**

     * Python 3.9
     * Python 3.12
   * Ensures compatibility across environments

3. **Sets up the environment**

   * Installs Python
   * Installs project dependencies from `requirements.txt`

4. **Runs the test suite**

   * Executes the `run_tests.sh` script
   * Runs all modules except `main.py`
   * Uses embedded doctests inside each module

5. **Fails on errors**

   * If any test fails → the CI job fails

---

Happy CI! All tests passed, time for coffee :)