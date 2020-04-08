from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import *
import datetime

def init_spark():
    spark = SparkSession \
        .builder\
        .getOrCreate()
    return spark

def create_udf(date_type):
    if date_type == 'year':
        return udf(lambda d: datetime.datetime.strptime(d, "%Y-%m-%d").year, IntegerType())
    elif date_type == 'month':
        return udf(lambda d: datetime.datetime.strptime(d, "%Y-%m-%d").month, IntegerType())
    else:
        return udf(lambda d: datetime.datetime.strptime(d, "%Y-%m-%d").day, IntegerType())

def crime_name_to_number(name):
    if name == 'Introduction':
        return 1
    # name == 'Vol de véhicule à moteur'
    elif 'Vol de' in name:
        return 2
    # name == 'Vol dans / sur véhicule à moteur'
    elif 'Vol dans' in name:
        return 3
    # name == 'Méfait'
    elif 'fait' in name:
        return 4
    # name == 'Vol(s) qualifié'
    elif 'qualifi' in name:
        return 5
    # name == 'Infraction entraînant la mort'
    elif 'Infraction' in name:
        return 6
    else:
        print(name)
        assert False

def time_of_day_to_number(name):
    if name == 'jour':
        return 1
    elif name == 'soir':
        return 2
    elif name == 'nuit':
        return 3
    else:
        print(name)
        assert False

def preprocess(file_name, keep_incomplete_records=False):
    spark = init_spark()
    df = spark.read.csv("../data/crimes_dataset.csv", header=True, mode="DROPMALFORMED")

    if not keep_incomplete_records:
        # Remove records with no latitude, longitude
        df = df.filter(df.X != 0).filter(df.X != 1)

    # Add year, month, day
    df = df.withColumn("YEAR", create_udf('year')("DATE"))
    df = df.withColumn("MONTH", create_udf('month')("DATE"))
    df = df.withColumn("DAY", create_udf('day')("DATE"))

    # Translate values to numbers
    df = df.withColumn("CATEGORY", udf(crime_name_to_number, IntegerType())("CATEGORIE"))
    df = df.withColumn("TIME_OF_DAY", udf(time_of_day_to_number, IntegerType())("QUART"))

    # Print
    df = df.drop('CATEGORIE', 'DATE', 'QUART', 'X', 'Y')
    df.toPandas().to_csv('../data/' + file_name, index=False)


if __name__ == '__main__':
    preprocess('crimes_dataset_processed.csv')
    preprocess('crimes_dataset_processed_incomplete.csv', keep_incomplete_records=True)
