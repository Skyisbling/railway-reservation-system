#import modules

import streamlit as st
import sqlite3 as sql
import pandas as pd

#initialising database

conn=sql.connect('railway.db')
page1='login or signup'
cur=conn.cursor()

#create tables USERS, EMPLOYEES, TRAINS

def create_table():
    cur.execute('CREATE TABLE IF NOT EXISTS USERS'
                '(USERNAME TEXT,'
                'PASSWORD TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS EMPLOYEES'
                '(EMPLOYEE_ID TEXT,'
                'PASSWORD TEXT,'
                'DESIGNATION TEXT)')

    cur.execute('CREATE TABLE IF NOT EXISTS TRAINS'
                '(TRAIN_NUMBER TEXT,'
                'TRAIN_NAME TEXT,'
                'DEPARTURE_DATE TEXT,'
                'START_DESTINATION TEXT,'
                'END_DESTINATION TEXT)')
create_table() #CALLING FUNCTION


#add train function
def add_train(TRAIN_NUMBER, TRAIN_NAME, DEPARTURE_DATE, START_DESTINATION, END_DESTINATION):
    cur.execute("INSERT INTO TRAINS (TRAIN_NUMBER, TRAIN_NAME,DEPARTURE_DATE, START_DESTINATION, END_DESTINATION) VALUES(?,?,?,?,?)",(TRAIN_NUMBER, TRAIN_NAME, DEPARTURE_DATE, START_DESTINATION, END_DESTINATION))
    conn.commit()
    create_seat_table(TRAIN_NUMBER)


#delete train
def delete_train(TRAIN_NUMBER, DEPARTURE_DATE):
    cur.execute("DROP TABLE IF EXISTS SEATS_" + TRAIN_NUMBER)
    train_query = cur.execute(
        "SELECT * FROM TRAINS WHERE TRAIN_NUMBER = ?", (TRAIN_NUMBER,))
    train_data = train_query.fetchone()
    if train_data:
        cur.execute("DELETE FROM TRAINS WHERE TRAIN_NUMBER = ? AND DEPARTURE_DATE=?",
                    (TRAIN_NUMBER, DEPARTURE_DATE))

        conn.commit()
        st.success(f"Train with Train Number {TRAIN_NUMBER} has been deleted.")
    else:
        st.error(f"No such Train with Number {TRAIN_NUMBER} is available")



conn = sql.connect('railway.db')
cur = conn.cursor()

