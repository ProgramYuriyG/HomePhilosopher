# HomePhilosopher
A website designed for viewing the differences in environmental data, crime rates, and weather between various counties across the Unites States

Climate Data is gathered from https://app.climate.azavea.com/accounts/api/
Crime Data is gathered from https://crime-data-explorer.fr.cloud.gov/api
Weather Data is gathered from https://www.ncdc.noaa.gov/

### Uses:
Python/Django – used for requests to the api's along with building the web application and running the local server

HTML/CSS – for the web pages

Python/Jquery/Javascript - for django template pages


## How To Use:
- First Clone the repo to any folder location and cd into it
- Once you are in the folder location, cd into "countymap"
- Perform any pip installations that are needed:
  - pandas
  - django
- Now you can run the command: python manage.py runserver
- Once this has finished, you can now go to your local host url (standard is: http://127.0.0.1:8000/)

