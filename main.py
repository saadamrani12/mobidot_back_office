from app import create_app
# from werkzeug.serving import run_simple

app = create_app()

if __name__ == '__main__':
    app.run(port=5001, debug=False)
