## dq_check


## Overview

`dq_check` is a Python package that provides a data quality check function encapsulated in the `DQCheck` class. It allows you to perform data quality checks on tables using SQL queries and save the results into a Delta table for auditing purposes.

## Features

- Perform data quality checks on specified tables using SQL queries.
- Save audit logs of data quality checks into a Delta table.
- Handle aggregation checks and basic data quality metrics.
- Supports PySpark and Pandas integration.

## Installation

You can install `dq_check` from PyPI using pip:

## bash

pip install dq_check


## Usage

Here's an example of how to use the DQCheck class from the dq_check package:

from pyspark.sql import SparkSession
from dq_check import DQCheck

## Initialize Spark session
spark = SparkSession.builder.appName("DQCheckExample").getOrCreate()

## Create an instance of DQCheck
dq_checker = DQCheck(spark)

## Define the data quality check parameters
table_type = "delta"  # Type of the table ('delta' or 'asql')
table_name = "your_table_name"  # Name of the table
primary_keys = ["your_primary_key"]  # List of primary key columns
sql_query = "SELECT * FROM your_table WHERE condition"  # Data quality check query

## Perform the data quality check
dq_checker.perform_dq_check(
    table_type,
    table_name,
    primary_keys,
    sql_query,
    quality_threshold_percentage=5,  # Quality threshold percentage
    data_batch_identifier_name=None,  # Optional batch identifier name
    data_batch_identifier_value=None,  # Optional batch identifier value
    audit_table_name="your_audit_log_table"  # Name of the Delta table to store audit logs
)


## Configuration

Adjust the parameters passed to the perform_dq_check method based on your requirements.

## Dependencies

PySpark
Pandas

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests on the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or feedback, open a github issue