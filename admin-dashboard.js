document.addEventListener("DOMContentLoaded", () => {
    fetchProducts();
    document.getElementById("productForm").addEventListener("submit", addProduct);
    document.getElementById("image").addEventListener("change", previewImage);
});

// ✅ Fetch and display regular products
async function fetchProducts() {
    try {
        const response = await fetch("http://127.0.0.1:5003/get-products");
        const products = await response.json();
        const tableBody = document.getElementById("productList");
        tableBody.innerHTML = "";

        if (products.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align:center;">No products available</td></tr>`;
            return;
        }

        products.forEach(product => {
            const row = `<tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>$${product.price}</td>
                <td>${product.stock}</td>
                <td><img src="/static/images/${product.image}" width="50" alt="Product Image"></td>
                <td>
                    <button onclick="editProduct(${product.id})">✏️ Edit</button>
                    <button onclick="deleteProduct(${product.id})">🗑️ Delete</button>
                </td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error fetching products:", error);
        alert("Failed to fetch products.");
    }
}

// ✅ Function to add a new product
async function addProduct(event) {
    event.preventDefault(); // Prevent form from refreshing the page

    const name = document.getElementById("name").value.trim();
    const price = document.getElementById("price").value.trim();
    const stock = document.getElementById("stock").value.trim();
    const image = document.getElementById("image").files[0];

    if (!name || !price || !stock || !image) {
        alert("Please fill in all fields and upload an image!");
        return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("price", price);
    formData.append("stock", stock);
    formData.append("image", image);

    console.log("Form Data:", [...formData.entries()]); // ✅ Debugging

    try {
        const response = await fetch("http://127.0.0.1:5003/add-product", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("Server Response:", result); // ✅ Debugging

        if (response.ok) {
            alert("Product added successfully!");
            document.getElementById("productForm").reset(); // Reset form
            document.getElementById("imagePreview").classList.add("hidden"); // Hide preview
            fetchProducts(); // Refresh product list
        } else {
            alert("Error: " + result.error);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to add product.");
    }
}

// ✅ Preview image before uploading
function previewImage() {
    const file = document.getElementById("image").files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgPreview = document.getElementById("imagePreview");
            imgPreview.src = e.target.result;
            imgPreview.classList.remove("hidden");
        };
        reader.readAsDataURL(file);
    }
}

// ✅ Function to edit product
async function editProduct(productId) {
    let newName = prompt("Enter new name:");
    let newPrice = prompt("Enter new price:");
    let newStock = prompt("Enter new stock:");

    if (newName && newPrice && newStock) {
        const response = await fetch(`http://127.0.0.1:5003/edit-product/${productId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newName, price: newPrice, stock: newStock })
        });

        if (response.ok) {
            alert("Product updated successfully!");
            fetchProducts(); // Refresh product list
        } else {
            alert("Failed to update product.");
        }
    }
}

// ✅ Function to delete product
async function deleteProduct(productId) {
    if (confirm("Are you sure you want to delete this product?")) {
        const response = await fetch(`http://127.0.0.1:5003/delete-product/${productId}`, {
            method: "DELETE"
        });

        if (response.ok) {
            alert("Product deleted successfully!");
            fetchProducts(); // Refresh product list
        } else {
            alert("Failed to delete product.");
        }
    }
}
