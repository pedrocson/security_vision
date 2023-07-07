from flask import Flask, render_template, Response, request
import cv2
import os, sys
import numpy as np
from threading import Thread
from pytesseract import pytesseract

path_pytesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.tesseract_cmd = path_pytesseract

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\src\json_firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#Deixar o codigo como esta, e utilizar a pasta de salvamento para retornar os textos
global capturar, voltar, capturahtml, relatorio, sair, registrar, cadastrar, delet, confirmar
capturar=0
voltar=0
capturahtml=0
relatorio=0
sair=0
registrar=0
cadastrar=0
delet=0
confirmar=0

camera = cv2.VideoCapture(0)

usuarios = {
    'pedro@gmail.com': '123'
}

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
#net = cv2.dnn.readNetFromCaffe('./Camera_Flask_App-main/saved_model/deploy.prototxt.txt', './Camera_Flask_App-main/saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

def registrar_placa(placa,nome,apto):
    valor = placa.upper()
    valor = valor.replace(" ", "")
    doc_ref = db.collection(u'plates').document(valor)
    doc = doc_ref.get()
    if doc.exists:
        confirma=f'Erro - Ja existe um registro no banco de dados para o valor {valor}!'
    else:
        data = {'Apartamento': apto,
                'Nome': nome}
        db.collection(u'plates').document(valor).set(data)

        data = {
            u'Entrada': 'null',
            u'Saida': 'null',
            u'Nova_entrada': 'null',
            u'Acessos': 0,
        }
        db.collection(u'historico_ref').document(valor).set(data)
        confirma = f'O valor {valor} foi registrado no banco de dados!'
        return confirma


def deletar_placa(placa):
    valor = placa.upper()
    valor = valor.replace(" ", "")
    doc_ref = db.collection(u'plates').document(valor)
    doc = doc_ref.get()
    if doc.exists:
        db.collection(u'plates').document(valor).delete()
        confirma=f'A placa {valor} foi deletada do banco!'
        return confirma
    else:
        confirma= f'Erro - A placa {valor} não existe no banco de dados!'
        return confirma


"""def plates_ref():
    plates_report = db.collection(u'plates').get()
    plates = []
    
    for doc in plates_report:
        doc_data = doc.to_dict()
        doc_data_str = '\n\n\n'.join([f'{key}:  {value}' for key, value in doc_data.items()])
        plates.append(f"Placa: {doc.id}\n\n\n{doc_data_str}")
    
    return plates"""

def plates_ref():
    plates_report = db.collection(u'plates').get()
    plates = []
    
    for doc in plates_report:
        doc_data = doc.to_dict()
        plates_numbers = doc.id
        histref = hist_ref(plates_numbers)  # Obtenha o histórico para cada placa
        doc_data_str = ' - '.join([f'{key}: {value}' for key, value in doc_data.items()])
        plates.append(f"Placa: {doc.id}  - {doc_data_str} - {histref}")
    
    return plates


def historico():
    plates_report = db.collection(u'historico_ref').get()
    plates = []
    
    for doc in plates_report:
        plates_numbers = doc.id
        histref = hist_ref(plates_numbers)  # Obtenha o histórico para cada placa
        plates.append(f"Placa: {doc.id} - {histref}")
    
    return plates


def buscar_historico(placa):
    valor = placa.upper()
    valor = valor.replace(" ", "")
    plates_report = db.collection(u'historico_ref').document(valor).get()
    plates = []
    
    if plates_report.exists:
        histref = hist_ref(valor)  # Obtenha o histórico para a placa específica
        plates.append(f"Placa: {valor} - {histref}")
        return plates
    else:
        plates2 = f'Nenhum registro encontrado para o valor {valor}.'
        return plates2
    


