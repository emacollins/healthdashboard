# Health Dashboard ETL Process

The ETL process is designed to take in the ZIP export from the Health App on your iPhone, extract the relevant data files, transform and clean the data to a flat file in a proper data structure, and load into a PostgresSQL DB fact and dimension tables.

The pipeline is broken up into various components that can be deployed individually. The pipeline itself orchestrates the running of these components to automate the process of loading new data into the database. Artifacts of each component are stored at various stages to be stored and load into the subsequent component.

Each component is deployed as a task on AWS Elastic Container Service (ECS). All tasks run on a single cluster, and are triggered in the pipeline. 


## Components

### Extract
The extract component unzips the original export, and pulls out the XML file. This is then converted to a CSV flat file for processing, while making no modifications to the data itself.

### Transform
The transform component loads all 3 files from the extract step (Record, Workout, and ActivitySumamry), and peforms a number of cleaning and manipulation steps to ensure data integrity and compatibility with the database schema. 

### Load
The load step takes the output of the transform step, and connects to the SQL server to load data in. This involves a collection of SQL scripts and the `psycopg2` library.


## Pipeline

The pipeline defines a class to handle launching and monitoring each component as an ECS task. Each pipeline run will follow the order EXTRACT -> TRANSFORM -> LOAD.