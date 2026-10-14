from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/energy')
def category_energy():
    return render_template('category_energy.html')

@app.route('/category/transport')
def category_transport():
    return render_template('category_transport.html')

@app.route('/category/forest')
def category_forest():
    return render_template('category_forest.html')

if __name__ == '__main__':
    app.run(debug=True)