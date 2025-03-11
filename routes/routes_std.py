# from flask import render_template, request, jsonify
# from app import app, db
# from models import User

# @app.route("/")
# def index():
#     users = User.query.all()
#     return render_template("index.html", users=users)

# @app.route("/create", methods=["POST"])
# def create_user():
#     name = request.form["name"]
#     email = request.form["email"]
#     user = User(name=name, email=email)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"message": "User created successfully"})

# @app.route("/delete/<int:user_id>")
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({"message": "User deleted successfully"})
#     return jsonify({"message": "User not found"})

# if __name__ == "__main__":
#     app.run(debug=True)