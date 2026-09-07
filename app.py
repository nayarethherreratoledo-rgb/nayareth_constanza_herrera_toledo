# ======================================================
# SISTEMA DE GESTIÓN DE PACIENTES
# CLÍNICA SALUDTOTAL
# ======================================================

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():

    conexion = mysql.connector.connect(

        host="localhost",

        user="root",

        password="654321",

        database="saludtotal"

    )

    return conexion

# ======================================================
# FUNCIÓN AGREGAR PACIENTE
# ======================================================

def agregar():

    nombre = txt_nombre.get().strip()
    edad = txt_edad.get().strip()
    genero = combo_genero.get().strip()
    historial = txt_historial.get("1.0", tk.END).strip()
    tratamiento = txt_tratamiento.get().strip()
    medicamento = txt_medicamento.get().strip()
    contacto = txt_contacto.get().strip()

    if nombre == "":
        messagebox.showwarning("Aviso", "Debe ingresar el nombre del paciente.")
        return

    if not edad.isdigit():
        messagebox.showwarning("Aviso", "La edad debe ser un número entero.")
        return

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO Pacientes
        (Nombre, Edad, Genero, HistorialMedico, Tratamiento, Medicamento, Contacto)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        datos = (
            nombre,
            int(edad),
            genero,
            historial,
            tratamiento,
            medicamento,
            contacto
        )

        cursor.execute(sql, datos)
        conexion.commit()

        cursor.close()
        conexion.close()

        messagebox.showinfo(
            "Registro",
            "Paciente agregado correctamente."
        )

        limpiar()
        mostrar()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No fue posible agregar el paciente.\n\nDetalle del error:\n{error}"
        )


# ======================================================
# FUNCIÓN MOSTRAR PACIENTES
# ======================================================

def mostrar():

    try:
        for fila in tabla.get_children():
            tabla.delete(fila)

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Pacientes")

        registros = cursor.fetchall()

        for registro in registros:
            tabla.insert("", tk.END, values=registro)

        cursor.close()
        conexion.close()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No fue posible mostrar los pacientes.\n\nDetalle del error:\n{error}"
        )


# ======================================================
# LIMPIAR FORMULARIO
# ======================================================

def limpiar():

    txt_id.config(state="normal")
    txt_id.delete(0, tk.END)
    txt_id.config(state="readonly")

    txt_nombre.delete(0, tk.END)

    txt_edad.delete(0, tk.END)

    combo_genero.set("")

    txt_historial.delete("1.0", tk.END)

    txt_tratamiento.delete(0, tk.END)

    txt_medicamento.delete(0, tk.END)

    txt_contacto.delete(0, tk.END)


# ======================================================
# CARGAR DATOS EN EL FORMULARIO
# ======================================================

def seleccionar(event):

    seleccion = tabla.focus()

    if seleccion == "":
        return

    datos = tabla.item(seleccion)

    fila = datos["values"]

    txt_id.config(state="normal")
    txt_id.delete(0, tk.END)
    txt_id.insert(0, fila[0])
    txt_id.config(state="readonly")

    txt_nombre.delete(0, tk.END)
    txt_nombre.insert(0, fila[1])

    txt_edad.delete(0, tk.END)
    txt_edad.insert(0, fila[2])

    combo_genero.set(fila[3])

    txt_historial.delete("1.0", tk.END)
    txt_historial.insert("1.0", fila[4])

    txt_tratamiento.delete(0, tk.END)
    txt_tratamiento.insert(0, fila[5])

    txt_medicamento.delete(0, tk.END)
    txt_medicamento.insert(0, fila[6])

    txt_contacto.delete(0, tk.END)
    txt_contacto.insert(0, fila[7])


# ======================================================
# VENTANA PRINCIPAL
# ======================================================

ventana = tk.Tk()

ventana.title("Clínica SaludTotal")

ventana.geometry("980x720")

ventana.resizable(False, False)


# ======================================================
# TÍTULO
# ======================================================

titulo = tk.Label(

    ventana,

    text="Sistema de Gestión de Pacientes - Clínica SaludTotal",

    font=("Arial", 16, "bold")

)

titulo.pack(pady=10)


# ======================================================
# FRAME DATOS DEL PACIENTE
# ======================================================

