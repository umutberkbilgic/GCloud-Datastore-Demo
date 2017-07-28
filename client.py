# Umut Berk Bilgic
# July 2017
# @ Sebit Information & Education Technologies
# METU Teknokent, Ankara, Turkey
# v4

from Tkinter import *
from google.cloud import datastore
import datetime
import tkMessageBox

# GLOBALS
client = datastore.Client()

def place(thing, r, c, px, py):
	thing.grid(row = r, column = c, padx = px, pady = py)
def p(text):
	tkMessageBox.showinfo("Google Cloud", text)
	
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

# PAGES
class LoginPage():
	def __init__(self, master):
		self.master = master
		self.master.title("Login")
		
		# create
		self.label_username = Label(self.master, text = "Username:")
		self.label_password = Label(self.master, text = "Password:")
		self.entry_username = Entry(self.master, width = 10)
		self.button_login = Button(self.master, text = "Login", command = self.login)
		self.entry_password = Entry(self.master, show = "*", width = 10)
		self.button_register = Button(self.master, text = "Register", command = self.register)
		
		# place
		place(self.label_username, 0, 0, 5, 5)
		place(self.label_password, 1, 0, 5, 5)		
		place(self.entry_username, 0, 1, 5, 5)
		place(self.button_login, 2, 1, 5, 5)
		place(self.entry_password, 1, 1, 5, 5)
		place(self.button_register, 2, 0, 5, 5)
		
		# attribute
		self.username = ""
		self.id = -1
		
		self.master.bind("<Return>", self.enter)
		self.master.bind("<Escape>", self.escape)
		
	def escape(self, event):
		self.quit()
		
	def enter(self, event):
		self.login()
		
	def profile(self):
		self.disable()
		
		profile_window = Toplevel(self.master)
		profile_page = ProfilePage(profile_window)
		
	def quit(self):
		self.master.destroy()
		
	def disable(self):
		self.entry_password.config(state = "disabled")
		self.entry_username.config(state = "disabled")
		self.button_login.config(state = "disabled")
		self.button_register.config(state = "disabled")
		
	def enable(self):
		self.entry_password.config(state = "normal")
		self.entry_username.config(state = "normal")
		self.button_login.config(state = "normal")
		self.button_register.config(state = "normal")
		
	def reset_entries(self):
		self.entry_password.delete(0, "end")
		self.entry_username.delete(0, "end")
		
	def login(self):
		username = self.entry_username.get()
		password = self.entry_password.get()

		# retrieve user
		user_id = retrieve_user_by_username(username)

		if (user_id == -1):
			p("User does not exist. Please register.\n")
			self.reset_entries()
		else:
			key = client.key("data", user_id)
			ent = client.get(key)

			stored = ent.get("password")

			if (str(password) != str(stored)):
				p("Wrong password. Please try again.\n")
				self.reset_entries()
				
			else:
				self.username = self.entry_username.get()
				self.id = retrieve_user_by_username(self.username)
			
				self.reset_entries()
				self.profile()
				
	def register(self):
		self.disable()
		
		register_window = Toplevel(self.master)
		register_page = RegisterPage(register_window)
	
class ProfilePage():
	def __init__(self, master):
		self.master = master
		self.master.title("Profile")
		
		# create
		self.label_comment = Label(self.master, text = "Comment:")
		self.entry_comment = Entry(self.master, width = 40)
		self.button_logout = Button(self.master, text = "Logout", command = self.logout)
		self.button_post = Button(self.master, text = "Post", command = self.post)
		self.button_show = Button(self.master, text = "Show", command = self.comments)
		
		#place
		place(self.label_comment, 0, 0, 5, 5)
		place(self.entry_comment, 0, 1, 5, 5)
		place(self.button_logout, 1, 0, 5, 5)
		place(self.button_post,   1, 1, 5, 5)
		place(self.button_show,   1, 2, 5, 5)
		
		self.master.bind("<Return>", self.enter)
		self.master.bind("<Escape>", self.escape)
		
	def escape(self, event):
		self.logout()
		
	def enter(self, event):
		self.post()
		
	def logout(self):
		self.master.destroy()
		login_page.enable()
		
	def post(self):
		c = datastore.Client()
		kind = "comments"
					
		key = c.key(kind)
		post = datastore.Entity(key)
					
		post.update({
			"comment" : unicode(self.entry_comment.get()),
			"username" : unicode(login_page.username),
			"userid" : int(login_page.id),
			"posttime" : datetime.datetime.utcnow() })
		
		c.put(post)
		
		self.entry_comment.delete(0, "end")
		
	def comments(self):
		comments_window = Toplevel(self.master)
		comments_page = CommentsPage(comments_window)
		
	def disable(self):
		self.entry_comment.config(state = "disabled")
		self.button_logout.config(state = "disabled")
		self.button_post.config(state = "disabled")
		self.button_show.config(state = "disabled")
		
	def enable(self):
		self.entry_comment.config(state = "normal")
		self.button_logout.config(state = "normal")
		self.button_post.config(state = "normal")
		self.button_show.config(state = "normal")
		
		
