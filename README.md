# TASTE
#### Video Demo:  [<https://youtu.be/DAFe7rx6XlQ>](https://youtu.be/DAFe7rx6XlQ)
#### Description: 
- TASTE is a web-based application using Python and SQL. 
- The purpose is to save time deciding what to eat.
#### Organization:
- **application.py** configures our web server, defines functions, e.g., index, login, logout, and register.
- **helpers.py** defines functions to help with application.py, login_required and apology.
- **requirements.txt** includes a list of required libraries for our application.
- **taste.db** is the database to store our data.
- **static/** is a directory of static files.
  - **favicon.ico** is the icon on our website's title
  - **styles.css** is the CSS file
- **templates/** is a directory for files that will be used to create our final HTML.
  - **login.html** is returned when **login** function is requested via **"GET"**. User will log in on **login.html**.
  - **register.html** is returned when **register** function is requested via **"GET"**. User will register on **register.html**.
  - **password.html** is returned when **password** function is requested via **"GET"**. User can change password on **password.html**.
  - **apology.html** is returned when **apology** function is requested. User will be notified under certain conditions, e.g., user attempts to register with a username that already exists. 
  - **index.html** is returned when **index** function is requested. User will see **index.html** after logging in; **index.html** shows food reviews that the user has stored in **taste.db**.
  - **layout.html** includes common content that is shared between html files.
  - **add.html** is returned when **add** function is requested via **"GET"**. User can add food reviews to **taste.db** on **add.html**.
  - **search_food.html** is returned when **search_food** function is requested via **"GET"**. User can search food reviews that the user has stored in **taste.db** by **search by food** feature on **search_food.html**.
  - **searched_food.html** is returned when **search_food** function is requested via **"POST"**; **searched_food.html** shows the result of **search by food** feature.
  - **search_rate.html** is returned when **search_rate** function is requested via **"GET"**. User can search food reviews that the user has stored in **taste.db** by **search by rate** feature on **search_rate.html**.
  - **searched_rate.html** is returned when **search_rate** function is requested via **"POST"**; **searched_rate.html** shows the result of **search by rate** feature.
  - **search_region.html** is returned when **search_region** function is requested via **"GET"**. User can search food reviews that the user has stored in **taste.db** by **search by region** feature on **search_region.html**.
  - **searched_region.html** is returned when **search_region** function is requested via **"POST"**; **searched_region.html** shows the result of **search by region** feature.
  - **search_restaurant.html** is returned when **search_restaurant** function is requested via **"GET"**. User can search food reviews that the user has stored in **taste.db** by **search by restaurant** feature on **search_restaurant.html**.
  - **searched_restaurant.html** is returned when **search_restaurant** function is requested via **"POST"**; **searched_restaurant.html** shows the result of **search by restaurant** feature.
  - **search_style.html** is returned when **search_style** function is requested via **"GET"**. User can search food reviews that the user has stored in **taste.db** by **search by style** feature on **search_style.html**.
  - **searched_style.html** is returned when **search_style** function is requested via **"POST"**; **searched_style.html** shows the result of **search by style** feature.
  - **random.html** is returned when **random** function is requested via **"GET"**. User can get a randomly generated option from food reviews that the user has stored in **taste.db** by **random** feature.
  - **randomed.html** is returned when **random** function is requested via **"POST"**; **randomed.html** shows the result of **random** feature.
