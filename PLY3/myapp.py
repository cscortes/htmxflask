from select import select
import flask 

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("index.html")


def selected(val):
    res = ['','','','']
    res[int(val if val is not None else 0)] = 'selected'
    return res

@app.route('/callback/<int:selectnum>', methods=['POST'])
def callback(selectnum):    
    sel1 = flask.request.form['pos1'] if selectnum == 1 else None
    sel2 = flask.request.form['pos2'] if selectnum == 2 else None
    sel3 = flask.request.form['pos3'] if selectnum == 3 else None
     
    val = sel1 or sel2 or sel3 
    
    if sel1 is None and flask.request.form['pos1'] != val:
        sel1 = flask.request.form['pos1']
    if sel2 is None and flask.request.form['pos2'] != val:
        sel2 = flask.request.form['pos2'] 
    if sel3 is None and flask.request.form['pos3'] != val:
        sel3 = flask.request.form['pos3']

    s1 = selected(sel1)
    s2 = selected(sel2)
    s3 = selected(sel3)

    return      f"""                
                <div class="col-md-4">
                    <select name="pos1" hx-post="/callback/1" hx-target="#idx_row" class="form-select">
                        <option value="0" {s1[0]}>&lt;None&gt;</option>
                        <option value="1" {s1[1]}>1</option>
                        <option value="2" {s1[2]}>2</option>
                        <option value="3" {s1[3]}>3</option>
                    </select>""" + \
                f"""
                </div>
                <div class="col-md-4">
                    <select name="pos2" hx-post="/callback/2" hx-target="#idx_row" class="form-select">
                        <option value="0" {s2[0]}>&lt;None&gt;</option>
                        <option value="1" {s2[1]}>1</option>
                        <option value="2" {s2[2]}>2</option>
                        <option value="3" {s2[3]}>3</option>
                    </select>
                </div>""" + \
                f"""
                <div class="col-md-4">
                    <select name="pos3" hx-post="/callback/3" hx-target="#idx_row" class="form-select">
                        <option value="0" {s3[0]}>&lt;None&gt;</option>
                        <option value="1" {s3[1]}>1</option>
                        <option value="2" {s3[2]}>2</option>
                        <option value="3" {s3[3]}>3</option>
                    </select>
                </div>
""" 

if __name__ == '__main__':
   app.run()
   
   