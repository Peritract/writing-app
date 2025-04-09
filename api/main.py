"""A simple API to track writing."""

from flask import Flask, request

from database_functions import load_all_entries, is_valid_entry, save_new_entry, get_db_connection

api = Flask(__name__)

@api.get("/")
def index():
    return {
        "message": "Welcome to the Writing App API."
    }

@api.route("/entry", methods=["GET", "POST"])
def get_or_create_entries():

    if request.method == "GET":
        entries = load_all_entries(conn)
        args = request.args

        if "author" in args:
            author = args["author"]
            entries = [e for e in entries
                       if e["author"].lower() == author.lower()]

        return entries
    else:
        new_entry = request.json
        if is_valid_entry(new_entry):
            try:
                created_entry = save_new_entry(conn, new_entry)
                return created_entry, 201
            except ValueError:
                return {"error": True, "message": "No such author."}, 400 
        else:
             return {"error": True, "message": "Invalid entry."}, 400   
        

if __name__ == "__main__":
    with get_db_connection() as conn:
        api.run(port=8080, debug=True)
