# Patrick

COMMAND_FLAGS = {
	'help': (),
	'quit': (),
	'tool': ('v', 'a', 'e', 'd'),
	'categ': ('v', 'a', 'e', 'd'),
	'reqs': ('g', 'r'),
	'search': ()
}

def main():
	conn = get_conn()  # TODO
  
	logged_in = False

	while not logged_in:
		print('Welcome to MvieLvrs tools application')
		inp = input('Enter "login" to login or "new" to create an account: ').lower()
		if inp == 'login':
			print('Logging in')
			username = input('Username: ')
			password = input('Password: ')
			if login_user(conn, username, password):
				print('Login successful')
				logged_in = True
			else:
				print('Incorrect login')
		elif inp == 'new':
			print('Creating user')
			username = input('Username: ')
			password = input('Password: ')
			first_name = input('First Name: ')
			last_name = input('Last Name: ')
			email = input('Email: ')
			
			succ, e_type = create_user(conn, username, password, first_name, last_name, email):
			if succ:
				print('Created successfully')
				logged_in = True
			if e_type == 'username':
				print('Username already in use')
			elif e_type == 'email':
				print('Email already in use')
			else:
				print('Error on creation')
		else:
			print('Unrecognized input')
  
	print('You are now logged in')
	
	while True:
		print('Enter a command ("help" for help)')
		inp = input('> ').lower()
		command, *flags = inp.split()
		if command not in COMMAND_FLAGS:
			print('Unknown command - see "help"')
		elif bool(flags) != bool(COMMAND_FLAGS[command]) or flags and flags[0] not in COMMAND_FLAGS[command]:
			print('Invalid usage - see "help"')
		elif command == 'help':
			print('Commands:')
			print('help             -  displays this menu')
			print('quit             -  exits the program')
			print('tool [v a e d]   -  manage your tools [view add edit delete]')
			print('categ [v a e d]  -  manage your categories [view add edit delete]')
			print('reqs [g r]       -  manage your borrow requests [given recieved]')
			print('search           -  search for tool')
		elif command == 'quit':
			break
		elif command == 'tool':
			if flags[0] == 'v':
				pass
			elif flags[0] == '
		elif command == 'categ':
			pass
		elif command == 'reqs':
			pass
		elif command == 'search':
			pass
  
	print('Thanks for trusting Mvie Lovers!')

if __name__ == '__main__':
	main()
