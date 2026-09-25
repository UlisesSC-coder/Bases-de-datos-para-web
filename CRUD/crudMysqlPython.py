#Es 100% importacion de pymysql, no se necesita instalar nada adicional,
#  ya que pymysql es un modulo de Python que permite 
# interactuar con bases de datos MySQL.
import pymysql




def crear_tabla(conexion):
    sql = """
        CREATE TABLE IF NOT EXISTS usuario1 (
            idusuario INT PRIMARY KEY AUTO_INCREMENT,
            nombres VARCHAR(25) NOT NULL,
            apellidoPaterno VARCHAR(25) NOT NULL,
            apellidoMaterno VARCHAR(25) NOT NULL,
            `user` VARCHAR(10) NOT NULL,
            pwd VARCHAR(10) NOT NULL
        )
    """
    try:
        # Se utiliza un cursor para ejecutar la consulta SQL
        with conexion.cursor() as cursor:
            cursor.execute(sql)
        # Se confirma la transaccion para guardar los cambios en la base de datos
        conexion.commit()
        print("La tabla esta lista.")
    except pymysql.Error as error:
        conexion.rollback()
        print(f"No se pudo crear la tabla: {error}")


def insertar_datos(conexion):
    datos = (
        input("Dame los nombres del usuario: "),
        input("Dame el apellido paterno del usuario: "),
        input("Dame el apellido materno del usuario: "),
        input("Dame el usuario: "),
        input("Dame la contrasena: "),
    )
    sql = """
        INSERT INTO usuario1
        # Se especifican las columnas y los valores a insertar
            (nombres, apellidoPaterno, apellidoMaterno, `user`, pwd)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        with conexion.cursor() as cursor:
            # Se utiliza un cursor para ejecutar la consulta SQL con los datos proporcionados
            cursor.execute(sql, datos)
        conexion.commit()
        print("Registrado correctamente.")
    except pymysql.Error as error:
        conexion.rollback()
        print(f"No se pudo registrar el usuario: {error}")


def eliminar_datos(conexion):
    try:
        id_usuario = int(input("Dame el id del usuario: "))
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM usuario1 WHERE idusuario = %s", (id_usuario,))
            filas_eliminadas = cursor.rowcount
        conexion.commit()
        print("Eliminado correctamente." if filas_eliminadas else "No existe ese usuario.")
    except (ValueError, pymysql.Error) as error:
        conexion.rollback()
        print(f"No se pudo eliminar el usuario: {error}")


def actualizar_datos(conexion):
    try:
        id_usuario = int(input("Dame el id del usuario: "))
    except ValueError:
        print("El id debe ser un numero entero.")
        return

    datos = (
        input("Dame los nombres del usuario: "),
        input("Dame el apellido paterno del usuario: "),
        input("Dame el apellido materno del usuario: "),
        input("Dame el usuario: "),
        input("Dame la contrasena: "),
        id_usuario,
    )
    sql = """
        UPDATE usuario1
        SET nombres = %s, apellidoPaterno = %s, apellidoMaterno = %s,
            `user` = %s, pwd = %s
        WHERE idusuario = %s
    """
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, datos)
            filas_actualizadas = cursor.rowcount
        conexion.commit()
        print("Actualizado correctamente." if filas_actualizadas else "No existe ese usuario.")
    except pymysql.Error as error:
        conexion.rollback()
        print(f"No se pudo actualizar el usuario: {error}")


def listar_datos(conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                """SELECT idusuario, nombres, apellidoPaterno, apellidoMaterno,
                          `user`, pwd
                   FROM usuario1
                   ORDER BY idusuario"""
            )
            # Se obtiene todos los resultados de la consulta SQL
            usuarios = cursor.fetchall()
        if not usuarios:
            print("No hay usuarios registrados.")
            return
        for usuario in usuarios:
            print(usuario)

            
    except pymysql.Error as error: # Se captura cualquier error que ocurra durante la ejecucion de la consulta SQL
        print(f"No se pudieron listar los usuarios: {error}")


def main():
    try:
        # Esta variable nos permite establecer la conexion a la base de datos
        conexion = pymysql.connect(

            # Se especifica el host, usuario, contraseña, base de datos y codificación de caracteres
            host="localhost",
            user="root",
            password="",
            database="dbPython",
            charset="utf8mb4",
            autocommit=False,
        )
        print("Conexion exitosa.")

        
    except pymysql.Error as error: # Se captura cualquier error que ocurra durante la conexion a la base de datos
        print(f"No se pudo conectar a MySQL: {error}")
        return

    try:
        crear_tabla(conexion)
        while True:
            print("\n1. Insertar\n2. Listar\n3. Actualizar\n4. Eliminar\n5. Salir")
            opcion = input("Elige una opcion: ").strip()
            if opcion == "1":
                insertar_datos(conexion)
            elif opcion == "2":
                listar_datos(conexion)
            elif opcion == "3":
                actualizar_datos(conexion)
            elif opcion == "4":
                eliminar_datos(conexion)
            elif opcion == "5":
                break
            else:
                print("Opcion no valida.")
    finally:

        # Se cierra la conexion a la base de datos al finalizar el programa
        conexion.close()
        print("Conexion cerrada.")


if __name__ == "__main__":
    main()


