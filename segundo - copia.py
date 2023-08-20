import tkinter as tk
import pygame
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import sys
import pandas as pd
from tkcalendar import DateEntry
from tkinter import messagebox
import copy
import serial
from serial.serialutil import SerialException
from datetime import datetime, timedelta


def busquedaselectiva(base, index, a):
    contador = 0
    buscado = a.split(" ")
    indicelist = []
    indice = 0
    for i in base:
         #este me reecorre el array de la lista
        comparado = i[index]
        comparado = comparado.split(" ")
        coincidencia = [0] * len(buscado)
        recorrido = 0
        vcontrol = 0
        recorridos = int(len(comparado)/len(buscado))
        y = 0
        while True:
            for x in comparado:
                if buscado[y] == x :
                    coincidencia[y]= 1
                    comparado.remove(x)
                    break
            y += 1
            if y >= len(buscado):
                y = 0
                recorrido +=1
            if all(z > 0 for z in coincidencia):
                contador += 1 
                vcontrol += 1
                coincidencia = [0] * len(buscado)
            if recorrido >= recorridos:
                break
        if vcontrol > 0:
            indicelist.append(indice)
        indice += 1
    return indicelist
def volver(ventana):
    ventana.destroy()
    IniciarSesion(basedatos)
def barra(ventana):
    barra = tk.Menu(ventana)
    opciones = tk.Menu(barra, tearoff = 0)
    barra.add_cascade(label="Opciones", menu=opciones)
    opciones.add_command(label = "Cerrar sesion", command= lambda: volver(ventana))
    opciones.add_separator()
    opciones.add_command(label = "Salir", command= sys.exit)
    ventana.config(menu = barra)
def crearBoton(root, text, icon_path, command = None, sitio = "top"):
    # Cargar el icono desde el archivo
    icono = Image.open(icon_path)
    icono = icono.resize((32, 32))  # Ajustar el tamaño del icono si es necesario
    icono_tk = ImageTk.PhotoImage(icono)  # Mantener una referencia al objeto ImageTk.PhotoImage

    # Crear el botón con el icono
    boton = ttk.Button(root, text=text, image=icono_tk, command=command, compound="left")
    boton.image = icono_tk  # Asignar la imagen al atributo 'image' del botón
    boton.pack(side= sitio)
def EXTRAERDATOS(base, k):
    datos = []
    for i in base:
        datos.append(i[k])
    return datos
def excel (LISTA, na, nf):
    fechaF = EXTRAERDATOS(LISTA, 0)
    CF = EXTRAERDATOS(LISTA, 1)
    NP = EXTRAERDATOS(LISTA, 2)
    CP = EXTRAERDATOS(LISTA, 3)
    CPR = EXTRAERDATOS(LISTA, 4)
    costoPr = []
    for i in CPR:
        i = i.replace("$", "")
        i = float(i)
        costoPr.append(i)
    TD = EXTRAERDATOS(LISTA, 5)
    ND = EXTRAERDATOS(LISTA, 6)
    data = {
        'Fecha': fechaF,
        'Cedula': CF,
        'Nombre del producto': NP,
        'Codigo del producto': CP,
        'Costo': costoPr,
        'Tipo de doctor': TD,
        'Nombre doctor': ND
    }
    df = pd.DataFrame(data)
    suma_costo = df['Costo'].sum()
    total_row = pd.DataFrame([['Total', '', '', '', suma_costo, '', '']],
                            columns=df.columns)
    df = pd.concat([df, total_row], ignore_index=True)

    return df

   # writer = pd.ExcelWriter(na, engine='xlsxwriter')
   # df.to_excel(writer, index=False, sheet_name="factura#" + str(nf))
   # worksheet = writer.sheets["factura#" + str(nf)]
    #worksheet.set_column('A:G', 15)
    #writer._save()

class baseDatos:
    def __init__(self):
        self.doctores = [["2", "2", "Doctor Chapatin", 1, 0, [], "Doctor General", [], "drchapatin.png"],
                         ["4", "4", "Dr House", 1, 0, [], "Doctor General", [], "drhouse.png"],
                         ["2384935", "2384935L", "Luis Alirio", 2, 0, [], "Doctor Especialista", [], "rutaimg"],
                         ["5675234", "5675234J", "Jose Ramiro", 2, 0, [], "Doctor Especialista", [], "rutaimg"],
                         ["34678456", "34678456K", "Karla Martinez", 3, 0, [], "Cirujano", [], "rutaimg"],
                         ["88345745", "88345745B", "Brenda Perez", 3, 0, [], "Cirujano", [], "rutaimg"]]
        self.pacientes = [["1", "1", "Sergio Rincon", [], 3, "calle 30", "COOPSALUD"],
                          ["11925685", "11925685J", "Julian Perez", [], 2, "calle 22", "SALUDVIDA"]]#agregar correo y direccion de la imagen, el correo es para enviar la factura por correo 
        self.deudas = [["08/07/2023", "1111", "Jarabe", "23", "$23","Doctor General", "Juan Pablo", 2, "20kg", "10grados"]]
        self.admins = [["admin", "admin", "Andres Rincon", 0, 0], ["amdin2", "admin", "Sergio Rincon", 0, 0]]

        #PRODUCTOS:
        self.GranArea = ["Jarabe", "Pastillas", "Material clinico"]
        self.presentaciones = ["10ml", "20ml", "15ml"]
        self.presentacionesP = ["10u", "20u", "30u"]
        self.presentacionesMC = ["batas", "jeringas", "tapabocas"]
        self.marcas = ["Pfizer", "J&J", "AstraZeneca"]
        self.examenesG = [["Examen de la vista", "$50", "200"], ["examen del pancreas", "$40", "201"], ["colonoscopia", "$2", "202"]]
        self.examenesE = [["Quimio", "$200", "203"], ["examen de higado", "$30", "204"], ["examen de sangre", "$70", "205"]]
        self.examenesC = [["examen de sangre", "$60", "206"], ["examen de orina", "$80", "207"], ["colonoscopia", "$10", "208"]]
        self.LISTAGENERAL = [['Jarabe', '10ml', 'Pfizer', '$8', '1', 'jarabe1.png'], ['Jarabe', '10ml', 'J&J', '$15', '2', 'jarabe2.png'], ['Jarabe', '10ml', 'AstraZeneca', '$25', '3', 'jarabe3.png'],
                             ['Jarabe', '20ml', 'Pfizer', '$7', '4', 'jarabe1.png'], ['Jarabe', '20ml', 'J&J', '$13', '5', 'jarabe2.png'], ['Jarabe', '20ml', 'AstraZeneca', '$22', '6', 'jarabe3.png'],
                             ['Jarabe', '15ml', 'Pfizer', '$31', '7', 'jarabe1.png'], ['Jarabe', '15ml', 'J&J', '$26', '8', 'jarabe2.png'], ['Jarabe', '15ml', 'AstraZeneca', '$2', '9', 'jarabe3.png'],
                             ['Pastillas', '10u', 'Pfizer', '$18', '10', 'pastillas1.png'], ['Pastillas', '10u', 'J&J', '$39', '11', 'pastillas2.png'], ['Pastillas', '10u', 'AstraZeneca', '$18', '12', 'pastillas3.png'],
                             ['Pastillas', '20u', 'Pfizer', '$32', '13', 'pastillas1.png'], ['Pastillas', '20u', 'J&J', '$6', '14', 'pastillas2.png'], ['Pastillas', '20u', 'AstraZeneca', '$28', '15', 'pastillas3.png'],
                             ['Pastillas', '30u', 'Pfizer', '$30', '16', 'pastillas1.png'], ['Pastillas', '30u', 'J&J', '$15', '17', 'pastillas2.png'], ['Pastillas', '30u', 'AstraZeneca', '$10', '18', 'pastillas3.png'],
                             ['Material Clinico', 'batas', 'Pfizer', '$19', '19', 'bata.png'], ['Material Clinico', 'batas', 'J&J', '$8', '20', 'bata2.png'],
                             ['Material Clinico', 'batas', 'AstraZeneca', '$3', '21', 'bata3.png'], ['Material Clinico', 'jeringas', 'Pfizer', '$9', '22', 'jeringa.png'],
                             ['Material Clinico', 'jeringas', 'J&J', '$33', '23', 'jeringa2.jpg'], ['Material Clinico', 'jeringas', 'AstraZeneca', '$10', '24', 'jeringa3.jpg'],
                             ['Material Clinico', 'tapabocas', 'Pfizer', '$23', '25', 'tapabocas.png'], ['Material Clinico', 'tapabocas', 'J&J', '$4', '26', 'tapabocas2.png'], ['Material Clinico', 'tapabocas', 'AstraZeneca', '$31', '27', 'tapabocas3.png']]
        #CITAS
        self.LISTA = []
        self.dto = 1
        self.fd = 0
        self.ft = 0
        self.fm= 0

        #self.LISTAGENERAL = self.LISTAPRODUCTOS()
        #costos = [random.randint(2, 40) for _ in range(len(self.LISTAGENERAL))] #GENERA PRECIOS ALEATORIOS PARA LOS PRODUCTOS
        #n = 0
        #for i in self.LISTAGENERAL: #inserto los precios a la lista combinada de los productos en la posicion 3
        #    i.insert(3, "$" + str(costos[n]))
        #   n += 1
        lcode = self.LISTAGENERAL[-1][4]
        self.lcode = int(lcode)
        self.codigoe = 209
    def LISTAPRODUCTOS(self):
        combinaciones = []
        n = 0 
        for presentacion in self.presentaciones:
            for marca in self.marcas:
                n += 1
                combinacion = ["Jarabe", presentacion, marca, str(n)]
                combinaciones.append(combinacion)
        for presentacion in self.presentacionesP:
            for marca in self.marcas:
                n += 1
                combinacion = ["Pastillas", presentacion, marca, str(n)]
                combinaciones.append(combinacion)
        for presentacion in self.presentacionesMC:
            for marca in self.marcas:
                n += 1
                combinacion = ["Material Clinico", presentacion, marca, str(n)]
                combinaciones.append(combinacion)
        return combinaciones
    
