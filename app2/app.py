# app.py

from flask import Flask, request, Response, session, redirect, url_for, jsonify, render_template
from functools import wraps
from uuid import uuid4, UUID
 
app = Flask(__name__)
app.secret_key = 'VFJBSU46VHVOM0w='
app.trains = {}


def get_train_from_json():
    train_data = request.get_json()
    if not train_data:
        raise InvalidUsage('Please provide json data')
    #print(train_data)    
    return train_data

def set_train(train_id=None, data=None, update=False):
    if train_id is None:
        train_id =  str(uuid4())
    
    if data is None:
        data = get_train_from_json()
        if data is None:
            raise InvalidUsage('Please provide json data')
    

    if update:
        app.trains[train_id].update(data)
    else:
        app.trains[train_id] = data
    
    return train_id


@app.route('/')
def root():
    return 'Hello!'


def check_auth(username, password):
    return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
    return Response('Could not verify your access level for that URL.\n' 'You have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return please_authenticate()
        return func(*args, **kwargs)

    return wrapper


@app.route('/login', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))


def requires_user_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


@app.route('/hello')
@requires_user_session
def hello():
    return render_template('greeting.html', name=session['username'])


@app.route('/logout', methods=['GET', 'POST'])
@requires_user_session
def logout():
    if request.method == 'GET':
        return redirect(url_for('root'))
    del session['username']
    return redirect(url_for('root'))


@app.route('/trains', methods=['GET', 'POST'])
@requires_user_session
def trains():
    if request.method == 'GET':
        return jsonify(app.trains)
    elif request.method == 'POST':
        train_id = set_train()
        print(app.trains[train_id])
        return redirect(url_for('trains', train_id=train_id, format='json'))

@app.route('/trains/<train_id>',
           methods=['GET', 'DELETE'])
def train(train_id):
    #if train_id not in app.trains:
    #    return 'No such train', 404

    if request.method == 'DELETE':
        del app.trains[train_id]
        return '', 204

    if request.method == 'GET':
        return jsonify(app.trains[train_id])


if __name__ == '__main__':
    app.run(debug=True)
