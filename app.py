# app = create_app()
# with app.app_context(): # without this , postgresql doesn`t works
#     db.create_all()

from microblog import app


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)