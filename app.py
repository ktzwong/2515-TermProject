from flask import Flask

# if __name__ "__main__":
#     app.run(debug=True, port=8888)

'''
will run the flask web application, in debug mode, that listens on port 8888
listens on local interfaces, access via localhost or 127.0.0.1 
'''

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"

app.instance_path = Path(" ").resolve()



