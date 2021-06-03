from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()

while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    menu_option = int(input())
    print("")
    # printing out tasks for today
    if menu_option == 1:
        print(f'Today {today.day} {today.strftime("%b")}:')
        rows = session.query(Task).filter(Task.deadline == today.date()).all()
        if len(rows) > 0:
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}')
        else:
            print('Nothing to do!\n')
    # printing out tasks for every day of this week
    elif menu_option == 2:
        for i in range(7):
            day = today + timedelta(days=i)
            print(f'{day.strftime("%A")} {day.day} {day.strftime("%b")}:')
            rows = session.query(Task).filter(Task.deadline == day.date()).all()
            if len(rows) > 0:
                for i in range(len(rows)):
                    print(f'{i+1}. {rows[i].task}')
                print("")
            else:
                print('Nothing to do!\n')
    # printing out all tasks sorted by date
    elif menu_option == 3:
        print('All tasks:')
        rows = session.query(Task).order_by(Task.deadline).all()
        if len(rows) > 0:
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
        print("")
    # printing out tasks that are past due
    elif menu_option == 4:
        print("Missed tasks:")
        rows = session.query(Task).filter(Task.deadline < today.date()).all()
        if len(rows) > 0:
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
            print("")
        else:
            print('Nothing is missed!\n')
    # adding new tasks to the database
    elif menu_option == 5:
        print('Enter task')
        new_task = input()
        print('Enter deadline')
        deadline = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Task(task=new_task, deadline=deadline.date())
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')
    # deleting a task
    elif menu_option == 6:
        print("Choose the number of the task you want to delete:")
        rows = session.query(Task).order_by(Task.deadline).all()
        if len(rows) > 0:
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
            task_number = int(input())
            session.delete(rows[task_number-1])
            session.commit()
        else:
            print("Nothing to delete\n")
    elif menu_option == 0:
        print('Bye!')
        break
