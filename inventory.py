from flask import Flask, request, jsonify
import mysql.connector
import firebase_admin
from firebase_admin import db, credentials

app = Flask(__name__)

# 🔹 Connect to MySQL
try:
    mysql_db = mysql.connector.connect(
        host="localhost",
        user="root",  # Change if you have a different username
        password="drishu04",  # Change to your MySQL password
        database="inventory_system"
    )
    cursor = mysql_db.cursor(dictionary=True)
    print("✅ Connected to MySQL")
except mysql.connector.Error as err:
    print(f"❌ MySQL Connection Error: {err}")
    exit()

# 🔹 Connect to Firebase
try:
    cred = credentials.Certificate("firebase-adminsdk.json")  # Replace with your JSON file
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-firebase-database.firebaseio.com'
    })
    print("✅ Connected to Firebase")
except Exception as e:
    print(f"❌ Firebase Connection Error: {e}")
    exit()

# ------------------ ADMIN APIS ------------------

# 1️⃣ Get Full Inventory (Admin Only)
@app.route('/admin_inventory', methods=['GET'])
def admin_inventory():
    try:
        cursor.execute("SELECT * FROM products")
        inventory = cursor.fetchall()
        return jsonify(inventory)
    except Exception as e:
        return jsonify({"error": str(e)})

# 2️⃣ Add New Product
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.json
        cursor.execute("""
            INSERT INTO products (name, category, price, customization_options, stock, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data["name"], data["category"], data["price"], data["customization_options"], data["stock"], data["image_url"]))
        mysql_db.commit()
        return jsonify({"message": "Product added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# 3️⃣ Update Product Stock
@app.route('/update_stock', methods=['POST'])
def update_stock():
    try:
        data = request.json
        cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (data["stock"], data["product_id"]))
        mysql_db.commit()
        return jsonify({"message": "Stock updated!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# 4️⃣ Delete Product
@app.route('/delete_product', methods=['POST'])
def delete_product():
    try:
        data = request.json
        cursor.execute("DELETE FROM products WHERE id = %s", (data["product_id"],))
        mysql_db.commit()
        return jsonify({"message": "Product deleted!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# 5️⃣ Get All Orders (Admin)
@app.route('/admin_orders', methods=['GET'])
def admin_orders():
    try:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)})

# 6️⃣ Approve or Reject Order
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    try:
        data = request.json
        cursor.execute("UPDATE orders SET admin_status = %s WHERE id = %s", (data["status"], data["order_id"]))
        mysql_db.commit()
        return jsonify({"message": "Order status updated!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# ------------------ USER APIS ------------------

# 7️⃣ Place Custom Order (Save in Firebase)
@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        data = request.json
        ref = db.reference("/orders")
        order_id = ref.push(data).key  # Generate a unique order ID
        return jsonify({"message": "Order placed!", "order_id": order_id})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
