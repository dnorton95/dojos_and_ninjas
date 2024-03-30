from flask_app import app
from flask import redirect, render_template, request
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja
#Create an HTTP Root Route, a homepage
@app.route("/")
#Define a function that you want to be performed when this route is opened
def index():
    dojos = Dojo.get_all()
    #In this case, we're rendering an html template that we will build
    return render_template("template.html", dojos=dojos)

#this is the route that we defined in our HTML template
@app.post("/create_dojo")
def create_dojo():
    if not Dojo.validate_dojo(request.form):
        return redirect('/')
    #import the class method functionality from the correct controller, and use a . to grab the class method
    #using the class method, we'll request the form from our HTML sheet
    Dojo.create_dojo(request.form)
    #never return a render_template when users are inputting info
    #return a redirect to an HTTP route that will render our HTML template
    return redirect("/")

@app.route("/create_ninja")
def create_ninja():
    dojos=Dojo.get_all()
    return render_template("create_ninja.html", dojos=dojos)

@app.post("/new_ninja")
def new_ninja():
    if not Ninja.validate_ninja(request.form):
        return redirect('/create_ninja')
    #import the class method functionality from the correct controller, and use a . to grab the class method
    #using the class method, we'll request the form from our HTML sheet
    Ninja.create_ninja(request.form)
    #never return a render_template when users are inputting info
    #return a redirect to an HTTP route that will render our HTML template
    return redirect("/all_ninjas")

@app.route("/all_ninjas")
def all_ninjas():
    ninjas=Ninja.get_all()
    return render_template("all_ninjas.html", ninjas=ninjas)

@app.route("/dojo/<int:dojo_id>")
def display_dojo_ninjas(dojo_id):
    dojo = Dojo.get_dojo_by_id(dojo_id)
    ninjas = Ninja.get_ninjas_by_dojo(dojo_id)
    return render_template("dojo_ninjas.html", dojo=dojo, ninjas=ninjas)
