import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    """Main page that displays the three interdependent select dropdowns."""
    return flask.render_template("index.html")


def get_selected_states(selected_value):
    """
    Generate the 'selected' attribute for each option based on the selected
    value.

    Args:
        selected_value: The currently selected value (0, 1, 2, or 3)

    Returns:
        List of 'selected' attributes for options 0, 1, 2, 3
    """
    # Handle None or invalid values
    if selected_value is None:
        selected_value = 0

    # Convert to integer safely
    try:
        selected_value = int(selected_value)
        if selected_value not in [0, 1, 2, 3]:
            selected_value = 0
    except (ValueError, TypeError):
        selected_value = 0

    # Create list of selected states
    return ['selected' if i == selected_value else '' for i in range(4)]


@app.route('/callback/<int:selectnum>', methods=['POST'])
def callback(selectnum):
    """
    HTMX callback endpoint that handles dropdown changes.

    When a dropdown is changed, this endpoint:
    1. Gets the new value from the changed dropdown
    2. Sets all other dropdowns to None (mutual exclusion)
    3. Returns updated HTML for all three dropdowns

    Args:
        selectnum: Which dropdown was changed (1, 2, or 3)

    Returns:
        HTML fragment with updated dropdown states
    """
    # Get the value from the dropdown that was changed
    form_data = flask.request.form

    # Initialize all selections to None
    sel1 = sel2 = sel3 = None

    # Set the value for the dropdown that was changed
    if selectnum == 1:
        sel1 = form_data.get('pos1', '0')
    elif selectnum == 2:
        sel2 = form_data.get('pos2', '0')
    elif selectnum == 3:
        sel3 = form_data.get('pos3', '0')

    # Get selected states for each dropdown
    s1 = get_selected_states(sel1)
    s2 = get_selected_states(sel2)
    s3 = get_selected_states(sel3)

    # Return updated HTML for all three dropdowns
    return flask.render_template_string("""
        <div class="col-md-4">
            <select name="pos1" hx-post="/callback/1" hx-target="#idx_row"
                    class="form-select">
                <option value="0" {{ s1[0] }}>&lt;None&gt;</option>
                <option value="1" {{ s1[1] }}>1</option>
                <option value="2" {{ s1[2] }}>2</option>
                <option value="3" {{ s1[3] }}>3</option>
            </select>
        </div>
        <div class="col-md-4">
            <select name="pos2" hx-post="/callback/2" hx-target="#idx_row"
                    class="form-select">
                <option value="0" {{ s2[0] }}>&lt;None&gt;</option>
                <option value="1" {{ s2[1] }}>1</option>
                <option value="2" {{ s2[2] }}>2</option>
                <option value="3" {{ s2[3] }}>3</option>
            </select>
        </div>
        <div class="col-md-4">
            <select name="pos3" hx-post="/callback/3" hx-target="#idx_row"
                    class="form-select">
                <option value="0" {{ s3[0] }}>&lt;None&gt;</option>
                <option value="1" {{ s3[1] }}>1</option>
                <option value="2" {{ s3[2] }}>2</option>
                <option value="3" {{ s3[3] }}>3</option>
            </select>
        </div>
    """, s1=s1, s2=s2, s3=s3)


if __name__ == '__main__':
    app.run(debug=True)
