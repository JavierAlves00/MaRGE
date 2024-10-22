#---------------------------------------------  Variables globales ----------------------------
vg_idioma = "" # Idioma de la aplicación
vg_logo = "" # carga del logotipo empresa
vg_qss = "" # carga hoja de estilos
vg_ancho_pantalla = 0# resolución pantalla width
vg_alto_pantalla = 0# resolución pantalla height
vg_ruta_app = ""
vg_idUsuario = 0
vg_usuario_nombre = ""
vg_usuario_nivel = ""
vg_icon_patch = ""
vg_medidaPeso = ""
vg_paciente = "" #guarda el dni del paciente para crear la carpeta de adquisiciones
vg_apellido1 = ""
vg_apellido2 = ""
vg_nombre = ""
vg_cipnsns = ""
vg_fNacimiento = ""
vg_altura = ""
vg_peso = ""
vg_genero = ""
vg_fAlta = ""
vg_hAlta = ""
vg_observaciones = ""
vg_edad = ""
vg_fechaHora = "" #guarda en formato ddmmyyyy_hhmmss para crear la carpeta en adquisiciones
vg_id_paciente = ""
vg_id_estudio = ""
vg_id_protocolo = ""
vg_protocolo_secuencia = ""
vg_id_nombre_protocolo = ""
vg_id_lado = ""
vg_id_orientacion = ""
vg_vengo_buscar = False
vg_mensaje = ""
vg_ruta_dicom =""
vg_unidad_usb =""
a_frm_buscar_exp = False
#----------------------------------------------------------------------------------------------

#----------------------------------------- textos app idioma ----------------------------------
vg_aceptar = ""
vg_cancelar = ""
vg_salir = ""
vg_msg_eliminar = ""
vg_usuario = ""
vg_contrasenya = ""
msg_contrasenya = ""
msg_contrasenya2 = ""

#----------------------------------------------------------------------------------------------

main_gui = None

# marcos procesos iniciados de actualizar MaRCoS, iniciar MaRCoS y pasar a enabled GPA/RFPA
vg_act_marcos = False
vg_ini_marcos = False
vg_gpa_rfpa = False