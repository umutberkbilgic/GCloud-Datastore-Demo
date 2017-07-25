
# Umut Berk Bilgic
# July 2017
# @ Sebit Information & Education Technologies
# METU Teknokent, Ankara, Turkey

from google.cloud import datastore
import time
import os

client = datastore.Client()
DELAY = 2

# Main loop 
while True:
	# info
	print("[1]: Livefeeed, [0]: Exit")
	prompt = raw_input("\n>> ")
	print("")

	if (prompt == "1" or prompt.lower() == "livefeed"):
		
		while (True):
			
			c = datastore.Client()
			kind = "comments"

			query = c.query(kind = "comments")
			query.add_filter("posttime", ">", 0)
			query.order = ["-posttime"]

			result_list = list(query.fetch())

			comment_id_list = []

			for r in result_list:
				r = str(r)
				index_start = r.find("u'comments', ") + 13
				index_end = r.find("L", index_start)
				comment_id_list.append(int(r[index_start : index_end]))
			
			comment_final_list = ""
			
			for id in comment_id_list:	
				comment_key = c.key(kind, id)
				ent = client.get(comment_key)

				comment = ent.get("comment")
				username = ent.get("username")
				
				comment_final_list += (username + ": " + comment + "\n")
				
			# makes things look instant
			os.system("clear")
			print comment_final_list
				
			time.sleep(DELAY)
			
	elif (prompt == "0" or prompt.lower() == "exit"):
		print("Exiting...\n")
		exit()

	else:
		print("\nInvalid input.\n")
		
		
