def login_details():
    user_name = input('Please enter your username: ')
    email = input('Please enter your email: ')
    password = input('please enter a password: ')    # print(user_name)
    # print(email)    
    email_file = open("email.txt", "a")
    email_file.write(user_name+'\n'+email+'\n'+password+'\n\n')
    email_file.close()
    # print(email_file)
    return email_file