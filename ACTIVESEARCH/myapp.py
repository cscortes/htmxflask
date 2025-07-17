import flask

app = flask.Flask(__name__, static_url_path='/static')


class User:
    """Simple user class for demonstration purposes."""
    id = 0

    def __init__(self, fname, lname, email):
        User.id += 1
        self.id = User.id
        self.fname = fname
        self.lname = lname
        self.email = email

    def search(self, word):
        """Archives user data for the given word across name and email."""
        if word is None:
            return False
        all_data = self.fname + self.lname + self.email
        return word.lower() in all_data.lower()


# Sample user data for demonstration - 24iverse users
users = [
    User("John", "Smith", "jsmith@company.com"),
    User("Jane", "Doe", "jane.doe@email.org"),
    User("Bob", "Johnson", "bob.j@tech.net"),

    User("Maria", "Garcia", "mgarcia@business.com"),
    User("Carlos", "Rodriguez", "crodriguez@work.org"),
    User("Diana", "Davis", "ddavis@corp.net"),

    User("Edward", "Miller", "emiller@office.com"),
    User("Sofia", "Martinez", "smartinez@company.org"),
    User("George", "Taylor", "gtaylor@business.net"),

    User("Helen", "Anderson", "handerson@work.com"),
    User("Jose", "Lopez", "jlopez@email.org"),
    User("Julia", "Jackson", "jjackson@corp.com"),

    User("Ana", "Gonzalez", "agonzalez@enterprise.com"),
    User("David", "Wilson", "dwilson@startup.net"),
    User("Isabella", "Hernandez", "ihernandez@agency.org"),

    User("Michael", "Brown", "mbrown@consulting.com"),
    User("Elena", "Torres", "etorres@studio.net"),
    User("Robert", "Jones", "rjones@partners.org"),

    User("Carmen", "Flores", "cflores@creative.com"),
    User("Thomas", "Moore", "tmoore@innovate.net"),
    User("Patricia", "Rivera", "privera@design.org"),

    User("Christopher", "Lee", "clee@venture.com"),
    User("Gabriela", "Cruz", "gcruz@dynamic.net"),
    User("Daniel", "White", "dwhite@strategic.org")
]


@app.route('/')
@app.route('/index.html')
def root():
    """Provides the main search page."""
    return flask.render_template("index.html", users=users)


@app.route('/search/', methods=['POST'])
def search():
    """
    Handles search requests and return filtered user results as HTML fragment.
    """
    search_word = flask.request.form.get('search', None)

    # If search is empty, return all users
    if not search_word or search_word.strip() == '':
        match_users = users
    else:
        match_users = [user for user in users if user.search(search_word)]

    # Handle no matching results (only when there was actually a search term)
    if ((search_word) and (search_word.strip() != '') and (not match_users)):
        return '''
        <tr>
        <td colspan="4" class="no-results">No users found</td>
        </tr>'''

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
    return flask.render_template_string(templ, users=match_users)


if __name__ == '__main__':
    app.run(debug=True)
