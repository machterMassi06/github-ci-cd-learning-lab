import argparse

from filters import all_user_filters
from mini_fink_science import classify
from spark_utils import get_spark_session

sciences_modules = [classify]


def parse_args():
    parser = argparse.ArgumentParser(description="Fink mini pipeline")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input JSON file (of alerts) ",
    )

    parser.add_argument(
        "--science",
        action="store_true",
        help="Apply science modules or not",
    )

    parser.add_argument(
        "--filters", default="", help="Comma-separated filters (e.g. filter_1,filter_2)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # spark init
    spark = get_spark_session()

    print(f"\n Loading data from: {args.input}")
    df = spark.read.json(args.input)

    #  science modules
    if args.science:
        print("\nApplying science modules :")
        for sm in sciences_modules:
            print(f"Applying science module : {sm.__name__} ")
            df = df.withColumn("class", sm(df["mag"]))

    #  filters
    if args.filters:
        print("Applying filters in series (in the same df) : ")

        available_filters = {f.__name__: f for f in all_user_filters()}

        for filt_name in args.filters.split(","):
            filt_name = filt_name.strip()

            if filt_name not in available_filters:
                print(f" Unknown filter: {filt_name}")
                continue

            print(f" Applying {filt_name}")
            df = df.filter(available_filters[filt_name]())

    df.show()


if __name__ == "__main__":
    main()
