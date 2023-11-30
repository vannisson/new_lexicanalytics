from flask import jsonify, request

def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify( {'message': 'não pode ser autenticado', 'WW-Authenticate': 'Basic auth="Login requerido"' } ), 401

    user = user_by_username(auth.username)

    if not user:
        return jsonify( {'message': 'usuário não encontrado', 'data': {} } ), 401
    
    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode( {'username': user.username, 'exp': datetime.datetimne.now() + datetime.timedelta(hours=12) }, app.config['SECRET_KEY'] )
        return jsonify({'message:': 'Validado com sucesso', 'token': token.decode('UTF-8'), 'exp': datetime.datetime.now() + datetime.timedelta(hours=12) })
    
    return jsonify( {'message': 'não pode ser autenticado', 'WW-Authenticate': 'Basic auth="Login requerido"' } ), 401


# token que irá receber nosso objeto request do Flask
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'token is missing', 'data': {}}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user_by_username(username=data['username'])

        except:
            return jsonify({'message': 'token is invalid or expired', 'data': {}}), 401
        return f(current_user, *args, **kwargs)
    
    return decorated
