from app import create_app

app = create_app()

@app.route('/')
def homepage():
    return 'Welcome to HBnB'

if __name__ == '__main__':
    app.run(debug=True)
