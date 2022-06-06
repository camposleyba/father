import pickle

class createCredentials():

	def __init__(self, user, psw):
		self.user = user
		self.psw = psw

	def create(self, name):
		''' Create function, takes 1 parameter which is the name of the credentials file to be created
		and locally saved.
		It uses pickle library to create a binary file with the user and password provided in the
		class initiation.'''
		dict_cred={
			"user":self.user,
			"password":self.psw
		}

		with open(name, "wb") as f:
			pickle.dump(dict_cred,f)
			print("Credentials successfully created!")