# -*- coding: utf-8 -*-
from os import name
from flask import Flask, render_template, request, session, url_for, redirect, session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

usuario = {}

producto_usuarios = {"Pax Noche Caja X 6 Sobres Granulos Panela Limon": [], "Condones Durex Extra Seguro 3 Unidades": [], "Sevedol Extra Fuerte Caja X 24 Tabletas": [], "Crema NIVEA cuidado nutritivo 100 ml": []}
# segunda variable para no añadir al carrito, servira para el perfil
producto_usuarios2 = {"Pax Noche Caja X 6 Sobres Granulos Panela Limon": [], "Condones Durex Extra Seguro 3 Unidades": [], "Sevedol Extra Fuerte Caja X 24 Tabletas": [], "Crema NIVEA cuidado nutritivo 100 ml": []}


descripcion_producto = {
    "Pax Noche Caja X 6 Sobres Granulos Panela Limon": {
    "imagen": "https://www.cruzverde.com.co/dw/image/v2/BDPM_PRD/on/demandware.static/-/Sites-masterCatalog_Colombia/default/dw7b74d7be/images/large/105031-1-PAX-CALIENTE-NOCHE--500+10+2-MG-GRANULA-CAJ-X-6SOB-X-6GR-PANELA-LIMON.jpg?sw=1000&sh=1000",
    "Valor": "11,000",
    },
    "Condones Durex Extra Seguro 3 Unidades": {
    "imagen": "https://www.cruzverde.com.co/dw/image/v2/BDPM_PRD/on/demandware.static/-/Sites-masterCatalog_Colombia/default/dw05bd6a7a/images/large/111351-1-PRESERVAT-EXTRA-SEGURO-CAJ-X-3-DUREX.jpg?sw=1000&sh=1000",
    "Valor": "7,200",
    },
    "Sevedol Extra Fuerte Caja X 24 Tabletas": {
    "imagen": "https://jumbocolombiafood.vteximg.com.br/arquivos/ids/3518334-1000-1000/7702870070536.jpg?v=637287046652400000",
    "Valor": "35,000",
    },
    "Crema NIVEA cuidado nutritivo 100 ml": {
    "imagen": "https://mercaldas.vtexassets.com/arquivos/ids/189095/Crema-NIVEA-100-Cuidado-Nutritivo_43232.jpg?v=6372361980431000000",
    "Valor": "15,100",
    }
    }


app = Flask(__name__)
app.secret_key = "ajhsdg56dkgasdhbs"


#----------------------- cambio de menu --------------------------
@app.route('/')
def inicio():
    if 'user' in session:
        return render_template('inicio.html', mostrar_login=False)
    return render_template('inicio.html', mostrar_login=True)

@app.route('/registro')
def registro():
    if 'user' in session:
        return render_template('registro.html', mostrar_login=False)
    return render_template('registro.html', mostrar_login=True)

@app.route('/interfazproductos')
def productos():
    if 'user' in session:
        return render_template('productos.html', mostrar_login=False)
    return render_template('productos.html', mostrar_login=True)

#----------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/contacto_dos')
def contacto_dos():
    return render_template('contacto_dos.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/politicas')
def politicas():
    return render_template('politicas.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/mas')
def mas():
    return render_template('mas.html')

#----------------- perfil -----------------

@app.route('/perfil')
def perfil():
    
    if 'user' in session:
        name = session['user']
        #usuario2 = usuario[correo]["correo"]
        arreglo_productos = []
        for producto in producto_usuarios2 :
            for correo_usuario in producto_usuarios2[producto]:
                if correo_usuario == name:
                    producto_comprado = []
                    producto_comprado.append(producto)
                    producto_comprado.append(descripcion_producto[producto]['imagen'])
                    producto_comprado.append(descripcion_producto[producto]['Valor'])
                    arreglo_productos.append(producto_comprado)
    return render_template('perfil.html', arreglo_productos = arreglo_productos, nombre_usuario=name) #nombre_usuario2=usuario2 )
    



#------------------------ realizar compra --------------------------------

@app.route('/t_realizar_compra')
def realizar_compra():
    if 'user' in session:
        correo = session['user']
        return render_template('t_realizar_compra.html')
    return render_template('out.html')


#--------------------------- compra definitiva---------------------------

