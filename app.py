import os

from flask import Flask, render_template, request, redirect, url_for
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host=os.environ.get('REDIS_HOST'), port=os.environ.get('REDIS_PORT'), db=0,
                                 password=os.environ.get('REDIS_PWD'))


@app.route('/')
def index():
    # gets all user keys from the client
    user_keys = redis_client.keys('user:*')
    users = []

    for user_key in user_keys:
        # get the value with the key
        user_data = redis_client.hgetall(user_key)
        user_entry = {user_key.decode('utf-8'): user_data}
        users.append(user_entry)

    # render the template with the user data
    return render_template('index.html', users=users)


@app.route('/submit', methods=['POST'])
def submit():
    # get form data
    name = request.form['name']
    email = request.form['email']

    # save user entries with the user:"email" key
    user_key = f"user:{email}"
    # save the complete entry
    redis_client.hmset(user_key, {'name': name, 'email': email})

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