#CREATE seat table
def create_seat_table(TRAIN_NUMBER):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS SEATS_{TRAIN_NUMBER}
                (SEAT_NUMBER INTEGER PRIMARY KEY,
                SEAT_TYPE TEXT,
                BOOKED INTEGER,
                PASSENGER_NAME TEXT,
                PASSENGER_AGE INTEGER,
                PASSENGER_GENDER TEXT);''')
    for i in range(1, 51):
        val = categorize_seat(i)
        cur.execute(f'''INSERT INTO SEATS_{TRAIN_NUMBER}(SEAT_NUMBER, SEAT_TYPE, BOOKED, PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER) VALUES (?,?,?,?,?,?);''', (
            i, val, 0, "", "", ""))
    conn.commit()



#categorize seat in train
def categorize_seat(SEAT_NUMBER):
    match SEAT_NUMBER%10 :
        case 0|4|5|9 :
            return "Window"
        case 2|3|6|7 :
            return "Aisle"
        case _:
            return 'Middle'


#allocate available seat
def allocate_next_available_seat(TRAIN_NUMBER, SEAT_TYPE):
    seat_query = cur.execute(f"SELECT SEAT_NUMBER FROM SEATS_{TRAIN_NUMBER} WHERE BOOKED=0 AND SEAT_TYPE=? ORDER BY SEAT_NUMBER ASC", (SEAT_TYPE,))
    result = seat_query.fetchone()

    if result:
        return result[0]  # Extracting the seat number
    else:
        st.error("No available seats of this type in the selected train.")
        return None


#BOOK TICKETS
def book_ticket(TRAIN_NUMBER, PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER, SEAT_TYPE):
    train_query = cur.execute("SELECT * FROM TRAINS WHERE TRAIN_NUMBER = ?", (TRAIN_NUMBER,))
    train_data = train_query.fetchone()
    
    if train_data:
        SEAT_NUMBER = allocate_next_available_seat(TRAIN_NUMBER, SEAT_TYPE)
        if SEAT_NUMBER:
            cur.execute(f"""
                UPDATE SEATS_{TRAIN_NUMBER} 
                SET BOOKED=1, PASSENGER_NAME=?, PASSENGER_AGE=?, PASSENGER_GENDER=? 
                WHERE SEAT_NUMBER=?
            """, (PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER, SEAT_NUMBER))
            
            conn.commit()
            st.success(f"Successfully booked seat {SEAT_NUMBER} ({SEAT_TYPE}) for {PASSENGER_NAME}.")
        else:
            st.error("No available seats for booking in this train.")
    else:
        st.error(f"No such Train with Number {TRAIN_NUMBER} is available")


#CANCEL TICKET
def cancel_tickets(TRAIN_NUMBER, SEAT_NUMBER):
    train_query = cur.execute(
        "SELECT * FROM TRAINS WHERE TRAIN_NUMBER = ?", (TRAIN_NUMBER,))
    train_data = train_query.fetchone()
    if train_data:
        cur.execute(
            f'''UPDATE SEATS_{TRAIN_NUMBER} SET BOOKED=0, PASSENGER_NAME='', PASSENGER_AGE='', PASSENGER_GENDER='' WHERE SEAT_NUMBER=?''', (SEAT_NUMBER,))
        conn.commit()
        st.success(
            f"Successfully Cancelled Seat {SEAT_NUMBER} from {TRAIN_NUMBER} .")
    else:
        st.error(f"No such Train with Number {TRAIN_NUMBER} is available")


#SEARCHING TRAINS BY TRAIN NUMBER
def search_train(TRAIN_NUMBER):
    train_query=cur.execute('SELECT * FROM TRAINS WHERE TRAIN_NUMBER=?',(TRAIN_NUMBER,))
    train_data=train_query.fetchone()
    return train_data



#SEARCH TRAIN BY DESTINATION
def train_destination(START_DESTINATION, END_DESTINATION):
    train_query=cur.execute('SELECT * FROM TRAINS WHERE START_DESTINATION=? AND END_DESTINATION=?', (START_DESTINATION, END_DESTINATION))
    train_data=train_query.fetchone()
    return train_data


#view seats
def view_seats(TRAIN_NUMBER):
    train_query=cur.execute("SELECT * FROM TRAINS WHERE TRAIN_NUMBER=? ", (TRAIN_NUMBER,))
    train_data=train_query.fetchone()

    if train_data:
        #return train data
        seat_query=cur.execute(f'''SELECT ('Number: ' || SEAT_NUMBER || 
        '\nType: ' || SEAT_TYPE || 
        '\nName: ' || PASSENGER_NAME || 
        '\nAge: ' || PASSENGER_AGE || 
        '\nGender: ' || PASSENGER_GENDER) AS Details, 
       BOOKED 
