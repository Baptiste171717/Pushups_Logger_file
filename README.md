# 🚀 Welcome to your new awesome project!

THis is an apllication which will generate a workout program.
What this Fitness-app does :

-First you choose the frequency, which is the number of times you want to train per week. You must train at least once a week, and you cannot exceed seven workouts per week.

-Then, you can choose how much time you want to workout, the default duration is 120 minutes. Thus T_max represents the approximate duration you want for a training session.

-After, you can say whether you want some monotony with your session, that is whether you want to have different exercises for each workout-session.

-Then, you can decide whether you want to do only cardio, bodybuilding, or mix them both.

-Finally, a new workout program will be generated for a whole month, and you will be able to access any session whenever you want.

-Have the best workout time!!!

To give more details: You have a requirement file with all the module you need to make this app work, then you have the dockerfile which allows you to dockerize this web-application.
To do so, all you need is to enter : docker build --tag name_of_your_container ., it will buil a container with everything that you need inside.
Then you can run this command : docker run -d -p 5000:5000 name_of_your_container, which allows you to run your container and to look at the result at http://localhost:5000/

The webpack.config.js and the package json files are used to configuerate the web parameters of your application, it allows also to make sure that you have everything that you need in terms of frontend modules/assets to run your application.

In the instance directory, you can finc two databases, one used for the user and the other used to store all the workout exercices that the application can provide in your workout-program. The pushups_logger directory contains the foundations of the application, that leans, the templates, the static data like the images, the css files, the json files needed to make the tempaltes work, and finally the python files that make you application run.

Flask is the python module which is used to create the application. 

There are some functionnalities which were not implemented but almost coded. For example in the file main.py, some finctions are commented, these functions would actually allow the user to dtransform the database which contains all the workout exercise, it coulf first display it which some pagination, and then it could change it by adding or deleting new exercices or even by modifying some. The template that sould be use for that is almost completly coded, it is the all_workouts.html template.. These are potential options to improve the application.

