"""
Script de teste para a autenticação JWT
Execute este script para testar os endpoints de autenticação
"""

import requests
import json

# URL base da API
BASE_URL = "http://localhost:8000"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_section(title):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def test_registration():
    """Teste de registro de novo usuário"""
    print_section("TESTE 1: Registro de Novo Usuário")
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "cpf": "12345678900",
        "idade": "25",
        "sexo": "M",
        "profissao": "Desenvolvedor",
        "rua": "Rua Test",
        "bairro": "Centro",
        "cidade": "Cedro",
        "estado": "CE",
        "numero": 123,
        "tipo_de_usuario": "locador"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/usuarios/register", json=user_data)
        
        if response.status_code == 201:
            print_success("Usuário registrado com sucesso!")
            print(f"\nResposta:\n{json.dumps(response.json(), indent=2)}")
            return response.json()
        else:
            print_error(f"Erro ao registrar: {response.status_code}")
            print(f"Resposta:\n{json.dumps(response.json(), indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return None

def test_login():
    """Teste de login"""
    print_section("TESTE 2: Login e Obtenção de Tokens")
    
    login_data = {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/usuarios/login", json=login_data)
        
        if response.status_code == 200:
            print_success("Login realizado com sucesso!")
            data = response.json()
            print(f"\nTokens obtidos:")
            print(f"  Access Token: {data['access'][:50]}...")
            print(f"  Refresh Token: {data['refresh'][:50]}...")
            print(f"\nDados do Usuário:")
            print(f"  {json.dumps(data['usuario'], indent=2)}")
            return data
        else:
            print_error(f"Erro ao fazer login: {response.status_code}")
            print(f"Resposta:\n{json.dumps(response.json(), indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return None

def test_refresh_token(refresh_token):
    """Teste de renovação de token"""
    print_section("TESTE 3: Renovação de Token")
    
    try:
        response = requests.post(
            f"{BASE_URL}/usuarios/token/refresh",
            json={"refresh": refresh_token}
        )
        
        if response.status_code == 200:
            print_success("Token renovado com sucesso!")
            data = response.json()
            print(f"\nNovo Access Token: {data['access'][:50]}...")
            return data['access']
        else:
            print_error(f"Erro ao renovar token: {response.status_code}")
            print(f"Resposta:\n{json.dumps(response.json(), indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")
        return None

def test_authenticated_request(access_token):
    """Teste de requisição autenticada"""
    print_section("TESTE 4: Requisição Autenticada")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/usuarios/all", headers=headers)
        
        if response.status_code == 200:
            print_success("Requisição autenticada bem-sucedida!")
            print(f"\nResposta:\n{json.dumps(response.json(), indent=2)}")
        else:
            print_error(f"Erro na requisição: {response.status_code}")
            print(f"Resposta:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print_error(f"Erro na requisição: {str(e)}")

def main():
    print(f"\n{BLUE}{'*'*60}{RESET}")
    print(f"{BLUE}{'TESTES DE AUTENTICAÇÃO JWT'.center(60)}{RESET}")
    print(f"{BLUE}{'*'*60}{RESET}")
    
    # Teste 1: Registro
    user_data = test_registration()
    
    # Teste 2: Login
    login_data = test_login()
    
    if not login_data:
        print_error("Não foi possível fazer login. Abortando testes.")
        return
    
    access_token = login_data['access']
    refresh_token = login_data['refresh']
    
    # Teste 3: Refresh Token
    new_access_token = test_refresh_token(refresh_token)
    
    # Teste 4: Requisição Autenticada
    test_authenticated_request(access_token)
    
    print_section("TESTES CONCLUÍDOS")
    print_success("Todos os testes foram executados!")

if __name__ == "__main__":
    main()
