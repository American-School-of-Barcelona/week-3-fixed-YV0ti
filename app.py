from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/display")
def display():
    tasks = []
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append(row)
    return render_template("display.html", tasks=tasks)


@app.route("/display/<project_title>")
def display_project(project_title):
    tasks = []
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["project_title"] == project_title:
                tasks.append(row)
    return render_template("display.html", tasks=tasks, project_title=project_title)


@app.route("/input", methods=["GET", "POST"])
def input_task():
    # Build project list first — needed for both GET and POST
    projects = []
    seen = set()
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = row["project_title"]
            if t not in seen:
                projects.append(t)
                seen.add(t)

    if request.method == "POST":
        project_title = request.form["project_title"]
        title = request.form["title"]
        description = request.form["description"]
        status = request.form["status"]
        next_steps = request.form["next_steps"]

        fieldnames = ["datetime", "project_title", "title", "description", "status", "next_steps"]

        # ✅ Open the file here, before using DictWriter
        with open("tasks.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "project_title": project_title,
                "title": title,
                "description": description,
                "status": status,
                "next_steps": next_steps,
            })

        # ✅ Redirect after saving
        return redirect(url_for("display"))

    # GET request — show the empty form
    return render_template("input.html", projects=projects)


if __name__ == "__main__":
    app.run(debug=True)