class IniciarSesion:
    def __init__(self, basedatos):
        self.base = basedatos
        self.login()

    def login(self):   
        self.ventana = ThemedTk(theme="breeze")
        barra(self.ventana)
        self.ventana.iconbitmap("C:/Users/SergioR/Pictures/iconos/clinicaicono.ico")
        self.ventana.title("CLINICA -- INICIO DE SESION")
        self.ventana.geometry("400x600")
        self.ventana.config(background = "#5271FF")
        fuente = font.Font(family="Hospital", size=20, weight="bold")
        Logo = Image.open("C:/Users/SergioR/Pictures/iconos/ClinicaLogo.png")
        Logo = Logo.resize((150, 150))
        Logo_tk = ImageTk.PhotoImage(Logo)
        self.NombreClinica = tk.Label(self.ventana, image= Logo_tk, background= "#5271FF")
        self.NombreClinica.pack(padx= 0)
        self.etiqueta(self.ventana, "USUARIO", "#5271FF", 0, 5, fg = "white")
        self.usuario = ttk.Entry(self.ventana)
        self.usuario.pack()
        self.etiqueta(self.ventana, "CONTRASEÑA", "#5271FF", 0, 5, fg = "white")
        self.contra = ttk.Entry(self.ventana, show= "*") 
        self.contra.pack()
        self.mensaje_fallido = tk.Label(self.ventana, text="", fg="red", background= "#5271FF")
        self.mensaje_fallido.pack()
        imagen = Image.open("C:/Users/SergioR/Pictures/iconos/doctor_bayter.png")
        imagen = imagen.resize((200, 150))
        imagen_tk = ImageTk.PhotoImage(imagen)
        boton = ttk.Button(self.ventana, text= "INICIAR SESION", command= self.iniciar_sesion)
        boton.pack()
        label_imagen = tk.Label(self.ventana, image=imagen_tk, background= "#5271FF")
        label_imagen.pack(pady= 3)
        self.ventana.mainloop()

    def iniciar_sesion(self):
        usuario = self.usuario.get()
        contra = self.contra.get()
        caso1 = self.comprobarDatos(self.base.admins, usuario, contra)
        caso2 = self.comprobarDatos(self.base.pacientes, usuario, contra)
        caso3 = self.comprobarDatos(self.base.doctores, usuario, contra)
        if caso1[0] == 1:
            print("admin")
            self.caso = caso1
            self.ventana.destroy()
            self.menu = menuAdmin(basedatos)

        elif caso2[0] == 1:
            print("paciente")
            self.caso = caso2
            self.ventana.destroy()
            self.menu = menuPaciente(basedatos, self.caso)
            
        elif caso3[0] == 1:
            print("doctor")
            self.caso = caso3
            self.ventana.destroy()
            self.menu = menuDoctor(basedatos, self.caso)
        else: 
            self.usuario.delete(0, tk.END)
            self.contra.delete(0, tk.END)
            self.mensaje_fallido.config(text="Inicio de sesión fallido")

    def comprobarDatos(self, base, usuario, contra):
        for i in base:
            usuarioBase = i[0]
            contraBase = i[1]
            nombreBase = i[2]
            tipoD = i[3]
            estrato = i[4]
            if usuarioBase == usuario and contraBase == contra:
                print("Bienvenido "+ nombreBase)
                return [1, nombreBase, usuarioBase, tipoD, i, estrato]
        return [0,0]
    
    def etiqueta (self, x,  text, color, px = 0, py = 0, fg = "black"):
        etiqueta = tk.Label(x, text=text, background= color, fg= fg)
        etiqueta.pack(padx= px, pady= py)



