import pyspark.sql.functions as F


def filter_1():
    """
    Filters alerts with mag < 16.0 
    >>> df = spark.read.json("data/fink_alerts_sample.json")
    >>> df.filter(filter_1()).count()
    1
    """
    return F.col("mag") < 16.0

def filter_2():
    """
    Filters alerts with mag >= 16.0 
    >>> df = spark.read.json("data/fink_alerts_sample.json")
    >>> df.filter(filter_2()).count()
    5
    """    
    return F.col("mag") >= 16.0

def filter_3():
    """
    Filters alerts with fid == 1
    >>> df = spark.read.json("data/fink_alerts_sample.json")
    >>> df.filter(filter_3()).count()
    4
    """ 
    return F.col("fid") == 1

def filter_4():
    """
    Filters alerts with fid == 2
    >>> df = spark.read.json("data/fink_alerts_sample.json")
    >>> df.filter(filter_4()).count()
    2
    """ 
    return F.col("fid") == 2

def filter_5():
    """
    Filters alerts with 18.0 <= mag <= 19.5
    >>> df = spark.read.json("data/fink_alerts_sample.json")
    >>> df.filter(filter_5()).count()
    2
    """ 
    return (F.col("mag") >= 18.0) & (F.col("mag") <= 19.5)

def all_user_filters():
    """ Returns list of all user filters functions """
    userfilters = [filter_1, filter_2,filter_3,filter_4, filter_5]
    return userfilters

if __name__=="__main__":
    from tests.run_tests import run_spark_tests
    run_spark_tests(globals(),verbose=False,module_name=__file__)