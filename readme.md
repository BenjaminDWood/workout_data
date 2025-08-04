## Workout Data Dashboard

A project to help visualise exercise data (currently far more geared towards weightlifting exercises), in order to show different areas of progress week-to-week and month-to-month through Tableau visualisation. 

Python work mostly used pandas in order to preprocess the data and create working tables. Ideally the database of exercises could be maintained and accessed through mySQL, but using .csv connections is the most straightforward way when using public versions of the software.

Dashboards show percentage of exercises focused on each muscle group & progress over time for heaviest weight, average weight, total weight, and total reps by week.

### Files

- workout_data_script.py: Script for preprocessing raw data originally
- workout_data_tidy.ipynb: A tidied version of the Jupyter workbook used for preprocessing
- daily_strength2.csv: Raw data imported from app
- Other .csv files: Created dataframes
- new_exercise.ipynb: Contains work on creating a script to allow users to add new exercises
- New_Data.ipynb: Contains work on creating a script to integrate new data into the existing table automatically.


