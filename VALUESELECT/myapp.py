import csv 
import flask
# URLS Served:
# / OR /index.html
# /models/
# /static/js/htmx.js  (really, cause got nothing else )

app = flask.Flask(__name__, static_url_path='/static')

mmdb = {}
with open("car.csv") as csvfile:
    for make, model in csv.reader(csvfile, quotechar="'"):
        if make not in mmdb.keys():
            mmdb[make] = []
        mmdb[make].append(model)

@app.route('/models/', methods=['GET'])
def getmodels():
    templ = """
    {%for amodel in models %}
        <option value="{{ amodel }}">{{ amodel }}</option>
    {% endfor %}
    """
    models = mmdb[flask.request.args.get("makeselected")]
    return flask.render_template_string(templ, models=models)

@app.route('/')
@app.route('/index.html')
def index():
    makers = sorted(mmdb.keys())
    models = mmdb[makers[0]]
    return flask.render_template('index.html', models=models, makers=makers)

if __name__ == '__main__':
   app.run(debug = True)