frame = tk.LabelFrame(

    ventana,

    text="Datos del Paciente",

    padx=10,

    pady=10

)

frame.pack(fill="x", padx=10)


# ======================================================
# FILA 1
# ======================================================

tk.Label(frame, text="ID").grid(row=0, column=0, padx=5, pady=5)

txt_id = tk.Entry(frame, width=10, state="readonly")

txt_id.grid(row=0, column=1)


tk.Label(frame, text="Nombre").grid(row=0, column=2)

txt_nombre = tk.Entry(frame, width=35)

txt_nombre.grid(row=0, column=3)


# ======================================================
# FILA 2
# ======================================================

tk.Label(frame, text="Edad").grid(row=1, column=0)

txt_edad = tk.Entry(frame, width=10)

txt_edad.grid(row=1, column=1)


tk.Label(frame, text="Género").grid(row=1, column=2)

combo_genero = ttk.Combobox(
    frame,
    width=32,
    values=["Masculino", "Femenino", "Otro"],
    state="readonly"
)

combo_genero.grid(row=1, column=3)


# ======================================================
# FILA 3
# ======================================================

tk.Label(frame, text="Contacto").grid(row=2, column=0)

txt_contacto = tk.Entry(frame, width=50)

txt_contacto.grid(

    row=2,

    column=1,

    columnspan=3,

    sticky="we"

)


# ======================================================
# FILA 4
# ======================================================

tk.Label(frame, text="Historial Médico").grid(row=3, column=0)

txt_historial = tk.Text(

    frame,

    width=60,

    height=5

)

txt_historial.grid(

    row=3,

    column=1,

    columnspan=3,

    pady=5

)


# ======================================================
# FILA 5
# ======================================================

tk.Label(frame, text="Tratamiento").grid(row=4, column=0)

txt_tratamiento = tk.Entry(frame, width=50)

txt_tratamiento.grid(

    row=4,

    column=1,

    columnspan=3,

    sticky="we"

)


# ======================================================
# FILA 6
# ======================================================

tk.Label(frame, text="Medicamento").grid(row=5, column=0)

txt_medicamento = tk.Entry(frame, width=50)

txt_medicamento.grid(

    row=5,

    column=1,

    columnspan=3,

    sticky="we"

)

# ======================================================
# ACTUALIZAR PACIENTE
# ======================================================

