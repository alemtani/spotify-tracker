from dotenv import load_dotenv
from flask_app import create_app

# First load environment variables
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run()