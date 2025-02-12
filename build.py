import Pyinstaller.__main__
import os
from pathlib import Path

def create_executable():
    # Diretório atual do script
    current_dir = Path(__file__).parent.absolute()

    # Nome do arquivo principal
    main_file = str(current_dir / "middleware.py")

    # Nome do executável
    exe_name = "OctopusTaxMiddleware"

    # Ícone do executável (opcional)
    icon_path = str(current_dir / "icon.ico") if (current_dir / "icon.ico").exists() else None
    
    # Configuração do Pyinstaller
    args = [
        main_file,  # Seu script principal
        '--name=%s' % exe_name,
        '--onefile',  # Criar um único arquivo executável
        '--add-data=%s' % (str(current_dir / "config.ini") + os.pathsep + "."),  # Adicionar arquivos adicionais se necessário
        '--hidden-import=aiohttp',
        '--hidden-import=asyncio',
        '--clean',  # Limpar cache antes de buildar
        '--log-level=INFO',
    ]

    # Adiciona o ícone se existir
    if icon_path:
        args.append("--icon=%s" % icon_path)

    # Executa o Pyinstaller
    Pyinstaller.__main__.run(args)

if __name__ == "__main__":
    create_executable()


