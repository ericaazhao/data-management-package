Airflow Fraud Dataset Processing

Overview

This project demonstrates how to process a synthetic financial fraud dataset using Apache Airflow. The dataset contains various types of transactions (e.g., PAYMENT, TRANSFER, CASH_OUT) and includes labeled information on whether a transaction is fraudulent. The main objectives of this project are to clean the dataset, perform feature engineering, and prepare the data for further analysis.

Dataset Information

    •	Original dataset: Synthetic_Financial_Datasets_For_Fraud_Detection.csv
    •	Processed dataset: processed_dataset.csv (or processed_fraud_dataset.csv if renamed)
    •	Number of rows in original dataset: [Add row count, e.g., 635,000 rows]
    •	Number of columns in original dataset: 11 columns

Key Features Added

    1.	amount_to_balance_ratio: A calculated feature representing the ratio of transaction amount to the sender’s original balance (amount / oldbalanceOrg).
    2.	high_value_transaction: A boolean flag indicating whether the transaction value exceeds $100,000 (True for high-value transactions, False otherwise).

Steps to Run the DAG

    1.	Environment Setup
    •	Ensure Apache Airflow is installed and running on your system. You can install required dependencies with the following:

pip install pandas airflow apache-airflow-providers-docker 2. Dataset Placement
• Place the original dataset in the following directory:
/opt/airflow/dags/data/Synthetic_Financial_Datasets_For_Fraud_Detection.csv 3. Deploy the DAG
• Copy the DAG file example_dag_with_dataset.py into the Airflow dags/ directory.
• Start Airflow services:
airflow scheduler
airflow webserver
• Open the Airflow web interface and trigger the DAG manually. 4. Processed Dataset
• After the DAG execution, the processed dataset will be saved in the following location:
/opt/airflow/dags/data/processed_dataset.csv
• If you wish to change the file name, update the variable processed_file in the DAG Python script before running the DAG.

File Descriptions

    •	example_dag_with_dataset.py: The Airflow DAG file responsible for orchestrating the dataset processing steps.
    •	Synthetic_Financial_Datasets_For_Fraud_Detection.csv: The original dataset used for processing.
    •	processed_dataset.csv: The output file containing the cleaned and enhanced dataset.

Processing Workflow

    1.	Read Dataset: Load the original dataset using pandas.
    2.	Clean Column Names: Remove unnecessary spaces or formatting issues in the column names.
    3.	Feature Engineering:
    •	Calculate amount_to_balance_ratio for all rows where the original balance (oldbalanceOrg) is greater than zero.
    •	Create a binary flag high_value_transaction to label transactions exceeding $100,000.
    4.	Save Processed Dataset: Export the processed DataFrame to a CSV file.

Example DAG Output

After successful execution, the processed dataset will contain the following columns:
• step
• type
• amount
• nameOrig
• oldbalanceOrg
• newbalanceOrig
• nameDest
• oldbalanceDest
• newbalanceDest
• isFraud
• isFlaggedFraud
• New columns:
• amount_to_balance_ratio
• high_value_transaction

Next Steps

    1.	Perform exploratory data analysis (EDA) to identify patterns in fraudulent and non-fraudulent transactions.
    2.	Develop and evaluate predictive models for fraud detection using the processed dataset.
