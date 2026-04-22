import argparse
from pyspark.sql import SparkSession

from pipeline.registry import SCIENCE_MODULES, FILTERS


def parse_args():
    parser = argparse.ArgumentParser(description="Fink mini pipeline")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input JSONL file of alerts "
    )

    parser.add_argument(
        "--science",
        default="",
        help="Comma-separated science modules (e.g. is_bright,classify)"
    )

    parser.add_argument(
        "--filters",
        default="",
        help="Comma-separated filters (e.g. filter_1,filter_2)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # spark init


    #  science modules
    if args.science:
        for name in args.science.split(","):
            name = name.strip()
            if name in SCIENCE_MODULES:
                df = df.withColumn(
                    name,
                    SCIENCE_MODULES[name](df["mag"])
                )

    #  filters
    if args.filters:
        for name in args.filters.split(","):
            name = name.strip()
            if name in FILTERS:
                df = FILTERS[name](df)

    df.show()


if __name__ == "__main__":
    main()