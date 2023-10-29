from flask import Flask, jsonify, request
from models import db, Lists, Items, SubItems, SubSubItems
from flask_cors import CORS


app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "http://localhost:3000",
            "methods": ["GET", "POST", "PUT", "DELETE"],
        }
    },
)  # noqa
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.secret_key = "test"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/api/lists", methods=["GET"])
def get_all_lists():
    lists = Lists.query.all()
    serialized_lists = [todo_list.to_dict() for todo_list in lists]
    return jsonify(serialized_lists)


@app.route("/api/lists", methods=["POST"])
def create_list():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_list = Lists(title=title)

    try:
        db.session.add(new_list)
        db.session.commit()
        return jsonify(new_list.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to create the list"}), 500
    finally:
        db.session.close()


# Endpoints for Items
@app.route("/api/lists/<int:list_id>/items", methods=["GET"])
def get_all_items(list_id):
    items = Items.query.filter_by(list_id=list_id).all()
    serialized_items = [item.to_dict() for item in items]
    return jsonify(serialized_items)


@app.route("/api/lists/<int:list_id>/items", methods=["POST"])
def create_item(list_id):
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_item = Items(title=title, list_id=list_id)

    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to create the item"}), 500
    finally:
        db.session.close()


@app.route("/api/lists/<int:list_id>/items/<int:item_id>", methods=["PUT"])  # noqa
def update_item_visibility(list_id, item_id):
    data = request.get_json()
    is_visible = data.get("is_visible")
    item = Items.query.filter_by(list_id=list_id, id=item_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    try:
        item.is_visible = is_visible
        db.session.commit()
        return jsonify(item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to update item visibility"}), 500
    finally:
        db.session.close()


@app.route("api/lists/<int:listId>/items/<int:itemId>", methods=["PUT"])
def update_item_done_status(listId, itemId):
    data = request.get_json()
    is_done = data.get("is_done")
    item_done = Items.query.filter_by(list_id=listId, id=itemId).first()
    if not item_done:
        return jsonify({"error": "Item not found"}), 404
    try:
        item_done.is_done = is_done
        db.session.commit()
        return jsonify(item_done.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to update item visibility"}), 500
    finally:
        db.session.close()


# Endpoints for SubItems
@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems", methods=["GET"]
)  # noqa
def get_all_subitems(list_id, item_id):
    subitems = SubItems.query.filter_by(list_id=list_id, item_id=item_id).all()
    serialized_subitems = [subitem.to_dict() for subitem in subitems]
    return jsonify(serialized_subitems)


@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems", methods=["POST"]
)  # noqa
def create_subitem(list_id, item_id):
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_subitem = SubItems(title=title, list_id=list_id, item_id=item_id)

    try:
        db.session.add(new_subitem)
        db.session.commit()
        return jsonify(new_subitem.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to create the subitem"}), 500
    finally:
        db.session.close()


# Endpoints for SubSubItems
@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems/<int:sub_item_id>/subsubitems",  # noqa
    methods=["GET"],
)
def get_all_subsubitems(list_id, item_id, sub_item_id):
    subsubitems = SubSubItems.query.filter_by(
        list_id=list_id, item_id=item_id, sub_item_id=sub_item_id
    ).all()
    serialized_subsubitems = [
        subsubitem.to_dict() for subsubitem in subsubitems
    ]  # noqa
    return jsonify(serialized_subsubitems)


@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems/<int:sub_item_id>/subsubitems",  # noqa
    methods=["POST"],  # noqa
)
def create_subsubitem(list_id, item_id, sub_item_id):
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_subsubitem = SubSubItems(
        title=title, list_id=list_id, item_id=item_id, sub_item_id=sub_item_id
    )

    try:
        db.session.add(new_subsubitem)
        db.session.commit()
        return jsonify(new_subsubitem.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to create the subsubitem"}), 500
    finally:
        db.session.close()


@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems/<int:sub_item_id>",
    methods=["PUT"],
)  # noqa
def update_sub_item_visibility(list_id, item_id, sub_item_id):
    data = request.get_json()
    is_sub_visible = data.get("is_sub_visible")
    subitem = SubItems.query.filter_by(
        list_id=list_id, item_id=item_id, id=sub_item_id
    ).first()
    if not subitem:
        return jsonify({"error": "Subitem not found"}), 404

    try:
        subitem.is_sub_visible = is_sub_visible
        db.session.commit()
        return jsonify(subitem.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to update item visibility"}), 500
    finally:
        db.session.close()


@app.route("/api/lists/<int:list_id>", methods=["DELETE"])
def delete_list(list_id):
    todo_list = Lists.query.get(list_id)
    if not todo_list:
        return jsonify({"error": "List not found"}), 404

    try:
        db.session.delete(todo_list)
        db.session.commit()
        return jsonify({"message": "List deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to delete the list"}), 500
    finally:
        db.session.close()


@app.route("/api/lists/<int:list_id>/items/<int:item_id>", methods=["DELETE"])
def delete_item(list_id, item_id):
    item = Items.query.filter_by(list_id=list_id, id=item_id).first()
    print(item)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to delete the item"}), 500
    finally:
        db.session.close()


@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems/<int:sub_item_id>",
    methods=["DELETE"],
)
def delete_subitem(list_id, item_id, sub_item_id):
    subitem = SubItems.query.filter_by(
        list_id=list_id, item_id=item_id, id=sub_item_id
    ).first()
    if not subitem:
        return jsonify({"error": "Subitem not found"}), 404

    try:
        db.session.delete(subitem)
        db.session.commit()
        return jsonify({"message": "Subitem deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to delete the subitem"}), 500
    finally:
        db.session.close()


@app.route(
    "/api/lists/<int:list_id>/items/<int:item_id>/subitems/<int:sub_item_id>/subsubitems/<int:sub_sub_item_id>",  # noqa
    methods=["DELETE"],
)
def delete_subsubitem(list_id, item_id, sub_item_id, sub_sub_item_id):
    subsubitem = SubSubItems.query.filter_by(
        list_id=list_id,
        item_id=item_id,
        sub_item_id=sub_item_id,
        id=sub_sub_item_id,  # noqa
    ).first()
    if not subsubitem:
        return jsonify({"error": "SubSubItem not found"}), 404

    try:
        db.session.delete(subsubitem)
        db.session.commit()
        return jsonify({"message": "SubSubItem deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to delete the subsubitem"}), 500
    finally:
        db.session.close()


if __name__ == "__main__":
    app.run(debug=True)