FROM SEATS_{TRAIN_NUMBER} 
ORDER BY SEAT_NUMBER ASC;''')   
        result=seat_query.fetchall()
        if result:
            st.dataframe(data=result)
    else:
        st.error(f"No such Train with Number {TRAIN_NUMBER} is available")



def train_functions(): 
    st.title("Train Administrator")
    functions = st.sidebar.selectbox("Select Train Functions", [
        "Add Train", "View Trains", "Search Train", "Delete Train", "Book Ticket", "Cancel Ticket", "View Seats"])
    
    if functions == "Add Train":
        st.header("Add New Train")
        with st.form(key='new_train_details'):
            TRAIN_NUMBER = st.text_input("Train Number")
            TRAIN_NAME = st.text_input("Train Name")
            DEPARTURE_DATE = st.date_input("Date of Departure")
            START_DESTINATION = st.text_input("Start Destination")
            END_DESTINATION = st.text_input("End Destination")
            submitted = st.form_submit_button("Add Train")

        if submitted and TRAIN_NAME != "" and TRAIN_NUMBER != '' and START_DESTINATION != "" and END_DESTINATION != "":
            add_train(TRAIN_NUMBER, TRAIN_NAME, DEPARTURE_DATE, START_DESTINATION, END_DESTINATION)
            st.success("Train Added Successfully!")

    elif functions == "View Trains":
        st.title("View All Trains")
        train_query = cur.execute("SELECT * FROM TRAINS")
        trains = train_query.fetchall()

        if trains:
            st.header("Available Trains:")
            st.dataframe(data=trains)
        else:
            st.error("No trains available in the database.")

    elif functions == "Search Train":
        st.title("Train Details Search")

        st.write("Search by Train Number:")
        TRAIN_NUMBER = st.text_input("Enter Train Number:")

        st.write("Search by Start and End Destination:")
        START_DESTINATION = st.text_input("Start Destination:")
        END_DESTINATION = st.text_input("End Destination:")

        if st.button("Search by Train Number"):
            if TRAIN_NUMBER:
                train_data = search_train(TRAIN_NUMBER)
                if train_data:
                    st.header("Search Result:")
                    st.table(pd.DataFrame([train_data], columns=[
                        "Train Number", "Train Name", "Departure Date", "Start Destination", "End Destination"]))
                else:
                    st.error(f"No train found with the train number: {TRAIN_NUMBER}")

        if st.button("Search by Destinations"):
            if START_DESTINATION and END_DESTINATION:
                train_data = train_destination(START_DESTINATION, END_DESTINATION)
                if train_data:
                    st.header("Search Results:")
                    df = pd.DataFrame([train_data], columns=[
                        "Train Number", "Train Name", "Departure Date", "Start Destination", "End Destination"])
                    st.dataframe(df)
                else:
                    st.error("No trains found for the given source and destination.")

    elif functions == "Delete Train":
        st.title("Delete Train")
        TRAIN_NUMBER = st.text_input("Enter Train Number to delete:")
        DEPARTURE_DATE = st.date_input("Enter the Train Departure date")
        if st.button("Delete Train"):
            if TRAIN_NUMBER:
                cur.execute(f"DROP TABLE IF EXISTS SEATS_{TRAIN_NUMBER}")
                delete_train(TRAIN_NUMBER, DEPARTURE_DATE)

    elif functions == "Book Ticket":
        st.title("Book Train Ticket")
        TRAIN_NUMBER = st.text_input("Enter Train Number:")
        if TRAIN_NUMBER.isdigit():
            TRAIN_NUMBER = int(TRAIN_NUMBER)
        else:
            TRAIN_NUMBER=None
        SEAT_TYPE = st.selectbox("Seat Type", ["Aisle", "Middle", "Window"], index=0)
        PASSENGER_NAME = st.text_input("Passenger Name")
        PASSENGER_AGE = st.number_input("Passenger Age", min_value=1)
        PASSENGER_GENDER = st.selectbox("Passenger Gender", ["Male", "Female", "Other"], index=0)

        if st.button("Book Ticket"):
            if TRAIN_NUMBER and PASSENGER_NAME and PASSENGER_AGE and PASSENGER_GENDER:
                book_ticket(TRAIN_NUMBER, PASSENGER_NAME, PASSENGER_AGE, PASSENGER_GENDER, SEAT_TYPE)

    elif functions == "Cancel Ticket":
        st.title("Cancel Ticket")
        TRAIN_NUMBER = st.text_input("Enter Train Number:")
        SEAT_NUMBER = st.number_input("Enter Seat Number", min_value=1)
        if st.button("Cancel Ticket"):
            if TRAIN_NUMBER and SEAT_NUMBER:
                cancel_tickets(TRAIN_NUMBER, SEAT_NUMBER)

    elif functions == "View Seats":
        st.title("View Seats")
        TRAIN_NUMBER = st.text_input("Enter Train Number:")
        if st.button("Submit"):
            if TRAIN_NUMBER:
                view_seats(TRAIN_NUMBER)

train_functions()

# allocate_next_available_seat()
# print(f"Allocated seat number: {SEAT_NUMBER}, Type: {type(SEAT_NUMBER)}")
