#!/usr/bin/python3
"""
A simple Flask web application that displays a list of states.

This module sets up a Flask application with a single route to display
a list of states from a database using a template. It also ensures that
the database session is properly closed after each request.

Dependencies:
- Flask: For creating the web application.
- models: For interacting with the database.
- models.state: For accessing the State model.

Usage:
- Run this script to start the Flask development server.
- Access the application at http://0.0.0.0:5000/states_list to see the list of states.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def handle():
    """
    Handle requests to the /states_list route.

    Fetches all State objects from the storage engine and renders them
    using the '7-states_list.html' template.

    Returns:
        str: Rendered HTML page displaying a list of states.
    """
    # Fetch all State objects from the storage and get their values
    states = storage.all(State).values()
    
    # Render the '7-states_list.html' template with the list of states
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """
    Clean up the database session after each request.

    This function is called after each request to close the SQLAlchemy
    session, ensuring that resources are properly released.

    Args:
        exception (Exception): The exception raised, if any, during the request.
    """
    # Close the storage engine session to release resources
    storage.close()


if __name__ == '__main__':
    # Run the Flask development server on host 0.0.0.0 and port 5000
    app.run(host="0.0.0.0", port=5000)
