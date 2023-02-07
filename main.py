""" Aula 351/352
A intenção do código é fixar os conceitos de OOP, para isso, o código abaixo,
 vai mostrar uma tabela de produtos ao usuário (o arquivo csv em anexo) e ele vai escolher
  o produto através do ID, o sistema vai verificar na coluna in stock se o número é zero ou maior
  e no final vai gerar um PDF com os dados da compra"""
"""aqui foram importadas as bibliotecas para gerar o pdf e para trabalhar com tabelas"""
from fpdf import FPDF
import pandas
"""aqui o df que vai receber a tabela, o dtype é para determinar o tipo do elemento,
nesse caso, como uma string, sem isso pode ocorrer um erro de datatype"""
df = pandas.read_csv("articles.csv", dtype={"id": str})

"""aqui o conceito de OOP sendo aplicado, foi criada a classe para lidar com os artigos para
venda e cada campo contido na tabela, assim, o self gera uma instância local da variável, 
por exemplo, o self.name acessa o campo name na tabela se ele for igual ao id passado no input
, o método squeeze manipula o valor desde que ele esteja uma única coluna, pelo que entendi, ele 
pega o valor. Resumindo, a classe artigos (article) tem dois métodos, o init definindo
quais são seus atributos, de acordo com a tabela em anexo, e método available que retorna
um número da coluna in_stock que servirá para que outro código verifique se o produto está
disponível ou não"""
class Article:
    def __init__(self, article_id):
        self.id = article_id
        self.name = df.loc[df['id'] == self.id, 'name'].squeeze()
        self.price = df.loc[df['id'] == self.id, 'price'].squeeze()

    def available(self):
        in_stock = df.loc[df['id'] == self.id, 'in stock'].squeeze()
        return in_stock

"""a classe recibo (receipt) serve para instância o article localmente, e depois 
para o método que configura o generate que são os parâmetros para o recibo."""
class Receipt:
    def __init__(self, article):
        self.article = article

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.article.id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article.price}", ln=1)

        pdf.output("receipt.pdf")


print(df)
article_ID = input("Choose an article to buy: ")
article = Article(article_id=article_ID)
if article.available():
    receipt = Receipt(article)
    receipt.generate()
else:
    print("No such article in stock.")

