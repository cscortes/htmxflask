import flask

app = flask.Flask(__name__, static_url_path='/static')

class User:
    id = 0
    def __init__(self, fname, lname, email ):
        User.id  +=1
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

@app.route('/index.html')
def root():
    return flask.render_template("index.html")


@app.route('/search/', methods=['POST'])
def search():
    templ =             {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.fname }}</td>
                <td>{{ user.lname }}</td>
                <td>{{ user.email }}</td>
            </tr>
            {% endfor %}
    searchWord = flask.request.form.get('search', None)
    matchusers = [user for user in users if user.search(searchWord)]
    return flask.render_template_string(templ,users=matchusers)


if __name__ == '__main__':
   app.run(debug = True) 