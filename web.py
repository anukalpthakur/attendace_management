from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Inline templates
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .container { width: 300px; margin: auto; }
        input { width: 100%; padding: 10px; margin: 5px 0; }
        button { padding: 10px; width: 100%; background-color: blue; color: white; border: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

home_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .container { width: 300px; margin: auto; }
        a { text-decoration: none; padding: 10px; display: block; background: blue; color: white; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, {{ username }}</h2>
        <a href="/dashboard">Go to Dashboard</a>
        <a href="/logout">Logout</a>
    </div>
</body>
</html>
"""

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .container { width: 300px; margin: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Dashboard</h2>
        <p>Welcome, {{ username }}! This is your dashboard.</p>
        <a href="/">Go to Home</a>
    </div>
</body>
</html>
"""

users = {"admin": "password"}  # Dummy users database

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            return redirect(url_for("home", username=username))
        else:
            return "<h3>Invalid Credentials! Try again.</h3>" + login_html
    return render_template_string(login_html)

@app.route("/home")
def home():
    username = request.args.get("username", "Guest")
    return render_template_string(home_html, username=username)

@app.route("/dashboard")
def dashboard():
    username = request.args.get("username", "Guest")
    return render_template_string(dashboard_html, username=username)

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
