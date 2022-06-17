# Use-Google-geocoding-and-distance-matrix-APIs-using-Python
As a development practitioner working on education-related interventions in Lower and Middle Income Country (LMIC) contexts, you may often be interested to know  the average distance traveled by a student to the school. Generally,  public schools keep the record of students' home addresses in their admission registers. Using this secondary data we can measure the distance travelled by each student from his/her home to his/her respective school. To do this we use Google geocoding API to turn student's physical addresses to geo location coordinates. We then use these coordinates to measure distance by leveraging google's distance matrix api and export the data as a csv file. 

Using the location coordinates, we can further use readily  available shape files of the administrative boundaries in QGIS to find which district each student belongs to. 

You need to have a developer's account on Google to be able to use the APIs. Once you have registered, Google adds free credit of upto $200 into your account. You can use this credit to use their APIs (once you have exhauseted your credit, you will be charged to your credit card. If you don't wish to be charged beyond the given credit, set a limit on the number of requests sent to the server). For further details please visit Google's APIs page. 

![](image3.png)




![](image4.png)
