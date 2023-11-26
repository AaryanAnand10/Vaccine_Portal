import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        id_number = request.form["id_number"]

        if name and id_number:
            return redirect(url_for("vaccine", name=name, id_number=id_number))

    return render_template("login.html")

@app.route("/vaccine/<name>/<id_number>")
def vaccine(name, id_number):
    vaccine_name = "Pfizer" # Assuming the vaccine is Pfizer
    return render_template("vaccine.html", name=name, vaccine_name=vaccine_name)



# establish a connection to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123#123",
    database="practice"
)

class Node:
    def __init__(self, name, age, gen, idtype, id, mob, comor):
        self.name = name
        self.age = int(age) # Convert age to an integer
        self.gen = gen
        self.idtype = idtype
        self.id = id
        self.mob = mob
        self.comor = comor
        self.link = None

start = None

def heading():
    print("Heading")

def details():
    global start
    heading()
    print("\t\t\t\tEnter Candidate Number (Max 4 People): ")
    n = int(input())

    for i in range(1, n+1):
        os.system("cls")
        heading()
        print("\t\t\t\tEnter The %dth Candidate Name: " % i)
        a = input()
        print("Enter the Candidates Age: ")
        z = input()
        print("\t\t\t\tEnter The %dth Candidate Gender: " % i)
        b = input()
        print("\t\t\t\tEnter The %dth Candidate Id-Type: " % i)
        c = input()
        print("\t\t\t\tEnter The %dth Candidate Id-Number: " % i)
        d = input()
        print("\t\t\t\tEnter The %dth Candidate Mobile Number: " % i)
        e = input()
        print("\t\t\t\tEnter The %dth Candidate Comor: " % i)
        f = input()

        new_node = Node(a, z, b, c, d, e, f)
        if start is None:
            start = new_node
        else:
            current = start
            while current.link is not None:
                current = current.link
            current.link = new_node



from waitress import serve
serve(app, host="0.0.0.0", port=8080)

def suggest_vaccine(age):
    if 12 <= age < 18:
        return "Pfizer-BioNTech or Moderna"
    elif 18 <= age < 30:
        return "Moderna, Pfizer-BioNTech, or Johnson & Johnson"
    elif 30 <= age < 50:
        return "Moderna, Pfizer-BioNTech, Johnson & Johnson, or AstraZeneca"
    elif age >= 50:
        return "Moderna, Pfizer-BioNTech, Johnson & Johnson, AstraZeneca, or Sinopharm"
    else:
        return "Age not eligible for vaccination"

def venue():
    print("Venue")

def receipt():
    print("Receipt")

def sql_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123#123",
            database="practice"
        )
        cursor = connection.cursor()
        print("Connected to MySQL")

        current = start
        while current is not None:
            sql_insert_query = """ INSERT INTO candidates (name, age, gen, idtype, id, mob, comor) VALUES (%s, %s, %s, %s, %s, %s, %s); """
            insert_tuple = (current.name, current.age, current.gen, current.idtype, current.id, current.mob, current.comor)
            cursor.execute(sql_insert_query, insert_tuple)
            connection.commit()
            print(f"Record inserted for {current.name}")
            current = current.link

        cursor.close()
        connection.close()
        print("MySQL connection is closed")

    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL: {error}")



if __name__ == "__main__":
    details()
    sql_connection()
    venue()
    receipt()

    # Suggest vaccines based on the entered age for each candidate
    current = start
    while current is not None:
        print(f"\nSuggested vaccine  for {current.name} ({current.age} years old): {suggest_vaccine(current.age)}")
        current = current.link


def index():
    if request.method == "POST":
        global start
        start = None  # Reset the linked list for each request
        details()
        suggestions = []

        current = start
        while current is not None:
            suggestion = f"Suggested vaccine for {current.name} ({current.age} years old): {suggest_vaccine(current.age)}"
            suggestions.append(suggestion)
            current = current.link

        return render_template("index.html", suggestions=suggestions)

    return render_template("index.html", suggestions=[])

if __name__ == "__main__":
    app.run(debug=True)


