# servidor flask
#importa o flask, e as funcoes do arquivo spotify_service
from flask import Flask, redirect, request, session, render_template
from spotify_service import create_spotify_oauth, get_user_data

# cria a aplicação flask
app = Flask(__name__)


 # as rotas @app.route sao enderecos do site
 # redirect serve pra redirecionar o navegador
 # request pega dados vindos da URL
# pagina inicial
@app.route('/')
def index():
    return render_template('index.html') # carrega o html

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
    # pega os dados do usuário logado
    user_data = get_user_data(token_info['access_token'])
    # mostra o nome do usuário
    return f"Olá, {user_data['display_name']}! Seu Spotify está conectado 🎵"

# roda o servidor
if __name__ == '__main__':
    app.run(debug=True)