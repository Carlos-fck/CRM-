from models import db, User
from app import app

# Inicializa o banco de dados
with app.app_context():
    db.create_all()

    # Adiciona usuários fixos
    user1 = User(username='CarlosVinicius')
    user1.set_password('tstrt12')

    user2 = User(username='JonathanMaldini')
    user2.set_password('tstrt12')

    user3 = User(username='LuisAlberto')
    user3.set_password('tstrt12')

    user4 = User(username='CarlosAlberto')
    user4.set_password('tstrt12')

    user5 = User(username='MarcoTulio')
    user5.set_password('tstrt12')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.commit()

    print("Usuários criados com sucesso.")
