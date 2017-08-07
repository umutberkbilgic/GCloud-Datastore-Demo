#!/usr/bin/python
import cgi
from google.cloud import datastore
 
client = datastore.Client()
query = client.query(kind = "carlist")
query.add_filter("price", ">", 0)
query.order = ["-price"]
 
results = str(list(query.fetch())).split("Entity")
results.pop(0)
 
car_id_list = []
                   
for r in results:
    r = str(r)
    index_start = r.find("u'carlist', ") + 12
    index_end = r.find("L", index_start)
    car_id_list.append(int(r[index_start : index_end]))
 
table_str = "" 
 
for id in car_id_list: 
    car_key = client.key("carlist", id)
    ent = client.get(car_key)
           
    make =  str( ent.get("make"))
    model = str(ent.get("model"))
    color = str(ent.get("color"))
    year =  str(ent.get("year"))
    price = "$ " + str("{:,}".format(int( ent.get("price") )))
    power = str(ent.get("power"))
 
    table_str += """
    <tr>  
        <td>""" + make + """</td>
        <td>""" + model + """</td>
        <td>""" + color + """</td>
        <td>""" + year + """</td>
        <td>""" + price + """</td>
        <td>""" + power + """</td>
    </tr>"""   
 
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Car</title>"
print """
 
<style>
table {
   font-family: arial, sans-serif;
   border-collapse: collapse;
   width: 100%;
}
 
td, th {
   border: 1px solid #dddddd;
   text-align: left;
   padding: 8px;
}
 
tr:nth-child(even) {
   background-color: #dddddd;
}
</style>
 
"""
 
print "</head>"
print "<body>"
print "<h2> List of cars in database: </h2>"
 
print """
<table style="width:100%">
    <tr>
        <th>Make</th>
        <th>Model</th>
        <th>Color</th>
        <th>Year</th>
        <th>Price</th>
        <th>Horsepower</th>
    </tr>
"""
 
print table_str
 
print """</table>
 
<form action=\"http://35.195.58.189/\">
<input type=\"submit\" value=\"Go back\" />
</form>
 
</body>
</html>
"""
