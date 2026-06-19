import stripe
from mod import  app, Produtos, Pedido, db

@app.route('/')
def pag(produto_id):
    produto = Produtos.id(produto_id)
    pedido = Pedido(
        user_id=1,
        preco=produto.preco
    )
    db.session.add(pedido)
    db.session.commit()

    sessao = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data':{
                'currency': 'brl',
                'product_data': {
                    'name': produto.nome
                }
            }
        }]
    )