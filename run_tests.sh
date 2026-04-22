#!/bin/bash

show_help() {
    echo ""
    echo "Mini-Fink Test Runner"
    echo "_______________________________"
    echo ""
    echo "Usage:"
    echo "  ./run_tests.sh                     Run all tests"
    echo "  ./run_tests.sh --single_module X   Run a single module"
    echo "  ./run_tests.sh --help              Show help"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh"
    echo "  ./run_tests.sh --single_module mini_fink_science.py"
    echo "  ./run_tests.sh --single_module mini-fink-broker/mini_fink_science.py"
    echo ""
    exit 0
}


# PARSE ARGUMENTS
SINGLE_MODULE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --single_module)
      SINGLE_MODULE="$2"
      shift 2
      ;;
    --help|-h)
      show_help
      ;;
    *)
      shift
      ;;
  esac
done

echo "Running Mini fink broker Tests" 
echo "_______________________________"

export MINI_FINK_BROKER_HOME="./mini-fink-broker" # adapte with the truth path
source ./venv/bin/activate

# Test single module 

if [ -n "$SINGLE_MODULE" ]; then

    MODULE_PATH="$SINGLE_MODULE"

    if [ ! -f "$MODULE_PATH" ]; then
        MODULE_PATH="$MINI_FINK_BROKER_HOME/$SINGLE_MODULE"
    fi

    python3 "$MODULE_PATH"
    exit 0
fi

# Testing all modules

for file in $MINI_FINK_BROKER_HOME/*.py
do
    #  skip main.py
    if [[ "$(basename "$file")" == "main.py" ]]; then
        continue
    fi
    python "$file"
done 