import os
import random
import sys
import time
import names
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import string

# ==================== COLORES ====================
RESET = "\033[0m"
ROJO = "\033[38;5;196m"
AZUL = "\033[38;5;27m"
MORADO = "\033[38;5;201m"
VERDE = "\033[38;5;46m"

def print_neon(text, color=MORADO):
    print(f"{color}{text}{RESET}")

class DavoComboGenerator:
    def __init__(self):
        self.combo_dir = "/storage/emulated/0/combo"
        os.makedirs(self.combo_dir, exist_ok=True)

    def mostrar_header(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""
{AZUL}╔════════════════════════════════════════════════════════════════════╗
{ROJO}  ◀◀  GENERADOR DE COMBOS DAVO  ▶▶
{AZUL}╚════════════════════════════════════════════════════════════════════╝{RESET}

{ROJO}   ██████╗  █████╗ ██╗   ██╗ ██████╗ 
   ██╔══██╗██╔══██╗██║   ██║██╔═══██╗
   ██║  ██║███████║██║   ██║██║   ██║
   ██║  ██║██╔══██║╚██╗ ██╔╝██║   ██║
   ██████╔╝██║  ██║ ╚████╔╝ ╚██████╔╝
   ╚═════╝ ╚═╝  ╚═╝  ╚═══╝   ╚═════╝ {RESET}

{MORADO}               ✦ DAVO CYBER POWER ✦
{AZUL}           NEON COMBO SYSTEM
{RESET}""")

    def neon_menu(self):
        print(f"""
{VERDE}╔════════════════════════════════════════════════════════════════════════════╗
{VERDE}║                  Menú de generador de Combos                               ║
{VERDE}╚════════════════════════════════════════════════════════════════════════════╝{RESET}

{ROJO}1.- User:Pass (Num. de 2000 a 2050)
{AZUL}2.- User:User (Nombre-Nombre)
{ROJO}3.- User:Pass (Núm. de 1 a 99)
{AZUL}4.- User:Pass (Núm. de 100 a 999)
{ROJO}5.- User:Pass (Alfanuméricos)
{AZUL}6.- User:Pass (Año de Nacimiento)
{ROJO}7.- User:Pass (2022 al 2028)
{AZUL}8.- User:Pass (Núm. de 111 a 999)
{ROJO}9.- User:Numero (123 a 123..9)
{AZUL}10.- User:Numero (12345..Random)
{ROJO}11.- Combos numéricos (numero:número)
{AZUL}12.- Nombre:Alfanuméricos
{ROJO}13.- Eliminar Líneas Duplicadas
{AZUL}14.- Salir
{RESET}""")

    def eliminar_duplicados(self):
        ruta = input(f"{AZUL}Ingrese la ruta del archivo: {RESET}").strip()
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                lines = f.readlines()
            unique = list(set(lines))
            dir_out = "/sdcard/SinDuplicadas"
            os.makedirs(dir_out, exist_ok=True)
            salida = os.path.join(dir_out, os.path.basename(ruta))
            
            with open(salida, "w", encoding="utf-8") as f:
                f.writelines(unique)
            print_neon(f"✅ Archivo limpio guardado en: {salida}", MORADO)
        except Exception as e:
            print_neon(f"❌ Error: {e}", ROJO)

    def generar_linea(self, opcion, modo="3", lista_nombres=None):
        base = random.choice(lista_nombres).strip() if lista_nombres else names.get_first_name()

        if opcion == "1":   # 2000 a 2050
            num = random.randint(2000, 2050)
            izq = f"{base}{num}"
            der = base
        elif opcion == "2": # Nombre-Nombre
            izq = base
            der = names.get_last_name() if not lista_nombres else random.choice(lista_nombres).strip()
        elif opcion == "3": # 1 a 99
            num = random.randint(1, 99)
            izq = f"{base}{num}"
            der = base
        elif opcion == "4": # 100 a 999
            num = random.randint(100, 999)
            izq = f"{base}{num}"
            der = base
        elif opcion == "5": # Alfanuméricos
            alfanum = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(4,8)))
            izq = f"{base}{alfanum}"
            der = base
        elif opcion == "6": # Año de Nacimiento
            num = random.randint(1900, 2026)
            izq = f"{base}{num}"
            der = base
        elif opcion == "7": # 2022 al 2028
            num = random.randint(2022, 2028)
            izq = f"{base}{num}"
            der = base
        elif opcion == "8": # 111 a 999
            num = random.choice([str(i*111) for i in range(1,10)])
            izq = f"{base}{num}"
            der = base
        elif opcion == "9": # 123 a 123..9
            num = random.choice(["123","1234","12345","123456","321","4321","54321"])
            izq = base
            der = num
        elif opcion == "10": # Largo Random
            num = ''.join(random.choices(string.digits, k=random.randint(5,9)))
            izq = base
            der = num
        elif opcion == "11": # Numérico : Numérico
            return f"{random.randint(10000,999999)}:{random.randint(10000,999999)}"
        elif opcion == "12": # Nombre:Alfanumérico
            alfanum = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6,10)))
            izq = base
            der = alfanum
        else:
            izq = base
            der = base

        if modo == "1": return f"{izq}:{der}"
        if modo == "2": return f"{der}:{izq}"
        return f"{izq}:{der}" if random.random() < 0.5 else f"{der}:{izq}"

    def generar_combos(self, opcion):
        nombre = input(f"{AZUL}Nombre del archivo: {RESET}").strip()
        ruta_salida = os.path.join(self.combo_dir, f"{nombre}.txt")

        cantidad = int(input(f"{AZUL}Cantidad de líneas: {RESET}"))
        hilos = max(1, min(15, int(input(f"{MORADO}Hilos (1-15): {RESET}"))))

        modo = "3"
        if str(opcion) not in ["11", "12"]:
            print_neon("1 = Izquierda   2 = Derecha   3 = Ambos (Recomendado)", MORADO)
            modo = input(f"{AZUL}Elige: {RESET}").strip() or "3"

        lista_nombres = None
        if input(f"{MORADO}¿Usar lista propia? (1=Sí / Enter=No): {RESET}") == "1":
            ruta = input(f"{AZUL}Ruta del archivo: {RESET}").strip()
            if os.path.exists(ruta):
                with open(ruta, "r", encoding="utf-8") as f:
                    lista_nombres = [line.strip() for line in f if line.strip()]

        lock = threading.Lock()
        generados = set()

        def worker():
            while len(generados) < cantidad:
                linea = self.generar_linea(opcion, modo, lista_nombres)
                linea_nl = linea + "\n"
                with lock:
                    if linea_nl not in generados:
                        generados.add(linea_nl)
                        with open(ruta_salida, "a", encoding="utf-8") as f:
                            f.write(linea_nl)
                        return True
            return False

        with tqdm(total=cantidad, desc="Generando", ncols=80, colour="red") as pbar:
            with ThreadPoolExecutor(max_workers=hilos) as executor:
                futures = [executor.submit(worker) for _ in range(cantidad)]
                for _ in as_completed(futures):
                    pbar.update(1)

        print_neon(f"\n✅ Combo guardado en: {ruta_salida}", MORADO)

    def menu_principal(self):
        while True:
            self.mostrar_header()
            self.neon_menu()
            
            opcion = input(f"{ROJO}Ingrese su elección → {RESET}").strip()

            if opcion == "14":
                print_neon("\n👊 Gracias por usar DAVO Combo Generator", ROJO)
                sys.exit()
            elif opcion == "13":
                self.eliminar_duplicados()
                input(f"{AZUL}\nPresiona Enter...{RESET}")
            elif opcion in [str(i) for i in range(1,13)]:
                self.generar_combos(opcion)
                input(f"{AZUL}\nPresiona Enter para volver al menú...{RESET}")
            else:
                print_neon("❌ Opción inválida", ROJO)
                time.sleep(1)

if __name__ == "__main__":
    try:
        generator = DavoComboGenerator()
        generator.menu_principal()
    except KeyboardInterrupt:
        print_neon("\n\n👊 Saliendo...", ROJO)