from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from typing import Tuple, Dict, List, Optional
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType, MapType, ArrayType
import uuid

class _SparkSQLClient:
    def __init__(self, spark: SparkSession):
        """
        Initialize the SparkSQLClient with a Spark session.

        Args:
            spark (SparkSession): The Spark session to use for SQL execution.
        """
        self.spark = spark
    
    def read_sql(self, sql_query: str):
        """
        Execute the given SQL query using the Spark session.

        Args:
            sql_query (str): The SQL query to execute.

        Returns:
            DataFrame: The result of the SQL query as a PySpark DataFrame.
        """
        try:
            # Execute the SQL query and return the result as a DataFrame
            df = self.spark.sql(sql_query)
            return df
        except Exception as e:
            # Handle any exceptions that occur during SQL execution
            print(f"An error occurred while executing the SQL query: {e}")
            raise e
        

class DQCheck:
    """
    Class for performing data quality checks on a specified table using a given SQL query
    and saving the results into a Delta table for auditing purposes.
    """
    def __init__(self, spark: SparkSession, audit_table_name: str = "audit_log"):
        """
        Initialize the DQCheck class.

        Args:
            spark (SparkSession): The Spark session.
            audit_table_name (str): The name of the Delta table to store audit logs.
        """
        self.spark = spark
        self.audit_table_name = audit_table_name
    
    def perform_dq_check(self,
                         table_type: str,
                         table_name: str,
                         primary_keys: List[str],
                         sql_query: str,
                         scope: Optional[str] = None,
                         secret: Optional[str] = None,
                         data_batch_identifier_name: Optional[str] = None,
                         data_batch_identifier_value: Optional[str] = None,
                         quality_threshold_percentage: int = 5) -> None:
        """
        Perform data quality checks on a specified table using a given SQL query and save the results into a Delta table.

        Args:
            table_type (str): The type of the table ('delta' or 'asql').
            table_name (str): The name of the table.
            primary_keys (List[str]): List of primary key columns. 
            sql_query (str): The data quality check query.
            scope (Optional[str]): Optional scope parameter 
            secret (Optional[str]): Optional secret parameter 
            data_batch_identifier_name (Optional[str]): Optional batch identifier name.
            data_batch_identifier_value (Optional[str]): Optional batch identifier value.
            quality_threshold_percentage (int): Quality threshold percentage (default is 5%).

        Returns:
        Tuple[str, float, Dict[str, List]]: Tuple containing:
            - Status of the data quality check ('Passed' or 'Failed').
            - Percentage score of failed records.
            - Primary keys of failed records in dictionary format.
        
        Appends the resuls of DQ check to Delta table

        """

        # Validate input parameters

        # if not isinstance(self.spark, SparkSession):
        #     raise ValueError("Invalid input: 'spark' must be an instance of SparkSession.")
        
        if table_type not in ['delta', 'asql']:
            raise ValueError("Invalid input: 'table_type' must be 'delta' or 'asql'.")
        
        if not isinstance(table_name, str) or not table_name:
            raise ValueError("Invalid input: 'table_name' must be a non-empty string.")
        
        if not (table_name.count('.') == 2 or table_name.count('.') == 1):
            raise ValueError("Invalid input: 'table_name' must be a non-empty string and with (catalog and schema name) or with schema name only.")
        
        if not isinstance(primary_keys, list) or not all(isinstance(key, str) for key in primary_keys):
            raise ValueError("Invalid input: 'primary_keys' must be a list of strings.")
        
        if not isinstance(sql_query, str) or not sql_query:
            raise ValueError("Invalid input: 'sql_query' must be a non-empty string.")
        
        if data_batch_identifier_name is not None and not isinstance(data_batch_identifier_name, str):
            raise ValueError("Invalid input: 'data_batch_identifier_name' must be a string if provided.")
        
        if data_batch_identifier_value is not None and not isinstance(data_batch_identifier_value, str):
            raise ValueError("Invalid input: 'data_batch_identifier_value' must be a string if provided.")
        
        if not isinstance(quality_threshold_percentage, int) or quality_threshold_percentage < 0 or quality_threshold_percentage > 100:
            raise ValueError("Invalid input: 'quality_threshold_percentage' must be an integer between 0 and 100.")

        if not isinstance(self.audit_table_name, str) or not self.audit_table_name or not self.audit_table_name.count('.') == 2 :
            raise ValueError("Invalid input: 'audit_table_name' must be a non-empty string and with catalog and schema name.")
        
        #remove colon at end if present
        sql_query = sql_query.replace(';','')
        # Check if the query contains aggregation functions
        aggregates = ['min', 'max', 'avg', 'sum', 'count', 'group by']
        agg_ind = next(('y' for i in aggregates if i in sql_query.lower()), None)




        # Determine the SQL query for data extraction
        if data_batch_identifier_name is None:
                sql_stmt = f"SELECT * FROM {table_name}"
        else:
                sql_stmt = f"SELECT * FROM {table_name} WHERE {data_batch_identifier_name} = '{data_batch_identifier_value}'"
                
        print(f"Executing query: {sql_stmt}")

        if (table_type).lower() == 'delta':
            # Create an instance of SparkSQLClient
            client = _SparkSQLClient(self.spark)
        elif (table_type).lower() == 'asql':
            client = AzureSQLClient(database_jdbc_url=dbutils.secrets.get(scope=scope,key=secret)) 
        else:
            print(F"Invalid table type. It should either be delta or asql")
             
        #### DQ check logic     

        #get total count from table for batch id
        total_count_sql = f"with sql_sample as ({sql_stmt}) select count(*) as tot_cnt from sql_sample"
        print(F"total count sql:{total_count_sql}")
        #create dq check sql
        dq_sql = f"with sql_sample as ({sql_stmt}) " + sql_query.replace(table_name,'sql_sample')
        print(F"dq_sql:{dq_sql}")
        #get count of records failing dq check
        dq_count_sql = f"select count(*) as dq_cnt from ({dq_sql})"
        print(F"dq_count_sql:{dq_count_sql}")
        #create primary keys for select expression
        primary_keys_str = ','.join(primary_keys)
        dq_primary_key_sql = F"(select {primary_keys_str} from ({dq_sql}))"
        print(F"dq_primary_key_sql:{dq_primary_key_sql}")

        df_dq_count = client.read_sql(dq_count_sql)
        df_total_count = client.read_sql(total_count_sql)
        dq_count = list(df_dq_count.first().asDict().values())[0]
        total_count = list(df_total_count.first().asDict().values())[0]

        print(F"dq_cnt and total_cnt are {dq_count} and {total_count}")
        # Calculate percentage score of failed records
        percentage_score = (dq_count / total_count) * 100
        # Determine the status based on the quality threshold
        status = "Passed" if percentage_score <= quality_threshold_percentage else "Failed"
        # Collect primary keys of failed records
        failed_primary_keys = {}
        try:
            df_failed_primary_keys = client.read_sql(dq_primary_key_sql)
            failed_primary_keys = df_failed_primary_keys.select(primary_keys).toPandas().to_dict(orient='list')
            failed_primary_keys_sample = df_failed_primary_keys.select(primary_keys).limit(150).toPandas().to_dict(orient='list')
        except Exception as e:
            print(F"primary keys are not found in table {table_name}. Please see error below \n {e}")
                 


        # Define the schema for the audit log data
        audit_log_schema = StructType([
                    StructField("UniqueCheckID", StringType(), nullable=False),  # Unique ID for each check
                    StructField("CheckTimestamp", StringType(), nullable=False),  # Timestamp when the check was performed
                    StructField("TableName", StringType(), nullable=False),  # Name of the table being checked
                    StructField("TableType", StringType(), nullable=False),  # Type of the table ('delta' or 'asql')
                    StructField("QueryUsed", StringType(), nullable=False),  # Data quality check query used
                    StructField("Status", StringType(), nullable=False),  # Status of the data quality check ('Passed' or 'Failed')
                    StructField("FailedRecordsCount", IntegerType(), nullable=False),  # Count of failed records
                    StructField("FailedRecordsKeys", MapType(StringType(), ArrayType(StringType())), nullable=True),  # Primary keys of failed records
                    StructField("PercentageScore", FloatType(), nullable=False)  # Percentage score of failed records
                ])
                
        # Prepare the data to be written to the audit log table
        audit_log_data = {
                        "UniqueCheckID": str(uuid.uuid4()),  # Unique ID for each check
                        "CheckTimestamp": '',
                        "TableName": table_name,
                        "TableType": table_type,
                        "QueryUsed": sql_query,
                        "Status": status,
                        "FailedRecordsCount": dq_count,
                        "FailedRecordsKeys": failed_primary_keys,
                        "PercentageScore": round(percentage_score, 2)
                    }
                    
        #print(F"audit log data {audit_log_data}")
        # Create DataFrame for the audit log data
        
        audit_log_df = self.spark.createDataFrame([audit_log_data],schema=audit_log_schema).withColumn("CheckTimestamp",current_timestamp())

        print(F"Appending DQE results to table {self.audit_table_name}")     
        # Write the audit log data into the Delta table
        audit_log_df.write.format("delta").mode("append").saveAsTable(self.audit_table_name)

        return(status,percentage_score,failed_primary_keys_sample)