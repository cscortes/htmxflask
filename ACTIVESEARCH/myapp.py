import flask

# Server 3 urls:
# /static for /static/js/htmx.js /static/img/bars.svg 
# / or /index.html 
# /search/

app = flask.Flask(__name__, static_url_path='/static')

class User:
    id = 0
    def __init__(self, fname, lname, email ):
        User.id  += 1
        self.id = User.id 
        self.fname = fname
        self.lname = lname 
        self.email = email

    def search( self, word ):
        if (word is None):
            return False
        all = self.fname + self.lname + self.email
        return word.lower() in all.lower()

users = [
    User("abe", "vida", "abe@nowhere.com"),
    User("betty", "b", "bb@nowhere.com"),
    User("joe", "robinson", "jrobinson@nowhere.com"),

    User("Luis", "Cortes", "Luis@somewhere.com"),
    User("marty", "hinkle", "mhinkle@nowhere.com"),
    User("matthew", "robinson", "mrobinson@nowhere.com"),

    User("collin", "western", "cwest@nowhere.com"),
    User("marty", "hinkle II", "mhinkle2@nowhere.com"),
    User("joe", "robinson", "jrobinson@nowhere.com"),

    User("juan", "vida", "juanvida@nowhere.com"),
    User("marty", "hinkle III", "mhinkle3@nowhere.com"),
    User("zoe", "omega", "zoe@nowhere.com") 
]

@app.route("/")
@app.route("/index.html")
def root():
    return flask.render_template("index.html")


@app.route('/search/', methods=['POST'])
def search():
    templ = """
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.fname }}</td>
                <td>{{ user.lname }}</td>
                <td>{{ user.email }}</td>
            </tr>
            {% endfor %}
    """
    searchWord = flask.request.form.get('search', None)
    matchusers = [user for user in users if user.search(searchWord)]
    return flask.render_template_string(templ,users=matchusers)


if __name__ == '__main__':
   app.run(debug = True)
