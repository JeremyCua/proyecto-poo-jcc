import json
class JsonFile:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file)# dump:graba datos a un archivo json
      
    def read(self):
        try:
            with open(self.filename,'r') as file:
                data = json.load(file)# load:carga datos desde un archivo json
        except FileNotFoundError:
            data = []
        return data
     
    def find(self,atributo,buscado):
        try:
            with open(self.filename,'r') as file:
                datas = json.load(file)
                data = [item for item in datas if item[atributo] == buscado ]
        except FileNotFoundError:
            data = []
        return data
    
    def add_product(self, new_product):
        products = self.read()

        if products:
            new_product_id = max(product.get('id', 0) for product in products) + 1
        else:
            new_product_id = 1
            
        new_product = {'id' : new_product_id, ** new_product}
        products.append(new_product)
        self.save(products)
    
    def get_id_range(produtcs):
        ids = [produtc['id'] for produtc in produtcs]
        return f"[1 - {max(ids)}]"