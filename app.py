from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data storage
books = [
    {
        "id": 1,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Fiction",
        "year": 1960
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "genre": "Dystopian Fiction",
        "year": 1949
    },
    {
        "id": 3,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": "Romance",
        "year": 1813
    }
]

# Counter for auto-generating IDs
next_id = 4

def find_book_by_id(book_id):
    """Helper function to find a book by ID"""
    return next((book for book in books if book["id"] == book_id), None)

def validate_book_data(data, is_update=False):
    """Helper function to validate book data"""
    required_fields = ["title", "author", "genre", "year"]
    errors = []
    
    if not is_update:
        # For POST requests, all fields are required
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"'{field}' is required")
    
    # Validate year if provided
    if "year" in data and data["year"]:
        try:
            year = int(data["year"])
            if year < 0 or year > datetime.now().year + 10:
                errors.append("'year' must be a valid year")
        except (ValueError, TypeError):
            errors.append("'year' must be a valid integer")
    
    return errors

@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint that provides basic information about the API"""
    return jsonify({
        "message": "Welcome to the Library API",
        "description": "A  CRUD system for managing books",
        "endpoints": {
            "GET /": "This welcome message",
            "GET /health": "Health check",
            "GET /api/books": "Get all books",
            "GET /api/books/<id>": "Get book by ID",
            "POST /api/books": "Create new book",
            "PUT /api/books/<id>": "Update book by ID",
            "DELETE /api/books/<id>": "Delete book by ID",
            "GET /api/info": "API information"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "OK"})

@app.route('/api/books', methods=['GET'])
def get_all_books():
    """Get all the books from the library"""
    return jsonify({
        "books": books,
        "count": len(books)
    })

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """Get a single book by ID"""
    book = find_book_by_id(book_id)
    if book is None:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404
    
    return jsonify(book)

@app.route('/api/books', methods=['POST'])
def create_book():
    """Create a new book"""
    global next_id
    
    if not request.json:
        return jsonify({"error": "Request must contain JSON data"}), 400
    
    # Validate input data
    errors = validate_book_data(request.json)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    # Create new book
    new_book = {
        "id": next_id,
        "title": request.json["title"],
        "author": request.json["author"],
        "genre": request.json["genre"],
        "year": int(request.json["year"])
    }
    
    books.append(new_book)
    next_id += 1
    
    return jsonify({
        "message": "Book created successfully",
        "book": new_book
    }), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update an existing book"""
    if not request.json:
        return jsonify({"error": "Request must contain JSON data"}), 400
    
    book = find_book_by_id(book_id)
    if book is None:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404
    
    # Validate input data
    errors = validate_book_data(request.json, is_update=True)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
    
    # Update book fields
    if "title" in request.json:
        book["title"] = request.json["title"]
    if "author" in request.json:
        book["author"] = request.json["author"]
    if "genre" in request.json:
        book["genre"] = request.json["genre"]
    if "year" in request.json:
        book["year"] = int(request.json["year"])
    
    return jsonify({
        "message": "Book updated successfully",
        "book": book
    })

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book by ID"""
    book = find_book_by_id(book_id)
    if book is None:
        return jsonify({"error": f"Book with ID {book_id} not found"}), 404
    
    books.remove(book)
    
    return jsonify({
        "message": f"Book with ID {book_id} deleted successfully",
        "deleted_book": book
    })

@app.route('/api/info', methods=['GET'])
def get_api_info():
    """Get API metadata information"""
    return jsonify({
        "project_name": "Library API",
        "version": "1.0.0",
        "author": "Assistant",
        "description": "A Flask REST API for managing books with CRUD operations",
        "total_books": len(books),
        "endpoints_count": 8,
        "created": "2024"
    })

@app.route("/ui")
def ui():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Library Manager</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 p-4">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-3xl font-bold text-center mb-6">📚 Library Book Manager</h1>

            <div class="bg-white shadow-md rounded p-4 mb-6">
                <h2 class="text-xl font-semibold mb-2">Add New Book</h2>
                <form id="bookForm" class="grid grid-cols-2 gap-4">
                    <input type="text" placeholder="Title" id="title" class="border p-2 rounded" required>
                    <input type="text" placeholder="Author" id="author" class="border p-2 rounded" required>
                    <input type="text" placeholder="Genre" id="genre" class="border p-2 rounded" required>
                    <input type="number" placeholder="Year" id="year" class="border p-2 rounded" required>
                    <button type="submit" class="col-span-2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                        Add Book
                    </button>
                </form>
            </div>

            <div class="bg-white shadow-md rounded p-4">
                <h2 class="text-xl font-semibold mb-4">All Books</h2>
                <div id="bookList" class="space-y-4"></div>
            </div>
        </div>

        <script>
            const API_BASE = "/api/books";
            const bookList = document.getElementById("bookList");
            const bookForm = document.getElementById("bookForm");

            async function fetchBooks() {
                const res = await fetch(API_BASE);
                const data = await res.json();
                bookList.innerHTML = "";
                data.books.forEach(book => {
                    const div = document.createElement("div");
                    div.className = "border p-4 rounded bg-gray-50";
                    div.innerHTML = `
                        <h3 class="font-bold">${book.title}</h3>
                        <p>Author: ${book.author}</p>
                        <p>Genre: ${book.genre}</p>
                        <p>Year: ${book.year}</p>
                        <button onclick="deleteBook(${book.id})" class="mt-2 bg-red-500 text-white px-2 py-1 rounded">Delete</button>
                    `;
                    bookList.appendChild(div);
                });
            }

            async function deleteBook(id) {
                await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
                fetchBooks();
            }

            bookForm.addEventListener("submit", async (e) => {
                e.preventDefault();
                const title = document.getElementById("title").value;
                const author = document.getElementById("author").value;
                const genre = document.getElementById("genre").value;
                const year = document.getElementById("year").value;

                const res = await fetch(API_BASE, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title, author, genre, year })
                });

                if (res.ok) {
                    bookForm.reset();
                    fetchBooks();
                } else {
                    const data = await res.json();
                    alert("Error: " + (data?.error || "Unknown"));
                }
            });

            fetchBooks();
        </script>
    </body>
    </html>
    '''

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Library API...")
    print("Available endpoints:")
    print("- GET / (Welcome message)")
    print("- GET /health (Health check)")
    print("- GET /api/books (Get all books)")
    print("- GET /api/books/<id> (Get book by ID)")
    print("- POST /api/books (Create new book)")
    print("- PUT /api/books/<id> (Update book)")
    print("- DELETE /api/books/<id> (Delete book)")
    print("- GET /api/info (API information)")
    print("\nRunning on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
