from ast import literal_eval

'''
Módulo de gestión la lista de la compra

Un producto es una lista ['nombre', precio, 'categoria', ('nota1', 'nota2', ...), prioridad, True/False]

En lecciones posteriores veremos cómo transformar esto en una estructura más elegante.
'''

productos = []

def crear_producto(nombre, precio, categoria, notas, prioridad):
    return [nombre, precio, categoria, notas, prioridad, False]

def insertar(nombre, precio, categoria, notas=(), prioridad=3):
  '''Añade un producto nuevo a la lista con los parámetros dados'''
  if isinstance(notas, str) :
    notas = literal_eval(notas)
  productos.append(crear_producto(nombre, float(precio), categoria, notas, int(prioridad)))

def borrar(indice):
  '''Borra de la lista el producto que se encuentra en la posición indicada'''
  indice = int(indice)
  del productos[indice]

def actualizar_precio(indice, precio):
  '''Actualiza el precio del producto con el índice dado'''
  indice = int(indice)
  productos[indice][1] = precio

def cambiar_estado(indice):
  '''Cambia el estado del producto con el índice dado entre comprado o no'''
  indice = int(indice)
  productos[indice][-1] = not productos[indice][-1]

def listar_productos():
  '''Devuelve la lista de los productos'''
  return productos

def mostrar_productos(comprados=True, usos=(), categorias=[]):
  '''
  Muestra por pantalla todos los productos con su información. Si un producto ya ha sido comprado, se marca con una x al comienzo.
  La prioridad se indicará mediante el uso de asteriscos (*), es decir, un artículo con prioridad 5 se representará mediante cinco asteriscos (*****).
  Si comprados es False, no se muestran los productos ya comprados.
  Usos es una tupla o lista con notas o aclaraciones. Si está vacía, se muestran
  todos los productos. Si contiene alguna nota, sólo se muestran los productos
  que tengan todas las notas proporcionadas.
  Categorias es una lista con las categorías que se quieren obtener. Si está vacía, se muestran
  todos los productos. Si contiene alguna categoría, solo se muestran los productos cuya categoría
  esté contenida en la lista.
  Ejemplo en que sólo un producto ha sido comprado:
  >>> mostrar_productos()
  [x] Alimentación - Arroz integral - *** - 0.72 € - #risotto #arroz a la cubana
  [ ] Alimentación - Huevos - * - 1.20 € - #arroz a la cubana #tortilla 
  [ ] Cosméticos - Desmaquillante - ***** - 4.50 € - #fiesta #teatro

  >>> mostrar_productos(usos=('arroz a la cubana'))
  [x] Alimentación - Arroz integral - *** - 0.72 € - #risotto #arroz a la cubana
  [ ] Alimentación - Huevos - * - 1.20 € - #arroz a la cubana #tortilla
  '''
  #print(productos)
  for ix, producto in enumerate(productos):

    nombre, precio, categoria, notas, prioridad, comprado = producto

    # si se recibe que no se deben mostrar los artículos ya comprados (comprados==False), y este producto
    # ya se ha comprado, pasamos al siguiente sin imprimirlo
    if (not comprados) and comprado:
      continue
    
    # si la lista de categorías recibidas contiene alguna (no está vacía), y la categoría del producto
    # no está en la lista de categorías recibidas, pasamos al siguiente sin imprimirlo
    if categorias and categoria not in categorias:
      continue
    
    # si la tupla de usos contiene alguno (no está vacía) y no todos los usos recibidos están entre
    # los usos del producto, pasamos al siguiente sin imprimirlo
    if usos and not all(tag in notas for tag in usos):
      continue
    
    hashtags = " ".join("#"+nota for nota in notas)
    box = '[ ]'
    priority = '*' * prioridad
    if comprado:
      box = '[x]'
    texto = f'{ix}: {box} {categoria} - {nombre} - {priority} - {precio} €  - {hashtags}'
    print(texto)

def ordenar():
    '''
    Se ordena la lista de productos, poniendo aquellos con mayor prioridad al principio.
    Los productos ya comprados se colocal al final.
    '''
     # Traverse through 1 to len(arr)
    for i in range(1, len(productos)):
 
        producto = productos[i]

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        
        while j >= 0 and producto[-1] > productos[j][-1] or producto[-2] > productos[j][-2]:
          productos[j + 1] = productos[j]
          j -= 1
          if j < 0:
            break
        productos[j + 1] = producto

MENU = {
    "mostrar": mostrar_productos,
    "insertar": insertar,
    "borrar": borrar,
    "ordenar": ordenar,
    "comprado": cambiar_estado,
    "actualizar": actualizar_precio,
}

def menu():
    '''
    Menú interactivo para modificar la lista de la compra.
    Acciones:

    -  mostrar
    -  insertar <nombre>; <precio>; <categoria>; <notas en formato tupla separadas por comas>; <prioridad>
    -  borrar <indice>
    -  precio <numero>; <precio>
    -  comprado <numero>
    -  ayuda
    -  salir


    Por ejemplo:

    #-> mostrar
    #-> insertar Garbanzos; 0.68; Alimentación; ('cocido', 'hummus'); 3
    #-> insertar Hierbabuena; 1.5; Alimentación; ('cocktails',);  1
    #-> mostrar
    [ ] Alimentación - Garbanzos - *** - 0.68 € - #cocido #hummus
    [ ] Alimentación - Hierbabuena - * - 1.5 € - #cocktails
    #-> comprado 0
    #-> mostrar
    [x] Alimentación - Garbanzos - *** - 0.68 € - #cocido #hummus
    [ ] Alimentación - Hierbabuena - * - 1.5 € - #cocktails

    '''
    print('Menú interactivo de tareas')
    print()
    while True:
        tokens = input('-> ').split(' ', 1)
        if len(tokens) < 1:
            continue
        comando = tokens[0]
        args = []
        if len(tokens) > 1:
            args =  [x.strip() for x in tokens[1].split(';')]
        
        if comando in MENU:
            v = MENU[comando](*args)
            if v:
                print(v)
        elif comando == 'ayuda':
            print('Opciones disponibles:')
            for comando, func in MENU.items():
                print(f'\t{comando}: {func.__doc__.strip()}')
        elif comando == 'salir':
            return
        elif comando.startswith('salir'):
            return
        else:
          print('Opciones disponibles:')
          for comando, func in MENU.items():
            print(f'\t{comando}: {func.__doc__.strip()}')


def prueba_manual():
    print('Insertando 3 productos')
    insertar('Desmaquillante', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
    insertar('Desmaquillante 2', 4.5, 'Cosméticos', ('fiesta', 'teatro'), 5)
    insertar('Garbanzos', 0.68, 'Alimentación', ('cocido', 'hummus'), 3)
    insertar('Hierbabuena', 1.5, 'Alimentación', ('cocktails', 'postres'), 1)

    seccion('Lista de la compra sin ordenar ni formatear')

    print(productos)

    seccion('Lista de la compra sin ordenar ni formatear (con cambio)')
    print('Cambiando un producto a comprado')
    cambiar_estado(0)
    print(productos)


    seccion('Lista de la compra sin ordenar')
    mostrar_productos()

    seccion('Lista de la compra filtrada')
    mostrar_productos(usos=('cocido',))

    seccion('Lista de la compra ordenada')
    ordenar()
    mostrar_productos()


def seccion(texto):
    print()
    print('-'*10, texto, '-'*40)
    print()


if __name__ == "__main__":
    #prueba_manual()
    menu()