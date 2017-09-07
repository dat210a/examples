"""flask_example
Python file:
This is an example file that shows a very basic site running on a Flask server.
The '@app.route()' decorator is used to tell flask what to do when someone requests a site
with the path in the parameter.

For the Jinja2 {{ url_for() }}, the parameter is the name of the function for the page you want to render.
This is why {{ url_for(number) }} will lead you to the /apples/ path.

The default address for the Flask server is http://127.0.0.1:5000/

Templates:
A demonstration of loops in templating can be found in the 'page.html' template.
Otherwise, the templates just demonstrate basic templating.
"""
from flask import Flask, render_template

app = Flask(__name__)

# Flask configuration parameters #
app.config['debug'] = False  # Set this to True if you intend to make changes to this file
app.secret_key = 'random string'


# Flask routes #
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page')
def page():
    return render_template('page.html')


@app.route('/apples/<int:num>')
def number(num):
    """The number passed as part of the URL will be fed into the function.
    This means that while the 'page' template only lists a few links, you can manually
    type in /apples/25 and Flask will render page 25.

    This might not be desirable behaviour, so in a real-world application there will
    likely need to be some checks on functions that have input arguments.
    """
    return render_template('number.html', page_number=num)

if __name__ == '__main__':
    app.run()
