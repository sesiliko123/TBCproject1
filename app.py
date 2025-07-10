from ext import app

from routes import home, register, login, logout, product_detail, create_product, edit_product, delete_product

if __name__ == "__main__":
    app.run(debug=True)

