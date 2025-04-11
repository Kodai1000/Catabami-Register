#Business Logic
# 商品情報(class ProductsInformation)
# レシートデータ管理(class ReceiptData)
# 


class ProductsInformation:
    def __init__(self):
        self.products = []

    def add(self, name, price, category):
        self.products.append(
            {
                "name":name,
                "price":price,
                "category":category
            }
        )

class Receipt:
    def __init__(self):
        self.tables = []
        
    def add_table(self, name):
        self.tables.append({
            "name":name,
            "products_list":[]
        })
    
    def add_product_to_tab(self, table_id, product_id):
        bought = products_information.products[table_id]
        self.tables[table_id]["products_list"].append(
            {
                "name":bought["name"],
                "price":bought["price"],
                "quantity":1
            }
        )
    
    def plus_quantity(self, table_id, products_list_id):
        self.tables[table_id][products_list_id]["quantity"] += 1

    def minus_quantity(self, table_id, products_list_id):
        self.tables[table_id][products_list_id]["quantity"] -= 1

if __name__ == "__main__":
    products_information = ProductsInformation()
    receipt = Receipt()