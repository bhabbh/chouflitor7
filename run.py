import os

os.environ['GOOGLE_MAPS_API_KEY'] = 'AIzaSyB0eBlupelDc_Wg4CHohhYv5id9fqlw9lQ'


def setup_database():
    from app import app, db

    with app.app_context():
        db.create_all()


def reset_database():
    from app import app, db
    with app.app_context():
        db.drop_all()
        db.create_all()
    print("Database has been reset.")


def run_app():
    from app import app

    app.run(debug=True)


if __name__ == "__main__":

    print("Resetting database...")
    reset_database()

    print("Running the app...")
    run_app()
