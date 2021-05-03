# ETL

This project aims to extract basic information of the Steam store web and load it into a PostgreSQL database.

### EXTRACT

Scrap basic data of games published in the Steam store, such as link, id, name, price, user tags and genre, using BeautifulSoup.

The primary key of this table is id. This information is important for the next step, because we need to guarantee that this value is unique.

### TRANSFORM

During this step we check if there null values and if there empty values for genre and transform the data into a dataframe.

### LOAD

Use SQLAlchemy to load the dataframe into a PostgreSQL database installed locally.

## Structure

This repo contains the python script for ETL pipeline and dataframe extracted.
