# HomePhilosopher
A website designed for viewing the differences in environmental data, crime rates, and weather between various counties across the Unites States. <br>


Climate Data is gathered from https://app.climate.azavea.com/accounts/api/ <br>
Crime Data is gathered from https://crime-data-explorer.fr.cloud.gov/api <br>
Weather Data is gathered from https://www.ncdc.noaa.gov/ <br>

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

### Homepage

![](/Home%20Philosopher%20Screenshots/homepage.PNG)

### United States County Mapper

![](/Home%20Philosopher%20Screenshots/county_map.png)

### County Comparison

![](/Home%20Philosopher%20Screenshots/county_comparison.PNG)


### Future Implementations
- Address Lookup
- Connect with more Api's and lower call times
- able to connect to houses for sale and have a comparison show up that way
