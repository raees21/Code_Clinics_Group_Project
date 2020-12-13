import os.path

def login_func():
    """
    get the user informatiom
    """
    
    if os.path.exists('login_info'):
        print('User details exist')
        login_info = open("login_info", "a")
        login_info.close()
    else:
        true = True
        user_name = input('Please enter your username: ')
        email = input('Please enter your student_email: ')
        while true:
            if '@'in email:
                (user_nam, email_url) = email.split('@')
                if user_nam == user_name and email_url == "student.wethinkcode.co.za":
                    print(user_nam)
                    print(email_url)
                    true = False
                else:
                    print('Invalid login details')
                    user_name = input('Please enter your username: ')
                    email = input('Please enter your email: ')
            else:
                print("Invalid email address, please try again")
                # user_name = input('Please enter your username: ')
                email = input('Please enter your email: ')


        login_info = open("login_info", "a")
        login_info.write(user_name+'\n'+email+'\n')
        login_info.close()
        
    return login_info