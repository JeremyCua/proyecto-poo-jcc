from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
import math 
import colorama
from colorama import Back, Fore, Style

path, _ = os.path.split(os.path.abspath(__file__))
product_json = JsonFile(path+'/archivos/products.json')
clsJson = JsonFile(path+'/archivos/clients.json')

def validar_cedula(ced):
    suma = 0
    mul = 1
    index = len(ced)
    while index > 0:
        index -= 1
        num = int(ced[index]) * mul
        suma += num - (num > 9) * 9
        mul = 1 << index % 2

    return suma % 10 == 0 and suma > 0

# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        while True:
            borrarPantalla()
            user_ID = input("Ingrese el numero de cedula (solo numeros): ")
            
            if not user_ID.isdigit():
                print("La cedula debe contener solo numeros. Vuelva a intentarlo.")
                continuar = input("¿Desea continuar ingresando clientes? (s/n): ")
                if continuar.lower() != "s":
                    break
                continue
            
            clients = clsJson.read()
            if any(client['dni'] == user_ID for client in clients):
                print("La cedula ya existe en la base de datos. Vuelva a intentarlo.")
                continuar = input("¿Desea continuar ingresando clientes? (s/n): ")
                if continuar.lower() != "s":
                    break
                continue
            
            if not validar_cedula(user_ID):
                print("Cedula invalida. Vuelva a intentarlo.")
                continuar = input("¿Desea continuar ingresando clientes? (s/n): ")
                if continuar.lower() != "s":
                    break
                continue
            else:
                print("Cedula Valida.")
                name = input("Ingrese el nombre: ")
                last_name = input("Ingrese el apellido: ")
                user_value = float(input("Ingrese el valor del usuario: "))
                new_client = {
                    'dni': user_ID,
                    'nombre': name,
                    'apellido': last_name,
                    'valor': user_value
                }
                clients.append(new_client)
                clsJson.save(clients)
                continuar = input("¿Desea continuar ingresando clientes? (s/n): ")
                if continuar.lower() != "s":
                    break

    def update(self):
        while True:
            borrarPantalla()
            clients = clsJson.read()
            user_ID = input("Ingrese la cédula del cliente: ")

            client_found = False
            for client in clients:
                if 'dni' in client and client['dni'] == user_ID:
                    client_found = True
                    print("Cliente encontrado")
                    print("Nombre:", client['nombre'])
                    print("Apellido:", client['apellido'])
                    print("Valor:", client['valor'])

                    opcion = input("¿Qué desea actualizar? (nombre/apellido/valor): ")
                    new_value = input("Ingrese el nuevo valor: ")
                    if opcion == "valor":
                        new_value = float(new_value)
                    client[opcion] = new_value  # Actualizar el cliente

                    clsJson.save(clients)
                    print('Guardado')
                    break  # Salir del bucle for si se encuentra el cliente

            if not client_found:
                print("Cliente no encontrado.")

            continuar = input("¿Desea continuar? (s/n): ")
            if continuar.lower() != "s":
                break
            time.sleep(3)

    def delete(self):
        while True:
            borrarPantalla()
            clients = clsJson.read()
            user_ID = input("Ingrese la cédula del cliente: ")

            client_found = False
            for client in clients:
                if 'dni' in client and client['dni'] == user_ID:
                    client_found = True
                    print("Cliente encontrado")
                    print("Nombre:", client['nombre'])
                    print("Apellido:", client['apellido'])
                    print("Valor:", client['valor'])

                    opcion = input("¿Esta seguro de eliminar este usuario? s/n): ")
                    if opcion.lower() == 's':
                        clients.remove(client)
                        print('Usuario eliminado...')
                        clsJson.save(clients)
                        break
                    else:
                        print('Error')
            if not client_found:
                print("Cliente no encontrado.")

            continuar = input("¿Desea continuar eliminando clientes? (s/n): ")
            if continuar.lower() != 's':
                break
        
        print("Regresando al menu Clientes...")
        time.sleep(2)

    def consult(self):
        while True:
            borrarPantalla()
            clients = clsJson.read()
            user_ID = input(Fore.CYAN + "Ingrese la cedula que desea consultar: " + Fore.WHITE)

            client_found = False
            for client in clients:
                if 'dni' in client and client['dni'] == user_ID:
                    client_found = True
                    print("Cliente encontrado.")
                    print("Nombre:", client['nombre'])
                    print("Apellido:", client['apellido'])
                    print("Valor:", client['valor'])
                    break
            
            if not client_found:
                print('El cliente no existe.')

            continuar = input("¿Desea continuar consultando clientes? (s/n): ")
            if continuar.lower() != 's':
                break

        print("Regresando al menu Clientes...")
        time.sleep(2)         

