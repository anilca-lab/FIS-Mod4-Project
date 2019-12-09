# FIS-Mod4-Project
This project examines the relationship between the overall effectiveness of the police and the stop-question-frisk policy change in NYC.

Date: December 2019

Project Members: Brad Johnson and Anil Onal

Goals: To come up with the model specification appropriate to examine the proposed relationship, collect the necessary data, and train and test the model.

Responsibilities:
 - Define project scope and focus
 - Collect data
 - Formulate question
 - Perform exploratory data analysis
 - Train a model
 - Test the model
 - Create Master Notebook
 - Create presentation
 - Lint/clean code file
 
Summary of files:
 - Master_Notebook.ipynb: Jupyter Notebook documenting the code and the analysis for the project. Written for a technical audience
 - data files:
     - df.csv: reported offenses, arrests, stops, and population aggregated annually and at the precinct level
     - borough_df.csv: borough and precinct data
     - offense_types_df.csv : offense types and keys data
     The following files have been used to create df.csv: 
     - [Offenses reported to the NYPD](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i)
      [download CSV](https://data.cityofnewyork.us/api/views/qgea-i56i/rows.csv?accessType=DOWNLOAD)
     - [Arrests by the NYPD](https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u) 
      [download CSV](https://data.cityofnewyork.us/api/views/8h9b-rp9u/rows.csv?accessType=DOWNLOAD)
     - [NYPD stop-question-frisk data](https://www1.nyc.gov/site/nypd/stats/reports-analysis/stopfrisk.page) 
     - [John Keefe: NYC precinct population data for 2010](https://johnkeefe.net/nyc-police-precinct-and-census-data) 
    [download CSV](https://github.com/pinnnnnn/MAP_Spring_2016/blob/master/NYC_Blocks_2010CensusData_Plus_Precincts.csv)
 - data_prep.py: Code used to clean data
 - data_modeler.py: Code used to engineer features and do modeling
 - visualizations.py: Code to produce visualizations
 - training.py: Code for model fitting
 - test.py: Code for model testing
 - Stop-question-frisk.pdf: PDF of slideshow presentation
 - [Slideshow](https://docs.google.com/presentation/d/1qCCb5k9CuM3CH0Y8Wq6eowyCYQgKv3oVReTsgcaw0Ok/)
