import os
from datetime import date

from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect, CSRFError

from manage_user import insert_user, retrieve_all_users, retrieve_user, mail_check

app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = False

PASSWORD = "admin"

# CSRF protection routine
# SECRET_KEY = os.urandom(32)
SECRET_KEY = "word_of_widsom" # security downgrade to avoid crash on heroku
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)

# render  CSRF error page 400
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

# render error page 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# render admin page (sorta ok)
@app.route('/admin', methods = ["GET", "POST"])
def admin():
    
    user_list = ""
    invalid = ""
    
    if request.method == "POST":
        psw = request.form['password']
        
        if psw == PASSWORD:
            user_list = retrieve_all_users()
        else:
            invalid = "[!] Wrong password"
  
    return render_template("admin.html", user_list = user_list, invalid=invalid)

# render query page (to be written)
@app.route('/retrieve', methods = ["GET", "POST"])
def retrieve():
    
    user_data = ""
    invalid = ""
    
    if request.method == "POST":
        requested_user = str(request.form['req_username'])
        
        try: 
            user_data = retrieve_user(requested_user)
        except Exception as e:
            invalid = "[!] User not found"
  
    return render_template("retrieve.html", user_data = user_data, invalid=invalid)

# render main page (to be written)
@app.route('/', methods = ["GET", "POST"])
def input_page():
    
    errors = ""
    today = date.today()
    
    if request.method == "POST":
        user_name = str(request.form['name'])
        user_mail = str(request.form['mail'])
        user_phone = str(request.form['phone'])
        
        if user_name != "" and user_mail != "" and user_phone != "" and mail_check(user_mail):
            try:
                insert_user(user_name, user_mail, user_phone)
                return render_template("results.html", 
                                       user_name=user_name, user_mail=user_mail, user_phone=user_phone, today_date=today)
            
            except Exception as e:
                errors = f"[!] Errors found: {e}"
        elif user_name == "" or user_mail == "" or user_phone == "":
            errors = "[!] You must fill in all the fields"
        elif not mail_check(user_mail):
            errors = "[!] Invalid email"

    return render_template("main.html", today=today, errors=errors)

if __name__ == '__main__':
    app.run(use_reloader=False)
