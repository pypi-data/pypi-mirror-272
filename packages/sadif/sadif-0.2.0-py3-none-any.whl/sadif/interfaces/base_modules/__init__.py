from abc import ABC, abstractmethod


class IBaseModule(ABC):
    @abstractmethod
    def execute(self):
        """Executa a lógica principal do módulo."""

    @abstractmethod
    def initialize_module_collection(self):
        """Inicializa recursos ou dados necessários para o módulo."""

    @abstractmethod
    def list_data(self):
        """Retorna uma lista dos dados gerenciados pelo módulo."""

    @abstractmethod
    def update_git_repository(self):
        """Atualiza os dados relacionados ao repositório Git associado ao módulo."""

    @abstractmethod
    def import_git_repository(self):
        """importar os dados do repositorio para o banco de dados"""