def actualizar():

    if txt_id.get() == "":
        messagebox.showwarning(
            "Aviso",
            "Seleccione un paciente."
        )
        return

    nombre = txt_nombre.get().strip()
    edad = txt_edad.get().strip()
    genero = combo_genero.get().strip()
    historial = txt_historial.get("1.0", tk.END).strip()
    tratamiento = txt_tratamiento.get().strip()
    medicamento = txt_medicamento.get().strip()
    contacto = txt_contacto.get().strip()

    if nombre == "":
        messagebox.showwarning("Aviso", "Debe ingresar el nombre del paciente.")
        return

    if not edad.isdigit():
        messagebox.showwarning("Aviso", "La edad debe ser un número entero.")
        return

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE Pacientes
        SET Nombre=%s,
            Edad=%s,
            Genero=%s,
            HistorialMedico=%s,
            Tratamiento=%s,
            Medicamento=%s,
            Contacto=%s
        WHERE ID=%s
        """

        datos = (
            nombre,
            int(edad),
            genero,
            historial,
            tratamiento,
            medicamento,
            contacto,
            txt_id.get()
        )

        cursor.execute(sql, datos)
        conexion.commit()

        cursor.close()
        conexion.close()

        messagebox.showinfo(
            "Actualización",
            "Paciente actualizado correctamente."
        )

        limpiar()
        mostrar()

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No fue posible actualizar el paciente.\n\nDetalle del error:\n{error}"
        )


# ======================================================
# ELIMINAR PACIENTE
# ======================================================

def eliminar():

    if txt_id.get() == "":
        messagebox.showwarning(
            "Aviso",
            "Seleccione un paciente."
        )
        return

    respuesta = messagebox.askyesno(
        "Confirmación",
        "¿Desea eliminar este paciente?"
    )

    if respuesta:
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "DELETE FROM Pacientes WHERE ID=%s",
                (txt_id.get(),)
            )

            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo(
                "Eliminar",
                "Paciente eliminado correctamente."
            )

            limpiar()
            mostrar()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible eliminar el paciente.\n\nDetalle del error:\n{error}"
            )


# ======================================================
# GENERAR INFORME
# ======================================================

def generar_informe():

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM Pacientes")

        pacientes = cursor.fetchall()

        cursor.close()
        conexion.close()

        informe = ""

        informe += "========= INFORME DE PACIENTES =========\n\n"

        informe += f"Total de pacientes registrados: {len(pacientes)}\n\n"

        for paciente in pacientes:

            informe += f"ID: {paciente[0]}\n"
            informe += f"Nombre: {paciente[1]}\n"
            informe += f"Edad: {paciente[2]}\n"
            informe += f"Género: {paciente[3]}\n"
            informe += f"Historial: {paciente[4]}\n"
            informe += f"Tratamiento: {paciente[5]}\n"
            informe += f"Medicamento: {paciente[6]}\n"
            informe += f"Contacto: {paciente[7]}\n"
            informe += "--------------------------------------\n"

        messagebox.showinfo(
            "Informe",
            informe
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No fue posible generar el informe.\n\nDetalle del error:\n{error}"
        )


# ======================================================
# FRAME BOTONES
# ======================================================

frame_botones = tk.Frame(ventana)

frame_botones.pack(pady=10)


btn_agregar = tk.Button(

    frame_botones,

    text="Agregar",

    width=15,

    command=agregar

)

btn_agregar.grid(row=0, column=0, padx=5)


btn_actualizar = tk.Button(

    frame_botones,

    text="Actualizar",

    width=15,

    command=actualizar

)

btn_actualizar.grid(row=0, column=1, padx=5)


btn_eliminar = tk.Button(

    frame_botones,

    text="Eliminar",

    width=15,

    command=eliminar

)

btn_eliminar.grid(row=0, column=2, padx=5)


btn_mostrar = tk.Button(

    frame_botones,

    text="Mostrar",

    width=15,

    command=mostrar

)

btn_mostrar.grid(row=0, column=3, padx=5)


btn_limpiar = tk.Button(

    frame_botones,

    text="Limpiar",

    width=15,

    command=limpiar

)

btn_limpiar.grid(row=0, column=4, padx=5)


btn_informe = tk.Button(

    frame_botones,

    text="Generar Informe",

    width=18,

    command=generar_informe

)

btn_informe.grid(row=0, column=5, padx=5)


# ======================================================
# TREEVIEW
# ======================================================

tabla = ttk.Treeview(
    ventana,
    columns=(
        "ID",
        "Nombre",
        "Edad",
        "Genero",
        "Historial",
        "Tratamiento",
        "Medicamento",
        "Contacto"
    ),
    show="headings",
    height=12
)

tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")
tabla.heading("Genero", text="Género")
tabla.heading("Historial", text="Historial Médico")
tabla.heading("Tratamiento", text="Tratamiento")
tabla.heading("Medicamento", text="Medicamento")
tabla.heading("Contacto", text="Contacto")

tabla.column("ID", width=45, anchor="center")
tabla.column("Nombre", width=160)
tabla.column("Edad", width=55, anchor="center")
tabla.column("Genero", width=90, anchor="center")
tabla.column("Historial", width=180)
tabla.column("Tratamiento", width=150)
tabla.column("Medicamento", width=150)
tabla.column("Contacto", width=170)

tabla.pack(
    padx=10,
    pady=10,
    fill="both"
)

tabla.bind(
    "<<TreeviewSelect>>",
    seleccionar
)

# ======================================================
# CARGAR LOS PACIENTES AL INICIAR
# ======================================================

try:

    mostrar()

except Exception as error:

    messagebox.showerror(

        "Error",

        f"""No fue posible conectar con la base de datos.

Verifique que:

• MySQL esté iniciado.
• La base de datos 'saludtotal' exista.
• Las credenciales de la función conectar() sean correctas.

Detalle del error:

{error}
"""

    )


# ======================================================
# INICIAR LA APLICACIÓN
# ======================================================

ventana.mainloop()