class menuAdmin:
    def __init__(self, basedatos):
        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/SergioR/Music/AUDIOS DISCORD/MILIDEL.mp3")
        pygame.mixer.music.play()
        self.menu3 = None
        self.base = basedatos
        self.menu_admin = ThemedTk(theme="breeze")
        barra(self.menu_admin)
        self.menu_admin.iconbitmap("C:/Users/SergioR/Pictures/iconos/clinicaicono.ico")
        self.menuAdmin = tk.Frame(self.menu_admin)
        self.menuAdmin.pack(anchor= "nw", fill= "x")
        crearBoton(self.menuAdmin, "Crear perfil paciente", "crearPaciente.png", command= self.crear_paciente, sitio = "left")
        crearBoton(self.menuAdmin, "Modificar medicamento o examenes", "modificarMed.png", command= self.modificar, sitio = "left") 
        crearBoton(self.menuAdmin, "Ingresar o eliminar medicamentos", "ingresarMed.png", command= self.ingresar_eliminar, sitio = "left")
        crearBoton(self.menuAdmin, "Crear perfil doctor", "crearD.png", command= self.crear_doctor, sitio = "left") 
        crearBoton(self.menuAdmin, "Ver facturas", "verFacturas.png", command= self.Facturas, sitio = "left")                              
        crearBoton(self.menuAdmin, "Salir", "salir.png", command= lambda: volver(self.menu_admin), sitio = "left")                              
        self.menu_admin.title("MENU ADMINISTRADOR")
        self.menu_admin.geometry("1280x600")
        self.menu_admin.mainloop()

    def validate_numeric_input(self, action, value_if_allowed, text):
        if action == '1':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        elif action == '0':
            return True
        elif action == 'focusout':
            try:
                int(text)
                return True
            except ValueError:
                return False
        else:
            return False


 #------------------------------------------------------------------------------------   
    def crear_paciente(self):#TA BIEN
        numeros = [1, 2, 3, 4, 5]
        self.menuAdmin.pack_forget()
        self.crearP = tk.Frame(self.menu_admin)
        self.crearP.pack()
        validation = self.crearP.register(self.validate_numeric_input)
        IniciarSesion.etiqueta(self, self.crearP, "INGRESE LOS DATOS PARA CREAR EL PACIENTE", None, 0, 10)
        IniciarSesion.etiqueta(self, self.crearP, "CEDULA", None, 0, 0)
        self.documento = ttk.Entry(self.crearP, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.documento.pack(pady= 5)
        IniciarSesion.etiqueta(self, self.crearP, "NOMBRE", None, 0, 0)
        self.nombre = ttk.Entry(self.crearP)
        self.nombre.pack(pady = 5)
        IniciarSesion.etiqueta(self, self.crearP, "DIRECCIÓN", None, 0, 0)
        self.direccion = ttk.Entry(self.crearP)
        self.direccion.pack(pady = 5)
        IniciarSesion.etiqueta(self, self.crearP, "EPS", None, 0, 0)
        self.eps = ttk.Entry(self.crearP)
        self.eps.pack(pady = 5)
        IniciarSesion.etiqueta(self, self.crearP, "ESTRATO", None, 0, 0)
        self.estrato = ttk.Combobox(self.crearP, values = numeros, state= "readonly")
        self.estrato.pack(pady=5)
        self.mensaje_fallido = tk.Label(self.crearP, text="", fg="red")
        self.mensaje_fallido.pack()        
        boton1 = ttk.Button(self.crearP, text="CREAR", command= self.agregar_paciente)
        boton2 = ttk.Button(self.crearP, text = "Volver", command= lambda: self.volverMA(self.crearP))
        boton1.pack(anchor= tk.CENTER, pady= 3)
        boton2.pack(anchor= tk.CENTER)
        self.crearP.mainloop()
    def agregar_paciente(self):#TA BIEN
        nombre = self.nombre.get()
        direccion = self.direccion.get()
        documento = self.documento.get()
        estrato = self.estrato.get()
        eps = self.eps.get()
        if nombre and direccion and documento and estrato and eps:
            for i in self.base.pacientes:
                if i[0] == self.documento.get():
                    self.mensaje_fallido.config(text= "usuario ya registrado", fg= "red")
                    return
            nuevo_paciente = [documento, documento + nombre[0].upper(), nombre.lower(), [], int(estrato), direccion, eps]
            self.base.pacientes.append(nuevo_paciente)
            self.mensaje_fallido.config(text= "usuario creado", fg= "green")
            print(self.base.pacientes)
        else:
            self.mensaje_fallido.config(text= "llene todas las casillas",fg = "red")
            print("llene todas las casillas")
            return
 #------------------------------------------------------------------------------------   
    def crear_doctor(self):#TA BIEN
        numeros = ["1. Doctor General", "2. Doctor Especialista", "3. Cirujano"]
        self.menuAdmin.pack_forget()
        self.crearD = tk.Frame(self.menu_admin)
        self.crearD.pack()
        validation = self.crearD.register(self.validate_numeric_input)
        IniciarSesion.etiqueta(self, self.crearD, "INGRESE LOS DATOS PARA CREAR EL PACIENTE", None, 0, 10)
        IniciarSesion.etiqueta(self, self.crearD, "CEDULA", None, 0, 0)
        self.documento = ttk.Entry(self.crearD, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.documento.pack(pady= 5)
        IniciarSesion.etiqueta(self, self.crearD, "NOMBRE", None, 0, 0)
        self.nombre = ttk.Entry(self.crearD)
        self.nombre.pack(pady = 5)
        IniciarSesion.etiqueta(self, self.crearD, "TIPO DE DOCTOR", None, 0, 0)
        self.tipoD = ttk.Combobox(self.crearD, values = numeros, state= "readonly")
        self.tipoD.pack(pady=5)
        self.rutaimagen = ttk.Entry(self.crearD, state="readonly")
        self.rutaimagen.pack()
        boton_imagen = ttk.Button(self.crearD, text="Seleccionar imagen", command=self.seleccionar_imagen)
        boton_imagen.pack()
        self.mensaje_fallido = tk.Label(self.crearD, text="", fg="red")
        self.mensaje_fallido.pack()        
        boton1 = ttk.Button(self.crearD, text="CREAR", command= self.agregar_doctor)
        boton2 = ttk.Button(self.crearD, text = "Volver", command= lambda: self.volverMA(self.crearD))
        boton1.pack(anchor= tk.CENTER, pady= 3)
        boton2.pack(anchor= tk.CENTER)
        self.crearD.mainloop()        
    def agregar_doctor(self): #TA BIEN
        nombre = self.nombre.get()
        documento = self.documento.get()
        tipoD = self.tipoD.get()
        rutaimagen = self.rutaimagen.get()
        if nombre and tipoD and documento and rutaimagen:
            for i in self.base.doctores:
                if i[0] == self.documento.get():
                    self.mensaje_fallido.config(text= "usuario ya registrado", fg= "red")
                    return
            self.base.doctores.append([documento, documento + nombre[0].upper(), nombre.lower(), int(tipoD[0]), 0, [], tipoD[3:], [], rutaimagen])
            self.mensaje_fallido.config(text= "usuario creado", fg= "green")
            print(self.base.doctores)
        else:
            self.mensaje_fallido.config(text= "llene todas las casillas",fg = "red")
            print("llene todas las casillas")
            return            
    def seleccionar_imagen(self):
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if ruta_imagen:
            self.rutaimagen.config(state='normal')
            self.rutaimagen.delete(0, tk.END)
            self.rutaimagen.insert(tk.END, ruta_imagen)
            self.rutaimagen.config(state='readonly')
    
 #------------------------------------------------------------------------------------   
    def ingresar_eliminar(self):#MENU INGRESAR O ELIMINAR
        self.menuAdmin.pack_forget()
        self.frame_principal = tk.Frame(self.menu_admin)
        self.frame_principal.pack()
        etiqueta = tk.Label(self.frame_principal, text="INGRESAR O ELIMINAR MEDICAMENTOS")
        etiqueta.pack()
        boton1 = ttk.Button(self.frame_principal, text="1. Ingresar nuevo medicamento", command=self.menu31)
        boton1.pack(pady= 5)
        boton2 = ttk.Button(self.frame_principal, text="2. Ingresar nuevo examen", command= self.menu32)
        boton2.pack(pady= 5)
        boton3 = ttk.Button(self.frame_principal, text="3. Eliminar medicamento", command = self.menu33)
        boton3.pack(pady= 5)
        boton4 = ttk.Button(self.frame_principal, text="4. Eliminar examen", command = self.menu34)
        boton4.pack(pady= 5)        
        boton5 = ttk.Button(self.frame_principal, text= "Volver", command= lambda: self.volverMA(self.frame_principal))
        boton5.pack()
    def menu31(self):#NUEVO MEDICAMENTO
        self.frame_principal.pack_forget()
        self.frame31 = tk.Frame(self.menu_admin)
        validation = self.frame31.register(self.validate_numeric_input)
        self.frame31.pack()
        etiqueta = tk.Label(self.frame31, text="Ingresar nuevo medicamento")
        etiqueta.pack()
        AreaL = tk.Label(self.frame31, text="Area")
        AreaL.pack()
        self.area = ttk.Entry(self.frame31)
        self.area.pack(pady= 5)
        PresentacionL = tk.Label(self.frame31, text="Presentacion")
        PresentacionL.pack()
        self.presentacion = ttk.Entry(self.frame31)
        self.presentacion.pack(pady= 5)
        MarcaL = tk.Label(self.frame31, text="Marca")
        MarcaL.pack()
        self.marca = ttk.Entry(self.frame31)
        self.marca.pack(pady= 5)    
        CostoL = tk.Label(self.frame31, text="Costo")
        CostoL.pack()
        self.costo = ttk.Entry(self.frame31, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.costo.pack(pady= 5)
        self.rutaimagen = ttk.Entry(self.frame31, state="readonly")
        self.rutaimagen.pack()
        boton_imagen = ttk.Button(self.frame31, text="Seleccionar imagen", command=self.seleccionar_imagen)
        boton_imagen.pack()
        self.mensaje_fallido = tk.Label(self.frame31, text="", fg="red")
        self.mensaje_fallido.pack()          
        boton_accion = ttk.Button(self.frame31, text="Añadir medicamento", command= self.addmed)
        boton_accion.pack(pady= 5)
        boton_volver = ttk.Button(self.frame31, text="Volver al Menú Principal", command= lambda: self.volverIE(self.frame31))
        boton_volver.pack(pady= 5)
    def addmed(self):#AGREGA NUEVO MEDICAMENTO
        area = self.area.get()
        presentacion = self.presentacion.get()
        costo = self.costo.get()
        marca = self.marca.get()
        lcode = self.base.lcode
        rutaimagen = self.rutaimagen.get()
        if area and costo and presentacion and marca and rutaimagen:
            costo = "$" + self.costo.get()
            if area in self.base.GranArea:
                if presentacion in self.base.presentaciones and marca in self.base.marcas:
                    self.mensaje_fallido.config(text = "este producto ya existe", fg= "red")
                elif presentacion in self.base.presentaciones:
                    self.base.marcas.append(marca)
                    lcode += 1
                    self.base.LISTAGENERAL.append([area, presentacion, marca, costo, str(lcode), rutaimagen])
                    self.mensaje_fallido.config(text = "El producto agregado fue: " + area + " de " + presentacion + " de la marca: "+ marca + " y cuesta: "+ costo, fg= "green")
                elif marca in self.base.marcas:
                    lcode += 1
                    self.base.presentaciones.append(presentacion)
                    self.base.LISTAGENERAL.append([area, presentacion, marca, costo, str(lcode), rutaimagen])
                    self.mensaje_fallido.config(text = "El producto agregado fue: " + area + " de " + presentacion + " de la marca: "+ marca + " y cuesta: "+ costo, fg= "green")
                    lcode += 1
                    self.base.presentaciones.append(presentacion)
                    self.base.marcas.append(marca)
                    self.base.LISTAGENERAL.append([area, presentacion, marca, costo, str(lcode), rutaimagen])
                    self.mensaje_fallido.config(text = "El producto agregado fue: " + area + " de " + presentacion + " de la marca: "+ marca + " y cuesta: "+ costo, fg= "green")
            else:
                self.base.GranArea.append(area)
                if not marca in self.base.marcas: self.base.marcas.append(marca)
                if not presentacion in self.base.presentaciones: self.base.presentaciones.append(presentacion)
                lcode += 1
                self.base.LISTAGENERAL.append([area, presentacion, marca, costo, str(lcode), rutaimagen])
                self.mensaje_fallido.config(text = "El producto agregado fue: " + area + " de " + presentacion + " de la marca: "+ marca + " y cuesta: "+ costo, fg= "green")
        else:
            self.mensaje_fallido.config(text= "llene todas las casillas",fg = "red")
            print("llene todas las casillas")
            return            
    def menu32(self):#NUEVO EXAMEN
        self.frame_principal.pack_forget()
        numeros = ["1. Doctor General", "2. Doctor Especialista", "3. Cirujano"]
        self.frame32 = tk.Frame(self.menu_admin)
        validation = self.frame32.register(self.validate_numeric_input)
        self.frame32.pack()
        etiqueta = tk.Label(self.frame32, text="Ingresar nuevo examen")
        etiqueta.pack()
        nombreL = tk.Label(self.frame32, text="Nombre del nuevo examen")
        nombreL.pack()
        self.nombreE = ttk.Entry(self.frame32)
        self.nombreE.pack(pady= 5)
        CostoL = tk.Label(self.frame32, text="Costo")
        CostoL.pack()
        self.costo = ttk.Entry(self.frame32, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.costo.pack(pady= 5)
        tipoDL = tk.Label(self.frame32, text="Seleccione el doctor al que desea asignarle el examen")
        tipoDL.pack()
        self.tipoD = ttk.Combobox(self.frame32, values = numeros, state= "readonly")
        self.tipoD.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.frame32, text="", fg="red")
        self.mensaje_fallido.pack()          
        boton_accion = ttk.Button(self.frame32, text="Añadir examen", command= self.addex)
        boton_accion.pack(pady= 5)
        boton_volver = ttk.Button(self.frame32, text="Volver al Menú Principal", command= lambda: self.volverIE(self.frame32))
        boton_volver.pack(pady= 5)
    def addex(self):#AGREGA NUEVO EXAMEN
        tipoE = self.tipoD.get()
        nombreE = self.nombreE.get()
        costo = self.costo.get()
        if not tipoE or not nombreE or not costo:
            self.mensaje_fallido.config(text= "llene todos los datos", fg="red")
            return
        tipoE = tipoE[0]
        tipoE = int(tipoE)
        codigoe = self.base.codigoe
        if tipoE == 1:
            examenes = self.EXTRAERDATOS(self.base.examenesG, 0)
            if not nombreE in examenes:
                codigoe += 1
                self.base.examenesG.append([nombreE, "$" + str(costo), str(codigoe)])
                self.mensaje_fallido.config(text = "Examen agregado con exito.", fg= "green")
                print(self.base.examenesG)
            else: self.mensaje_fallido.config(text = "Examen ya existente.", fg= "red")
        elif tipoE == 2:
            examenes = self.EXTRAERDATOS(self.base.examenesE, 0)
            if not nombreE in examenes:
                codigoe += 1
                self.base.examenesE.append([nombreE, "$" + str(costo), str(codigoe)])
                self.mensaje_fallido.config(text = "Examen agregado con exito.", fg= "green")
                print(self.base.examenesE)
            else: self.mensaje_fallido.config(text = "Examen ya existente.", fg= "red")
        elif tipoE == 3:
            examenes = self.EXTRAERDATOS(self.base.examenesC, 0)
            if not nombreE in examenes:
                codigoe += 1
                self.base.examenesC.append([nombreE, "$" + str(costo), str(codigoe)])
                self.mensaje_fallido.config(text = "Examen agregado con exito.", fg= "green")
                print(self.base.examenesC)
            else: self.mensaje_fallido.config(text = "Examen ya existente.", fg= "red")
    def menu33(self):#ELIMINAR MEDICAMENTO
        self.frame_principal.pack_forget()
        self.frame33 = tk.Frame(self.menu_admin)
        self.frame33.pack()
        validation = self.frame33.register(self.validate_numeric_input)
        etiqueta = tk.Label(self.frame33, text="ELIMINAR MEDICAMENTO")
        etiqueta.pack(pady= 10)
        CodigoL = tk.Label(self.frame33, text="Ingrese el codigo del medicamento a eliminar")
        CodigoL.pack()
        self.codigo = ttk.Entry(self.frame33, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.codigo.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.frame33, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton_eliminar = ttk.Button(self.frame33, text= "Eliminar", command= self.sure)
        boton_eliminar.pack()
        boton_volver = ttk.Button(self.frame33, text="Volver al Menú Principal", command= lambda: self.volverIE(self.frame33))
        boton_volver.pack(pady= 5)
    def sure(self):#SEGURO?
        codigo = self.codigo.get()
        if not codigo:
            self.mensaje_fallido.config(text = "ingrese el codigo del producto", fg= "red")
            return
        index = busquedaselectiva(self.base.LISTAGENERAL, 4, codigo)
        if index == []:
            self.mensaje_fallido.config(text = "no existe producto con este codigo", fg= "red")
            return 
        self.mensaje_fallido.config(text = "", fg= "red")
        self.index = index[0]  
        self.seguro = tk.Toplevel(self.menu_admin)
        self.seguro.transient(self.menu_admin)
        self.seguro.grab_set()
        self.seguro.title("¿ESTÁ SEGURO?")
        self.seguro.geometry("350x100")
        frame = tk.Frame(self.seguro)
        frame.pack()
        self.mensaje = tk.Label(frame, text = "El producto es "+ self.base.LISTAGENERAL[self.index][0] + " de " + self.base.LISTAGENERAL[self.index][1] + " marca " + self.base.LISTAGENERAL[self.index][2] + "\nseguro desea eliminarlo?", fg= "green")
        self.mensaje.pack()
        si = ttk.Button(frame, text = "SÍ", command= lambda: self.borrar(self.base.LISTAGENERAL))
        si.pack(side="left", padx=10, pady=10)
        no = ttk.Button(frame, text= "NO", command= self.seguro.destroy)
        no.pack(side="left", padx=10, pady=10) 
    def borrar(self, base):#BORRA MEDICAMENTO
        base.pop(self.index)
        self.mensaje_fallido.config(text = "Se eliminó el producto", fg= "green")
        self.seguro.destroy()
    def menu34(self):#ELIMINAR EXAMEN
        numeros = ["1. Doctor General", "2. Doctor Especialista", "3. Cirujano"]
        self.frame_principal.pack_forget()
        self.frame34 = tk.Frame(self.menu_admin)
        self.frame34.pack()
        validation = self.frame34.register(self.validate_numeric_input)
        etiqueta = tk.Label(self.frame34, text="ELIMINAR EXAMEN")
        etiqueta.pack(pady= 10)
        self.tipoD = ttk.Combobox(self.frame34, values = numeros, state= "readonly")
        self.tipoD.pack()
        CodigoL = tk.Label(self.frame34, text="Ingrese el codigo del medicamento a eliminar")
        CodigoL.pack()
        self.codigo = ttk.Entry(self.frame34, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.codigo.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.frame34, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton_eliminar = ttk.Button(self.frame34, text= "Eliminar", command= self.sureE)
        boton_eliminar.pack()
        boton_volver = ttk.Button(self.frame34, text="Volver al Menú Principal", command= lambda: self.volverIE(self.frame34))
        boton_volver.pack(pady= 5)
    def sureE(self):#SEGUROE?
        codigo = self.codigo.get()
        tipoD = self.tipoD.get()
        if not codigo:
            self.mensaje_fallido.config(text = "ingrese el codigo del examen", fg= "red")
            return
        if not tipoD:
            self.mensaje_fallido.config(text = "ingrese el tipo de doctor", fg= "red")
            return            
        tipoD = int(tipoD[0])
        if tipoD == 1:
            self.baseE = self.base.examenesG
        elif tipoD == 2:
            self.baseE = self.base.examenesE
        elif tipoD == 3:
            self.baseE = self.base.examenesC
        index = busquedaselectiva(self.baseE, 2, codigo)
        if index == []:
            self.mensaje_fallido.config(text = "examen no hallado", fg= "red")
            return
        self.mensaje_fallido.config(text = "", fg= "red")
        self.index = index[0]  
        self.seguro = tk.Toplevel(self.menu_admin)
        self.seguro.transient(self.menu_admin)
        self.seguro.grab_set()
        self.seguro.title("¿ESTÁ SEGURO?")
        self.seguro.geometry("250x100")
        frame = tk.Frame(self.seguro)
        frame.pack()
        self.mensaje = tk.Label(frame, text = "El examen es " + self.baseE[self.index][0] + "\nseguro desea eliminarlo?", fg= "green")
        self.mensaje.pack()
        si = ttk.Button(frame, text = "SÍ", command= lambda: self.borrar(self.baseE))
        si.pack(side="left", padx=10, pady=10)
        no = ttk.Button(frame, text= "NO", command= self.seguro.destroy)
        no.pack(side="left", padx=10, pady=10)     
    def volverIE(self, frame):
        frame.pack_forget()
        self.frame_principal.pack()
 #------------------------------------------------------------------------------------   
    def modificar(self):
        self.menuAdmin.pack_forget()
        self.frame_principal = tk.Frame(self.menu_admin)
        self.frame_principal.pack()
        etiqueta = tk.Label(self.frame_principal, text="MODIFICAR MEDICAMENTOS O EXAMENES")
        etiqueta.pack()
        boton1 = ttk.Button(self.frame_principal, text="1. Modificar medicamento", command= self.modM)
        boton1.pack(pady= 5)
        boton2 = ttk.Button(self.frame_principal, text="2. Modificar examen", command= self.modE)
        boton2.pack(pady= 5)
        boton3 = ttk.Button(self.frame_principal, text= "Volver", command= lambda: self.volverMA(self.frame_principal))
        boton3.pack()
    def modM(self):
        self.frame_principal.pack_forget()
        self.framemodM = tk.Frame(self.menu_admin)
        self.framemodM.pack()
        validation = self.framemodM.register(self.validate_numeric_input)
        CodigoL = tk.Label(self.framemodM, text="Ingrese el codigo del medicamento a modificar")
        CodigoL.pack()
        self.codigo = ttk.Entry(self.framemodM, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.codigo.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.framemodM, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton = ttk.Button(self.framemodM, text = "Buscar", command= self.busquedaM)
        boton.pack(pady=5)
        boton_volver = ttk.Button(self.framemodM, text="Volver al Menú Principal", command= lambda: self.volverIE(self.framemodM))
        boton_volver.pack(pady= 5)
    def busquedaM(self):
        codigo = self.codigo.get()
        if not codigo: 
            self.mensaje_fallido.config(text= "ingrese el codigo del medicamento", fg= "red")
            return  
        index = busquedaselectiva(self.base.LISTAGENERAL, 4, codigo)
        if index == []:
            self.mensaje_fallido.config(text= "el medicamento no existe", fg= "red")
            return
        self.index = index[0]
        GranArea = self.base.LISTAGENERAL[self.index][0]
        Marca = self.base.LISTAGENERAL[self.index][2]
        Presentacion = self.base.LISTAGENERAL[self.index][1]
        costo = self.base.LISTAGENERAL[self.index][3]
        self.framemodM.pack_forget()
        self.menuMod = tk.Frame(self.menu_admin)
        self.menuMod.pack()
        self.GranArea = tk.Label(self.menuMod, text="El Gran Area es: " + GranArea, fg ="green")
        self.GranArea.pack() 
        self.Marca = tk.Label(self.menuMod, text="La marca es: " + Marca, fg ="green")
        self.Marca.pack()
        self.Presentacion = tk.Label(self.menuMod, text="La presentacion es: " + Presentacion, fg ="green")
        self.Presentacion.pack()
        self.Costo = tk.Label(self.menuMod, text="El costo es: " + costo, fg ="green")
        self.Costo.pack()
        cambioL = tk.Label(self.menuMod, text="Ingrese el cambio que desea hacer")
        cambioL.pack()        
        self.cambio = ttk.Entry(self.menuMod)
        self.cambio.pack()
        self.mensaje_fallido = tk.Label(self.menuMod, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton = ttk.Button(self.menuMod, text = "Gran Area", command = lambda: self.cambiar(0, self.GranArea, "Gran Area", self.base.LISTAGENERAL))
        boton.pack(pady=5)
        boton1 = ttk.Button(self.menuMod, text = "Presentacion", command = lambda: self.cambiar(1, self.Presentacion, "Presentacion", self.base.LISTAGENERAL))
        boton1.pack(pady=5)
        boton2 = ttk.Button(self.menuMod, text = "Marca", command = lambda: self.cambiar(2, self.Marca, "Marca", self.base.LISTAGENERAL))
        boton2.pack(pady=5)
        boton3 = ttk.Button(self.menuMod, text = "Costo", command = lambda: self.cambiarC(self.base.LISTAGENERAL, 3))
        boton3.pack(pady=5)
        boton_volver = ttk.Button(self.menuMod, text="Volver al Menú Principal", command= lambda: self.volverIE(self.menuMod))
        boton_volver.pack(pady= 5)
    def cambiar(self, k, etiqueta, palabra, base):
        cambio = self.cambio.get()
        if not cambio:
            self.mensaje_fallido.config(text= "llene el espacio de cambio.")
            return
        base[self.index][k] = cambio
        etiqueta.config(text = palabra + " cambió por: " + cambio)
    def cambiarC(self, base, k):
        cambio = self.cambio.get()
        if not cambio:
            self.mensaje_fallido.config(text= "llene el espacio de cambio.")
            return
        try:
            cambio = int(cambio)
        except:
            self.mensaje_fallido.config(text= "El precio tiene que ser un entero.")
            return
        cambio = "$" + str(cambio)
        base[self.index][k] = cambio
        self.Costo.config(text= "El nuevo costo es: "+ cambio)
    def modE(self):
        numeros = ["1. Doctor General", "2. Doctor Especialista", "3. Cirujano"]
        self.frame_principal.pack_forget()
        self.framemodE = tk.Frame(self.menu_admin)
        self.framemodE.pack()
        validation = self.framemodE.register(self.validate_numeric_input)
        CodigoL = tk.Label(self.framemodE, text="Ingrese el codigo del medicamento a modificar")
        CodigoL.pack()
        self.tipoD = ttk.Combobox(self.framemodE, values = numeros, state= "readonly")
        self.tipoD.pack()
        self.codigo = ttk.Entry(self.framemodE, validate="all", validatecommand=(validation, '%d', '%P', '%s'))
        self.codigo.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.framemodE, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton = ttk.Button(self.framemodE, text = "Buscar", command= self.busquedaE)
        boton.pack(pady=5)
        boton_volver = ttk.Button(self.framemodE, text="Volver al Menú Principal", command= lambda: self.volverIE(self.framemodE))
        boton_volver.pack(pady= 5)
    def busquedaE(self):
        codigo = self.codigo.get()
        tipoD = self.tipoD.get()
        if not codigo:
            self.mensaje_fallido.config(text = "ingrese el codigo del examen", fg= "red")
            return
        if not tipoD:
            self.mensaje_fallido.config(text = "ingrese el tipo de doctor", fg= "red")
            return            
        tipoD = int(tipoD[0])
        if tipoD == 1:
            self.baseE = self.base.examenesG
        elif tipoD == 2:
            self.baseE = self.base.examenesE
        elif tipoD == 3:
            self.baseE = self.base.examenesC
        index = busquedaselectiva(self.baseE, 2, codigo)
        if index == []:
            self.mensaje_fallido.config(text = "examen no hallado", fg= "red")
            return
        self.mensaje_fallido.config(text = "", fg= "red")
        self.index = index[0]
        costo = self.baseE[self.index][1]
        nombre = self.baseE[self.index][0]
        self.framemodE.pack_forget()
        self.menuModE = tk.Frame(self.menu_admin)
        self.menuModE.pack()
        self.nombreE = tk.Label(self.menuModE, text="El nombre es: " + nombre, fg ="green")
        self.nombreE.pack() 
        self.Costo = tk.Label(self.menuModE, text="El costo es: " + costo, fg ="green")
        self.Costo.pack()   
        cambioL = tk.Label(self.menuModE, text="Ingrese el cambio que desea hacer")
        cambioL.pack()        
        self.cambio = ttk.Entry(self.menuModE)
        self.cambio.pack()
        self.mensaje_fallido = tk.Label(self.menuModE, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton = ttk.Button(self.menuModE, text = "Nombre", command= lambda: self.cambiar(0, self.nombreE, "Nombre", self.base.LISTAGENERAL))
        boton.pack(pady=5)
        boton1 = ttk.Button(self.menuModE, text = "Costo", command= lambda: self.cambiarC(self.baseE, 1))
        boton1.pack(pady=5)
        boton_volver = ttk.Button(self.menuModE, text="Volver al Menú Principal", command= lambda: self.volverIE(self.menuModE))
        boton_volver.pack(pady= 5)
#------------------------------------------------------------------------------------
    def Facturas(self):
        self.menu_admin.geometry("1280x700")
        self.menuAdmin.pack_forget()
        self.frame_principal = tk.Frame(self.menu_admin)
        self.frame_principal.pack()
        label = tk.Label(self.frame_principal, text= "Desea ver la factura por:", background= None)
        label.pack(pady= 5)
        boton1 = ttk.Button(self.frame_principal, text= "Mes", command= self.MES)
        boton1.pack(pady= 5)
        boton2 = ttk.Button(self.frame_principal, text= "Total", command= self.TOTAL)
        boton2.pack(pady= 5)
        boton3 = ttk.Button(self.frame_principal, text= "Doctor", command= self.TIPODOC)
        boton3.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.frame_principal, text="", fg="red", background= None)
        self.mensaje_fallido.pack(pady = 5) 
        self.salir = ttk.Button(self.frame_principal, text= "Volver", command= lambda: self.volverMA(self.frame_principal))
        self.salir.pack(pady= 5)
    def MES(self):
        for widget in self.frame_principal.winfo_children():
            widget.config(state="disabled")
        self.frame2 = tk.Frame(self.menu_admin, background="#33FF90")
        self.frame2.pack(fill= tk.BOTH, expand= True)
        label = tk.Label(self.frame2, text= "Facturas por mes:", background= "#33FF90", fg= "white")
        label.pack()
        self.cal = DateEntry(self.frame2, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.cal.pack(padx=10, pady=10)
        self.mensaje_fallido2 = tk.Label(self.frame2, text="", fg="red", background= "#33FF90")
        self.mensaje_fallido2.pack(pady = 5) 
        siguiente = ttk.Button(self.frame2, text= "Siguiente", command= self.verFacturaM)
        siguiente.pack(pady = 5)
        salir = ttk.Button(self.frame2, text= "Volver", command= self.volverVF)
        salir.pack(pady = 5)
    def TOTAL(self):
        for widget in self.frame_principal.winfo_children():
            widget.config(state="disabled")
        self.frame2 = tk.Frame(self.menu_admin, background="#33FF90")
        self.frame2.pack(fill= tk.BOTH, expand= True)
        label = tk.Label(self.frame2, text= "Facturas:", background= "#33FF90", fg= "white")
        label.pack()
        self.mensaje_fallido2 = tk.Label(self.frame2, text="", fg="red", background= "#33FF90")
        self.mensaje_fallido2.pack(pady = 5) 
        if self.base.deudas == []:
            volver = ttk.Button(self.frame2, text = "Volver", command= self.volverVF)
            volver.pack(pady = 5)
            self.mensaje_fallido2.config(text= "No hay facturas en la base de datos.", fg= "red")
            return
        self.nombreArchivo = f"factura_Total{self.base.ft}.xlsx"
        self.df = excel(self.base.deudas, self.nombreArchivo, self.base.ft)
        self.MostrarDF(self.df, self.frame2)
        self. generar = ttk.Button(self.frame2, text = "Generar factura", command= lambda: self.Generar(1))
        self.generar.pack(pady = 5)
        volver = ttk.Button(self.frame2, text = "Volver", command= self.volverVF)
        volver.pack(pady = 5)        
    def verFacturaM(self):
        LISTA = []
        fechaseparada = []
        datoSeparado = []
        fecha = self.cal.get_date()
        self.fecha = fecha.strftime('%d/%m/%Y')
        self.fecha = self.fecha[3:]
        print(self.fecha)
        for i in self.base.deudas:
            fechaseparada.append(i[0])
        for j in fechaseparada:
            datoSeparado.append([j[-7:]])
        print(datoSeparado)
        index = busquedaselectiva(datoSeparado, 0, self.fecha)
        print(index)
        if index == []:
            self.mensaje_fallido2.config(text= "No hay facturas para este mes y año.", fg= "red")
            return
        for i in self.frame2.winfo_children():
            i.pack_forget()
        for k in index:
            LISTA.append(self.base.deudas[k])
        self.nombreArchivo = f"factura_Mes{self.base.fm}.xlsx"
        self.df = excel(LISTA, self.nombreArchivo, self.base.fm)
        self.MostrarDF(self.df, self.frame2)
        self.generar = ttk.Button(self.frame2, text = "Generar factura", command= lambda: self.Generar(2))
        self.generar.pack(pady = 5)
        volver = ttk.Button(self.frame2, text = "Volver", command= self.volverVF)
        volver.pack(pady = 5)
    
    def TIPODOC(self):
        for widget in self.frame_principal.winfo_children():
            widget.config(state="disabled") 
        self.frame2 = tk.Frame(self.menu_admin, background="#33FF90")
        self.frame2.pack(fill= tk.BOTH, expand= True)   
        label = tk.Label(self.frame2, text= "Seleccione el tipo de doctor para ver las facturas:", background="#33FF90")   
        label.pack()
        numeros = ["1. Doctor General", "2. Doctor Especialista", "3. Cirujano"]
        self.tipoD = ttk.Combobox(self.frame2, values = numeros, state= "readonly")
        self.tipoD.pack(pady=5)
        self.mensaje_fallido2 = tk.Label(self.frame2, text="", fg="red", background= "#33FF90")
        self.mensaje_fallido2.pack(pady = 5) 
        verF = ttk.Button(self.frame2, text= "Ver factura", command= self.VerFacturaTD)
        verF.pack(pady = 5)
        salir = ttk.Button(self.frame2, text= "volver", command= self.volverVF)
        salir.pack(pady = 5)
    def VerFacturaTD(self):
        LISTA = []
        tipoD = self.tipoD.get()
        tipoD = tipoD[3:]
        print(tipoD)
        index = busquedaselectiva(self.base.deudas, 5, tipoD)
        if index == []:
            self.mensaje_fallido2.config(text= "No hay facturas para este tipo de doctor.", fg= "red")
            return
        for i in self.frame2.winfo_children():
            i.pack_forget()
        for i in index:
            LISTA.append(self.base.deudas[i])
        self.nombreArchivo = f"factura_{self.base.fd}.xlsx"
        self.df = excel(LISTA, self.nombreArchivo, self.base.fd)
        self.MostrarDF(self.df, self.frame2)
        self.generar = ttk.Button(self.frame2, text = "Generar factura", command= lambda: self.Generar(3))
        self.generar.pack(pady = 5)
        volver = ttk.Button(self.frame2, text = "Volver", command= self.volverVF)
        volver.pack(pady = 5)        

    def Generar(self, f):
        if f == 1:
            self.generar.config(state= "disabled")
            writer = pd.ExcelWriter(self.nombreArchivo, engine='xlsxwriter')
            self.df.to_excel(writer, index=False, sheet_name="factura#" + str(self.base.ft))
            worksheet = writer.sheets["factura#" + str(self.base.ft)]
            worksheet.set_column('A:G', 15)
            writer._save()
            self.base.ft += 1
        elif f == 2:
            self.generar.config(state= "disabled")
            writer = pd.ExcelWriter(self.nombreArchivo, engine='xlsxwriter')
            self.df.to_excel(writer, index=False, sheet_name="factura#" + str(self.base.fm))
            worksheet = writer.sheets["factura#" + str(self.base.fm)]
            worksheet.set_column('A:G', 15)
            writer._save()
            self.base.fm += 1
        elif f == 3:
            self.generar.config(state= "disabled")
            writer = pd.ExcelWriter(self.nombreArchivo, engine='xlsxwriter')
            self.df.to_excel(writer, index=False, sheet_name="factura#" + str(self.base.fd))
            worksheet = writer.sheets["factura#" + str(self.base.fd)]
            worksheet.set_column('A:G', 15)
            writer._save()
            self.base.fd += 1
    def volverVF(self):
        self.frame2.pack_forget()
        for widget in self.frame_principal.winfo_children():
            widget.config(state="active")
    def MostrarDF(self, dataframe, ventana):
        # Variable para almacenar el índice del doctor seleccionado
        selected_index = tk.StringVar()

        def on_select(event):
            selection = event.widget.selection()
            if selection:
                # Obtiene el índice de la fila seleccionada
                index = int(event.widget.index(selection))
                # Asigna el índice del doctor a la variable selected_index
                selected_index.set(str(index + 1))  # Suma 1 para tener índices basados en 1

        # Crea el Treeview
        treeview = ttk.Treeview(ventana, selectmode='browse')
        treeview.pack(side= "top")

        # Agrega columnas al Treeview
        columns = dataframe.columns.tolist()
        treeview['columns'] = columns

        # Ajusta el ancho de las columnas
        for column in columns:
            treeview.column(column, width=100)
            treeview.heading(column, text=column)

        treeview.column("#0", width=0, stretch=tk.NO)

        # Agrega filas al Treeview
        for index, row in dataframe.iterrows():
            values = row.tolist()
            treeview.insert('', 'end', values=values)

        # Asigna la función de control de eventos a la selección de filas
        treeview.bind('<<TreeviewSelect>>', on_select)
#------------------------------------------------------------------------------------
    def volverMA(self, ventana):
        ventana.pack_forget()
        self.menuAdmin.pack(anchor= "nw", fill= "x")
    def EXTRAERDATOS(self, base, k):
        datos = []
        for i in base:
            datos.append(i[k])
        return datos
#--------------------MENU PACIENTE---------------------------------------------------
class menuPaciente:
    def __init__(self, basedatos, caso):
        self.base = basedatos
        self.caso = caso
        print(self.caso)
        self.LISTA = []
        self.cedulaUsuario = caso[2]
        self.fechauser = caso[3]
        self.estrato = caso[5]
        self.nombreUsuario = caso[1]
        self.contrac = caso[4][1]
        self.EPS = caso[4][6]
        self.direccion = caso[4][5]
        self.dcto = self.descuento(self.estrato)
        self.menu_paciente = ThemedTk(theme="breeze")
        barra(self.menu_paciente)
        self.menu_paciente.iconbitmap("C:/Users/SergioR/Pictures/iconos/clinicaicono.ico")
        self.framePaciente =tk.Frame(self.menu_paciente)
        self.framePaciente.pack(anchor= "nw", fill= "x")
        self.menu_paciente.title("MENU PACIENTE")
        self.menu_paciente.geometry("600x600")
        crearBoton(self.framePaciente, "Modificar datos", "C:/Users/SergioR/Pictures/iconos/modificarDatos.png", command= self.modificar, sitio = "left") 
        crearBoton(self.framePaciente, "Pedir cita", "C:/Users/SergioR/Pictures/iconos/cita.png", sitio = "left", command= self.pedirCitas) 
        crearBoton(self.framePaciente, "Ver examenes y costos", "C:/Users/SergioR/Pictures/iconos/verExamenes.png", sitio = "left", command= self.verExamenes) 
        crearBoton(self.framePaciente, "Salir", "C:/Users/SergioR/Pictures/iconos/salir.png", sitio = "left", command= lambda: volver(self.menu_paciente))         

#----------------------------------------------------------------------------------
    def modificar(self):#OPCION1
        self.framePaciente.pack_forget()
        self.frame_principal = tk.Frame(self.menu_paciente)
        self.frame_principal.pack()
        etiqueta = tk.Label(self.frame_principal, text="MODIFICAR SUS DATOS")
        etiqueta.pack()
        self.nombre = tk.Label(self.frame_principal, text="Su nombre es: " + self.nombreUsuario, fg = "green")
        self.nombre.pack()
        self.contra = tk.Label(self.frame_principal, text="Su contraseña es: " + self.contrac, fg = "green")
        self.contra.pack()
        self.direccionL = tk.Label(self.frame_principal, text="Su direccion es: " + self.direccion, fg = "green")
        self.direccionL.pack()
        self.eps = tk.Label(self.frame_principal, text="Su eps es: " + self.EPS, fg = "green")
        self.eps.pack()
        self.cambio = tk.Label(self.frame_principal, text="Ingrese el cambio:")
        self.cambio.pack()
        self.codigo = ttk.Entry(self.frame_principal)
        self.codigo.pack(pady= 5)
        self.mensaje_fallido = tk.Label(self.frame_principal, text="", fg="red")
        self.mensaje_fallido.pack() 
        boton1 = ttk.Button(self.frame_principal, text= "Contraseña", command= lambda: self.sure(1, self.contra, "Su nueva contraseña es: "))
        boton1.pack(pady=5)
        boton2 = ttk.Button(self.frame_principal, text= "Nombre", command= lambda: self.sure(2, self.nombre, "Su nuevo nombre es: "))
        boton2.pack(pady=5)
        boton3 = ttk.Button(self.frame_principal, text= "Dirección", command= lambda: self.sure(6, self.direccionL, "Su nueva dirección es: "))
        boton3.pack(pady=5)
        boton4 = ttk.Button(self.frame_principal, text= "EPS", command= lambda: self.sure(5, self.eps, "Su nueva eps es: "))
        boton4.pack(pady=5)
        boton5 = ttk.Button(self.frame_principal, text= "Volver", command= lambda: self.volverMP(self.frame_principal))
        boton5.pack(pady=5)
    def sure(self, k, etiqueta, mensaje):#SEGURO?
        codigo = self.codigo.get()
        index = busquedaselectiva(self.base.pacientes, 0, self.cedulaUsuario)
        index = index[0]
        if not codigo:
            self.mensaje_fallido.config(text = "ingrese el cambio que desea hacer", fg= "red")
            return
        self.mensaje_fallido.config(text = "", fg= "red")
        self.seguro = tk.Toplevel(self.menu_paciente)
        self.seguro.transient(self.menu_paciente)
        self.seguro.grab_set()
        self.seguro.title("¿ESTÁ SEGURO?")
        self.seguro.geometry("400x100")
        ms = tk.Label(self.seguro, text= mensaje + codigo + ", ¿seguro desea cambiarlo?", fg= "red")
        ms.pack()
        si = ttk.Button(self.seguro, text = "SÍ", command= lambda: self.cambiar(index, k, etiqueta, mensaje))
        si.pack(side="left", padx=10, pady=10)
        no = ttk.Button(self.seguro, text= "NO", command= self.seguro.destroy)
        no.pack(side="left", padx=10, pady=10) 
    def cambiar(self, index, k, etiqueta, mensaje):#CAMBIO
        cambio = self.codigo.get()
        self.base.pacientes[index][k] = cambio
        self.mensaje_fallido.config(text= "Se realizó el cambio", fg= "green")
        etiqueta.config(text = mensaje + cambio)
        self.seguro.destroy()
#----------------------------------------------------------------------------------
    def pedirCitas(self):#MUESTRA DOCTORES
        self.framePaciente.pack_forget()
        df = pd.DataFrame(self.base.doctores, columns= ["Cedula", "Codigo", "Nombre:", "Columna1", "Columna2", "Columna3", "Tipo de doctor:", "Columna4", "directorio"])
        df = df[["Nombre:", "Tipo de doctor:"]]
        df = df.reset_index(drop=True)
        df.index = df.index + 1
        self.pedirC = tk.Frame(self.menu_paciente)
        self.pedirC.pack()
        label = tk.Label(self.pedirC, text="seleccione el doctor con el que desea pedir su cita: ")
        label.pack()
        self.MostrarDF(df, self.pedirC)
        self.mensaje_fallido = tk.Label(self.pedirC, text="", fg="red")
        self.mensaje_fallido.pack()
        siguiente = ttk.Button(self.pedirC, text= "Siguiente", command= self.pedirCita2 )
        siguiente.pack()
        volver = ttk.Button(self.pedirC, text= "Volver", command= lambda: self.volverMP(self.pedirC) )
        volver.pack()
    def pedirCita2(self):#MUESTRA FECHAS
        seleccion = self.entry.get()
        if not seleccion:
            self.mensaje_fallido.config(text="Seleccione el doctor con el que desea pedir su cita.", fg= "red")
            return
        fecha_actual = datetime.today()
        fecha_minima = fecha_actual + timedelta(days=1)
        self.pedirC.pack_forget()
        self.pedirC2 = tk.Frame(self.menu_paciente)
        self.pedirC2.pack()
        seleccion = int(seleccion)
        self.citas = self.base.doctores[seleccion-1][5]
        self.fechas = self.base.doctores[seleccion-1][7]
        label = tk.Label(self.pedirC2, text="Seleccione la fecha de su cita: ")
        label.pack()
        self.cal = DateEntry(self.pedirC2, width=12, background='darkblue', foreground='white', borderwidth=2, mindate=fecha_minima)
        self.cal.pack(padx=10, pady=10)
        self.mensaje_fallido = tk.Label(self.pedirC2, text="", fg="red")
        self.mensaje_fallido.pack()        
        self.siguiente = ttk.Button(self.pedirC2, text= "Siguiente", command= self.horarios)
        self.siguiente.pack()
    def horarios(self):#MUESTRA HORARIOS
        fecha = self.cal.get_date()
        self.fecha = fecha.strftime('%d/%m/%Y')
        self.confirmacion = busquedaselectiva(self.fechas, 0, self.fecha)
        self.siguiente.config(state= "disabled")
        if self.confirmacion == []:
            label = tk.Label(self.pedirC2, text= "Seleccione el horario de su cita:")
            label.pack()
            self.horario = ["1. 7a.m", "2. 8a.m", "3. 9a.m", "4. 10a.m", "5. 11a.m", "6. 12a.m"]
            self.Hora = ttk.Combobox(self.pedirC2, values = self.horario, state= "readonly")
            self.Hora.pack(pady= 5)
            siguiente = ttk.Button(self.pedirC2, text= "Agendar", command= self.agendar)
            siguiente.pack()
        else:
            self.index = self.confirmacion[0]
            self.horario = self.fechas[self.index][1]
            self.Hora = ttk.Combobox(self.pedirC2, values = self.horario, state= "readonly")
            self.Hora.pack(pady= 5)
            siguiente = ttk.Button(self.pedirC2, text= "Agendar", command= self.agendar)
            siguiente.pack()
    def agendar(self):#EJECUTA LA ACCION
        hora = self.Hora.get()
        if not hora:
            self.mensaje_fallido.config(text="Seleccione el horario de su cita.", fg= "red")
            return     
        hora = int(hora[0])       
        indexuser = busquedaselectiva(self.fechauser, 0, self.fecha)
        if not indexuser == []:
            for k in indexuser:
                if self.horario[hora-1] in self.fechauser[k][1]:
                    self.mensaje_fallido.config(text="Usted ya tiene una cita en esta fecha y hora.", fg= "red")
                    return
        self.citas.append([self.fecha, self.horario[hora-1], self.cedulaUsuario, self.estrato, self.nombreUsuario])
        self.fechauser.append([self.fecha, self.horario[hora-1]])
        messagebox.showinfo("Mensaje", "Cita agregada correctamente.")
        if self.confirmacion == []:
            del self.horario[hora-1]
            self.fechas.append([self.fecha, self.horario])
        else:
            del self.fechas[self.index][1][hora-1]
        self.pedirC2.pack_forget()
        self.pedirC.pack()
#----------------------------------------------------------------------------------
    def verExamenes(self):
        LISTA = []
        self.frame_principal = tk.Frame(self.menu_paciente)
        self.frame_principal.pack()
        index = busquedaselectiva(self.base.deudas, 1, self.cedulaUsuario)
        if index == []:
            messagebox.showwarning("Mensaje", "El paciente no tiene historial en la base de datos.")
            self.frame_principal.destroy()
        else:
            self.framePaciente.pack_forget()
            self.menu_paciente.geometry("1200x700")
            label = tk.Label(self.frame_principal, text= "HISTORIAL PACIENTE:")
            label.pack()
            mensaje_error = tk.Label(self.frame_principal, text= "", fg = "red")
            mensaje_error.pack()
            for i in index:
                LISTA.append(copy.deepcopy(self.base.deudas[i]))
            suma = 0
            for j in LISTA:
                j[4] = j[4].replace("$", "")
                j[4] = float(j[4])
                suma = suma + j[4]
                j[4] = "$" + str(j[4])
            mensaje_error.config(text = "su total es de: " + str(suma), fg= "green")
            df = pd.DataFrame(LISTA, columns=["Fecha", "Cedula", "Nombre del Producto", "Código", "Costo", "Tipo de doctor", "Nombre Doctor", "Cantidad", "Peso", "Temperatura"])
            self.MostrarDF(df, self.frame_principal)
            volver = ttk.Button(self.frame_principal, text= "volver", command= lambda: self.volverMP(self.frame_principal))
            volver.pack()

#----------------------------------------------------------------------------------
    def volverMP(self, ventana):
        ventana.pack_forget()
        self.framePaciente.pack(anchor= "nw", fill= "x")
    def descuento(self, estrato):
        if estrato == 1:
            dto = 0.50
            return dto
        elif estrato == 2:
            dto = 0.60
            return dto
        elif estrato == 3:
            dto = 0.70
            return dto
        elif estrato == 4:
            dto = 0.80
            return dto
        elif estrato == 5:
            dto = 0.90
            return dto

    def validate_numeric_input(self, action, value_if_allowed, text):
        if action == '1':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        elif action == '0':
            return True
        elif action == 'focusout':
            try:
                int(text)
                return True
            except ValueError:
                return False
        else:
            return False

    def MostrarDF(self, dataframe, ventana):
        # Variable para almacenar el índice del doctor seleccionado
        selected_index = tk.StringVar()

        def on_select(event):
            selection = event.widget.selection()
            if selection:
                # Obtiene el índice de la fila seleccionada
                index = int(event.widget.index(selection))
                # Asigna el índice del doctor a la variable selected_index
                selected_index.set(str(index + 1))  # Suma 1 para tener índices basados en 1

        # Crea el Treeview
        treeview = ttk.Treeview(ventana, selectmode='browse')
        treeview.pack(side= "top")

        # Agrega columnas al Treeview
        columns = dataframe.columns.tolist()
        treeview['columns'] = columns

        # Ajusta el ancho de las columnas
        for column in columns:
            treeview.column(column, width=100)
            treeview.heading(column, text=column)

        treeview.column("#0", width=0, stretch=tk.NO)

        # Agrega filas al Treeview
        for index, row in dataframe.iterrows():
            values = row.tolist()
            treeview.insert('', 'end', values=values)

        # Asigna la función de control de eventos a la selección de filas
        treeview.bind('<<TreeviewSelect>>', on_select)
        self.entry = ttk.Entry(ventana, textvariable=selected_index, state="readonly")

class menuDoctor:
    def __init__(self, basedatos, caso):
        self.menu_doctor = ThemedTk(theme="breeze")
        self.base = basedatos
        self.contador = 0
        self.caso = caso
        self.cedulaUsuario = caso[0]
        self.nombreUsuario = caso[1]
        self.citas = caso[4][5]
        self.ruta = caso[4][8]
        self.examen = self.tipoDoctor(caso[4][3])[0]
        self.clasedoctor = caso[4][6]
        barra = tk.Menu(self.menu_doctor)
        opciones = tk.Menu(barra, tearoff = 0)
        info = tk.Menu(barra, tearoff = 0)
        barra.add_cascade(label="Opciones", menu=opciones)
        barra.add_cascade(label="Ver info", menu=info)
        opciones.add_command(label = "Cerrar sesion", command= lambda: volver(self.menu_doctor))
        opciones.add_separator()
        opciones.add_command(label = "Salir", command= sys.exit)
        info.add_command(label = "Carnet Doctor", command= self.carnet)
        self.menu_doctor.config(menu = barra)
        self.menuDoctor = tk.Frame(self.menu_doctor)
        self.menuDoctor.pack()
        self.menuDoctor.pack(anchor= "nw", fill= "x")
        self.menu_doctor.title("MENU PACIENTE")
        self.menu_doctor.geometry("600x600")
        self.menu_doctor.iconbitmap("C:/Users/SergioR/Pictures/iconos/clinicaicono.ico")
        crearBoton(self.menuDoctor, "Ver citas", "C:/Users/SergioR/Pictures/iconos/citas.png", command= self.vercitas, sitio = "left") 
        crearBoton(self.menuDoctor, "Ver historial clinico", "C:/Users/SergioR/Pictures/iconos/historial.png", sitio = "left", command= self.historial)
        crearBoton(self.menuDoctor, "Salir", "C:/Users/SergioR/Pictures/iconos/salir.png", sitio = "left", command= lambda: volver(self.menu_doctor))         
#----------------------------------------------------------------------------------

    def vercitas(self):
        if self.citas == []:
            messagebox.showinfo("Mensaje", "Usted no tiene citas agendadas.")
            return
        self.menuDoctor.pack_forget()
        self.frame_principal = tk.Frame(self.menu_doctor)
        self.frame_principal.pack()   
        df = pd.DataFrame(self.citas, columns=["Fecha", "Hora", "Cedula", "Estrato", "Nombre Paciente",])
        self.MostrarDF(df, self.frame_principal)
        self.siguiente = ttk.Button(self.frame_principal, text= "Siguiente", command= self.sensores)
        self.siguiente.pack()
        self.volver = ttk.Button(self.frame_principal, text= "Volver", command= lambda: self.volverMP(self.frame_principal))
        self.volver.pack(pady = 5)
    def vercitas2(self):
        self.seleccion = self.entry.get()
        if not self.seleccion:
            messagebox.showwarning("Mensaje", "Seleccione la cita")
            return
        self.siguiente.pack_forget()
        self.seleccion = int(self.seleccion)
        self.cedulaPaciente = self.citas[self.seleccion-1][2]
        self.fechadeuda = self.citas[self.seleccion-1][0]
        self.estratoPaciente = self.citas[self.seleccion-1][3]
        self.dto = self.descuento(self.estratoPaciente) 
        self.volver.pack_forget()
        addex = ttk.Button(self.frame_principal, text= "Agregar un examen.", command= self.agregarExamen)
        addex.pack(pady = 5)
        addmed = ttk.Button(self.frame_principal, text= "Agregar medicamentos.", command= self.agregarMedicamento)
        addmed.pack(pady = 5)
        self.volver.pack(pady = 5)
    def agregarExamen(self):
        for i in self.frame_principal.winfo_children():
            i.pack_forget()
        df = pd.DataFrame(self.examen, columns=["Nombre del examen", "Costo", "Código"])
        label = tk.Label(self.frame_principal, text= "Agregar examen:")
        label.pack(pady= 5)
        self.MostrarDF(df, self.frame_principal)
        agregar = ttk.Button(self.frame_principal, text= "agregar", command= self.agregrarExamenac)
        agregar.pack(pady = 5)
        self.volver.pack(pady = 5)
    def agregrarExamenac(self):
        index = self.entry.get()
        if not index:
            messagebox.showwarning("Mensaje", "Seleccione la cita el medicamento")
            return
        index = int(index)            
        nombreProducto = self.examen[index-1][0]
        costoProducto = self.examen[index-1][1][:]
        codigo = self.examen[index-1][2]
        costoProducto = float(costoProducto.replace("$", ""))
        costoProducto = round(costoProducto*self.dto, 3)
        self.base.deudas.append([self.fechadeuda, self.cedulaPaciente, nombreProducto, codigo, "$" + str(costoProducto), self.clasedoctor, self.nombreUsuario, 1, self.peso, self.temperatura])
        self.seguro = tk.Toplevel(self.menu_doctor)
        self.seguro.transient(self.menu_doctor)
        self.seguro.grab_set()
        self.seguro.title("¿ESTÁ SEGURO?")
        self.seguro.geometry("350x100")
        frame = tk.Frame(self.seguro)
        frame.pack()
        self.mensaje = tk.Label(frame, text = "¿Desea agrear otro examen o medicamento al paciente?", fg= "green")
        self.mensaje.pack()
        si = ttk.Button(frame, text = "SÍ", command= self.si)
        si.pack(side="left", padx=10, pady=10)
        no = ttk.Button(frame, text= "NO", command= self.no)
        no.pack(side="left", padx=10, pady=10) 
    
    def agregarMedicamento(self):
        for i in self.frame_principal.winfo_children():
            i.pack_forget()
        df = pd.DataFrame(self.base.LISTAGENERAL, columns=["Area", "Presentacion", "Marca", "Costo", "Codigo", "path"])
        df = df[["Area", "Presentacion", "Marca", "Costo", "Codigo"]]
        label = tk.Label(self.frame_principal, text= "Agregar medicamento:")  
        label.pack()
        self.entry = 0  
        self.MostrarDF(df, self.frame_principal)
        self.cantidad= ttk.Spinbox(self.frame_principal, from_=1, to=5, state= "readonly")
        self.cantidad.set(1)
        self.cantidad.pack()
        agregar = ttk.Button(self.frame_principal, text= "agregar", command= self.agregarMedicamentoac)
        agregar.pack(pady = 5)
        self.volver.pack(pady= 5)

    def agregarMedicamentoac(self):
        index = self.entry.get()
        if not index:
            messagebox.showwarning("Mensaje", "Seleccione la cita el medicamento")
            return
        index = int(index)
        nombreProducto = self.base.LISTAGENERAL[index-1][0]
        costoProducto = self.base.LISTAGENERAL[index-1][3][:]
        codigo = self.base.LISTAGENERAL[index-1][4]
        path = self.base.LISTAGENERAL[index-1][5]
        cantidad = int(self.cantidad.get())
        costoProducto = float(costoProducto.replace("$", ""))
        costoProducto = round(costoProducto*self.dto, 3)
        costoProducto = round(costoProducto*cantidad, 3)
        self.base.deudas.append([self.fechadeuda, self.cedulaPaciente, nombreProducto, codigo, "$" + str(costoProducto), self.clasedoctor, self.nombreUsuario, cantidad, self.peso, self.temperatura])
        self.seguro = tk.Toplevel(self.menu_doctor)
        self.seguro.transient(self.menu_doctor)
        self.seguro.grab_set()
        self.seguro.title("¿ESTÁ SEGURO?")
        self.seguro.geometry("350x350")
        frame = tk.Frame(self.seguro)
        frame.pack()
        self.mensaje = tk.Label(frame, text = "¿Desea agrear otro examen o medicamento al paciente?", fg= "green")
        self.mensaje.pack()
        imagen = Image.open(path)  
        imagen = imagen.resize((200, 200))
        self.imagen_tk = ImageTk.PhotoImage(imagen)
        label_foto = tk.Label(self.seguro, image=self.imagen_tk)
        label_foto.pack(pady=10)
        si = ttk.Button(frame, text = "SÍ", command= self.si)
        si.pack(side="left", padx=10, pady=10)
        no = ttk.Button(frame, text= "NO", command= self.no)
        no.pack(side="left", padx=10, pady=10) 

    def no(self):
        del self.citas[self.seleccion-1]
        self.seguro.destroy()
        self.contador = 0
        self.volverMP(self.frame_principal)
    def si(self):
        self.seguro.destroy()
        self.frame_principal.pack_forget()
        self.vercitas()
#----------------------------------------------------------------------------------
    def historial(self):
        self.menuDoctor.pack_forget()
        self.frame_principal = tk.Frame(self.menu_doctor)
        self.frame_principal.pack()
        label = tk.Label(self.frame_principal, text= "Ingrese el codigo del paciente a consultar:")
        label.pack()
        self.codigo = ttk.Entry(self.frame_principal) 
        self.codigo.pack()
        self.buscarb = ttk.Button(self.frame_principal, text = "buscar", command= self.buscar)
        self.buscarb.pack(pady =5)
        self.salir = ttk.Button(self.frame_principal, text= "salir", command= lambda: self.volverMP(self.frame_principal))
        self.salir.pack(pady =5)
    def buscar(self):
        LISTA = []
        codigo = self.codigo.get()
        index = busquedaselectiva(self.base.deudas, 1, codigo)
        if index == []:
            messagebox.showwarning("Mensaje", "paciente sin historial clinico")
            return
        for i in index:
            self.buscarb.pack_forget()
            self.salir.pack_forget()
            LISTA.append(self.base.deudas[i])
        self.menu_doctor.geometry("1200x700")
        df = pd.DataFrame(LISTA, columns=["Fecha:  ", "Cedula Paciente:  ", "Nombre del Producto:  ", "Código", "Costo", "Tipo de doctor:  ", "Nombre Doctor:  ", "Cantidad:  ", "Peso", "Temperatura"])
        df = df[["Fecha:  ", "Nombre Doctor:  ", "Tipo de doctor:  ", "Nombre del Producto:  ", "Cedula Paciente:  ", "Peso", "Temperatura"]]
        self.MostrarDF(df, self.frame_principal)
        self.salir.pack(pady = 5)
#----------------------------------------------------------------------------------
    def sensores(self):
        if self.contador == 1:
            self.vercitas2()
            return
        self.menuDoctor.pack_forget()
        self.senso = tk.Toplevel(self.menu_doctor)
        self.senso.transient(self.menu_doctor)
        self.senso.grab_set()
        self.var_dato = tk.StringVar()
        self.var_dato2  = tk.StringVar()
        label = tk.Label(self.senso, text= "Obtener dato")
        label.pack()
        self.entrada = ttk.Entry(self.senso, textvariable=self.var_dato, state= 'readonly')
        self.entrada.pack()
        self.entrada2 = ttk.Entry(self.senso, textvariable=self.var_dato2, state= 'readonly')
        self.entrada2.pack()
        boton = ttk.Button(self.senso, text= "obtener", command= self.obtenerDatos)
        boton.pack(pady= 5)
        volver = ttk.Button(self.senso, text= "salir", command=  lambda: self.volverPESO(self.senso))
        volver.pack(pady= 5)
        try:
            # Configuración de la comunicación serial
            puerto_serial = 'COM3'  # Reemplaza con el nombre correcto del puerto serial
            baudrate = 9600
            self.arduino = serial.Serial(puerto_serial, baudrate)
            self.recibir_datos()
        except SerialException:
            self.var_dato.set("Sin comunicación")  # Muestra un mensaje de error si no se puede establecer la conexión serial
    
    def recibir_datos(self):
        try:
            dato = self.arduino.readline().decode().strip()  # Lee el dato enviado por Arduino
            temperatura = dato[:20]
            peso = dato[-13:]
            self.var_dato.set(temperatura)  # Actualiza el valor de la variable StringVar con el dato recibido
            self.var_dato2.set(peso)
        except SerialException:
            self.var_dato.set("Sin comunicación")  
        
        self.senso.after(100, self.recibir_datos)  

    def obtenerDatos(self):
        print(self.entrada.get())
        print(self.entrada2.get())
        self.temperatura = self.entrada.get()
        self.peso = self.entrada2.get()
        self.contador = 1
        self.vercitas2()
        self.senso.destroy()

    def volverPESO(self, frame):
        frame.destroy()
        self.frame_principal.destroy()
        self.menuDoctor.pack(anchor= "nw", fill= "x")

#----------------------------------------------------------------------------------
    def tipoDoctor(self, tipoD):
        if tipoD == 1:
            return [self.base.examenesG, "Doctor General"]
        elif tipoD == 2:
            return [self.base.examenesE, "Doctor Especialista"]
        elif tipoD == 3:
            return [self.base.examenesC, "Cirujano"]
    def volverMP(self, ventana):
        ventana.destroy()
        self.menuDoctor.pack(anchor= "nw", fill= "x")
    def carnet(self):
        carnet = tk.Toplevel(self.menu_doctor)
        carnet.title("CARNET DOCTOR")
        carnet.geometry("300x400")
        imagen = Image.open(self.ruta)  
        imagen = imagen.resize((200, 200))
        self.imagen_tk = ImageTk.PhotoImage(imagen)
        label_foto = tk.Label(carnet, image=self.imagen_tk)
        label_foto.pack(pady=10)
        
        label_nombre = tk.Label(carnet, text=self.nombreUsuario, font=("Arial", 14))
        label_nombre.pack(pady=10)
        
        label_documento = tk.Label(carnet, text="Documento: " + str(self.cedulaUsuario), font=("Arial", 12))
        label_documento.pack(pady=10)

        label_tipod = tk.Label(carnet, text="Tipo de doctor: " + str(self.clasedoctor), font=("Arial", 12))
        label_tipod.pack(pady=10)
            
    def MostrarDF(self, dataframe, ventana):
        # Variable para almacenar el índice del doctor seleccionado
        selected_index = tk.StringVar()

        def on_select(event):
            selection = event.widget.selection()
            if selection:
                # Obtiene el índice de la fila seleccionada
                index = int(event.widget.index(selection))
                # Asigna el índice del doctor a la variable selected_index
                selected_index.set(str(index + 1))  # Suma 1 para tener índices basados en 1

        # Crea el Treeview
        self.treeview = ttk.Treeview(ventana, selectmode='browse')
        self.treeview.pack(side= "top")

        # Agrega columnas al Treeview
        columns = dataframe.columns.tolist()
        self.treeview['columns'] = columns

        # Ajusta el ancho de las columnas
        for column in columns:
            self.treeview.column(column, width=100)
            self.treeview.heading(column, text=column)

        self.treeview.column("#0", width=0, stretch=tk.NO)

        # Agrega filas al Treeview
        for index, row in dataframe.iterrows():
            values = row.tolist()
            self.treeview.insert('', 'end', values=values)

        # Asigna la función de control de eventos a la selección de filas
        self.treeview.bind('<<TreeviewSelect>>', on_select)
        self.entry = ttk.Entry(ventana, textvariable=selected_index, state="readonly")

    def descuento(self, estrato):
            if estrato == 1:
                dto = 0.50
                return dto
            elif estrato == 2:
                dto = 0.60
                return dto
            elif estrato == 3:
                dto = 0.70
                return dto
            elif estrato == 4:
                dto = 0.80
                return dto
            elif estrato == 5:
                dto = 0.90
                return dto
    
basedatos = baseDatos()
login = IniciarSesion(basedatos)
