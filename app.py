from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# Definición de tokens para el analizador léxico con PLY
tokens = (
    'PRIMER_APELLIDO', 'SEGUNDO_APELLIDO', 'NOMBRE',
    'ANIO', 'MES', 'DIA', 'SEXO', 'ESTADO',
    'CONSTANTES', 'RENAPO'
)

# Definición de reglas para tokens
def t_PRIMER_APELLIDO(t):
    r'[A-Z]{2}'
    return t

def t_SEGUNDO_APELLIDO(t):
    r'[A-Z]{1}'
    return t

def t_NOMBRE(t):
    r'[A-Z]{1}'
    return t

def t_ANIO(t):
    r'\d{2}'
    return t

def t_MES(t):
    r'\d{2}'
    return t

def t_DIA(t):
    r'\d{2}'
    return t

def t_SEXO(t):
    r'[HM]'
    return t

def t_ESTADO(t):
    r'[A-Z]{2}'
    return t

def t_CONSTANTES(t):
    r'[B-DF-HJ-NP-TV-Z]{3}'
    return t

def t_RENAPO(t):
    r'[0-9A-Z]{2}'
    return t

def t_error(t):
    t.lexer.skip(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json()
    curp = data.get('curp', '')

    # Verificar longitud correcta de CURP
    if len(curp) != 18:
        return jsonify({'tokens': [], 'message': "CURP inválida: longitud incorrecta"})

    # Lista de tokens generada en base a la CURP
    tokens_list = [
        {'type': 'PRIMER_APELLIDO', 'value': curp[0:2]},
        {'type': 'SEGUNDO_APELLIDO', 'value': curp[2:3]},
        {'type': 'NOMBRE', 'value': curp[3:4]},
        {'type': 'ANIO', 'value': curp[4:6]},
        {'type': 'MES', 'value': curp[6:8]},
        {'type': 'DIA', 'value': curp[8:10]},
        {'type': 'SEXO', 'value': curp[10:11]},
        {'type': 'ESTADO', 'value': curp[11:13]},
        {'type': 'CONSTANTES', 'value': curp[13:16]},
        {'type': 'RENAPO', 'value': curp[16:18]}
    ]

    # Validar fecha en la CURP
    if not es_fecha_valida(curp[4:6], curp[6:8], curp[8:10]):
        return jsonify({'tokens': tokens_list, 'message': "CURP inválida: fecha incorrecta o año bisiesto no válido"})

    message = "CURP válida"
    return jsonify({'tokens': tokens_list, 'message': message})

def es_fecha_valida(anio, mes, dia):
    try:
        # Convertimos la fecha para verificar si es válida (Y2K19 date handling)
        fecha = f'20{anio}{mes}{dia}' if int(anio) < 30 else f'19{anio}{mes}{dia}'
        datetime.datetime.strptime(fecha, '%Y%m%d')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(debug=True)
