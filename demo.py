from google.cloud import datastore
import datetime

datastore_client = datastore.Client()
kind = "users"

# open saved user id counter
countRecord = open("useridcount.txt","r")
count = int(countRecord.read())

while True:
	prompt = raw_input("[1]: display, [2]: add/update, [3]: delete, else: exit")
	
	if (prompt == 1):
		name = raw_input("Username: ")
		
		key = datastore_client.key(kind, name)
		ent = datastore_client.get(key)
		
		print ("Raw data from server: " + ent + "\n...")
		
	elif (prompt == 2):
		# get the name that will be updated/created
		name = raw_input("Username: ")

		# get user query
		query1 = unicode(raw_input("e-mail:   "))
		query2 = unicode(raw_input("Password: "))

		# Set which kind and entity is being worked on
		user_key = datastore_client.key(kind, name)
		user = datastore.Entity(key = user_key)

		# changes/additions to be made
		user.update({ "email":query1, 
					  "pass":query2, 
					  "id":count,
					  "updated":datetime.datetime.utcnow()})

		# send changes to google cloud datastore API
		datastore_client.put(user)

		# console log
		print ("\n'" + name + "' has been updated.")
		print ("User-ID: " + str(count) + "\n...\n")

		# increment local counter and rewrite useridcount.txt
		count = count + 1
		countRecord = open("useridcount.txt","w")
		countRecord.write(str(count))
		
	elif (prompt == 3):
		name = raw_input("Username: ")
		
		sure = raw_input("Are you sure?(y/n): ")
		if (sure == "y"):
			key = datastore_client.key(kind, name)
			datastore_client.delete(key)
		else
			print ("Canceling the delete operation. No changes have been made.\n")
		
	else:
		print("\nExiting Datastore console.\n")
		exit()
	

	
	


