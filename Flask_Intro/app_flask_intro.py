from flask import Flask

app = Flask(__name__)   # This is for referencing this file (Auto referencing ?)

@app.route('/')     # index route, so when we browse to the URL we don't immediatelly just 404.
                    # Flask set-up routes with app route decorator. We are going to pass the URL string of our route
def index():        # Define the function for the previous route
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)     # = True, so if we have any errors they will pop-up and we can see

