from flask import Flask
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()  # This loads the environment variables from .env file.
cwd = os.getcwd()

# Implement Update API
@app.route('/upload', methods=['POST'])
def upload_file():
    return None

#Implement home page
@app.route('/')
def index():
    return None

#Implement List function here
@app.route('/list')
def listItems():
  return None

# Implement Edit function here
@app.route('/edit')
def editItems():
    return None

@app.route('/update', methods=['POST'])
def update():
  """
  Update the record when the update button is pressed
  """
  return None

@app.route('/delete', methods=['POST'])
def delete():
    """
    Delete the record when the delete button is pressed
    """
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Listen on all network interfaces.