#!/usr/bin/python3
"""return hello HBNB using flask"""

from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State


app = Flask(__name__)



@app.route('/cities_by_states', strict_slashes=False)
def handel():
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)

@app.teardown_appcontext
def teardown(exec):
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0")
