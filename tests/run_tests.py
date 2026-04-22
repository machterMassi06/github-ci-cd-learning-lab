import sys
import doctest
from pyspark.sql import SparkSession
import time


def run_spark_tests(globs=None, verbose=False, module_name="unknown"):
    """
    Spark + doctest runner .

    Parameters
    ----------
    globs : dict
        Global namespace to test
    verbose : bool
        Print doctest output
    """

    if globs is None:
        globs = {}

    #  Spark session
    spark = (
        SparkSession.builder.master("local[2]").appName("MiniFinkTests").getOrCreate()
    )

    globs["spark"] = spark

    print("==============================\n")
    print(f"Module tested : {module_name}")

    #  run doctests
    start_time = time.time()
    result = doctest.testmod(globs=globs, verbose=verbose)

    failed = result.failed
    attempted = result.attempted

    duration = time.time() - start_time

    # REPORT

    print(f"✔ Tests executed : {attempted}")
    print(f"❌ Tests failed  : {failed}")
    print(f"⏱ Duration      : {duration:.2f}s")
    print("==============================\n")
    if failed > 0:
        print("❌ TESTS: FAILED")
    else:
        print("✅ TESTS: SUCCESS")

    sys.exit(failed)
