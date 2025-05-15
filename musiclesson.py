# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'music_lessons.db'

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    db.close()

# This is the filename of the database to be used
DB_NAME = 'music_lessons.db'
# This is the SQL to connect to all the tables in the database
TABLES = (" music_lesson "
           "LEFT JOIN school ON music_lesson.school_id = school.school_id "
           "LEFT JOIN instrument ON music_lesson.instrument_id = instrument.instrument_id "
           "LEFT JOIN gender ON music_lesson.gender_id = gender.gender_id "
           "LEFT JOIN days ON music_lesson.day_id = days.day_id "
           "LEFT JOIN info ON music_lesson.parentinfo_id = info.parentinfo_id   ")

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  

menu_choice = ''
while menu_choice != 'Z':
    menu_choice = input('Welcome to your music lessons database\n\n'
                        'Type the letter for the information you want:\n'
                        'A: All lessons on a Monday\n'
                        'B: All lessons on a Wednesday\n'
                        'C: Information on parents that owe you money\n'
                        'D: All lessons on a certain day\n'
                        'E: All students of a certain instrument\n'
                        'F: All data\n'
                        'Z: Exit\n\n' 
                        'Type option here: ')
    menu_choice = menu_choice.upper()
    if menu_choice == 'A':
         print_query('Monday lessons')
    elif menu_choice == 'B':
         print_query('Wednesday lessons')
    elif menu_choice == 'C':
         print_query('Parents who owe')
    elif menu_choice == 'D':
         lesson = input('What day do you want to see? ')
         print_parameter_query("child_first, school, parent_name, parent_phone, instrument, time", "day = ? ORDER BY time ASC",lesson)
    elif menu_choice == 'E':
         instrument = input('What instruments do you want to see? ')
         print_parameter_query("child_first, parent_name, school, parent_phone, time, day", "instrument = ? ORDER BY birth_date DESC",instrument)    
    elif menu_choice == 'F':
         print_query('tests')
         #final  code