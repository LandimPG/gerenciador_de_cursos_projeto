import sys
import os

# Ajusta o caminho para importar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gerenciadores.gerenciador_sistema import GerenciadorSistema
from src.interface.cli import MenuCli

def main():

    sistema = GerenciadorSistema()

    interface = MenuCli(sistema)

    interface.iniciar()

if __name__ == "__main__":

    main() # Carrega os dados iniciais
