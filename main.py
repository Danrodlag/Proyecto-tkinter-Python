# En este archivo de python solo debería estar la interfaz gráfica, y las comprobaciones
# El codigo de la base de datos estará en el archivo db, incluida la clase constructora de sqlalchemy
import tkinter
from tkinter import ttk
from tkinter import *
import db
from db import Producto


class Productos:

    def __init__(self, root):

        self.ventana = root
        self.ventana.title("App de gestor de Productos")
        self.ventana.resizable(1, 1)  # Si se puede cambiar el tamaño
        self.ventana.wm_iconbitmap("recursos/M6_P2_icon.ico")

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo producto", font=("Calibri", 16, "bold"))
        frame.grid(row=0, columnspan=3, column=0, pady=20)  # Posición del frame principal

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)
        # Entry Nombre
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry Precio
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=2, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=3, column=0)
        # Entry Categoria
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.grid(row=3, column=1)

        # CheckButton para stock
        s = ttk.Style()
        s.configure('my.TCheckbutton', font=("Calibri", 14, "bold"))
        self.stock = tkinter.IntVar()
        self.check_stock = ttk.Checkbutton(frame, text='En stock', variable=self.stock,
                                           onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.check_stock.grid(row=4, column=0)

        # Botón de Añadir Producto
        s = ttk.Style()
        s.configure('my.TButton', font=("Calibri", 14, "bold"))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto",
                                        command=self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=3, sticky=W + E)

        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=5, column=0, columnspan=3, sticky=W + E)

        # Tabla Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(frame, height=15, columns=("c1", "c2", "c3", "c4"), style="mystyle.Treeview")
        self.tabla.grid(row=6, column=0, columnspan=3)
        self.tabla.heading("#0", text="Nombre", anchor=CENTER)
        self.tabla.heading("#1", text="Precio", anchor=CENTER)
        self.tabla.heading("#2", text="Categoria", anchor=CENTER)
        self.tabla.heading("#3", text="Stock", anchor=CENTER)

        # Botones de eliminar y editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        boton_eliminar = ttk.Button(text="ELIMINAR", style='my.TButton', command=self.del_producto)
        boton_eliminar.grid(row=7, column=0, sticky=W + E)
        boton_editar = ttk.Button(text="EDITAR", style='my.TButton', command=self.edit_producto)
        boton_editar.grid(row=7, column=1, sticky=W + E)

        self.get_productos()

    def stock_check(self, objeto):
        if objeto.stock == 0:
            return "No"
        elif objeto.stock == 1:
            return "Si"
        else:
            return "ERROR"

    def get_productos(self):

        # Borramos todos los registros
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        registros = db.session.query(Producto).all()
        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila.nombre, values=[fila.precio, fila.categoria, self.stock_check(fila)])

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection()[0])['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection()[0])['text']
        old_precio = self.tabla.item(self.tabla.selection()[0])['values'][0]  # El precio se encuentra dentro de lista
        old_categoria = self.tabla.item(self.tabla.selection()[0])['values'][1]

        self.ventana_editar = Toplevel()  # Crear una ventan por delante de la principal
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.resizable(True, True)
        self.ventana_editar.wm_iconbitmap('recursos/M6_P2_icon.ico')

        # Ahora creamos el frame
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente producto", font=("Calibri", 16, "bold"))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label del nombre antiguo, enseñando lo que ya estaba puesto
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # Y ahora el input/entry donde leera el nombre antiguo

        self.input_nombre_antiguo = Entry(frame_ep,
                                          textvariable=StringVar(self.ventana_editar, value=nombre), state="readonly",
                                          font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (ahora si podremos modificarlo)
        self.input_nombre_nuevo = Entry(frame_ep,
                                        textvariable=StringVar(self.ventana_editar, value=nombre),
                                        font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # El ratón aparecerá aquí por defecto

        # Ahora lo mismo pero con el precio
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13))
        self.etiqueta_precio_anituguo.grid(row=4, column=0)

        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep,
                                          textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state='readonly', font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep,
                                        textvariable=StringVar(self.ventana_editar, value=old_precio),
                                        font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label antigua categoria
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13))
        self.etiqueta_categoria_antigua.grid(row=2, column=2)

        # Y ahora el input/entry donde leera la categoria antigua
        self.input_categoria_antigua = Entry(frame_ep,
                                             textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                             state="readonly", font=('Calibri', 13))
        self.input_categoria_antigua.grid(row=2, column=3)

        # Label Categoria nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nueva.grid(row=3, column=2)

        # Entry Categoria nueva
        self.input_categoria_nueva = Entry(frame_ep,
                                           textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                           font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=3, column=3)

        # CheckButton para stock_nuevo
        s = ttk.Style()
        s.configure('my.TCheckbutton', font=("Calibri", 14, "bold"))
        self.input_stock_nuevo = tkinter.IntVar()
        self.check_stock = ttk.Checkbutton(frame_ep, text='En stock', variable=self.input_stock_nuevo,
                                           onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.check_stock.grid(row=4, column=2)

        self.mensaje['text'] = 'Editando el producto {}...'.format(nombre)

        # Boton Actualizar precio
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                           style='my.TButton',
                                           command=lambda:
                                           self.actualizar_productos(self.input_nombre_antiguo.get(),
                                                                     self.input_nombre_nuevo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.input_categoria_nueva.get(),
                                                                     self.input_stock_nuevo.get()))
        self.boton_actualizar.grid(row=6, columnspan=4, sticky=W + E)

    def add_producto(self):
        if self.validacion_precio() and self.validacion_nombre():
            producto = db.Producto(self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            # debug print(self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            print("Datos guardados")
            self.mensaje['text'] = 'Producto {} añadido con éxito'.format(
                self.nombre.get())  # Label ubicado entre el boton y la tabla
            self.nombre.delete(0, END)  # Borrar el campo nombre del formulario
            self.precio.delete(0, END)
            self.categoria.delete(0, END)

            db.session.add(producto)
            db.session.commit()
            db.session.close()

        elif self.validacion_precio() and self.validacion_nombre() == False:

            print("El nombre es obligatorio")

            self.mensaje["text"] = "El nombre es obligatorio"

        elif self.validacion_precio() == False and self.validacion_nombre():

            print("El precio es obligatorio")

            self.mensaje["text"] = "El precio es obligatorio"

        else:

            print("El nombre y el precio son obligatorios")

            self.mensaje["text"] = "El nombre y el precio son obligatorios"

        self.get_productos()

    def del_producto(self):
        # Debug
        # print(self.tabla.item(self.tabla.selection()[0]))
        try:
            self.tabla.item(self.tabla.selection()[0])['text']
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection()[0])['text']  # Esto devuelve el nombre directamente
        self.mensaje['text'] = '{} Ha sido eliminado'.format(nombre)

        db.session.query(Producto).filter_by(nombre=nombre).delete()
        self.get_productos()
        db.session.commit()
        db.session.close()

    def actualizar_productos(self, antiguo_nombre, nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock):

        # Primero buscamos cual es el elemento a cambiar, por eso necesitamos antiguo_nombre
        antiguo = db.session.query(Producto).filter_by(nombre=antiguo_nombre).first()
        antiguo.nombre = nuevo_nombre
        antiguo.precio = nuevo_precio
        antiguo.categoria = nueva_categoria
        antiguo.stock = nuevo_stock
        self.mensaje['text'] = 'Producto actualizado'
        self.get_productos()
        db.session.commit()
        db.session.close()
        self.ventana_editar.destroy()


if __name__ == "__main__":
    root = Tk()  # Ventana principal
    app = Productos(root)
    root.mainloop()  # No cerrar hasta que el usuario cierre
    db.Base.metadata.create_all(db.engine)
