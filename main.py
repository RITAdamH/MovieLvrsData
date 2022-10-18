# Patrick

def main():
  conn = get_conn()  # TODO
  
  while True:
    print('Welcome to MvieLvrs tools application')
    inp = input('Enter l to login or c to create an account: ').lower()
    if inp == 'l':
      print('Logging in')
      username = input('Username: ')
      password = input('Password: ')
      if login_user(conn, username, password):
        print('Login successful')
        break
      else:
        print('Incorrect login')
    elif inp == 'c':
      print('Creating user')
      create_user(conn, username, password, first_name, last_name, email)
    else:
      print('Unrecognized input')
