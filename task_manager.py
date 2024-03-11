# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

# Date format used for datetime string conversion
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Check if user file exists, create with default admin credentials if not
def load_user_data():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")
# Read user data from file and return as a list of username-password pairs
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    return [user.split(';') for user in user_data if user]

# Check if tasks file exists, create if not
def load_task_data():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass
    # Read task data from file and convert into a list of dictionaries
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
    # Initialise empty list
    # Iterate through each string in the task data
    task_list = []
    for t_str in task_data:
        if t_str:
            curr_t = {}
            task_components = t_str.split(";")
            curr_t['username'] = task_components[0]
            curr_t['title'] = task_components[1]
            curr_t['description'] = task_components[2]
            curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
            curr_t['completed'] = True if task_components[5] == "Yes" else False
            task_list.append(curr_t)

    return task_list

# Save the user data to the user.txt file
# If the file dose not exist create it
def save_user_data(username_password):
    with open("user.txt", "w") as out_file:
        user_data = [f"{k};{v}" for k, v in username_password.items()]
        out_file.write("\n".join(user_data))

# Save the task data to the task.txt file
# If the file dose not exist create it
def save_task_data(task_list):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            # Format task attributes as a string and append to the list
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        # Write the formatted list to the file
        task_file.write("\n".join(task_list_to_write))

# Register a new user 
def reg_user(username_password):
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username alresdy exists. Please choose a different one.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    # Add new user to the dictionary and save to file
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        save_user_data(username_password)
    else:
        print("Passwords do not match")

# Add a new task
def add_task(task_list):
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    # ask for task details
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    # Create a new task dictionary and add to the task list
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    save_task_data(task_list)
    print("Task successfully added.")

# View all tasks
def view_all(task_list):
    # Display task details for each task in the list
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# View tasks assigned to current user
def view_mine(username, task_list):
    task_number = 1
    task_indices = []
    # Display task details for each task for current user
    print("Your Tasks:")
    for i, t in enumerate(task_list):
        if t['username'] == username:
            disp_str = f"{task_number}. Task: {t['title']}\n"
            disp_str += f"   Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"   Description: {t['description']}\n"
            disp_str += f"   Completed: {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)
            task_indices.append(i)
            task_number += 1

    if not task_indices:
        print("No tasks assigned to you.")
        return -1
    # Allow user to edit or mark task complete
    while True:
        choice = input("Enter the number of the task you want to edit (or -1 to go back): ")
        if choice == '-1':
            return -1

        try:
            choice = int(choice)
            if 1 <= choice <= len(task_indices):
                return task_indices[choice - 1]
            else:
                print("Invalid task number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Mark tasks as complete
def mark_task_complete(task_list, task_index):
    task_list[task_index]['completed'] = True
    save_task_data(task_list)
    print("Task marked as complete.")

# Edit a task(username or due date )
def edit_task(task_list, task_index):
    if not task_list[task_index]['completed']:
        print("Editing options:")
        print("1. Edit assigned username")
        print("2. Edit due date")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            new_username = input("Enter the new assigned username: ")
            task_list[task_index]['username'] = new_username
            save_task_data(task_list)
            print("Username updated.")
        elif choice == '2':
            while True:
                try:
                    new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                    task_list[task_index]['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    save_task_data(task_list)
                    print("Due date updated.")
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified.")
        else:
            print("Invalid choice.")
    else:
        print("Tssk is already completed. Cannot edit.")

# Generate task/user report and overview, including percentage of completion
def generate_reports(task_list, username_password, task_report_path="task_overview.txt", user_report_path="user_overview.txt"):
    num_users = len(username_password)
    num_tasks = len(task_list)
    completed_tasks = sum(t['completed'] for t in task_list)
    incomplete_tasks = num_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and 'due_date' in t and t['due_date'].date() < datetime.now().date())

    task_overview = f"Total tasks: {num_tasks}\n"
    task_overview += f"Completed tasks: {completed_tasks}\n"
    task_overview += f"Incomplete tasks: {incomplete_tasks}\n"
    task_overview += f"Overdue tasks: {overdue_tasks}\n"
    task_overview += f"Percentage of incomplete tasks: {incomplete_tasks / num_tasks * 100:.2f}%\n"
    task_overview += f"Percentage of overdue tasks: {overdue_tasks / incomplete_tasks * 100:.2f}%" if incomplete_tasks != 0 else "\nPercentage of overdue tasks: 0.00%\n"

    user_overview = f"Total users: {num_users}\n"
    user_overview += f"Total tasks: {num_tasks}\n"

    for username, password in username_password.items():
        user_tasks = [t for t in task_list if 'username' in t and t.get('username') == username]
        total_user_tasks = len(user_tasks)

        user_overview += f"\nUser: {username}\n"
        user_overview += f"Total tasks assigned: {total_user_tasks}\n"

        if total_user_tasks > 0:
            completed_user_tasks = sum(t['completed'] for t in user_tasks)
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and 'due_date' in t and t['due_date'].date() < datetime.now().date())

            user_overview += f"Percentage of total tasks: {total_user_tasks / num_tasks * 100:.2f}%\n"
            user_overview += f"Percentage of completed tasks: {completed_user_tasks / total_user_tasks * 100:.2f}%\n"
            user_overview += f"Percentage of incomplete tasks: {incomplete_user_tasks / total_user_tasks * 100:.2f}%\n"
            user_overview += f"Percentage of overdue tasks: {overdue_user_tasks / incomplete_user_tasks * 100:.2f}%" if incomplete_user_tasks != 0 else "\nPercentage of overdue tasks: 0.00%\n"
        else:
            user_overview += "No tasks assigned.\n"
    # write task/user overview to appropriate files
    # Generate the appropriate files if they dont exist already
    try:
        with open(task_report_path, "w") as task_overview_file:
            task_overview_file.write(task_overview)

        with open(user_report_path, "w") as user_overview_file:
            user_overview_file.write(user_overview)
            print("User Overview:\n", user_overview)

    except Exception as e:
        print(f"Error writing reports: {e}")

# Display stats about the number of users and tasks
def display_statistics(users, tasks):
    print("-----------------------------------")
    print(f"Number of users: \t\t {len(users)}")
    print(f"Number of tasks: \t\t {len(tasks)}")
    print("-----------------------------------")

# Main menu functionality, including: user login and new function calls
def main():
    global username_password
    global task_list

    username_password = dict(load_user_data())
    task_list = load_task_data()

    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password:
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    while True:
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

        if menu == 'r':
            reg_user(username_password)

        elif menu == 'a':
            add_task(task_list)

        elif menu == 'va':
            view_all(task_list)

        elif menu == 'vm':
            task_index = view_mine(curr_user, task_list)
            if task_index != -1:
                action = input("Choose an action:\n1. Mark as complete\n2. Edit task\n: ")
                if action == '1':
                    mark_task_complete(task_list, task_index)
                elif action == '2':
                    edit_task(task_list, task_index)
                else:
                    print("Invalid choice.")

        elif menu == 'gr' and curr_user == 'admin':
            generate_reports(task_list, username_password, task_report_path="task_overview.txt", user_report_path="user_overview.txt")
        
        elif menu == 'ds' and curr_user == 'admin':
            display_statistics(username_password.keys(), task_list)
        
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("""Request not recognised or Admin permission required,
Please Try again:""")
# Runs the main function if the script is being executed directly
if __name__ == "__main__":
    main()