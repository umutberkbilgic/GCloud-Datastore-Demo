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
 
features = {"make"  : unicode(search_make),
            "model" : unicode(search_model),
            "year"  : int(search_year),
            "color" : unicode(search_color),
            "price" : int(search_price),
            "power" : int(search_power)}
car.update(features)
 
client.put(car)
 
format_price = ("{:,}".format(int(search_price)))
 
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Car</title>"
print "</head>"
print "<body>"
print "<h2> Make: "    + search_make  + "</h2>"
print "<h2> Model: "   + search_model + "</h2>"
print "<h2> Year: "    + search_year  + "</h2>"
print "<h2> Color: "   + search_color + "</h2>"
print "<h2> Price: $ " + format_price + "</h2>"
print "<h2> Power: "   + search_power + " HP </h2>"
 
print "<form action=\"http://35.195.58.189/\">"
print "<input type=\"submit\" value=\"Go Back\" />"
print "</form>"
 
print "<form action=\"/cgi-bin/cars.py\">"
print "<input type=\"submit\" value=\"View cars\" />"
print "</form>"
 
print "</body>"
print "</html>"
