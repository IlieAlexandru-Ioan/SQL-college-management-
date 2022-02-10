import mysql.connector
import getpass

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123Root!",
    database = "testdb"
)
command_handler = db.cursor(buffered=True) # enables running multiple queries without any problem

def admin_sesion():
    print("Login success welcome admin")
    while 1:
        print("\nAdmin menu")
        print("1. Register student")
        print("2. Register teacher")
        print("3. Delete existing student")
        print("4. Delete existing teacher")
        print("5. Logout")

        user_option = input(str("Option: "))
        if user_option == "1":
            print("\nRegister new student")
            username = input(str("Student username: "))
            passwd = str(getpass.getpass("Student password: "))
            query_vals = (username, passwd)
            command_handler.execute("insert into users (username, password, privilege) values(%s, %s, 'student')", query_vals)
            db.commit()
            print(f"{username} has registered as a student")
        elif user_option == "2":
            print("\nRegister new teacher")
            username = input(str("Teacher username: "))
            passwd = str(getpass.getpass("Teacher password: "))
            query_vals = (username, passwd)
            command_handler.execute("insert into users (username, password, privilege) values(%s, %s, 'teacher')",
                                    query_vals)
            db.commit()
            print(f"{username} has registered as a teacher")
        elif user_option == "3":
            print("\nDelete existing student account")
            username = input(str("Student username: "))
            query_vals = (username, "student")
            command_handler.execute("delete from users where username = %s and privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1: #how many rows are afected
                print("User not found")
            else:
                print(f"{username} has been deleted")
        elif user_option == "4":
            print("\nDelete existing teacher account")
            username = input(str("Teacher username: "))
            query_vals = (username, "teacher")
            command_handler.execute("delete from users where username = %s and privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1: #how many rows are afected
                print("User not found")
            else:
                print(f"{username} has been deleted")
        elif user_option == "5":
            break
        else:
            print("No valid option selected")

def teacher_session():
    print("Login success welcome teacher")
    while 1:
        print("\nteacher menu")
        print("1. Mark student register")
        print("2. View register")
        print("3. Logout")
        user_option = input(str("Option: "))
        if user_option == "1":
            print("\nMark student register")
            command_handler.execute("select username from users where privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date: DD/MM/YYYY: "))
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                status = input(str(f"Status for {str(record)} P/L/A: "))  # Present/Adsent/Late
                query_vals = (str(record), date, status)
                command_handler.execute("insert into attendance (username, date, status) values(%s, %s, %s)", query_vals)
                db.commit()
                print(f"{record} marked as {status}")

        elif user_option =="2":
            print("\nViewing all students registers")
            command_handler.execute("select username, date, status from attendance ")
            records = command_handler.fetchall()
            print("Dysplay all registers")
            for record in records:
                print(record)
        elif user_option == "3":
            break
        else:
            print("No valid option selected")

def student_session(username):
    while 1:
        print("1. View register")
        print("2. Download register")
        print("3. Logout")
        user_option = input(str("Option: "))
        if user_option == "1":
            command_handler.execute("select date,username, status from attendance where username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "2":
            print("Donwload register...")
            command_handler.execute("select date,username, status from attendance where username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                with open("register.txt", 'a') as f:
                    f.write(str(record))
                    f.write("\n")
            print("All records saved")
        elif user_option == "3":
            break
        else:
            print("No valid option selected")

def auth_admin():
    print("Admin login\n")
    username = input(str("Username : "))
    passwd = str(getpass.getpass("Password: "))
    if username == "admin":
        if passwd == "password":
            admin_sesion()
        else:
            print("Wrong password")
    else:
        print("login details not recognised")

def auth_teacher():
    print("\nTeacher login\n")
    username = input(str("Username: "))
    password = str(getpass.getpass("Password: "))
    query_vals = (username, password)
    command_handler.execute("select * from users where username = %s and password = %s and privilege = 'teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print("login not recognized")
    else:
        teacher_session()

def auth_student():
    print("\nStudent login\n")
    username = input(str("Username :"))
    password = str(getpass.getpass("Password: "))
    query_vals = (username, password)
    command_handler.execute("select username from users where username = %s and password = %s and privilege = 'student'", query_vals)
    username=command_handler.fetchone()
    if command_handler.rowcount <=0: #no results
        print("Invalid login details")
    else:
        student_session(username)
def main():
    while 1:
        print("Welcome to the collage system\n")
        print("1. Login as student")
        print("2. Login as teacher")
        print("3. Login as admin")
        print("4. Exit")
        user_option = input(str("Option: "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        elif user_option == "4":
            break
        else:
            print("No valid action was selected")
if __name__ == '__main__':
    main()



