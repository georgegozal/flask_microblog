from app import create_app

# with app.app_context():
#     db.create_all()

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
