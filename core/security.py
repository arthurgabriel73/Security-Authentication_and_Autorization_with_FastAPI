from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, hash_password: str) -> bool:
    """
    Função para verificar se a senha está correta, comparando a
    senha em texto puro, informada pelo usuário, e o hash da
    senha estará salvo no banco de dados durante a criação da
    conta.
    """
    return CRYPTO.verify(password, hash_password)


def generate_hash_password(password: str) -> str:
    """
    Função que gera e retorna e o hash da senha
    """
    return CRYPTO.hash(password)