class CrudProducts(ICrud):
    def create(self):
        continue_while = True 
        while continue_while:
            product_name = input("Ingrese el nombre del producto: ")
            product_name = product_name.capitalize()
            product_price = float(input("Ingrese el precio del producto: "))
            product_stock = int(input(f"Ingrese el stock del producto {product_name}: "))
                        
            new_product = {
                'descripcion': product_name,
                'precio': product_price,
                'stock': product_stock
            }
            product_json.add_product(new_product)
                    
            opcion = input("Desea seguir agregando productos? (s/n): ")
            if opcion != "s":
                continue_while = False

    def update(self):
        products = product_json.read()
        product_id = int(input("Ingrese el nombre del producto: "))
        
        for product in products: 
            if 'id' in product and product['id'] == product_id:
                product_found = True
                print("Producto Encontrado...")
                print("ID:", product['id'])
                print("Descripcion:", product['descripcion'])
                print("Precio:", product['precio'])
                print("Stock:", product['stock'])

                opcion = input("¿Qué desea actualizar? (Descripcion/Precio/Stock): ")
                new_value = input("Ingrese el nuevo valor: ")
                if opcion.lower() == "precio":
                    new_value = float(new_value)
                elif opcion.lower() == "stock":
                    new_value = int(new_value)

                product[opcion] = new_value

                product_json.save(products)
                print('Guardado')
                break

        if not product_found:
            print("Error, no encontrado.")
            return
        
        continuar = input("¿Desea continuar? (s/n): ")
        if continuar.lower() != "s":
            return
        time.sleep(3)
                        

    def delete(self):
        products = product_json.read()
        max_id = max(product.get('id', 0) for product in products)
        print(f"ID de los productos encontrado: 1 al{max_id}")

        product_id = int(input("Ingrese el ID del producto: "))

        for product in products: 
            if 'id' in product and product['id'] == product_id:
                product_found = True
                print("Producto Encontrado...")
                print("ID", product['id'])
                print("Descripcion", product['descripcion'])
                print("Precio:", product['precio'])
                print("Stock:", product['stock'])

                opcion = input("¿Está seguro de eliminar el producto (s/n)?: ")
                if opcion.lower() == 's':
                    products.remove(product)
                    print('Producto eliminado')
                else:
                    print('Error')
                product_json.save(products)
                break

        if not product_found:
            print("Error.")
        time.sleep(3)

    def consult(self):
        products = product_json.read()
        product_id = int(input("Ingrese la ID que desea consultar: "))

        product_found = False
        for product in products:
            if 'id' in product and product['id'] == product_id:
                product_found = True
                print("Producto encontrado...")
                print("ID:", product['id'])
                print("Descripcion:", product['descripcion'])
                print("Precio:", product['precio'])
                print("Stock:", product['stock'])
                break

        if not product_found:
            print('El producto no existe.')
        time.sleep(3)

        print("Regresando al menu...")
        time.sleep(2) 

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("Venta Grabada satisfactoriamente"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("Venta Cancelada"+reset_color)    
        time.sleep(2)    
    
    def update(self):
        json_file = JsonFile(path + "/archivos/invoices.json")
        invoices = json_file.read()

        print("Facturas Disponibles: ")
        for invoice in invoices:
            print(f"Factura#{invoice['factura']} - Cliente: {invoice['cliente']} - Fecha: {invoice['Fecha']}")

        invoice_id = input("Ingrese el numero de la factura que desea modificar: ")

        if not invoice_id.isdigit():
            print("Ingrese un numero de factura valido...")
            return
        invoice_id = int(invoice_id)

        invoice_index = None
        for index, invoice in enumerate(invoices):
            if invoice['factura'] == invoice_id:
                invoice_index = index 
                break
        if invoice_index is None:
            print(f"Error... La factura {invoice_id} no existe.")
            return
        
        print("Detalle de la factura seleccionada...")
        print(invoices[invoice_index])

        items = invoices[invoice_index]['detalle']
        print("Modifique los datos segun sea necesario...")
        while True:
            print('Productos en la factura.')
            for i, item in enumerate(items, start=1):
                print(f"{i}. Producto: {item['poducto']} - Cantidad {item['cantidad']}")
            print("Menu de Opciones...")
            print("1. Agregar Producto.")
            print("2. Modificar Cantidad.")
            print("3. Salir.")
            option = input("Seleccione una opcion... ")

            if option == "1":
                new_product = input("Ingrese el nombre del nuevo producto: ")
                new_quantity = int(input("Ingrese la cantidad del nuevo producto: "))
                items.append({"poducto": new_product, "cantidad": new_quantity})
                print("Producto agregado exitosamente.")

            elif option == "2":
                # Modificar la cantidad de un producto existente en la factura
                product_index = int(input("Ingrese el número de producto que desea modificar: ")) - 1
                if 0 <= product_index < len(items):
                    new_quantity = int(input("Ingrese la nueva cantidad: "))
                    items[product_index]['cantidad'] = new_quantity
                    print("Cantidad modificada exitosamente.")
                else:
                    print("Número de producto no válido.")

            elif option == "3":
                break

            else:
                print("Opción no válida.")

        # Actualizar los detalles de línea en la factura
        invoices[invoice_index]['detalle'] = items

        # Guardar la factura actualizada en el archivo JSON
        json_file.save(invoices)   

    def delete(self):
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        print("Facturas disponibles...")
        for invoice in invoices:
            print(f"Factura #{invoice['factura']} - Cliente: {invoice['cliente']} - Fecha: {invoice['Fecha']}")
        
        invoice_id = input("Ingrese el ID de la factura: ")

        if not invoice_id.isdigit():
            print("Error, ingrese un numero valido de la factura...")
            return
        invoice_id = int(invoice_id)

        invoice_exists = False
        for invoice in invoices:
            if invoice['factura'] == invoice_id:
                invoice_exists = True
                break
        if not invoice_exists:
            print(f"Error... La Factura {invoice_id} , no existe. ")
            return
        print('Factura eliminada correctamente...')
        time.sleep(3)
        invoices = [invoice for invoice in invoices if invoice['factura'] != invoice_id]
        for index, invoice in enumerate(invoices, start=1):
            invoice['factura'] = index
        json_file.save(invoices)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    


#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            clients = CrudClients() 
            menu_clients = Menu(Fore.MAGENTA + "Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                clients.create()
            elif opc1 == "2":
                clients.update()
            elif opc1 == "3":
                clients.delete()
            elif opc1 == "4":
                clients.consult()
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()  
            product = CrudProducts()  
            menu_products = Menu(Fore.LIGHTBLUE_EX + "Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                product.create()
            elif opc2 == "2":
                product.update()
            elif opc2 == "3":
                product.delete()
            elif opc2 == "4":
                product.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()

            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)

            elif opc3 == "3":
                sales.update()

            elif opc3 == "4":
                sales.delete()

    print("Regresando al menu Principal...")
    time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

