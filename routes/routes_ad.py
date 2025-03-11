# from flask import render_template, request, jsonify
# from app import app, db
# from models import Admin

# @app.route("/")
# def index():
#     admin = Admin.query.all()
#     return render_template("index.html", users=admin)

# @app.route("/create", methods=["POST"])
# def create_user():
#     name = request.form["name"]
#     email = request.form["email"]
#     admin = Admin(name=name, email=email)
#     db.session.add(admin)
#     db.session.commit()
#     return jsonify({"message": "User created successfully"})

# @app.route("/delete/<int:user_id>")
# def delete_user(user_id):
#     admin = Admin.query.get(user_id)
#     if admin:
#         db.session.delete(admin)
#         db.session.commit()
#         return jsonify({"message": "User deleted successfully"})
#     return jsonify({"message": "User not found"})

# if __name__ == "__main__":
#     app.run(debug=True)