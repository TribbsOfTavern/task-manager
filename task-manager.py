###
#   task-manager
#   Project 3 given by the AI overlords to learn Python.
#   Written on Stream @ twitch.tv/CodeNameTribbs
#   Requirements:
#   1. Create a program that allows user to manage tasks. Each Task should have the following:
#       - Title
#       - Description
#       - Due Date
#   2. Implemment a menu-driven interface that allows user to perform the following action:
#       - Add new task
#       - View a list of all tasks, including their title and due dates.
#       - View details of a specific task by entering its title.
#       - Mark a task as completed
#       - Delete a task.
#       - Save the tasks to a file when the program exits and load them from the file when the program
#           starts. You can use a text file or a more structured format like JSON
#   3. Use a list or another appropriate data structure to store the tasks.
#   4. implement error handling to handle situations like entering invalid due dates or trying to view details
#       of a non-existent task.
#   5. Ensure that the program provides a clear and user-friendly interface with information prompts and messages.
#
import json
import uuid

class Task():
    def __init__(self, title:str, details:str, duedate:str, id:str=""):
        """Create a Task instance with given title:str, details:str, duedate:str"""
        self.title = title
        self.details = details
        self.duedate = duedate
        self.is_complete = False
        if id == "":
            self.cid = str(uuid.uuid1())
        else: 
            self.cid = id
        
    def getId(self) -> str:
        """Return str for task uuid"""
        return self.cid
    
    def getTitle(self) -> str:
        """Return str for task title"""
        return self.title
    
    def getDetails(self) -> str:
        """Return str for task details"""
        return self.details
    
    def getDuedate(self) -> str:
        """Return str for task duedate."""
        return self.duedate
    
    def isComplete(self) -> bool:
        """Return bool for task is_complete"""
        return self.is_complete

    def markComplete(self):
        """Mark self as complete"""
        self.is_complete = True
        
    def asDict(self) -> dict:
        return  {
            'cid': self.cid,
            'title': self.title,
            'details': self.details,
            'duedate': self.duedate,
            'is_complete': self.is_complete
            }
        
        
class TaskManager():
    def __init__(self):
        self.task_list = []
    
    def loadTasksFromFile(self, filename:str):
        """Load tasks in from a file."""
        try:
            with open(filename, "r") as fo:
                loaded = json.load(fo)
            for task in loaded:
                self.task_list.append(Task(task['title'], task['details'], task['duedate'], task['cid']))
        except Exception as e:
            print("Error Loading File:", e)            
        
    def saveTasksToFile(self, filename:str):
        """Save tasks to file."""
        try:
            saves = []
            for task in self.task_list:
                saves.append(task.asDict())
            with open(filename, "w") as fo:
                json.dump(saves, fo, indent=4)
        except Exception as e:
            print("Error Saving File:", e)
    
    def addTask(self, new_task:Task):
        """Add a Task instance to the TaskManager list if task title does not already exist in list."""
        if self.task_list:
            exists = False
            for i, task in enumerate(self.task_list):
                if task.getTitle().lower() == new_task.getTitle().lower():
                    exists = True
                    break
            if not exists:
                self.task_list.append(new_task)
        else:
            self.task_list.append(new_task)
    
    def  removeTaskByTitle(self, title:str):
        """Given a title remove Task instance from TaskManger list."""
        for i, task in enumerate(self.task_list):
            if task.getTitle().lower() == title.lower():
                self.task_list.pop(i)
                return True
        return False
    
    def getAllTasks(self) -> list:
        """Get a list of all Task instances stored in TaskManger"""
        return self.task_list if self.task_list != [] else None
        
    def getTaskDetailsByTitle(self, title:str) -> str:
        """Given a title get Task instance details. Return None if no Task instance is found."""
        task = self.getTaskByTitle(title)
        if task:
            return task.getDetails()
        return None
    
    def getTaskByTitle(self, title:str):
        """Given the title, get a Task instance from TaskManager list. Return None if no task instance is found."""
        for task in self.task_list:
            if task.getTitle().lower() == title.lower():
                return task
        return None
    
    def markTaskCompleteByTitle(self, title:str):
        """Given a title of a Task instance, if Task instance exists in TaskManager, mark Task as complete."""
        task = self.getTaskByTitle(title)
        if task:
            for task in self.task_list:
                if task.getTitle().lower() == title.lower():
                    task.markComplete()
                    return True
        else:
            return False
        

