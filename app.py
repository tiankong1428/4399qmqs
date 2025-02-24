from flask import Flask, jsonify, request

app = Flask(__name__)

# 模拟数据
books = [
    {
        'id': 1,
        'title': 'Python Crash Course',
        'author': 'Eric Matthes'
    },
    {
        'id': 2,
        'title': 'Clean Code',
        'author': 'Robert C. Martin'
    }
]

# 获取所有书籍
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# 根据 ID 获取单本书籍
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify(book)

# 添加一本新书
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    if not new_book or 'title' not in new_book or 'author' not in new_book:
        return jsonify({'message': 'Invalid book data'}), 400
    new_book['id'] = max(book['id'] for book in books) + 1
    books.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)