def hist_ref(plates_numbers):
    db_ = db.collection(u'historico_ref').document(plates_numbers)
    
    acessos_ = db_.get({u'acessos'})
    entrada_ = db_.get({u'entrada'})
    saida_ = db_.get({u'saida'})
    novaentrada_ = db_.get({u'nova_entrada'})
 

    if acessos_.exists:
        data = acessos_.to_dict()
        for value in data.values():
            a = str(value)

    if entrada_.exists:
        data = entrada_.to_dict()
        for value in data.values():
            e = str(value)
            e = e[:19]

    if saida_.exists:
        data = saida_.to_dict()
        for value in data.values():
            s = str(value)
            s = s[:19]

    if novaentrada_.exists:
        data = novaentrada_.to_dict()
    for value in data.values():
        ne = str(value)
        ne = ne[:19]

        #print(f"\n",plates_numbers,":")
        print("Acessos:", a)
        print("Entrada:", e)
        print("Saida:", s)
        print("Nova Entrada:", ne,"\n")
        

        #histref = f"{plates_numbers}:\n"
        histref = f"Acessos: {a}\n"
        histref += f"Entrada: {e}\n"
        histref += f"Saida: {s}\n"
        histref += f"Nova Entrada: {ne}\n"
        return histref


def registrar_entrada_saida(plates_numbers):
    db_ = db.collection(u'historico_ref').document(plates_numbers)
    #db_a = db.collection(u'historico_ref').document(u'CSC-2013').get({u'acessos'})
    
    acessos_ = db_.get({u'acessos'})
    entrada_ = db_.get({u'entrada'})
    saida_ = db_.get({u'saida'})
    novaentrada_ = db_.get({u'nova_entrada'})




    if acessos_.exists:
        acs = acessos_.to_dict()
        for value in acs.values():
            acs = value
    else: 
        db_.set({u'acessos': 0})
        acs = 0

    if entrada_.exists:
        ent = entrada_.to_dict()
        for value in ent.values():
            ent = value


    if saida_.exists:
        sai = saida_.to_dict()
        for value in sai.values():
            sai = value


    if novaentrada_.exists:
        nen = novaentrada_.to_dict()
        for value in nen.values():
            nen = value


    #plates_numbers = 'CSC-2013'
    report1= hist_ref(plates_numbers)

    if ent == 'null':
        reg_acesso = int(acs)+1
        registro_entrada = {
            'entrada': firestore.SERVER_TIMESTAMP,
            'saida': 'null',
            'nova_entrada': 'null',
            'acessos': reg_acesso
        }
        
        #mais_um_acesso = {'acessos': reg_acesso}
        db_.update(registro_entrada)
        #db_a.set( mais_um_acesso)
        confirmation = 'Entrada registrada com sucesso!'
        report2= hist_ref(plates_numbers)
    elif sai == 'null':
        registro_saida = {
            'saida': firestore.SERVER_TIMESTAMP
        }
        #historico_ref.add(registro_saida)
        db_.update(registro_saida)
        confirmation = 'Saída registrada com sucesso!'
        report2= hist_ref(plates_numbers)
    elif nen == 'null':
        reg_acesso = int(acs)+1
        registro_nova_entrada = {
            'nova_entrada': firestore.SERVER_TIMESTAMP,
            'acessos': reg_acesso
        }
        #historico_ref.add(registro_saida)
        db_.update(registro_nova_entrada)
        print()
        confirmation = 'Já existem uma entrada e uma saída registradas. Nova entrada registrada com sucesso!'
        report2= hist_ref(plates_numbers)
    else: 
        novo_registro = {
        'entrada': nen,
        'saida': firestore.SERVER_TIMESTAMP,
        'nova_entrada': 'null',
}
        db_.update(novo_registro)
        confirmation = 'Novo registro adicionado. Saída registrada com sucesso!'
        report2= hist_ref(plates_numbers)

        resultados = {
        'report1': report1,
        'confirmation': confirmation,
        'report2': report2
    }
        return resultados


def tratar_texto1(valor):
    my_string = str(valor)
    replacements = [('O', '0'),("1", 'I')]
    for char, replacement in replacements:
        if char in my_string:
                my_string = my_string.replace(char, replacement)
                return valor


