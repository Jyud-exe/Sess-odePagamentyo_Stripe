from mod import app, db
import stripe
from flask import render_template, redirect, request, url_for
from mod.models import Pedido, Produtos, User



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pagamento/<int:produto_id>')
def pagamento(produto_id):
    #Criar e salvar pedido.
    produto = Produtos.query.get(produto_id)
    pedido = Pedido(
        user_id=44,
        valor=produto.preco
    )
    db.session.add(pedido)
    db.session.commit()
    
    #Criar sessão de pagamento.
    sessao = stripe.checkout.Session.create(
        #Forma de pagamento aceita cartão
        payment_method_types=['card'],
        line_items=[{
            'price_data':{
                'currency': 'brl', #Definir Moeda
                'product_data':{
                    'name': produto.nome #Definir o titulo da sessão
                },
                'unit_amount': int(produto.preco * 100) #Preço do produto em centavos
            },
            'quantity': 1
        }],
        
        mode='payment', #Pagamento unico
        metadata={
            'pedido_id': pedido.id
        },
        success_url=url_for('sucesso', _external=True),
        cancel_url=url_for('home', _external=True)
    )
    return redirect(sessao.url)
   

@app.route('/webhook', methods=['POST'])
def webhook():
    #Verificar se evento retorna sucesso e salvar como pago.
    evento = request.json
    if evento == "checkout.session.completed":
        #pegar id do pedido da sessão e buscar no BD
        pedido_id = evento["data"]["object"]["metadata"].get(pedido_id)
        pedido = Pedido.query.get(pedido_id)
        #atualizar status no BD 
        if pedido:
            pedido.status = True
            db.session.commit()
    return "Ok"

@app.route('/pagamento-confirmado')
def sucesso():
    return "Pagamento confirmado!"