@app.route('/comprar/<producto>')
def comprar_producto(producto):
    if 'user' in session:
        correo = session['user']
        print("parametro de ruta que llega: ", producto)
        productos = producto
        if producto == "Pax Noche Caja X 6 Sobres Granulos Panela Limon" or producto == "Condones Durex Extra Seguro 3 Unidades" or producto == "Crema NIVEA cuidado nutritivo 100 ml" or producto == "Sevedol Extra Fuerte Caja X 24 Tabletas":
            producto_usuarios2[producto].append(correo)
            print("Compra exitosa ", producto_usuarios2)
        else:
            return "Por favor compre un producto existente", 401
    
        #credenciales
        proveedor_correo = 'smtp.live.com: 587'
        remitente = 'C4milo311@outlook.com'
        password = 'Camilo311'
        #conexion a servidor
        servidor = smtplib.SMTP(proveedor_correo)
        servidor.starttls()
        servidor.ehlo()
        #autenticacion
        servidor.login(remitente, password)
        #mensaje 
        mensaje = "<h1>Has comprado el producto <b>{}</b> satisfactoriamente en Healthy Corporation</h1>".format(producto)
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = correo
        msg['Subject'] = 'Healthy Corporation'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
    return render_template('comprar_producto.html', nombre_usuario=correo, producto2=producto), 201

#------------------------ añadir producto --------------------------------

@app.route('/añadir_productos/<producto>')
def comprar_produd(producto):
    #aca verificamos si la cookie es valida y extraemos el correo
    #del usuario
    if 'user' in session:
        print("parametro de ruta que llega: ", producto)
        #aca extraemos el email del usuario
        correo = session['user']
        productos = producto
        #HACEMOS LA INSCRIPCION AL CURSO MEDIANTE SU correo
        if producto == "Pax Noche Caja X 6 Sobres Granulos Panela Limon" or producto == "Condones Durex Extra Seguro 3 Unidades" or producto == "Crema NIVEA cuidado nutritivo 100 ml" or producto == "Sevedol Extra Fuerte Caja X 24 Tabletas":
            producto_usuarios[producto].append(correo)
            print("Añadido al carrito ", producto_usuarios)
        else:
            return "Por favor añada un producto existente", 401
        
        return render_template('añadir_carrito.html', nombre_usuario=correo, producto2=productos), 201
    return render_template('out.html')



#-------------------------- carrito ------------------------------

@app.route('/carrito')
def carrrito():
    if 'user' in session:
        correo = session['user']
        arreglo_productos = []
        for producto in producto_usuarios :
            for correo_usuario in producto_usuarios[producto]:
                if correo_usuario == correo:
                    producto_comprado = []
                    producto_comprado.append(producto)
                    producto_comprado.append(descripcion_producto[producto]['imagen'])
                    producto_comprado.append(descripcion_producto[producto]['Valor'])
                    arreglo_productos.append(producto_comprado)
        return render_template('carrito.html', arreglo_productos = arreglo_productos)
    return render_template('out.html')



#------------------------- quitar producto -------------------------------

@app.route('/quitarproducto/<producto>')
def quitar_producto(producto):

    return "Usted ha quitado el producto {}".format(producto)



#------------------------- registro -------------------------------

@app.route('/formulario_registro', methods=['POST'])
def formulario_registro():
    name = request.form.get("name")
    correo = request.form.get("correo")
    password = request.form.get("password")
    print("--------", correo, password)
    usuario[correo] = {}
    usuario[correo]["password"] = password
    usuario[correo]["nombre"] = correo
    print("diccionario de usuarios: ", usuario)
    
    #credenciales
    proveedor_correo = 'smtp.live.com: 587'
    remitente = 'C4milo311@outlook.com'
    password = 'Camilo311'
    #conexion a servidor
    servidor = smtplib.SMTP(proveedor_correo)
    servidor.starttls()
    servidor.ehlo()
    #autenticacion
    servidor.login(remitente, password)
    #mensaje 
    mensaje = "<h1>Te haz registrado satisfactoriamente en Healthy Corporation {}</h1>".format(name)
    msg = MIMEMultipart()
    msg.attach(MIMEText(mensaje, 'html'))
    msg['From'] = remitente
    msg['To'] = correo
    msg['Subject'] = 'Bienvenido a Healthy Corporation'
    servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
    
    return render_template('login.html')

    

#---------------------- login ----------------------------------  

@app.route('/formulario_login', methods=['POST'])
def formulario_login():
    nombre = request.form.get("nombre")
    password = request.form.get("password")
    print("lllllllll ", nombre, password)
    if usuario.get(nombre):
        if usuario[nombre]["password"] == password:
            nombre = usuario[nombre]["nombre"]
            session['user'] = nombre
            return render_template('perfil.html', nombre_usuario=nombre)
        return render_template('contraseña_incorecta.html')
    return render_template('not_login.html')



#----------------------- eliminar cookie -----------------------------
# para perfil tambien

@app.route('/cerrar')
def cerrar_sesion():
    if 'user' in session:
        session.pop("user")
        return render_template('out2.html')
    return "Usted no tiene una sesion iniciada"


#------------------------------------------------- formularios de compra ----------------------------------------------------
 







#actualizae la pagina rapido
if __name__ == "__main__":
    app.run(debug = True, port=5000)