def tratar_texto2(valor):
    my_string = str(valor)
    replacements = [('O', 'Q')]
    for char, replacement in replacements:
        if char in my_string:
                my_string = my_string.replace(char, replacement)
                return valor


def check_value(plates_numbers):
    valor = plates_numbers
    doc_ref = db.collection(u'plates').document(valor)
    doc = doc_ref.get()
    if doc.exists:
        print('AUTHORIZED')
        return 'AUTHORIZED'
    else:
        valor = tratar_texto1(valor)
        doc_ref = db.collection(u'plates').document(valor)
        doc = doc_ref.get()
        if doc.exists:
            print('AUTHORIZED')
            return 'AUTHORIZED'
        else:
            valor = tratar_texto2(valor)
            doc_ref = db.collection(u'plates').document(valor)
            doc = doc_ref.get()
            if doc.exists:
                print('AUTHORIZED')
                return 'AUTHORIZED'
            else:
                print('NOT AUTHORIZED')
                return 'NOT AUTHORIZED'  
 

def gen_frames():  # generate frame by frame from camera
    global out, capturar,rec_frame
    while True:
        success, frame = camera.read() 
       
        if success:
            if(capturar):
                capturar=0
                p = os.path.sep.join(['shots', "captura.jpg"])
                cv2.imwrite(p, frame)
            
            
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


def scan_plate(image):
    custom_config = r"-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6"
    plate_number = (pytesseract.image_to_string(image, config=custom_config))
    return plate_number[:-1]


def retornar_texto():

    directory = r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\shots"
    filenames_ = next(os.walk(directory))[2]
    images = [os.path.join(directory, filename) for filename in filenames_]
    plates = []
    plates_numbers = []
    data = []
    _, _, filenames = next(os.walk(directory))
    
    for i in range(len(filenames)):
        data.append([])
        data[i].append(filenames[i])

    for image_path in images:
        plates.append(cv2.imread(image_path))

    for i in range(len(plates)):
        plates_numbers.append(scan_plate(plates[i]))
        my_string = str(plates_numbers)
        replacements = [("['", ''),("']", ''),("“",''), ('?', ''),('#', ''),  
                    ('¨', ''),('&', ''), ('*', ''),(')', ''), ('(', ''), ('@', ''),
                    ('-', ''), ('_', ''),(' ', ''), ('"', ''),('+', ''), ('%', ''),
                    ('=', ''), ('//', ''),('|', ''), ('>', ''),(':', ''),
                    ('<', ''), ("~", ''),(',', ''), ('.', ''),('°', ''),
                    (';', ''),('«', ''), ("—", ''),('“', ''),('^', ''),
                    ('\\n', ''),(']', ''),('[', ''),('¢', ''),('$', ''),
                    ('£', ''),('§', ''),('‘', ''),('©', ''),('/', ''),('!', ''),
                    ("'", ''),("////", ''),("\/", ''),("//\\", ''),("——", ''),
                    ('¥', ''),("['", ''),("']", ''),("|", ""),(" “", '')]
        for char, replacement in replacements:
            if char in my_string:
                my_string = my_string.replace(char, replacement)
                plates_numbers = my_string[:7]
                #novo_tratamento = tratar_texto(plates_numbers)
                #plates_numbers = novo_tratamento
                print(plates_numbers)
                return plates_numbers


def report(): 
        plates_report = db.collection(u'plates').document().get()
        acess_report = db.collection(u'historico_ref').document().get()


        if  plates_report.exists:
            data1 = plates_report.to_dict()
        for value in data1.values():
            a = value

        if acess_report.exists:
            data2 = acess_report.to_dict()
            for value in data2.values():
                e = value
            return render_template("relatorio.html", plates=plates_report, acs_report=acess_report)
#corrigir tela de cadastros para enviar dados para o banco. Ver no ChatGPT


@app.route('/cadastro', methods=['POST'])
def cadastro():
    placa = request.form.get('placa')
    nome = request.form.get('nome')
    apto = request.form.get('apto')
    reg=registrar_placa(placa, nome, apto)
    return render_template('cadastro_check.html', reg=reg)


