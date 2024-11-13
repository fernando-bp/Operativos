import random

class SistemaArchivos:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.espacio_libre = tamaño
        self.archivos = {}

    def mostrar_estado(self):
        print(f"Espacio libre: {self.espacio_libre}/{self.tamaño}")
        print("Archivos:", self.archivos)
0
class FAT32(SistemaArchivos):
    def __init__(self, tamaño):
        super().__init__(tamaño)
        self.FAT = [None] * tamaño

    def crear_archivo(self, nombre, tamaño):
        if tamaño > self.espacio_libre:
            print("Error: No hay suficiente espacio para crear el archivo.")
            return
        clusters = []
        for i in range(tamaño):
            while True:
                cluster = random.randint(0, self.tamaño - 1)
                if self.FAT[cluster] is None:
                    self.FAT[cluster] = nombre
                    clusters.append(cluster)
                    break
        self.archivos[nombre] = clusters
        self.espacio_libre -= tamaño
        print(f"Archivo '{nombre}' creado en clusters: {clusters}")

    def eliminar_archivo(self, nombre):
        if nombre not in self.archivos:
            print("Error: El archivo no existe.")
            return
        for cluster in self.archivos[nombre]:
            self.FAT[cluster] = None
        self.espacio_libre += len(self.archivos[nombre])
        del self.archivos[nombre]
        print(f"Archivo '{nombre}' eliminado.")

    def mostrar_estado_detallado(self):
        print("Estado del sistema FAT32:")
        for idx, value in enumerate(self.FAT):
            print(f"Cluster {idx}: {value}")
        self.mostrar_estado()

class Ext2(SistemaArchivos):
    def __init__(self, tamaño):
        super().__init__(tamaño)
        self.inodos = {}
        self.bloques = [None] * tamaño

    def crear_archivo(self, nombre, tamaño):
        if tamaño > self.espacio_libre:
            print("Error: No hay suficiente espacio para crear el archivo.")
            return
        bloques = []
        for i in range(tamaño):
            while True:
                bloque = random.randint(0, self.tamaño - 1)
                if self.bloques[bloque] is None:
                    self.bloques[bloque] = nombre
                    bloques.append(bloque)
                    break
        self.inodos[nombre] = bloques
        self.espacio_libre -= tamaño
        print(f"Archivo '{nombre}' creado en bloques: {bloques}")

    def eliminar_archivo(self, nombre):
        if nombre not in self.inodos:
            print("Error: El archivo no existe.")
            return
        for bloque in self.inodos[nombre]:
            self.bloques[bloque] = None
        self.espacio_libre += len(self.inodos[nombre])
        del self.inodos[nombre]
        print(f"Archivo '{nombre}' eliminado.")

    def mostrar_estado_detallado(self):
        print("Estado del sistema Ext2:")
        for idx, value in enumerate(self.bloques):
            print(f"Bloque {idx}: {value}")
        self.mostrar_estado()

# Prueba de estrés mejorada
def prueba_estres(sistema_archivos):
    for i in range(100):
        tamaño_archivo = random.randint(1, 5)  # Tamaño aleatorio entre 1 y 5
        sistema_archivos.crear_archivo(f"archivo_{i}", tamaño=tamaño_archivo)
    sistema_archivos.mostrar_estado_detallado()
    for i in range(100):
        sistema_archivos.eliminar_archivo(f"archivo_{i}")

# Ejecución de prueba de estrés en ambos sistemas
fat32 = FAT32(tamaño=200)
ext2 = Ext2(tamaño=200)

print("Prueba de estrés en FAT32")
prueba_estres(fat32)

print("\nPrueba de estrés en Ext2")
prueba_estres(ext2)