class CommentsPage:
	def __init__(self, master):
		self.master = master
		self.master.title("Comments")
		
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
						
		comment_final_str = ""
			
		for id in comment_id_list:	
			comment_key = c.key(kind, id)
			ent = client.get(comment_key)
			
			comment = ent.get("comment")
			username = ent.get("username")

			comment_final_str += (username + ": " + comment + "\n")
				
		self.label_comments = Label(self.master, text = comment_final_str, justify = LEFT)	
		self.label_comments.pack()
		
		self.master.bind("<Escape>", self.escape)
		
	def escape(self, event):
		self.master.destroy()

class RegisterPage:
	def __init__(self, master):
		self.master = master
		self.master.title("Register")
		
		
		self.entry_email = Entry(self.master, width = 10)
		self.entry_username = Entry(self.master, width = 10)
		self.entry_password = Entry(self.master, show = "*", width = 10)
		self.entry_c_password= Entry(self.master, show = "*", width = 10)
		self.label_email = Label(self.master, text = "E-mail:")
		self.label_username = Label(self.master, text = "Username:")
		self.label_password = Label(self.master, text = "Password:")
		self.label_c_password  = Label(self.master, text = "Confirm Password:")
		self.button_register = Button(self.master, text = "Register", command = self.register)
		
		place(self.entry_email, 0, 1, 5, 5)
		place(self.entry_username, 1, 1, 5, 5)
		place(self.entry_password, 2, 1, 5, 5)
		place(self.entry_c_password, 3, 1, 5, 5)
		place(self.label_email, 0, 0, 5, 5)
		place(self.label_username, 1, 0, 5, 5)
		place(self.label_password, 2, 0, 5, 5)
		place(self.label_c_password, 3, 0, 5, 5)
		place(self.button_register, 4, 1, 5, 5)
		
	def get_user_id_from_query(self, result_list):
		result_string = str(result_list[0])
		index_start = result_string.find("u'data', ") + 9
		index_end = result_string.find("L", index_start)
		return int(result_string[index_start : index_end])
		
	def retrieve_user_by_email(self, email):
		# returns user id || -1
		query = client.query(kind = "data")
		query.add_filter("email", "=", email)

		result = list(query.fetch())

		if (result != []): # user exists, return ID
			return self.get_user_id_from_query(result)
		else:
			return (-1)
		
	def reset_entries(self):
		self.entry_email.delete(0, "end")
		self.entry_username.delete(0, "end")
		self.entry_password.delete(0, "end")
		self.entry_c_password.delete(0, "end")
		
	def quit(self):
		self.master.destroy()
		
	def register(self):
		username = self.entry_username.get()
		email = self.entry_email.get()
		password = self.entry_password.get()
		c_password = self.entry_c_password.get()
		
		# retrieve user
		user_id = retrieve_user_by_username(username)
		
		if (user_id != -1): # check username
			p("Username already in use. Please try again.")
			self.reset_entries()
		else:
			user_id = self.retrieve_user_by_email(email)
			
			if (user_id != -1): # check email
				p("Email already in use. Please try again.")
				self.reset_entries()
			else:
				if (c_password != password): # check password
					p("Passwords did not match. Please try again.")
					self.reset_entries()
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
					
					p("Successfully registered as " + username + "\n")
					self.reset_entries()
					self.quit()

root = Tk()
login_page = LoginPage(root)
root.mainloop()
