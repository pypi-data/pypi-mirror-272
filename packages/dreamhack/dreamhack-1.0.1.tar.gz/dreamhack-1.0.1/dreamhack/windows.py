class windows():
  def create_windows_account(username, password): #type:ignore
    import subprocess
    command = f"net user {username} {password} /add /Y"
    try:
      subprocess.run(command, shell=False, check=True)
    except Exception as e: 
      raise e
    else:
      return username, password

  def multi_account_create(accounts, username=None, password=None): #type:ignore
    def random_string_generator(length):
      import random
      characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
      master = ""
      for x in range(int(length)):
        master = master + random.choice(characters)
      return master
    for x in range(int(accounts)): #type:ignore
      if username is None:
        username = random_string_generator(14)
      if password is None:
        password = random_string_generator(14)
      windows.create_windows_account(username, password) #type:ignore