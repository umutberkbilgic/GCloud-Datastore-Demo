# Umut Berk Bilgic
# July 2017
# @ Sebit Information & Education Technologies
# METU Teknokent, Ankara, Turkey

from google.cloud import datastore
import getpass
import datetime

client = datastore.Client()

is_logged_in = False
current_username = ""
current_email = ""
current_id = -1

def retrieve_user_by_password(password):
	# returns user id || -1
	query = client.query(kind = "data")
	query.add_filter("password", "=", password)
	
	result = list(query.fetch())
	
	if (result != []): # user exists, return ID
		result_string = str(result[0])
		index_start = result_string.find("u'data', ") + 9
		index_end = result_string.find("L", index_start)
		return int(result_string[index_start : index_end])	
	else:
		return (-1)
	
def retrieve_user_by_username(username):
	# returns user id || -1
	query = client.query(kind = "data")
	query.add_filter("username", "=", username)
	
	result = list(query.fetch())
	
	if (result != []): # user exists, return ID
		result_string = str(result[0])
		index_start = result_string.find("u'data', ") + 9
		index_end = result_string.find("L", index_start)
		return int(result_string[index_start : index_end])	
	else:
		return (-1)
	
def retrieve_user_by_email(email):
	# returns user id || -1
	query = client.query(kind = "data")
	query.add_filter("email", "=", email)
	
	result = list(query.fetch())
	
	if (result != []): # user exists, return ID
		return get_user_id_from_query(result)
	else:
		return (-1)
def get_user_id_from_query(result_list):
	result_string = str(result_list[0])
	index_start = result_string.find("u'data', ") + 9
	index_end = result_string.find("L", index_start)
	return int(result_string[index_start : index_end])
def login(username, password):
	# retrieve user
	user_id = retrieve_user_by_username(username)

	if (user_id == -1):
		print("User does not exist. Please register.\n")
		return [False, "", "", -1]
	else:
		key = client.key("data", user_id)
		ent = client.get(key)

		stored = ent.get("password")

		if (str(password) != str(stored)):
			print("Wrong password. Please try again.\n")
			return [False, "", "", -1]
		else:
			print("Login successfull!\n")
		
			return [True, username, ent.get("email"), user_id]

# Main loop 
while True:
	# info
	print("[1]: Login, [2]: Register, [3]: Logout, [4]: Profile, [0]: Exit")
	prompt = raw_input("\n>> ")
	print("")
	
	# LOGIN #################################################
	if (prompt == "1" or prompt.lower() == "login"):
		
		if (is_logged_in):
			print("You are already logged in as " + current_username)
			print("Please logout from this session to login as a different user.")
		else:
			username = raw_input("Username: ")
			password = str(getpass.getpass("Password: "))

			current_list = login(username, password)
			
			# update currents			
			is_logged_in = current_list[0]
			current_username = current_list[1]
			current_email = current_list[2]
			current_id = current_list[3]
			
	# REGISTER ##############################################			
	elif (prompt == "2" or prompt.lower() == "register"):
		email = raw_input("E-mail address: ")
		username = raw_input("Username: ")
		password = str(getpass.getpass("Password: ")) 
		c_password = str(getpass.getpass("Confirm password: "))
		
		# retrieve user
		user_id = retrieve_user_by_username(username)
		
		if (user_id != -1): # check username
			print("Username already in use. Please try again.")
		else:
			user_id = retrieve_user_by_email(email)
			
			if (user_id != -1): # check email
				print("Email already in use. Please try again.")
			else:
				if (c_password != password): # check password
					print("Passwords did not match. Please try again.")
				else:
					key = client.key("data")
					user = datastore.Entity(key)
					
					user.update({ 
						"date" : datetime.datetime.utcnow(),
						"email" : unicode(email), 
						"password" : unicode(password),
						"username" : unicode(username) })

					# send changes to google cloud datastore API
					client.put(user)
					
					print ("Successfully registered as " + username + "\n")
					
	# LOGOUT ################################################				
	elif (prompt == "3" or prompt.lower() == "logout"):
		print("Logging out of '" + current_username + "'...")
			  
		is_logged_in = False 
		current_username = ""
		current_email = ""
		current_id = -1
		
		print ("Successfully logged out.\n")
		
		
	# PROFILE ############################################### MAIN APPLICATION ##############
	elif (prompt == "4" or prompt.lower() == "profile"):
		if (is_logged_in):
			while (True):
				print("-----------------------------")
				print("Username: " + current_username)
				print("E-mail:   " + current_email)
				print("User ID:  " + str(current_id))
				print("-----------------------------")

				prompt = raw_input("[1]: Change password, [2]: Post comment, [3]: View comments, [0]: Return to main menu\n>>")

				if (prompt == "1"):
					password = str(getpass.getpass("Enter current password: "))
					
					key = client.key("data", current_id)
					user = client.get(key)
					
					current_password = user.get("password")
					
					if (password == current_password):
						new_password = str(getpass.getpass("Enter your new password: "))
						c_new_password = str(getpass.getpass("Confirm your new password: "))
												
						if (new_password == c_new_password):							
							user.update({ 
							"date" : datetime.datetime.utcnow(),
							"email" : unicode(current_email), 
							"password" : unicode(new_password),
							"username" : unicode(current_username) })
							
							client.put(user)
							
							print("\nSuccessfully updated password.\n")
							
						else:
							print("New passwords did not match. Please try again.")
					else:
						print("\nPlease re-enter your current password and try again.\n")
					
				elif (prompt == "2"):
					c = datastore.Client()
					kind = "comments"
					
					comment = raw_input("Enter comment: ")
					
					key = c.key(kind)
					post = datastore.Entity(key)
					
					post.update({
						"comment" : unicode(comment),
						"username" : unicode(current_username),
						"userid" : int(current_id),
						"posttime" : datetime.datetime.utcnow() })
					
					c.put(post)
					
				elif (prompt == "3"):
					c = datastore.Client()
					kind = "comments"
					
					query = c.query(kind = "comments")
					query.add_filter("userid", ">", 0)
					
					result_list = list(query.fetch())
					
					comment_id_list = []
					
					for r in result_list:
						r = str(r)
						index_start = r.find("u'comments', ") + 13
						index_end = r.find("L", index_start)
						comment_id_list.append(int(r[index_start : index_end]))
						
					for id in comment_id_list:	
						comment_key = c.key(kind, id)
						ent = client.get(comment_key)

						comment = ent.get("comment")
						username = ent.get("username")
						
						print ("Comment by " + username + ": " + comment + "\n")
					
				elif (prompt == "0"):
					print("\nReturning to the main menu.\n")
					break
				else:
					print("\nInvalid input.\n")
				
		else:
			print("\nPlease login to view your profile.\n")
		
	# EXIT ##################################################
	elif (prompt == "0" or prompt.lower() == "exit"):
		print("\nExiting...\n")
		exit()
		
	# INVALID ###############################################
	else:
		print("\nInvalid input.\n")
		
		
