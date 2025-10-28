import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from PIL import Image, ImageTk
import threading
from utils import rutas
from separados import Separados as SeparadosFrame


class Inventario(tk.Frame):
    db_name = 'database.db'

    def __init__(self, padre, username=None):
        super().__init__(padre)
        self.username = username
        self.widgets()
        self.cargar_sucursales()
        self.articulos_combobox()
        self.cargar_articulos()
        self.timer_articulos = None
        self.iniciar_actualizacion_periodica()

    def iniciar_actualizacion_periodica(self):
        self.cargar_articulos()
        self.after(10000, self.iniciar_actualizacion_periodica)  # Actualiza cada 10 segundos

    def widgets(self):
        #================================== Tabla de Artículos ==================================#
        canvas_articulos = tk.LabelFrame(self, text="Artículos", bg="#c9dbe1", font="Arial 16 bold")
        canvas_articulos.place(x=300, y=10, width=780, height=580)

        # Treeview como tabla
        self.tree = ttk.Treeview(canvas_articulos, columns=("Articulo", "Precio", "Costo", "Codigo", "Stock", "Stock Mínimo", "Sucursal"), show="headings")
        self.tree.heading("Articulo", text="Artículo")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Codigo", text="Código")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Stock Mínimo", text="Stock mínimo")
        self.tree.heading("Sucursal", text="Sucursal")

        self.tree.column("Articulo", width=150)
        self.tree.column("Precio", width=80)
        self.tree.column("Costo", width=80)
        self.tree.column("Codigo", width=120)
        self.tree.column("Stock", width=60)
        self.tree.column("Stock Mínimo", width=80)
        self.tree.column("Sucursal", width=120)

        self.tree.pack(fill="both", expand=True)

        #============================== Buscar ==============================#
        lblframe_buscar = LabelFrame(self, text="Buscar", bg="#c9dbe1", font="Arial 14 bold")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="Arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos)

        #=========================== Selección =============================#
        lblframe_seleccion = LabelFrame(self, text="Selección", bg="#c9dbe1", font="Arial 14 bold")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_seleccion, text="Artículo:", font="Arial 14", bg="#c9dbe1")
        self.label1.place(x=5, y=5)

        self.label2 = tk.Label(lblframe_seleccion, text="Precio:", font="Arial 14", bg="#c9dbe1")
        self.label2.place(x=5, y=40)

        self.label3 = tk.Label(lblframe_seleccion, text="Costo:", font="Arial 14", bg="#c9dbe1")
        self.label3.place(x=5, y=70)

        self.label4 = tk.Label(lblframe_seleccion, text="Stock:", font="Arial 14", bg="#c9dbe1")
        self.label4.place(x=5, y=100)

        self.label5 = tk.Label(lblframe_seleccion, text="Sucursal:", font="Arial 14", bg="#c9dbe1")
        self.label5.place(x=5, y=130)

        #=========================== Botones ==============================#
        lblframe_botones = LabelFrame(self, text="Opciones", bg="#c9dbe1", font="Arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)

        # Cargar imágenes para los botones
        self.imagen_agregar = Image.open(rutas("imagenes/agregarUsuario.png")).resize((30, 30))
        self.tk_imagen_agregar = ImageTk.PhotoImage(self.imagen_agregar)

        self.imagen_actualizar = Image.open(rutas("imagenes/actualizarUsuario.png")).resize((30, 30))
        self.tk_imagen_actualizar = ImageTk.PhotoImage(self.imagen_actualizar)

        self.imagen_eliminar = Image.open(rutas("imagenes/eliminarUsuario.png")).resize((30, 30))
        self.tk_imagen_eliminar = ImageTk.PhotoImage(self.imagen_eliminar)

        self.imagen_separados = Image.open(rutas("imagenes/separado.png")).resize((30, 30))
        self.tk_imagen_separados = ImageTk.PhotoImage(self.imagen_separados)

        # Botón Agregar
        btn_agregar = tk.Button(lblframe_botones, text="Agregar", compound=tk.LEFT, padx=10, font="Arial 12 bold",
                                bg="white", relief="raised", command=self.agregar_articulos)
        btn_agregar.config(image=self.tk_imagen_agregar)
        btn_agregar.image = self.tk_imagen_agregar
        btn_agregar.place(x=20, y=5, width=200, height=40)

        # Botón Editar
        btn_editar = tk.Button(lblframe_botones, text="Editar", compound=tk.LEFT, padx=10, font="Arial 12 bold",
                               bg="white", relief="raised", command=self.editar_articulos)
        btn_editar.config(image=self.tk_imagen_actualizar)
        btn_editar.image = self.tk_imagen_actualizar
        btn_editar.place(x=20, y = 55, width=200, height=40)

        # Botón Eliminar
        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", compound=tk.LEFT, padx=10, font="Arial 12 bold",
                                 bg="white", relief="raised", command=self.eliminar_articulos)
        btn_eliminar.config(image=self.tk_imagen_eliminar)
        btn_eliminar.image = self.tk_imagen_eliminar
        btn_eliminar.place(x=20, y=105, width=200, height=40)

        # Botón Separados
        btn_separados = tk.Button(lblframe_botones, text="Separados", compound=tk.LEFT, padx=10, font="Arial 12 bold",
                                  bg="white", relief="raised", command=self.abrir_separados)
        btn_separados.config(image=self.tk_imagen_separados)
        btn_separados.image = self.tk_imagen_separados
        btn_separados.place(x=20, y=155, width=200, height=40)

    # Botón Actualizar desde Excel
        btn_importar = tk.Button(lblframe_botones, text="Importar Excel", padx=10, font="Arial 12 bold",
                    bg="white", relief="raised", command=self.actualizar_desde_excel)
        btn_importar.place(x=20, y=205, width=200, height=40)

    def abrir_separados(self):
        ventana = tk.Toplevel(self)
        ventana.title("Módulo de Separados")
        ventana.geometry("1100x700+120+20")
        ventana.config(bg="#c9dbe1")
        # Pasa el username actual al frame de Separados
        frame = SeparadosFrame(ventana, username=self.username)
        frame.pack(fill="both", expand=True)
        ventana.focus_set()
        ventana.grab_set()

    def cargar_sucursales(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM sucursales")
            self.sucursales = [sucursal[0] for sucursal in cursor.fetchall()]
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar sucursales:", e)
            self.sucursales = []

    def articulos_combobox(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT DISTINCT articulo FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos

    def agregar_articulos(self):
        top = tk.Toplevel(self)
        top.title("Agregar artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#c9dbe1")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()        # Entradas
        campos = [("Código", 20), ("Artículo", 60), ("Precio", 100), ("Costo", 140), ("Stock", 180), ("Stock mínimo", 220)]
        entradas = {}

        for nombre, y in campos:
            tk.Label(top, text=f"{nombre}: ", font="Arial 12 bold", bg="#c9dbe1").place(x=20, y=y, height=25, width=110)
            entrada = ttk.Entry(top, font="Arial 12 bold")
            entrada.place(x=140, y=y, width=250, height=25)
            entradas[nombre.lower().replace(' ', '_')] = entrada
        
        # Combobox para sucursal
        tk.Label(top, text="Sucursal: ", font="Arial 12 bold", bg="#c9dbe1").place(x=20, y=260, height=25, width=110)
        combo_sucursal = ttk.Combobox(top, font="Arial 12 bold", state="readonly", values=self.sucursales)
        combo_sucursal.place(x=140, y=260, width=250, height=25)
        if self.sucursales:
            combo_sucursal.set(self.sucursales[0])
        entradas["sucursal"] = combo_sucursal

        def guardar():
            datos = {k: v.get() for k, v in entradas.items()}

            if not all(datos.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            try:
                datos["precio"] = float(datos["precio"])
                datos["costo"] = float(datos["costo"])
                datos["stock"] = int(datos["stock"])
                datos["stock_minimo"] = int(datos["stock_minimo"])
            except ValueError:
                messagebox.showerror("Error", "Precio, costo, stock y stock mínimo deben ser números.")
                return

            try:
                self.cur.execute("""
                    INSERT INTO articulos (articulo, precio, costo, codigo, stock, stock_minimo, sucursal)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (datos["articulo"], datos["precio"], datos["costo"],
                     datos["codigo"], datos["stock"], datos["stock_minimo"], datos["sucursal"])
                )
                self.con.commit()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente.")
                top.destroy()
                self.cargar_articulos()
            except sqlite3.Error as e:
                print("Error al agregar artículo:", e)
                messagebox.showerror("Error", "Error al agregar artículo.")

        tk.Button(top, text="Guardar", font="Arial 12 bold", command=guardar).place(x=50, y=320, width=150, height=40)
        tk.Button(top, text="Cancelar", font="Arial 12 bold", command=top.destroy).place(x=300, y=320, width=150, height=40)

    def cargar_articulos(self, filtro=None, categoria=None):
        self.after(0, self._cargar_articulos, filtro, categoria)
        # Se elimina el popup de alerta para evitar repeticiones en cada refresco.
        # El estado de stock bajo se indicará visualmente en la tabla con filas en rojo.

    def _cargar_articulos(self, filtro=None, categoria=None):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT articulo, precio, costo, codigo, stock, stock_minimo, sucursal FROM articulos"
        params = []

        if filtro:
            query += " WHERE articulo LIKE ? OR codigo LIKE ?"
            params.extend((f'%{filtro}%', f'%{filtro}%'))

        self.cur.execute(query, params)
        articulos = self.cur.fetchall()

        for articulo, precio, costo, codigo, stock, stock_minimo, sucursal in articulos:
            # Resaltar en rojo si el stock está por debajo del mínimo
            tags = ()
            try:
                if int(stock) < int(stock_minimo):
                    tags = ("bajo_minimo",)
            except Exception:
                pass
            self.tree.insert("", "end", values=(articulo, f"${precio:.2f}", f"${costo:.2f}", codigo, stock, stock_minimo, sucursal), tags=tags)
    # Configurar el estilo para resaltar (fondo y texto en rojo)
        self.tree.tag_configure("bajo_minimo", background="#ffcccc", foreground="red")

    def on_combobox_select(self, event):
        self.actualizar_label()

    def actualizar_label(self, event=None):
        valor = self.comboboxbuscar.get().strip()
        try:
            self.cur.execute("""
                SELECT articulo, precio, costo, stock, stock_minimo, sucursal 
                FROM articulos 
                WHERE articulo = ? OR codigo = ?
            """, (valor, valor))
            resultado = self.cur.fetchone()

            if resultado:
                articulo, precio, costo, stock, stock_minimo, sucursal = resultado
                self.label1.config(text=f"Articulo: {articulo}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Sucursal: {sucursal}")
                # Mostrar stock mínimo
                if hasattr(self, 'label_stock_minimo'):
                    self.label_stock_minimo.config(text=f"Stock Mínimo: {stock_minimo}")
                else:
                    self.label_stock_minimo = tk.Label(self.label4.master, text=f"Stock Mínimo: {stock_minimo}", font="Arial 14", bg="#c9dbe1")
                    self.label_stock_minimo.place(x=5, y=160)
                # Alerta si stock bajo
                if int(stock) < int(stock_minimo):
                    self.label4.config(fg="red")
                    self.label_stock_minimo.config(fg="red")
                else:
                    self.label4.config(fg="black")
                    self.label_stock_minimo.config(fg="black")
            else:
                for label in [self.label1, self.label2, self.label3, self.label4, self.label5]:
                    label.config(text="No encontrado")
                if hasattr(self, 'label_stock_minimo'):
                    self.label_stock_minimo.config(text="")
        except sqlite3.Error as e:
            print("Error al buscar artículo:", e)
            messagebox.showerror("Error", "Error al buscar artículo")

    def filtrar_articulos(self, event):
        if self.timer_articulos:
            self.after_cancel(self.timer_articulos)

        self.timer_articulos = self.after(300, self._filter_articulos)

    def _filter_articulos(self):
        typed = self.comboboxbuscar.get().strip()

        if not typed:
            self.comboboxbuscar['values'] = self.articulos
            self.cargar_articulos()
            return

        try:
            self.cur.execute("""
            SELECT DISTINCT articulo FROM articulos
            WHERE articulo LIKE ? OR codigo LIKE ?
            """, (f'%{typed}%', f'%{typed}%'))

            resultados = self.cur.fetchall()
            data = [row[0] for row in resultados]

            if data:
                self.comboboxbuscar['values'] = data
            else:
                self.comboboxbuscar['values'] = ['No se encontraron resultados']

            self.comboboxbuscar.event_generate('<Down>')
            self.cargar_articulos(filtro=typed)

        except sqlite3.Error as e:
            print("Error en filtro:", e)
            messagebox.showerror("Error", "No se pudo filtrar los artículos")
            
    def editar_articulos(self):
        selected_item = self.comboboxbuscar.get()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un artículo")
            return 

        self.cur.execute("SELECT articulo,precio,costo,codigo,stock,stock_minimo,sucursal FROM articulos WHERE articulo = ?", (selected_item,))
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error", "No se encontró el artículo")
            return
        
        top = tk.Toplevel(self)
        top.title("Editar Articulo")
        top.geometry("700x450+200+50")
        top.config(bg="#c9dbe1")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        (articulo, precio, costo, codigo , stock, stock_minimo, sucursal) = resultado
        
        tk.Label(top,text="Articulo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 20, width=80,height=25)
        entry_articulo = ttk.Entry(top,font="arial 12 bold")
        entry_articulo.place(x=120,y=20 ,width=250,height=30)
        entry_articulo.insert(0,articulo)
        
        tk.Label(top,text="Precio: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 60, width=80,height=25)
        entry_precio = ttk.Entry(top,font="arial 12 bold")
        entry_precio.place(x=120,y=60 ,width=250,height=30)
        entry_precio.insert(0,precio)
        
        tk.Label(top,text="Costo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 100, width=80,height=25)
        entry_costo = ttk.Entry(top,font="arial 12 bold")
        entry_costo.place(x=120,y=100 ,width=250,height=30)
        entry_costo.insert(0,costo)
        
        tk.Label(top,text="Codigo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 140, width=80,height=25)
        entry_codigo = ttk.Entry(top,font="arial 12 bold")
        entry_codigo.place(x=120,y=140 ,width=250,height=30)
        entry_codigo.insert(0,codigo)
        
        tk.Label(top,text="Stock: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 180, width=80,height=25)
        entry_stock = ttk.Entry(top,font="arial 12 bold")
        entry_stock.place(x=120,y=180 ,width=250,height=30)
        entry_stock.insert(0,stock)
        
        tk.Label(top,text="Stock Mínimo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 220, width=110,height=25)
        entry_stock_minimo = ttk.Entry(top,font="arial 12 bold")
        entry_stock_minimo.place(x=140,y=220 ,width=250,height=30)
        entry_stock_minimo.insert(0,stock_minimo)
        
        tk.Label(top, text="Sucursal: ", font="arial 12 bold", bg="#c9dbe1").place(x=20, y=260, width=80, height=25)
        combo_sucursal = ttk.Combobox(top, font="arial 12 bold", state="readonly", values=self.sucursales)
        combo_sucursal.place(x=120, y=260, width=250, height=30)
        if sucursal in self.sucursales:
            combo_sucursal.set(sucursal)
        elif self.sucursales:
            combo_sucursal.set(self.sucursales[0])
        entry_sucursal = combo_sucursal
        
        def guardar():
            nuevo_articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            codigo = entry_codigo.get()
            stock = entry_stock.get()
            stock_minimo = entry_stock_minimo.get()
            sucursal = entry_sucursal.get()
            
            if not nuevo_articulo or not precio or not costo or not codigo or not stock or not stock_minimo or not sucursal:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return 
            
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
                stock_minimo = int(stock_minimo)
            except ValueError:
                messagebox.showerror("Error", "Los campos precio, costo, stock y stock mínimo deben ser numericos")
                return
            
            self.cur.execute(
            "UPDATE articulos SET articulo = ?, precio = ?, costo = ?, codigo = ?, stock = ?, stock_minimo = ?, sucursal = ? WHERE articulo = ? OR codigo = ?",
            (nuevo_articulo, precio, costo, codigo, stock, stock_minimo, sucursal, selected_item, selected_item))
            self.con.commit()
            self.articulos_combobox()
            self.after(0,lambda: self.cargar_articulos(filtro=nuevo_articulo))
            top.destroy()
            messagebox.showinfo("Exito","Articulo editado exitosamente")
        btn_guardar  = tk.Button(top, text="Guardar", command=guardar,font="arial 12 bold")
        btn_guardar.place(x=260,y=350,width=150, height=40)
    
    def eliminar_articulos(self):
        valor = self.comboboxbuscar.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Por favor escribe el nombre o código del artículo que deseas eliminar.")
            return

        try:
            # Buscar el artículo por nombre o código
            self.cur.execute("SELECT articulo, codigo FROM articulos WHERE articulo = ? OR codigo = ?", (valor, valor))
            resultado = self.cur.fetchone()

            if not resultado:
                messagebox.showerror("Error", "No se encontró ningún artículo con ese nombre o código.")
                return

            articulo, codigo = resultado

        # Confirmación del usuario
            respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el artículo '{articulo}'?")
            if not respuesta:
                return

        # Eliminar de la base de datos
            self.cur.execute("DELETE FROM articulos WHERE articulo = ? AND codigo = ?", (articulo, codigo))
            self.con.commit()

        # Mostrar éxito
            messagebox.showinfo("Éxito", "Artículo eliminado correctamente")

        # Limpiar etiquetas
            for label in [self.label1, self.label2, self.label3, self.label4, self.label5]:
                label.config(text="")

        # Actualizar Combobox y tabla
            self.articulos_combobox()
            self.comboboxbuscar['values'] = self.articulos
            self.comboboxbuscar.set("")
            self.cargar_articulos()

        except Exception as e:
            print("Error al eliminar:", e)
            messagebox.showerror("Error", "No se pudo eliminar el artículo")

    # ===================== Importar y actualizar desde Excel/CSV ===================== #
    def actualizar_desde_excel(self):
        """
        Permite seleccionar un archivo Excel (.xlsx/.xlsm) o CSV exportado y actualizar
        los artículos existentes por 'codigo' (preferido) o por 'articulo'.
        Columnas soportadas (no todas obligatorias):
          - codigo / código
          - articulo / artículo
          - precio
          - costo
          - stock
          - stock_minimo / stock mínimo
          - sucursal
        Reglas:
          - Se actualiza solo si existe en la base. No se insertan nuevos.
          - Si hay ambos (codigo y articulo), se prioriza 'codigo'.
          - Números aceptan formatos con coma decimal.
        """
        try:
            file_path = filedialog.askopenfilename(
                title="Selecciona el archivo de Excel/CSV",
                filetypes=[
                    ("Excel (*.xlsx;*.xlsm)", "*.xlsx;*.xlsm"),
                    ("CSV (*.csv)", "*.csv"),
                    ("Todos", "*.*")
                ]
            )
            if not file_path:
                return

            ext = os.path.splitext(file_path)[1].lower()

            # Helpers locales
            import unicodedata, csv
            def _norm(s: str) -> str:
                if s is None:
                    return ""
                if not isinstance(s, str):
                    s = str(s)
                s = s.strip()
                s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
                return s.lower()

            def _to_float(val):
                if val is None or val == "":
                    return None
                if isinstance(val, (int, float)):
                    return float(val)
                s = str(val).strip()
                # Manejo de coma decimal y miles
                if s.count(',') == 1 and s.count('.') > 1:
                    s = s.replace('.', '')
                s = s.replace(' ', '')
                # Si hay coma y no hay punto, tratar coma como decimal
                if ',' in s and '.' not in s:
                    s = s.replace(',', '.')
                # Si hay ambos, asumir formato 1.234,56
                elif s.count('.') > 1 and ',' in s:
                    s = s.replace('.', '')
                    s = s.replace(',', '.')
                try:
                    return float(s)
                except Exception:
                    return None

            def _to_int(val):
                f = _to_float(val)
                return int(round(f)) if f is not None else None

            required_any = {"codigo", "articulo"}
            supported = {
                "codigo": "codigo",
                "articulo": "articulo",
                "precio": "precio",
                "costo": "costo",
                "stock": "stock",
                "stock_minimo": "stock_minimo",
                "stock minimo": "stock_minimo",
                "sucursal": "sucursal"
            }

            rows = []
            headers_map = {}

            if ext in (".xlsx", ".xlsm"):
                try:
                    import openpyxl
                except ImportError:
                    messagebox.showerror(
                        "Falta dependencia",
                        "Para leer archivos Excel (.xlsx) se requiere el paquete 'openpyxl'.\n"
                        "Instálalo o exporta a CSV e inténtalo de nuevo."
                    )
                    return
                wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
                ws = wb.active
                first = True
                for row in ws.iter_rows(values_only=True):
                    if first:
                        # construir headers
                        for idx, h in enumerate(row or []):
                            key = _norm(h)
                            if key in supported:
                                headers_map[idx] = supported[key]
                        first = False
                        continue
                    if not headers_map:
                        break
                    rd = {}
                    for idx, val in enumerate(row or []):
                        if idx in headers_map:
                            rd[headers_map[idx]] = val
                    if any(v not in (None, "") for v in rd.values()):
                        rows.append(rd)
            else:
                # CSV
                with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
                    sample = f.read(2048)
                    f.seek(0)
                    try:
                        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
                    except Exception:
                        dialect = csv.excel
                    reader = csv.reader(f, dialect)
                    try:
                        headers = next(reader)
                    except StopIteration:
                        messagebox.showerror("Archivo vacío", "El archivo seleccionado no tiene datos.")
                        return
                    norm_headers = [_norm(h) for h in headers]
                    for idx, nh in enumerate(norm_headers):
                        if nh in supported:
                            headers_map[idx] = supported[nh]
                    for row in reader:
                        rd = {}
                        for idx, val in enumerate(row):
                            if idx in headers_map:
                                rd[headers_map[idx]] = val
                        if any(v not in (None, "") for v in rd.values()):
                            rows.append(rd)

            if not rows:
                messagebox.showwarning("Sin datos", "No se encontraron filas válidas en el archivo.")
                return

            # Validar que haya al menos una columna de identificación
            has_id = any(any(k in r for k in required_any) for r in rows)
            if not has_id:
                messagebox.showerror(
                    "Faltan columnas",
                    "El archivo debe contener al menos una columna de identificación: 'codigo' o 'articulo'."
                )
                return

            # Procesar: actualizar si existe; insertar si no existe
            actualizados = 0
            insertados = 0
            no_encontrados = 0
            errores = 0

            for r in rows:
                # No normalizar el código: respetar exactamente como en BD
                codigo = r.get("codigo")
                if codigo is None:
                    codigo = ""
                else:
                    codigo = str(codigo).strip()

                # Artículo: permitir diferencias de mayúsculas/minúsculas
                articulo = r.get("articulo")
                if articulo is None:
                    articulo = ""
                else:
                    articulo = str(articulo).strip()

                # Construir SET dinámico
                precio = _to_float(r.get("precio"))
                costo = _to_float(r.get("costo"))
                stock = _to_int(r.get("stock"))
                stock_minimo = _to_int(r.get("stock_minimo"))
                sucursal = r.get("sucursal")
                sucursal = sucursal.strip() if isinstance(sucursal, str) else None

                set_parts = []
                params = []
                if precio is not None:
                    set_parts.append("precio = ?")
                    params.append(precio)
                if costo is not None:
                    set_parts.append("costo = ?")
                    params.append(costo)
                if stock is not None:
                    set_parts.append("stock = ?")
                    params.append(stock)
                if stock_minimo is not None:
                    set_parts.append("stock_minimo = ?")
                    params.append(stock_minimo)
                if sucursal:
                    set_parts.append("sucursal = ?")
                    params.append(sucursal)

                if not set_parts:
                    # Nada que actualizar en esta fila
                    continue

                try:
                    where_clause = None
                    where_val = None
                    if codigo:
                        where_clause = "codigo = ?"
                        where_val = codigo
                    elif articulo:
                        # Comparación case-insensitive para artículo
                        where_clause = "LOWER(articulo) = LOWER(?)"
                        where_val = articulo
                    else:
                        # Sin identificador no se puede procesar
                        no_encontrados += 1
                        continue

                    # Verificar existencia
                    self.cur.execute(f"SELECT COUNT(*) FROM articulos WHERE {where_clause}", (where_val,))
                    existe = self.cur.fetchone()[0]

                    if existe:
                        # Actualizar
                        sql = f"UPDATE articulos SET {', '.join(set_parts)} WHERE {where_clause}"
                        self.cur.execute(sql, (*params, where_val))
                        actualizados += self.cur.rowcount if hasattr(self.cur, 'rowcount') else 1
                    else:
                        # Insertar nuevo artículo
                        nuevo_articulo = articulo if articulo else (codigo or "")
                        nuevo_codigo = codigo
                        nuevo_precio = precio if precio is not None else 0.0
                        nuevo_costo = costo if costo is not None else 0.0
                        nuevo_stock = stock if stock is not None else 0
                        nuevo_stock_minimo = stock_minimo if stock_minimo is not None else 0
                        nuevo_sucursal = sucursal if sucursal else (self.sucursales[0] if getattr(self, 'sucursales', []) else "")

                        # Requiere al menos nombre de artículo para insertar
                        if not nuevo_articulo:
                            no_encontrados += 1
                            continue

                        self.cur.execute(
                            """
                            INSERT INTO articulos (articulo, precio, costo, codigo, stock, stock_minimo, sucursal)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (nuevo_articulo, nuevo_precio, nuevo_costo, nuevo_codigo, nuevo_stock, nuevo_stock_minimo, nuevo_sucursal)
                        )
                        insertados += 1
                except Exception as e:
                    print("Error procesando fila:", e)
                    errores += 1

            self.con.commit()
            self.articulos_combobox()
            self.cargar_articulos()

            messagebox.showinfo(
                "Actualización completada",
                f"Artículos insertados: {insertados}\n"
                f"Artículos actualizados: {actualizados}\n"
                f"No procesados (sin identificador o sin datos suficientes): {no_encontrados}\n"
                f"Filas con error: {errores}"
            )

        except Exception as e:
            print("Error en importación:", e)
            messagebox.showerror("Error", f"No se pudo completar la actualización: {e}")