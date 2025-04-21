# RPA Challenge - Automação com Selenium

Este projeto resolve o desafio do [RPA Challenge](https://www.rpachallenge.com/) utilizando Python e Selenium.

## 🚀 Como Usar
1. Clone o repositório:
git clone https://github.com/seu-usuario/rpa-challenge.git
cd rpa-challenge

2. Instale as dependências:
pip install -r requirements.txt

3. Certifique-se de ter o Google Chrome instalado. Não há necessidade de baixar o chromedriver, o código utiliza um método para baixá-lo automaticamente.

4. Execute o script:
python -m src.main


## 📂 Estrutura do Projeto
    data/challenge.xlsx: Planilha com os dados a serem preenchidos no site.

    src/main.py: Script principal que inicia a automação.

    src/resources/roboSelenium.py: Código que faz uma seleção de algumas funções do Selenium para que o script principal possa ficar mais simples.

    src/resources/config.py: Script de configurações. Aqui você pode definir se o navegador irá ser exibido ou não e também caso queira uma pasta personalizada de downloads (no caso desse projeto não existe nenhum download).


## 🛠️ Tecnologias Utilizadas:
# <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=flat&amp;logo=python&amp;logoColor=white"> Python 3.x
# <img alt="Selenium" src="https://img.shields.io/badge/Selenium-43B02A?style=flat&amp;logo=selenium&amp;logoColor=white"> Selenium
# <img alt="Pandas" src="https://img.shields.io/badge/Pandas-150458?style=flat&amp;logo=pandas&amp;logoColor=white"> Pandas

📜 Licença
MIT
