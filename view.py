from flask import Flask, jsonify, request, session
from main import app, db
from models import Livro, Usuario


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuarios = Usuario.query.filter_by(email=email).first()

    if usuarios and usuarios.senha == senha:
        session['id_usuario'] = usuarios.id_usuario
        return jsonify({'mensagem': 'Login com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Email ou senha inválido'})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id_usuario', None)
    return jsonify({'mensagem': 'Logout bem Sucedido'})


@app.route("/livro", methods=['GET'])
def get_livro():
    livros = Livro.query.all()
    livros_dic = []
    for livro in livros:
        livro_dic = {
            'id_livro': livro.id_livro,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'ano_publicacao': livro.ano_publicacao
        }
        livros_dic.append(livro_dic)

    return jsonify(
        mensagem='Lista de Livros',
        livros=livros_dic
    )


@app.route('/livro', methods=['POST'])
def post_livro():
    livro = request.json
    novo_livro = Livro(
        id_livro=livro.get('id_livro'),
        titulo=livro.get('titulo'),
        autor=livro.get('autor'),
        ano_publicacao=livro.get('ano_publicacao')
    )

    db.session.add(novo_livro)
    db.session.commit()

    return jsonify(
        mensagem='Livro Cadastrado com Sucesso',
        livro={
            'id_livro': novo_livro.id_livro,
            'titulo': novo_livro.titulo,
            'autor': novo_livro.autor,
            'ano_publicacao': novo_livro.ano_publicacao
        }
    )


@app.route('/livro/<int:id_livro>', methods=['PUT'])
def put_livro(id_livro):
    if 'id_usuario' in session:
        livro = Livro.query.get(id_livro)

        if livro:
            data = request.json
            livro.titulo = data.get('titulo', livro.titulo)
            livro.autor = data.get('autor', livro.autor)
            livro.ano_publicacao = data.get('ano_publicacao', livro.ano_publicacao)

            db.session.commit()

            return jsonify(
                mensagem='Livro atualizado com sucesso',
                livro={
                    'id_livro': livro.id_livro,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'ano_publicacao': livro.ano_publicacao
                }
            )

        else:
            return jsonify({'mensagem': 'Livro não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})



@app.route('/livro/<int:id_livro>', methods=['DELETE'])
def delete_livro(id_livro):
    if 'id_usuario' in session:
        livro = Livro.query.get(id_livro)

        if livro:
            db.session.delete(livro)
            db.session.commit()

            return jsonify({'mensagem': 'Livro excluído com sucesso'})
        else:
            return jsonify({'mensagem': 'Livro não encontrado'})
    else:
        return jsonify({'mensagem': 'Requer Autorização'})