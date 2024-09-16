from flask import Flask
app = Flask(__name__)

''' Launch the Flask App
Remember to put HTML file into "static" folder
Remember to get the name of html file right
'''
@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/app1', methods=['GETS'])
def launch_author():
    return 0

if __name__ == '__main__':
    app.run(debug=True, port = 1234)