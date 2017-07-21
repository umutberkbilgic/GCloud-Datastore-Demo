# Umut Berk Bilgic
# July 2017
# @ Sebit Information & Education Technologies
# METU Teknokent, Ankara, Turkey

from google.cloud import datastore
import datetime
import os

datastore_client = datastore.Client()
kind = "users"
project_url = "https://console.cloud.google.com/home/dashboard?project=sebit-gcloudtest-1"

# open saved user id counter
countRecord = open("useridcount.txt","r")
count = int(countRecord.read())

def clear_query_result(res):
	res = unicode(str(res))
	res = res.replace("u'", " ")
	res = res.replace("' ", " ")
	res = res.replace("  ", " ")
	res = res.replace("'", "")
	res = res.replace("}>", ",")
	
	return res

def shift_list_left(data):
	data_size = len(data)
	
	temp_list = [None] * (data_size - 1)
	
	for i in range(0, data_size - 1):
		temp_list[i] = data[i + 1]
		
	return temp_list

def format_date(inc_date):
	# incoming date format: year, month, day, hour, minute, tick/ms
	split_date = inc_date.split(", ")
	
	year = split_date[0]
	month = split_date[1]
	day = split_date[2]
	hour = split_date[3]
	minute = split_date[4]
	tick = split_date[5]
	
	calendar = day + "." + month + "." + year
	clock = hour + ":" + minute
	
	return (clock + " " + calendar + "(UTC)")

def pretty_print(res):
	res = clear_query_result(res)
	temp_list = res.split("Entity")
	splitted_list = shift_list_left(temp_list)
	
	pretty_print = ""
	pretty_users_all = ""
	pretty_id_all = ""
	pretty_updated_all = ""
	pretty_email_all = ""
	pretty_pass_all = ""
	
	for res in splitted_list:
		users_start = res.find("users, ") + 7
		users_end = res.find(") {", users_start)
		
		id_start = res.find("id: ") + 4
		id_end = res.find("L,", id_start)
		
		updated_start = res.find("updated: datetime.datetime(") + 27
		updated_end = res.find(", tz", updated_start)
		
		email_start = res.find("email: ") + 7
		email_end = res.find(",: ", email_start)
		
		pass_start = res.find("pass: ") + 6
		pass_end = res.find("}>", pass_start)
		
		pretty_users = res[users_start : users_end]
		pretty_id = res[id_start : id_end]
		pretty_updated = res[updated_start : updated_end]
		pretty_email = res[email_start : email_end]
		pretty_pass = res[pass_start : pass_end]
		
		pretty_updated = format_date(pretty_updated); # fix calendar formatting 
		
		pretty_print += "\n________________________\n\nUsername: " + pretty_users + "\nUser ID: " + pretty_id + "\nLast updated: "
		pretty_print += pretty_updated + "\nE-mail: " + pretty_email + "\nPassword: " + pretty_pass
		
		pretty_users_all += pretty_users + "|" # -> "Tirion Fordring|Sylvanas Windrunner|..."
		pretty_id_all += pretty_id + "|"
		pretty_updated_all += pretty_updated + "|"
		pretty_email_all += pretty_email + "|"
		pretty_pass_all += pretty_pass + "|"
		
	 
	return [pretty_print, pretty_users_all, pretty_id_all, pretty_updated_all, pretty_email_all, pretty_pass_all]
	
