import tkinter as tk
from tkinter import ttk, messagebox
import modelo.consultas_dao as consulta
import modelo.generos_dao as genero

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack()
        self.id_peli = None
        self.fondo = "#FBFCDD"
        self.config(bg=self.fondo)

       
        consulta.crear_tabla()

        self.label_form()
        self.input_form()
        self.botones_principales()
        self.mostrar_tabla()

    def label_form(self):
        tk.Label(self, text="Nombre: ", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Duración: ", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="Genero: ", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="Director: ", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=0, column=2, padx=10, pady=10)
        tk.Label(self, text="Actor Principal: ", font=('Arial',12,'bold'), bg=self.fondo, fg="#1931E8").grid(row=1, column=2, padx=10, pady=10)

    def input_form(self):
        self.nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.nombre, width=50, state='disabled')
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.duracion = tk.StringVar()
        self.entry_duracion = tk.Entry(self, textvariable=self.duracion, width=50, state='disabled')
        self.entry_duracion.grid(row=1, column=1, padx=10, pady=10)

        self.director = tk.StringVar()
        self.entry_director = tk.Entry(self, textvariable=self.director, width=50, state='disabled')
        self.entry_director.grid(row=0, column=3, padx=10, pady=10)

        self.actor_principal = tk.StringVar()
        self.entry_actor_pricipal = tk.Entry(self, textvariable=self.actor_principal, width=50, state='disabled')
        self.entry_actor_pricipal.grid(row=1, column=3, padx=10, pady=10)

        self.genero_manager = genero.GeneroManager()
        self.entry_genero = ttk.Combobox(self, state="readonly", width=25)
        self.entry_genero['values'] = self.genero_manager.get_nombres()
        if self.entry_genero['values']:
            self.entry_genero.current(0)
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10)

    def botones_principales(self):
        self.btn_alta = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.btn_alta.config(width=20, font=('Arial', 12,'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2')
        self.btn_alta.grid(row=3, column=0, padx=10, pady=10)

        self.btn_modi = tk.Button(self, text='Guardar', command=self.guardar_campos, state='disabled')
        self.btn_modi.config(width=20, font=('Arial', 12,'bold'), fg='#FFFFFF', bg='#0D2A83', cursor='hand2')
        self.btn_modi.grid(row=3, column=1, padx=10, pady=10)

        self.btn_cance = tk.Button(self, text='Cancelar', command=self.bloquear_campos, state='disabled')
        self.btn_cance.config(width=20, font=('Arial', 12,'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2')
        self.btn_cance.grid(row=3, column=2, padx=10, pady=10)

    def mostrar_tabla(self):
        # clear previous widgets in the row area
        for widget in self.grid_slaves(row=4):
            widget.destroy()

        self.lista_p = consulta.listar_peli()
        if not self.lista_p:
            self.lista_p = []

        self.lista_p.reverse()

        self.tabla = ttk.Treeview(self, columns=('Nombre','Duracion','Genero','Director','Actor Principal'))
        self.tabla.grid(row=4, column=0, columnspan=4, sticky='nse')

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=4, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Nombre')
        self.tabla.heading('#2', text='Duracion')
        self.tabla.heading('#3', text='Genero')
        self.tabla.heading('#4', text='Director')
        self.tabla.heading('#5', text='Actor Principal')

        for p in self.lista_p:
            # expected p: (ID, Nombre, Duracion, Director, Actor_Principal, GeneroNombre)
            self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[5], p[3], p[4]))

        self.btn_editar = tk.Button(self, text='Editar', command=self.editar_registro)
        self.btn_editar.config(width=20, font=('Arial', 12,'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2')
        self.btn_editar.grid(row=5, column=0, padx=10, pady=10)

        self.btn_delete = tk.Button(self, text='Delete', command=self.eliminar_regristro)
        self.btn_delete.config(width=20, font=('Arial', 12,'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2')
        self.btn_delete.grid(row=5, column=1, padx=10, pady=10)

    def editar_registro(self):
        try:
            sel = self.tabla.selection()
            if not sel:
                return
            self.id_peli = self.tabla.item(sel)['text']

            vals = self.tabla.item(sel)['values']
            self.nombre_peli = vals[0]
            self.dura_peli = vals[1]
            self.gene_peli = vals[2]
            self.director_peli = vals[3]
            self.actor_pricipal_peli = vals[4]

            self.habilitar_campos()
            self.nombre.set(self.nombre_peli)
            self.duracion.set(self.dura_peli)
            self.director.set(self.director_peli)
            self.actor_principal.set(self.actor_pricipal_peli)

            indice_genero = self.genero_manager.get_indice_por_nombre(self.gene_peli)
            if indice_genero is not None:
                self.entry_genero.current(indice_genero)
        except Exception as e:
            print('Error editar_registro:', e)

    def eliminar_regristro(self):
        sel = self.tabla.selection()
        if not sel:
            return
        self.id_peli = self.tabla.item(sel)['text']

        response = messagebox.askyesno("Confirmar","Desea borrar el registro ?")
        if response:
            consulta.borrar_peli(int(self.id_peli))
        else:
            messagebox.showinfo("MIRA BIEN", "CASI BORRAS ALGO EQUIVOCADO")

        self.id_peli = None
        self.mostrar_tabla()

    def guardar_campos(self):
        pelicula = consulta.Peliculas(
            self.nombre.get(),
            self.duracion.get(),
            self.genero_manager.get_id_por_indice(self.entry_genero.current()),
            self.actor_principal.get(),
            self.director.get()
        )

        if self.id_peli is None:
            consulta.guardar_peli(pelicula)
        else:
            consulta.editar_peli(pelicula, int(self.id_peli))

        self.mostrar_tabla()
        self.bloquear_campos()

    def habilitar_campos(self):
        self.entry_nombre.config(state='normal')
        self.entry_duracion.config(state='normal')
        self.entry_genero.config(state='normal')
        self.entry_director.config(state='normal')
        self.entry_actor_pricipal.config(state='normal')

        self.btn_modi.config(state='normal')
        self.btn_cance.config(state='normal')
        self.btn_alta.config(state='disabled')
        self.entry_genero.config(state='readonly')

    def bloquear_campos(self):
        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')
        self.entry_genero.config(state='disabled')
        self.entry_director.config(state='disabled')
        self.entry_actor_pricipal.config(state='disabled')

        self.btn_modi.config(state='disabled')
        self.btn_cance.config(state='disabled')
        self.btn_alta.config(state='normal')
        self.nombre.set('')
        self.duracion.set('')
        self.director.set('')
        self.actor_principal.set('')
        if self.entry_genero['values']:
            self.entry_genero.current(0)
        self.entry_genero.config(state='disabled')
        self.id_peli = None