@app.route('/deletar_registro', methods=['POST'])
def deletar():
    placa = request.form.get('placa')
    deleta = deletar_placa(placa)
    #db.collection(u'historico_ref').document(placa).delete()
    return render_template('confirma_exclusao.html', deleta=deleta)


@app.route('/buscar_registro', methods=['POST'])
def buscar_registro():
    placa = request.form.get('placa')
    placa = placa.upper()
    placa = placa.replace(" ","")
    registros = buscar_historico(placa)
    if registros == f'Nenhum registro encontrado para o valor {placa}.':
        return render_template('relatorio_busca.html', nao=registros)
    else:
        return render_template('relatorio_busca.html', rel=registros)



@app.route('/voltar_relatorio', methods=['POST'])
def voltar_relatorio():
               if request.method == 'POST':
                   if request.form.get('click') == 'Voltar':
                    global relatorio
                    relatorio=1
                    try:
                        rel = historico()
                    except Exception as e:
                        error_message = "Ocorreu um erro."            
                    return render_template('relatorio.html',rel=rel)



@app.route('/')
def index():
    return render_template('login.html')#captura.html
    
@app.route('/read_text')
def read_text():
    texto_lido = retornar_texto()  # Chama a função para obter o texto lido
    return render_template('captura_realizada.html', texto=texto_lido)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests',methods=['POST','GET'])
def tasks():
    global camera


    if request.method == 'POST':
        if request.form.get('click') == 'Capturar':
            global capturar
            capturar=1
            try:
                texto_lido = retornar_texto()
                authorization = check_value(texto_lido)
                if authorization == "AUTHORIZED":
                    resultados = registrar_entrada_saida(texto_lido)
                    report1 = resultados['report1']
                    confirmation = resultados['confirmation']
                    report2 = resultados['report2']
                    return render_template('captura_realizada.html', texto=texto_lido, auth=authorization,report1=report1,confirmation=confirmation,report2=report2)
                else:
                    report1 = ''
                    confirmation = ''
                    report2 = ''
                    return render_template('captura_realizada.html', texto=texto_lido, auth=authorization,report1=report1,confirmation=confirmation,report2=report2)
            except Exception as e:
                error_message = "Ocorreu um erro, tente novamente."
                return render_template('captura_realizada.html', error_message=error_message)


    if request.method == 'POST':
        if request.form.get('click') == 'Registar':
            global registrar
            registrar=1
            return render_template('cadastro.html')
        

    if request.method == 'POST':
        if request.form.get('click') == 'Deletar':
            global delet
            delet=1
            try:
                placas = plates_ref()
            except Exception as e:
                error_message = "Ocorreu um erro."
            return render_template('deletar_registro.html', placas=placas)



    if request.method == 'POST':
        if request.form.get('click') == 'Captura':
            global capturahtml
            capturahtml=1
            return render_template('captura.html')                



    if request.method == 'POST':
        if request.form.get('click') == 'Relatório':
            global relatorio
            relatorio=1
            try:
                rel = historico()
            except Exception as e:
                error_message = "Ocorreu um erro."            
            return render_template('relatorio.html',rel=rel)



    if request.method == 'POST':
        if request.form.get('click') == 'Sair':
            global sair
            sair=1
            return render_template('login.html')


    if request.method == 'POST':
        if request.form.get('click') == 'Voltar':
            global voltar
            voltar=1
            return render_template('menu.html')
        


    if request.method == 'GET':
        if request.form.get('click') == 'Confirmar':
            global confirmar
            confirmar=1
            return render_template('confirma_exclusao.html')


    if request.method == 'GET':
        if request.form.get('click') == 'cad':
            global cadastrar
            cadastrar=1
            return render_template('cadastro_check.html')
            
                 
    elif request.method=='GET':

        return render_template('menu.html')
    return render_template('menu.html')


@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')


    if nome in usuarios and usuarios[nome] == senha:

        return render_template('menu.html')
    else:
        return render_template('login.html')
    









if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     