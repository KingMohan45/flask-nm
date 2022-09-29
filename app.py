from flask import Flask 
# __name__ means the name of the current python module

app = Flask(__name__)


@app.route("/")    
def hello():   
    return "Hello World!"

if __name__ == "__main__":
    """
        When you run your Python script, Python assigns the name “__main__” to the script when executed.
        If we import another script, the if statement will prevent other scripts from running
    """     
    app.run()