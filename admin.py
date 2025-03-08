from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pymysql
import os
import uuid  # For unique image names

app = Flask(__name__)

# ✅ Enable CORS with all methods allowed
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}}, supports_credentials=True)

# ✅ MySQL Database Connection Function
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # Change if needed
        password="drishu04",  # Your MySQL password
        database="inventory_system",
        cursorclass=pymysql.cursors.DictCursor
    )

# ✅ Correct Image Upload Path
UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Route: Add Product
@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        image = request.files.get('image')

        if not name or not price or not stock:
            return jsonify({"error": "All fields are required!"}), 400

        # ✅ Save Image with Unique Name
        image_url = ""
        if image:
            ext = image.filename.rsplit('.', 1)[-1].lower()
            unique_filename = f"{uuid.uuid4()}.{ext}"
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            image.save(image_path)
            image_url = f"/static/images/{unique_filename}"

        # ✅ Insert into Database
        sql = "INSERT INTO products (name, price, stock, image_url) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, price, stock, image_url))
        conn.commit()

        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        cursor.close()
        conn.close()

# ✅ Route: Fetch All Products (Fixed Image URLs)
@app.route('/get-products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        # ✅ Ensure full image URLs for frontend
        for product in products:
            if product["image_url"]:
                product["image_url"] = f"http://127.0.0.1:5003{product['image_url']}"

        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ Route: Edit Product (Fixing 404 error)
@app.route('/edit-product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')

        if not name or not price or not stock:
            return jsonify({"error": "All fields are required!"}), 400

        # ✅ Update Product in Database
        sql = "UPDATE products SET name = %s, price = %s, stock = %s WHERE id = %s"
        cursor.execute(sql, (name, price, stock, product_id))
        conn.commit()

        return jsonify({"message": "Product updated successfully!"})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        cursor.close()
        conn.close()

# ✅ Route: Delete Product (Fixing 404 error)
@app.route('/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
        conn.commit()

        return jsonify({"message": "Product deleted successfully!"})
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    finally:
        cursor.close()
        conn.close()

# ✅ Start Flask Server
if __name__ == '__main__':
    app.run(port=5003, debug=True)
