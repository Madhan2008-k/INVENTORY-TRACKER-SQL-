```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Management System</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
        }

        h1, h2 {
            text-align: center;
            color: #174b35;
        }

        input, button {
            width: 100%;
            padding: 10px;
            margin: 7px 0;
            box-sizing: border-box;
        }

        button {
            background: #198754;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #12683f;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #198754;
            color: white;
        }

        .low-stock {
            color: red;
            font-weight: bold;
        }

        .edit {
            background: #e69500;
        }

        .delete {
            background: #dc3545;
        }

        .actions button {
            margin: 3px 0;
        }

        .summary {
            background: #e8f5e9;
            padding: 12px;
            margin: 10px 0;
            border-radius: 5px;
        }

        @media (max-width: 650px) {
            .container {
                padding: 10px;
            }

            table {
                font-size: 12px;
            }

            th, td {
                padding: 5px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <h1>Inventory Management System</h1>

    <h2>Add / Update Product</h2>

    <form id="productForm">

        <input type="hidden" id="productId">

        <input type="text" id="name"
               placeholder="Product Name" required>

        <input type="text" id="category"
               placeholder="Category" required>

        <input type="number" id="quantity"
               placeholder="Quantity" min="0" step="1" required>

        <input type="number" id="price"
               placeholder="Price" min="0" step="0.01" required>

        <button type="submit" id="saveButton">Add Product</button>

    </form>

    <h2>Inventory Summary</h2>

    <div class="summary">
        <p>Total Products: <span id="totalProducts">0</span></p>
        <p>Total Stock Quantity: <span id="totalQuantity">0</span></p>
        <p>Low-Stock Products: <span id="lowStockCount">0</span></p>
        <p>Total Inventory Value: ₹<span id="totalValue">0.00</span></p>
    </div>

    <h2>Product List</h2>

    <input type="text" id="search"
           placeholder="Search by product name or category">

    <label>
        <input type="checkbox" id="lowStockFilter"
               style="width:auto;">
        Show only low-stock products (quantity below 5)
    </label>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Product</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Value</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody id="productList"></tbody>
    </table>

</div>

<script>
    let products =
        JSON.parse(localStorage.getItem("products")) || [];

    let nextId = products.reduce(
        (max, product) => Math.max(max, product.id), 0
    ) + 1;

    const form = document.getElementById("productForm");

    function saveProducts() {
        localStorage.setItem("products", JSON.stringify(products));
    }

    function displayProducts() {
        const list = document.getElementById("productList");

        list.replaceChildren();

        const searchText =
            document.getElementById("search").value.toLowerCase();

        const lowStockOnly =
            document.getElementById("lowStockFilter").checked;

        const filteredProducts = products.filter(product => {
            const matchesSearch =
                product.name.toLowerCase().includes(searchText) ||
                product.category.toLowerCase().includes(searchText);

            const matchesStock =
                !lowStockOnly || product.quantity < 5;

            return matchesSearch && matchesStock;
        });

        filteredProducts.forEach(product => {
            const row = document.createElement("tr");

            const values = [
                product.id,
                product.name,
                product.category,
                product.quantity,
                "₹" + product.price.toFixed(2),
                "₹" + (product.quantity * product.price).toFixed(2)
            ];

            values.forEach((value, index) => {
                const cell = document.createElement("td");
                cell.textContent = value;

                if (index === 3 && product.quantity < 5) {
                    cell.className = "low-stock";
                }

                row.appendChild(cell);
            });

            const actions = document.createElement("td");
            actions.className = "actions";

            const editButton = document.createElement("button");
            editButton.textContent = "Edit";
            editButton.className = "edit";
            editButton.addEventListener("click", () => editProduct(product.id));

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.className = "delete";
            deleteButton.addEventListener("click", () => deleteProduct(product.id));

            actions.append(editButton, deleteButton);
            row.appendChild(actions);

            list.appendChild(row);
        });

        document.getElementById("totalProducts").textContent =
            products.length;

        document.getElementById("totalQuantity").textContent =
            products.reduce((sum, product) => sum + product.quantity, 0);

        document.getElementById("lowStockCount").textContent =
            products.filter(product => product.quantity < 5).length;

        const totalValue = products.reduce(
            (sum, product) => sum + product.quantity * product.price, 0
        );

        document.getElementById("totalValue").textContent =
            totalValue.toFixed(2);
    }

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const category = document.getElementById("category").value.trim();
        const quantity = Number(document.getElementById("quantity").value);
        const price = Number(document.getElementById("price").value);
        const productId = document.getElementById("productId").value;

        if (!name || !category ||
            document.getElementById("quantity").value === "" ||
            document.getElementById("price").value === "" ||
            !Number.isInteger(quantity) || quantity < 0 ||
            !Number.isFinite(price) || price < 0) {
            alert("Please enter valid product details.");
            return;
        }

        if (productId) {
            const index = products.findIndex(
                product => product.id === Number(productId)
            );

            if (index !== -1) {
                products[index] = {
                    id: Number(productId),
                    name,
                    category,
                    quantity,
                    price
                };
            }
        } else {
            products.push({
                id: nextId++,
                name,
                category,
                quantity,
                price
            });
        }

        saveProducts();

        form.reset();
        document.getElementById("productId").value = "";
        document.getElementById("saveButton").textContent = "Add Product";

        displayProducts();
    });

    function editProduct(id) {
        const product = products.find(product => product.id === id);

        if (!product) return;

        document.getElementById("productId").value = product.id;
        document.getElementById("name").value = product.name;
        document.getElementById("category").value = product.category;
        document.getElementById("quantity").value = product.quantity;
        document.getElementById("price").value = product.price;

        document.getElementById("saveButton").textContent = "Update Product";

        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function deleteProduct(id) {
        if (confirm("Are you sure you want to delete this product?")) {
            products = products.filter(product => product.id !== id);

            saveProducts();
            displayProducts();
        }
    }

    document.getElementById("search")
        .addEventListener("input", displayProducts);

    document.getElementById("lowStockFilter")
        .addEventListener("change", displayProducts);

    displayProducts();
</script>

</body>
</html>
```
