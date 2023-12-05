# from pyspark.sql import SparkSession
# from pyspark.sql.functions import explode

# # Initialize a SparkSession
# spark = SparkSession.builder.getOrCreate()

# # Sample data
# data = [(1, ["A", "B", "C"]), (2, ["D", "E", "F"])]

# # Create DataFrame
# df = spark.createDataFrame(data, ["id", "receipt_array"])

# # Explode the receipt_array column
# df_exploded = df.select("id", explode(df.receipt_array).alias("receipt"))

# # Show the DataFrame
# df_exploded.show()

import pandas as pd
import numpy as np
import random
import string

def generate_data(n=20000):
    # Generate 'n' random ids
    ids = np.arange(1, n+1)

    # Generate 'n' random receipt arrays
    receipt_arrays = [random.choices(string.ascii_uppercase, k=5) for _ in range(n)]

    # Create a DataFrame
    df = pd.DataFrame({
        'id': ids,
        'receipt_array': receipt_arrays
    })

    return df

# Generate 1 million records
df = generate_data()

print(df.head(1000))