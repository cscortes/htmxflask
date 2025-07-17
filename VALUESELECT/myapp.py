import csv
import flask

app = flask.Flask(__name__, static_url_path='/static')

# Global database to store make-model relationships
mmdb = {}


def load_car_data():
    """Load car make-model data from CSV file into memory."""
    try:
        with open("car.csv") as csvfile:
            for make, model in csv.reader(csvfile, quotechar="'"):
                if make not in mmdb:
                    mmdb[make] = []
                mmdb[make].append(model)
        total_models = sum(len(models) for models in mmdb.values())
        print(f"Loaded {len(mmdb)} car makes with {total_models} total models")
    except FileNotFoundError:
        print("Warning: car.csv not found. Using sample data.")
        # Fallback sample data
        mmdb.update({
            'Toyota': ['RAV4', 'Highlander', '4Runner', 'Sequoia'],
            'Honda': ['CR-V', 'Pilot', 'Passport', 'Ridgeline'],
            'Ford': ['Escape', 'Explorer', 'Edge', 'Expedition']
        })


# Load data on startup
load_car_data()


@app.route('/models/', methods=['GET'])
def getmodels():
    """
    HTMX endpoint that returns HTML fragment of model options for a selected
    make.

    Expected query parameter: makeselected (the car make)
    Returns: HTML fragment with <option> elements for models
    """
    selected_make = flask.request.args.get("makeselected")

    # Handle missing or invalid make selection
    if not selected_make or selected_make not in mmdb:
        return '<option value="">No models available</option>'

    # Get models for the selected make
    models = mmdb[selected_make]

    # Return HTML fragment with model options
    templ = """
    <option value="">Select a model...</option>
    {% for amodel in models %}
        <option value="{{ amodel }}">{{ amodel }}</option>
    {% endfor %}
    """
    return flask.render_template_string(templ, models=models)


@app.route('/')
@app.route('/index.html')
def index():
    """
    Main page that displays the cascading dropdown interface.

    Returns: HTML page with make dropdown populated and initial models shown
    """
    # Get sorted list of all available makes
    makers = sorted(mmdb.keys())

    # Get models for the first make (default selection)
    initial_models = mmdb[makers[0]] if makers else []

    return flask.render_template('index.html', models=initial_models,
                                 makers=makers)


if __name__ == '__main__':
    app.run(debug=True)
