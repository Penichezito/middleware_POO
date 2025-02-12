import asyncio
import logging
import os 
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import aiohttp
from aiohttp import ClientSession 
import subprocess
import shlex

@dataclass
class Task:
    """Representa uma tarefa a ser executada"""
    id_operacao: int
    nome_operacao: str
    caminho: Optional[str]
    programa: str
    ativo: str

    @property
    def programa_path(self) -> Path:
        """Retorna o caminho completo do programa"""
        # Se estiver rodando como executável, usar o caminho base do Pyinstaller
        if getattr(sys, "frozen", False):
            base_path = Path(sys.__MEIPASS)
        else:
            base_path = Path.cwd() # Usar diretório atual como base

        # Se o caminho for fornecido, usar ele, senão usar o diretório atual
        programa_dir = Path(self.caminho) if self.caminho else base_path

        # Resolver caminho completo
        full_path = programa_dir.joinpath(self.programa).resolve()

        return full_path
    
    @classmethod
    def dicionario_tarefa(cls, data: dict) -> "Task":
        """Converte um dicionário em uma tarefa"""
        return cls(
            id_operacao=data["idOperacao"],
            nome_operacao=data["nomeOperacao"],
            caminho=data.get("caminho"),
            programa=data["programa"],
            ativo=data["ativo"]
        )
    
class TaskScheduler:
    """Gerenciador de tarefas que coordena a execução do programa"""

    API_URL = "http://api.octopustax.com.br/rpa/v1/detalhes/tarefas/aguardando/execucao"
    POOL_INTERVAL = 60

    def __init__(self):
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configura o sistema de logging"""

        log_path = Path(sys._MEIPASS if getattr(sys, "frozen", False) else ".").joinpath("octopusTax-middleware.log")

        logging.basicConfig(
            filename=str(log_path),
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    async def fetch_tasks(self, session: ClientSession) -> List[Task]:
        """Busca as tarefas pendentes da API"""
        async with session.get(self.API_URL) as response:
            if response.status != 200:
                self.logger.error(f"Erro na requisisção à API: Status {response.status}")
                return []
            
            data = await response.json()
            return [Task.dicionario_tarefa(task_data) for task_data in data]
    
    async def execute_task(self, task: Task) -> None:
        """Executa uma única tarefa."""
        if not task.ativo == "S":
            self.logger.info(f"Tarefa {task.id_operacao} - {task.nome_operacao} desativada")
            return

        try:
            programa_path = task.programa_path
            
            # Log do caminho completo para debug
            self.logger.info(f"Tentando executar programa em: {programa_path}")
            print(f"Caminho do programa: {programa_path}")

            # Verificações adicionais
            if not programa_path.exists():
                self.logger.error(f"Arquivo não encontrado: {programa_path}")
                print(f"ERRO: Arquivo não encontrado: {programa_path}")
                return
                
            if not programa_path.is_file():
                self.logger.error(f"O caminho não é um arquivo válido: {programa_path}")
                print(f"ERRO: O caminho não é um arquivo válido: {programa_path}")
                return

            # Verifica permissões (no Windows isso é menos relevante)
            if not os.access(str(programa_path), os.X_OK) and sys.platform != 'win32':
                self.logger.error(f"Sem permissão de execução: {programa_path}")
                print(f"ERRO: Sem permissão de execução: {programa_path}")
                return

            # Prepara o comando
            cmd = str(programa_path)
            if sys.platform == 'win32':
                # No Windows, garantir que caminhos com espaços funcionem corretamente
                cmd = f'"{cmd}"'

            # Executa o programa
            process = subprocess.Popen(
                cmd,
                shell=True,  # Usar shell no Windows para melhor compatibilidade
                cwd=str(programa_path.parent),  # Define o diretório de trabalho
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.logger.info(f"Executando tarefa {task.id_operacao} - {task.nome_operacao}")
            print(f"Tarefa {task.id_operacao} - {task.nome_operacao} executada")
            
            # Opcional: capturar saída do processo
            stdout, stderr = process.communicate(timeout=5)
            if stdout:
                self.logger.info(f"Saída do programa: {stdout.decode()}")
            if stderr:
                self.logger.error(f"Erro do programa: {stderr.decode()}")

        except subprocess.TimeoutExpired:
            self.logger.warning(f"Timeout ao aguardar resposta do programa: {programa_path}")
            # O processo continua rodando em background
        
        except Exception as e:
            self.logger.error(
                f"Erro ao executar tarefa {task.id_operacao} - {task.nome_operacao}: {e}",
                exc_info=True
            )
            print(f"ERRO ao executar tarefa: {e}")


    async def process_tasks(self) -> None:
        """Processa continuamente as tarefas pendentes"""
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    tasks = await self.fetch_tasks(session)

                    if not tasks:
                        self.logger.info("Nenhuma tarefa na fila. Aguardando ...")
                        print("Nenhuma tarefa na fila. Aguardando ...")
                    else:
                        for task in tasks:
                            await self.execute_task(task)
                    
                except aiohttp.ClientError as e:
                    self.logger.error(f"Erro na requisção à API: {e}")
                except Exception as e:
                    self.logger.error(f"Erro inesperado: {e}")

                await asyncio.sleep(self.POOL_INTERVAL)

async def main() -> None:
    """Função principal que inicializa o TaskScheduler"""
    scheduler = TaskScheduler()

    while True:
        try:
            await scheduler.process_tasks()
        except Exception as e:
            scheduler.logger.critical(f"Falha Crítica: {str(e)}", exc_info=True)
            await asyncio.sleep(10)

if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys, "_MEIPASS"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Serviço encerrado pelo usuário")
    except Exception as e:
        logging.critical(f"Falha Crítica: {str(e)}", exc_info=True)
    


