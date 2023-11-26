from flask import Flask, render_template, request
import os

app = Flask(__name__)

class Node:
    def __init__(self, name, age, gen, idtype, id, mob, comor):
        self.name = name
        self.age = int(age)  # Convert age to an integer
        self.gen = gen
        self.idtype = idtype
        self.id = id
        self.mob = mob
        self.comor = comor
        self.link = None

start = None

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def heading():
    clear_screen()
    print("COVID-19 Vaccination Program\n")

def get_candidate_details(i):
    print(f"Enter details for Candidate {i}:")

    a = input("Name: ")
    z = input("Age: ")
    b = input("Gender: ")
    c = input("ID Type: ")
    d = input("ID Number: ")
    e = input("Mobile Number: ")
    f = input("Comorbidities: ")

    return a, z, b, c, d, e, f

def details():
    global start
    heading()
    n = int(input("Enter the number of candidates (Max 4): "))

    for i in range(1, n+1):
        clear_screen()
        heading()
        details = get_candidate_details(i)

        new_node = Node(*details)
        if start is None:
            start = new_node
        else:
            current = start
            while current.link is not None:
                current = current.link
            current.link = new_node

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

def display_vaccine_suggestions():
    clear_screen()
    heading()

    # Suggest vaccines based on the entered age for each candidate
    current = start
    while current is not None:
        print(f"\nSuggested vaccine for {current.name} ({current.age} years old): {suggest_vaccine(current.age)}")
        current = current.link

@app.route("/", methods=["GET", "POST"])
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
