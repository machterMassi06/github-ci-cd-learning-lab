import pandas as pd 
from pyspark.sql.functions import pandas_udf 

@pandas_udf("string")
def classify(magnitude: pd.Series) -> pd.Series:
    """
    Classify alerts based on magnitude.
    >>> df = spark.read.json("data/fink_alerts_sample.json")
    >>> sorted(df.select(classify(df["mag"])).rdd.map(lambda r: r[0]).collect())
    ['normal', 'normal', 'normal', 'very_bright', 'very_bright', 'very_bright']
    """
    return magnitude.apply(
        lambda x: "very_bright" if x < 18 else "normal"
    )

if __name__=="__main__":
    from tests.run_tests import run_spark_tests
    run_spark_tests(globals(),verbose=False,module_name=__file__)