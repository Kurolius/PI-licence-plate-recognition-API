import uvicorn
from route import app
from db import *
from security.create_data import init_data
create_db()
init_data()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8085)