while True:
	prompt = raw_input("\n...\n\n[1]: Display spesific user\n[2]: Add or update user\n[3]: Delete a user\n[4]: Filter\n[0]: Exit\n\n>>")
	
	if (prompt == "1" or prompt == "display"):
		name = raw_input("Username: ")
		
		key = datastore_client.key(kind, name)
		ent = datastore_client.get(key)

		if (str(ent) == "None"):
			print ("\nCONSOLE: No user with that name exists.")
		else:
			pretty_properties = pretty_print(ent)
			print (pretty_properties[0]) 
		
	elif (prompt == "2" or prompt == "add" or prompt == "update"):
		# get the name that will be updated/created
		name = raw_input("Username: ")

		# does the emtry exist? if so, update if not add
		key = datastore_client.key(kind, name)
		ent = datastore_client.get(key)
		
		found = (str(ent) != "None")

		# get user query
		query1 = unicode(raw_input("e-mail:   "))
		query2 = unicode(raw_input("Password: "))

		# Set which kind and entity is being worked on
		user_key = datastore_client.key(kind, name)
		user = datastore.Entity(key = user_key)

		# changes/additions to be made
		user.update({ 
			"email":query1, 
			"pass":query2,
			"id": count, 
			"updated":datetime.datetime.utcnow() })

		"""# if the user did not exist before update user ID too
		if (not found):
			user.update({"id":count})"""

		# send changes to google cloud datastore API
		datastore_client.put(user)

		# console log
		print ("\n'" + name + "' has been updated.")
		print ("User-ID: " + str(count))

		# increment local counter and rewrite useridcount.txt
		count = count + 1
		countRecord = open("useridcount.txt","w")
		countRecord.write(str(count))
		
	elif (prompt == "3" or prompt == "delete"):
		name = raw_input("Username: ")
		
		sure = raw_input("Are you sure?(y/n): ")
		if (sure == "y"):
			key = datastore_client.key(kind, name)
			delFlag = datastore_client.get(key)

			if (str(delFlag) == "None"):		
				print ("\nCONSOLE: No user with that name exists.")
			else:
				datastore_client.delete(key)
				print ("\nDeletion successful.")
			
		else:
			print ("Canceling the delete operation. No changes have been made.\n")
			
	elif (prompt == "4" or prompt == "search"):
		q_filter = unicode(raw_input("Type the query filter you want to apply: "))
		q_list = q_filter.split(" ")
		
		query = datastore_client.query(kind = "users")
		query.add_filter(q_list[0], q_list[1], int(q_list[2]))
		
		result = list(query.fetch())
		pretty_properties = pretty_print(result)
		print (pretty_properties[0])
		
	elif (prompt == "/resetuseridcount" or prompt == "/r"):
		countRecord = open("useridcount.txt","w")
		countRecord.write("0")
		print ("\nCONSOLE: Successfully resetted User-ID counter.\n")

	elif (prompt == "/clear" or prompt == "/c"):
		os.system("clear")
	elif (prompt == "/link" or prompt == "/l"):
		os.system("sensible-browser " + project_url)
		
	elif (prompt == "/displayalldata" or prompt == "/d"):
		query = datastore_client.query(kind = "users")
		query.add_filter("id", ">", -1)

		print ("CONSOLE: Connecting to Google Cloud Datastore Servers...")
		result = list(query.fetch())
		print ("CONSOLE: Query fetch completed.")
		
		print ("\n RAW data from Google Cloud servers: \n\n")
		print result
		print ("\n\n")
		
		pretty_properties = pretty_print(result)
		print (pretty_properties[0])
		
	elif (prompt == "/find" or prompt == "/f"):
		query = datastore_client.query(kind = "users")
		query.add_filter("id", ">", -1)
		result = list(query.fetch())
		pretty_properties = pretty_print(result)
		user_name_list = pretty_properties[1]
		
		user_name_split_list = user_name_list.split("|")
		user_name_split_list_lower = [None] * len(user_name_split_list)
		
		user_query = (raw_input("Search for : ")).lower()
		found_names = ""
		
		for i in range(0, len(user_name_split_list)):
			user_name_split_list_lower[i] = (user_name_split_list[i]).lower()
			index = (user_name_split_list_lower[i]).find(user_query)
			
			if (index != -1): # found
				found_names += user_name_split_list[i] + "\n"
			
		print ("Found names: \n" + found_names)
		
	elif (prompt == "0" or prompt == "exit"):
		print ("\nCONSOLE: Exiting Datastore console.")
		exit()
	else:
		print ("\nCONSOLE: Not valid.")
