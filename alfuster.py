import requests
import argparse
import subprocess
from tqdm import tqdm
from colorama import init, Fore, Style, Back
from concurrent.futures import ThreadPoolExecutor, as_completed

# Inicializar colorama
init(autoreset=True)

def print_figlet():
    result = subprocess.run(['figlet', 'Alfuster'], capture_output=True, text=True)
    print(Fore.RED + Style.BRIGHT + result.stdout + Style.RESET_ALL)
    print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "Made by Alaris ---> https://github.com/Alaristh" + Style.RESET_ALL)
    print(Fore.RED + Back.BLACK + Style.BRIGHT + '-' * 80 + Style.RESET_ALL)
    print(Fore.RED + Back.BLACK + Style.BRIGHT + "DISCLAIMER: I am not responsible for any misuse of this tool. Use it at your own risk." + Style.RESET_ALL)
    print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "© Alaris" + Style.RESET_ALL)
    print(Fore.RED + Back.BLACK + Style.BRIGHT + '-' * 80 + Style.RESET_ALL)

def check_directory(url, directory):
    full_url = f"{url}/{directory}"
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code == 200:
            return full_url
    except requests.RequestException:
        pass
    return None

def brute_force(url, wordlist, max_workers=10):
    try:
        with open(wordlist, 'r') as file:
            directories = file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The file {wordlist} does not exist.{Style.RESET_ALL}")
        return
    except PermissionError:
        print(f"{Fore.RED}Error: You do not have permission to read the file {wordlist}.{Style.RESET_ALL}")
        return
    
    found_directories = []
    
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_directory = {executor.submit(check_directory, url, directory): directory for directory in directories}
            
            # Inicializar tqdm para la barra de progreso con colores personalizados
            with tqdm(total=len(directories), desc=Fore.WHITE + "Brute Forcing" + Style.RESET_ALL, unit="dir", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.RED, Style.RESET_ALL)) as pbar:
                for future in as_completed(future_to_directory):
                    directory = future_to_directory[future]
                    try:
                        result = future.result()
                        if result:
                            found_directories.append(result)
                            tqdm.write(Fore.WHITE + Style.BRIGHT + f"[+] Found: {result}" + Style.RESET_ALL)  # Mostrar directorio encontrado sin interferir con tqdm
                    except Exception as e:
                        tqdm.write(Fore.RED + f"Error processing {directory}: {e}" + Style.RESET_ALL)
                    pbar.update(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted by the user. Shutting down..." + Style.RESET_ALL)
        return

    # Imprimir los directorios encontrados al final
    print(Fore.RED + Back.BLACK + Style.BRIGHT + "\nSummary of found directories:" + Style.RESET_ALL)
    for found in found_directories:
        print(Fore.WHITE + Style.BRIGHT + f"[+] Found: {found}" + Style.RESET_ALL)

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
        print(Fore.RED + "Error: The URL must start with 'http://' or 'https://'." + Style.RESET_ALL)
        return
    
    brute_force(args.url, args.wordlist)

if __name__ == "__main__":
    main()
