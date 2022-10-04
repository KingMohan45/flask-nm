

#local imports importing after app config 
from core import *
from routes import *
from models import db


if __name__ == '__main__':
    """
    This is the main entry point of the application
    """
    #get port from argument
    port = os.getenv("PORT", default=5000)
    db.create_all()
    app.run(port=port) # 0.0.0.0 can be set as host to run app on all interfaces