from app import create_app
import os

# with app.app_context():
#     db.create_all()

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
