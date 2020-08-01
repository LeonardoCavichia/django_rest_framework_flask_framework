from flask import Flask, render_template, redirect, url_for
import requests

from blueprints.users import login_required

app = Flask(__name__)


from blueprints import users, events

app.secret_key = "JDIJI1I2391JDJSDKDJKXXKQKDK"
app.register_blueprint(users.bp)
app.register_blueprint(events.bp)


@app.route('/')
@login_required
def hello_world():
    return redirect(url_for('user.users'))


if __name__ == '__main__':
    app.run()
