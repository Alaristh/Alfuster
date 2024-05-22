import requests
import argparse
import subprocess
from tqdm import tqdm
from colorama import init, Fore, Style

# Inicializar colorama
init()

def print_figlet():
    result = subprocess.run(['figlet', 'Alfuster'], capture_output=True, text=True)
    print(result.stdout)
    print(Fore.CYAN + "Made by Alaris ---> https://github.com" + Style.RESET_ALL)
    print('-' * 80)

def brute_force(url, wordlist):
    try:
        with open(wordlist, 'r') as file:
            directories = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: El archivo {wordlist} no existe.")
        return
    except PermissionError:
        print(f"Error: No tienes permiso para leer el archivo {wordlist}.")
        return
    
    found_directories = []
    
    try:
        # Inicializar tqdm para la barra de progreso
        with tqdm(total=len(directories), desc="Brute Forcing", unit="dir") as pbar:
            for directory in directories:
                full_url = f"{url}/{directory}"
                try:
                    response = requests.get(full_url)
                    if response.status_code == 200:
                        found_directories.append(full_url)
                except requests.RequestException as e:
                    print(f"Error al hacer la solicitud a {full_url}: {e}")
                finally:
                    pbar.update(1)  # Actualizar la barra de progreso
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario. Cerrando...")
        return

    # Imprimir los directorios encontrados al final
    for found in found_directories:
        print(f"[+] Found: {found}")

def main():
    # Imprimir créditos al inicio
    print_figlet()
    
    parser = argparse.ArgumentParser(description="Web Directory Brute Force Tool")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    
    args = parser.parse_args()
    
    # Verificar que la URL no termina con una barra
    if args.url.endswith('/'):
        args.url = args.url.rstrip('/')
    
    # Comprobar si la URL es válida
    if not args.url.startswith(('http://', 'https://')):
        print("Error: La URL debe comenzar con 'http://' o 'https://'.")
        return
    
    brute_force(args.url, args.wordlist)

if __name__ == "__main__":
    main()