def menu():
    """Print User Menu To The Screen"""
    text=""
    text+=f"{'Task Manger':_^40}\n"
    text+=f"{'    1.) View All Task':<40}\n"
    text+=f"{'    2.) Add New Task':<40}\n"
    text+=f"{'    3.) View Task Details':<40}\n"
    text+=f"{'    4.) Mark A Task Complete':<40}\n"
    text+=f"{'    5.) Remove A Task':<40}"
    print(text)

def pause():
    """Wait for user to press any key"""
    input("Press any key to continue... ")

def viewTasks(tasks:list):
    """Given a list of tasks, print formatted tasks to console."""
    text ="\n"
    text+=f"{'Title':_<20} {'Due Date':_<20}\n"
    for task in tasks:
       text+=f"{task.getTitle():<20} {task.getDuedate():<20}\n"
    text+="\n"
    print(text)

def app():
    """Run our task manger application"""
    file_name = "./tasks.json"
    task_manager = TaskManager()
    try:
        task_manager.loadTasksFromFile(file_name)
    except:
        open(file_name, "w").close()
    
    exit_app = False
    while not exit_app:
        menu()
        ins = input("Please choose an option: ")
        match ins:
            case "0": # Exit the application after loop ends.
                exit_app = True
            case "1": # View all tasks
                tasks = task_manager.getAllTasks()
                if tasks:
                    viewTasks(tasks)
                else:
                    print("There are currently no tasks in the queue.")
            case "2": # Add a new task
                title = input("Enter title of task: ")
                details = input("Enter some details of task: ")
                print("Please enter the following in format: YYYY-MM-DD")
                duedate = input("Enter year of duedate: ")
                new_task = Task(title, details, duedate)
                print('You enter the following information')
                print(f"{'Title':<20} {'Duedate':<15} {'Details'}")
                print(f"{new_task.getTitle():<20}  {new_task.getDuedate():<15} {new_task.getDetails()}")
                confirm = input("Does this information look correct? (y/n)")
                if confirm.lower() == "y" or confirm == "yes":
                    task_manager.addTask(new_task)
                    print(f"Task {new_task.getTitle()} was added to list.")
                else:
                    print("Task was not commited to list.")
                del title, details, duedate, new_task, confirm
            case "3": # View Task Details
                ins = input("Enter the task name to view: ")
                task = task_manager.getTaskByTitle(ins)
                if task:
                    print(f"{task.getTitle():<20} {'COMPLETE' if task.isComplete() else 'INCOMPLETE':<20}")
                    print(f"{task.getDetails()}\n")
                else:
                    print(f"Task {ins} was not found in list.")
                del task
            case "4": # Mark Task as Complete
                ins = input("Enter a task name to mark complete: ")
                added = task_manager.markTaskCompleteByTitle(ins)
                if added:
                    print(f"Task {ins} marked as complete.")
                else:
                    print(f"Task {ins} not found in list.")
                del added
            case "5": # Remove A Task
                ins = input("Enter the task title you would like to delete: ")
                deleted = task_manager.removeTaskByTitle(ins)
                if deleted:
                    print(f"Task {ins} was deleted.")
                else:
                    print(f"No task with title {ins} was found for deletion.")
                del deleted
            case _:
                print("Please choose a valid option.")
        
        pause()
        
        try:
            task_manager.saveTasksToFile(file_name)
        except Exception as e:
            print("Error when attempting to save file: ", e)

    print("Application exiting...")
    exit()

if __name__ == "__main__":
    app()