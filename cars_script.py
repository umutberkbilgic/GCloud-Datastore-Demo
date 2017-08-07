#!/usr/bin/python
import cgi
from google.cloud import datastore
 
client = datastore.Client()
key = client.key("carlist")
car = datastore.Entity(key)
 
form = cgi.FieldStorage()
 
search_make = form.getvalue("f_make")
search_model = form.getvalue("f_model")
search_year = form.getvalue("f_year")
search_color = form.getvalue("f_color")
search_price = form.getvalue("f_price")
search_power = form.getvalue("f_power")
 
try:
        search_price_final = int(search_price)
except ValueError:
        search_price_final = 0
 
try:
        search_power_final = int(search_power)
except ValueError:
        search_power_final = 0
 
try:
        search_year_final = int(search_year)
except ValueError:
        search_year_final = 0
 
search_make_final = unicode(search_make)
search_model_final = unicode(search_model)
search_color_final = unicode(search_color)
 
features = {"make"  : search_make_final,
            "model" : search_model_final,
            "year"  : search_year_final,
            "color" : search_color_final,
            "price" : search_price_final,
            "power" : search_power_final}
car.update(features)
 
client.put(car)
 
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Car</title>"
print "</head>"
print "<body>"
print "<h2> Make: "  + search_make_final  + "</h2>"
print "<h2> Model: " + search_model_final + "</h2>"
print "<h2> Year: "  + search_year_final  + "</h2>"
print "<h2> Color: " + search_color_final + "</h2>"
print "<h2> Price: $ " + search_price_final + "</h2>"
print "<h2> Power: "   + search_power_final + " HP </h2>"
 
print "<form action=\"http://35.195.58.189/\">"
print "<input type=\"submit\" value=\"Go Back\" />"
print "</form>"
 
print "</body>"
print "</html>"
