import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd


# Define a Python function to process the dataset
def process_dataset():
    # File path of the input dataset
    file_path = "/opt/airflow/dags/data/Synthetic_Financial_Datasets_For_Fraud_Detection.csv"
    
    # Step 1: Read the dataset
    try:
        df = pd.read_csv(file_path)
        print("Original Dataset Head (first 5 rows):")
        print(df.head())
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Step 2: Data Cleaning
    # Remove rows with missing values
    df.dropna(inplace=True)
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Step 3: Generate New Features
    # Create a column for the ratio of transaction amount to old balance
    df['amount_to_balance_ratio'] = df['amount'] / (df['oldbalanceOrg'] + 1e-9)  # Add a small value to prevent division by zero
    # Create a column to flag high-value transactions (e.g., transactions greater than 100,000)
    df['high_value_transaction'] = df['amount'] > 100000

    # Step 4: Data Filtering
    # Filter only 'TRANSFER' and 'CASH_OUT' transaction types
    filtered_df = df[df['type'].isin(['TRANSFER', 'CASH_OUT'])]

    # Step 5: Data Aggregation
    # Count the number of transactions by type and print the summary
    transaction_counts = filtered_df['type'].value_counts()
    print("\nTransaction Type Counts:")
    print(transaction_counts)

    # Step 6: Rename Columns
    # Convert all column names to lowercase for consistency
    filtered_df.columns = [col.lower() for col in filtered_df.columns]

    # Step 7: Save the processed dataset to a new file
    processed_file = "/opt/airflow/dags/data/processed_dataset.csv"
    try:
        filtered_df.to_csv(processed_file, index=False)
        print(f"\nProcessed dataset saved to {processed_file}")
        print("\nProcessed Dataset Head (first 5 rows):")
        print(filtered_df.head())
    except Exception as e:
        print(f"Error saving the file: {e}")
        return


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',  # The owner of the task
    'retries': 1,        # Number of retry attempts in case of failure
    'retry_delay': timedelta(minutes=5),  # Delay between retries
}

# Define the DAG
with DAG(
    dag_id='example_dag_with_dataset',  # Unique identifier for the DAG
    default_args=default_args,          # Default arguments for the DAG
    description='An example DAG with enhanced dataset processing',  # Description of the DAG
    schedule=None,  # DAG will only run when triggered manually
    start_date=datetime(2023, 11, 10),  # Start date for the DAG
    catchup=False,  # Do not backfill or run past executions
) as dag:

    # Define a task to process the dataset
    process_task = PythonOperator(
        task_id='process_dataset',  # Task identifier
        python_callable=process_dataset  # Function to execute
    )
