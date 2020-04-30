from flask import Flask, render_template, request, session, redirect, url_for
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'covid_19'

config = {

    "apiKey": "AIzaSyCrXpk7ZbcacVfx_-FL7u3_RlNnwnDN9NU",
    "authDomain": "lokaverk-1350a.firebaseapp.com",
    "databaseURL": "https://lokaverk-1350a.firebaseio.com",
    "projectId": "lokaverk-1350a",
    "storageBucket": "lokaverk-1350a.appspot.com",
    "messagingSenderId": "329421876012",
    "appId": "1:329421876012:web:b5ba5f878c9bd78bdbda89",
    "measurementId": "G-Z6FE2TENR5"


}

fb = pyrebase.initialize_app(config)
db = fb.database()


# Test route til að setja gögn í db
@app.route('/')
def index():
    return render_template("index.html")


# Test route til að sækja öll gögn úr db
@app.route('/login', methods=['GET', 'POST'])
def login():

    u = db.child("bill").get().val()
    lst = list(u.items())

    return render_template("innskra.html", bilar=lst)


@app.route('/nyskra')
def register():
    return render_template('register.html')

# Test route til að sækja öll gögn úr db
@app.route('/donyskra', methods=['GET', 'POST'])
def doregister():
    skrnr = []
    if request.method == 'POST':
        nr = request.form['nr']
        tegund = request.form['tegund']
        utegund = request.form['utegund']
        argerd = request.form['argerd']
        akstur = request.form['akstur']

        u = db.child("bill").get().val()
        lst = list(u.items())
        for i in lst:
            skrnr.append(i[1]['nr'])
        
        if nr not in skrnr:
            db.child("bill").push({"nr":nr, "tegund":tegund, "utegund":utegund, "argerd":argerd, "akstur":akstur})
            return render_template("registered.html", nr = nr)

        else:
            return render_template("userexsists", nr = nr)
    else:
        return render_template("no_method.html")

@app.route('/bill/<id>')
def bill(id):
    b = db.child("bill").child(id).get().val()
    bill = list(b.items())
    return render_template("car.html", bill = bill, id=id)


@app.route('/breytaeyda', methods=['POST'])
def breytaeyda():
    if request.method == 'POST':
        #eyda
        if request.form['submit'] == 'eyda':
            db.child("bill").child( request.form['id'] ).remove()
            return render_template("deleted.html", nr = request.form['nr'])
        else:
            db.child("bill").child(request.form['id']).update({"nr":request.form['nr'], "tegund":request.form['tegund'], "utegund":request.form['utegund'], "argerd":request.form['argerd'], "akstur":request.form['akstur']})
            return render_template("updated.html", nr = request.form['nr'])
    else:
        return render_template("no_method.html")


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return render_template("index.html")


@app.route('/topsecret')
def topsecret():
    if 'logged_in' in session:
        return render_template("topsecret.html")
    else:
        return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)

# skrifum nýjan í grunn hnútur sem heitir notandi 
# db.child("notandi").push({"notendanafn":"dsg", "lykilorð":1234}) 

# # förum í grunn og sækjum allar raðir ( öll gögn )
# u = db.child("notandi").get().val()
# lst = list(u.items())
