from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def users_table():
    users=User.get_all()
    print(users)
    return render_template("users.html", users = users)


@app.route('/users/new')
def create_user():
    return render_template('/new_user.html')

# posts new row
@app.route('/users/new_process', methods=['POST'])
def process():
    data = {
        'fname':request.form['fname'],
        'lname':request.form['lname'],
        'email':request.form['email'],
    }
    User.save(data)
    user = User.last(data)
    print(user)
    #we want it to redirect to '/users/<int:user_id>'
    return redirect(f"/users/{user[0]['id']}")


@app.route('/users/<int:user_id>')
def show_single_user(user_id):
    show_single = User.select_single({"id":user_id})
    return render_template('show_single_user.html',show_single=show_single)


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    User.delete({'id':user_id})
    return redirect('/')


@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    user = User.select_single({"id":user_id})
    return render_template('edit_user.html',user=user)


@app.route('/users/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    data = {
        'fname':request.form['fname'],
        'lname':request.form['lname'],
        'email':request.form['email'],
        'id':user_id
    }
    User.update(data)
    return redirect(f'/users/{user_id}')