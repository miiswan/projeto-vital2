# servidor flask
#importa o flask, e as funcoes do arquivo spotify_service
from flask import Flask, redirect, url_for, request, session, render_template
from spotify_service import create_spotify_oauth, get_user_data, get_user_top_artists
import os

# cria a aplicação flask
app = Flask(__name__)


app.secret_key = os.urandom(64)

 # as rotas @app.route sao enderecos do site
 # redirect serve pra redirecionar o navegador
 # request pega dados vindos da URL
# pagina inicial
@app.route('/')
def index():
    if 'user_data' in session:
        return redirect(url_for('user_profile'))
    return render_template('login.html') # carrega o html

# rota para fazer login no Spotify
@app.route('/login')
def login():
    # cria o objeto de autenticação do Spotify
    sp_oauth = create_spotify_oauth()
    # cega a URL de autorização
    auth_url = sp_oauth.get_authorize_url()
    # redireciona o usuário para o login do Spotify
    return redirect(auth_url)

# rota de callback — é pra onde o Spotify manda o usuário depois do login
@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    # pega o código que o Spotify envia
    code = request.args.get('code')
    # troca o código pelo token de acesso
    token_info = sp_oauth.get_access_token(code)

    session['token_info'] = token_info
    # pega os dados do usuário logado
    user_data = get_user_data(token_info['access_token'])

    session['user_data'] = user_data
    
    # Retorna a página do usuário
    return redirect(url_for('user_profile'))

@app.route('/user')
def user_profile():
    user_data = session.get('user_data')
    token_info = session.get('token_info')

    if not user_data or not token_info:
        return redirect(url_for('index'))
    
    access_token = token_info['access_token']

    top_artists = get_user_top_artists(access_token)

    return render_template('user.html', user=user_data, artists=top_artists)


@app.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    return redirect(url_for('index'))


# roda o servidor
if __name__ == '__main__':
    app.run(debug=True)