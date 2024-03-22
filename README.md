# Dashboard for Apple Health Data

This is a codebase to create a personalized health dashboard from the Apple Health data exported by the user. 

The project is broken up into major and minor components, including the ETL pipeline and Dash front end.

## ETL

The data pipeline is broken up into harvest, extract, transform, and load components.

### Harvest

### Extract

The extract step takes the harvested `.zip` file and converts the relevant XML files to CSV.gz files of rtabular data processing.