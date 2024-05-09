class   TRAMAS:
    """
    Dicha Librería implementa diferentes funciones que permiten calcular el checksum
    de una trama y crear una nueva trama, que posteriormente se podrá enviar.
    """
    def __init__(self) -> None:
        pass
    def calcular_checksum(self,trama):
        """
        Esta función toma una trama(bytearray) como entrada y calcula 
        el checksum para esa trama. Devuelve el valor entero del checksum.
        """
        # Suma todos los valores ASCII de los caracteres en la trama  
        check = sum(trama) % 256
         # Calcular el complemento a 2 del resultado anterior
        checksum = (256-check) % 256
        return checksum 
    
    def crear_trama(self,direccion_destino, numero_bytes, direccion_origen, comando, datos=[]):
        """
        Esta función construye una trama de acuerdo con la estructura proporcionada.Tiene 5 argumentos
        Hay que tener en cuenta que los datos que se introducen deben estar en formato string 
        Python variable='XX'
        Robotframework  ${variable}=    XX
        También a la hora de introducir datos, estso deben estar en forma de lista datos 
        Python -->datos=['XX','ZZ',..]
        Robotframework--> @{datos}= XX ZZ ...
        Finalmente, se devuelve la trama creada.
        """
        # Convertir cadenas de texto a bytes 
        direccion_destino_bytes = bytes.fromhex(direccion_destino)
        numero_bytes_bytes = bytes.fromhex(numero_bytes)
        direccion_origen_bytes = bytes.fromhex(direccion_origen)
        comando_bytes = bytes.fromhex(comando)
        # La funcion puede no recibir datos, por eso comprueba longitud de datos
        # para ver si tiene que convertir los datos o dejarlo vacio
        if len(datos)>0:
            datos_bytes = [bytes.fromhex(dato) for dato in datos.split()]
    
        # Construir la trama en forma de bytearray (valores en código ASCII)
        trama = bytearray()
        trama.extend(direccion_destino_bytes)
        trama.extend(numero_bytes_bytes)
        trama.extend(direccion_origen_bytes)
        trama.extend(comando_bytes)
            
        # Agregar los datos a la trama, si estos tienen longitud mayor de 0
        if len(datos)>0:
            for dato in datos_bytes:
                trama.extend(dato)
        
        # Calcular el checksum
        checksum = self.calcular_checksum(trama)
        
        # Añadir el checksum a la trama
        trama.append(checksum)
        
        return trama