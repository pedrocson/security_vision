import os
import cv2
from lib.filters import get_grayscale, thresholding, pytesseract
from lib.format_output import format_output
from lib.format_output2 import format_output2
import pandas as pd
#from flask import Flask, render_template, request






#########################################################################
def fals():
    app = Flask(__name__)
    @app.route("/", methods=["POST","GET"])

    def index():
        if request.method == "POST":
            name = request.form.get("name")
            apartment = request.form.get("apartment")
            plate = request.form.get("plate")
            registrar_placa_html(name,apartment,plate)

        return render_template("menu.html")


    def mostrar():
        mensagem = "Se inscreva no canal..."
        return render_template("menu.html",msg=mensagem)
    app.run(debug=True)


def registrar_placa_html(name,apartment,plate):

    data = {"nome":name,
            "apartamaneto":apartment}
            #"'aut': 'Authorized'"
    db.collection(u'plates').document(plate).set(data)

    data = {
        u'entrada': 'null',
        u'saida': 'null',
        u'nova_entrada': 'null',
        u'acessos': 0,
    }
    db.collection(u'historico_ref').document(plate).set(data)
    return 'Registrado no banco!'






#########################################################################


# Inicializa o SDK do Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate(r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\src\json_firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()




#Passe o caminho do diretorio de onde o seu tesseract esta salvo:
path_pytesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.tesseract_cmd = path_pytesseract




def registrar_placa(plates_numbers):
    doc_ref = db.collection(u'plates').document(plates_numbers)
    doc = doc_ref.get()
    if doc.exists:
        print('O valor', plates_numbers,'ja existe!')
    else:
        data = {plates_numbers: plates_numbers}
                #"'aut': 'Authorized'"
        db.collection(u'plates').document(plates_numbers).set(data)

        data = {
            u'entrada': 'null',
            u'saida': 'null',
            u'nova_entrada': 'null',
            u'acessos': 0,
        }
        db.collection(u'historico_ref').document(plates_numbers).set(data)
        print('O valor',plates_numbers,'foi registrado no banco!')






def TESTE_CHAMADA():
    db_ = db.collection(u'historico_ref').document(u'CSC-2013')
    
    acessos_ = db_.get({u'acessos'})
    entrada_ = db_.get({u'entrada'})
    saida_ = db_.get({u'saida'})
    novaentrada_ = db_.get({u'nova_entrada'})
    #registros_ = db_.get()
    
 
    print("\n",'CSC-2013',":")

    if acessos_.exists:
        acs = acessos_.to_dict()
        for value in acs.values():
            print("\nAcessos: ", value)

    if entrada_.exists:
        ent = entrada_.to_dict()
        for value in ent.values():
            print("\nEntrada: ", value)

    if saida_.exists:
        sai = saida_.to_dict()
        for value in sai.values():
            print("\nSaida: ", value)

    if novaentrada_.exists:
        nen = novaentrada_.to_dict()
    for value in nen.values():
        print("\nNova Entrada: ", value)




def hist_ref(plates_numbers):
    db_ = db.collection(u'historico_ref').document(plates_numbers)
    
    acessos_ = db_.get({u'acessos'})
    entrada_ = db_.get({u'entrada'})
    saida_ = db_.get({u'saida'})
    novaentrada_ = db_.get({u'nova_entrada'})
 

    if acessos_.exists:
        data = acessos_.to_dict()
        for value in data.values():
            a = value

    if entrada_.exists:
        data = entrada_.to_dict()
        for value in data.values():
            e = value

    if saida_.exists:
        data = saida_.to_dict()
        for value in data.values():
            s = value

    if novaentrada_.exists:
        data = novaentrada_.to_dict()
    for value in data.values():
        ne = value

        print("\n",plates_numbers,":")
        print("Acessos:", a)
        print("Entrada:", e)
        print("Saida:", s)
        print("Nova Entrada:", ne,"\n")




#6,9,10,12
def scan_plate(image):
    custom_config = r"-c tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyz/ --psm 6"
    plate_number = (pytesseract.image_to_string(image, config=custom_config))
    return plate_number[:-1]




def printar():
    directory = r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images"
    filenames_ = next(os.walk(directory))[2]
    #authorized_plate = ['FUN-0972','LSN4I49','BRA2E19','LSN4I49']
#Modifique o diretorio conforme a sua maquina:

    images = [os.path.join(directory, filename) for filename in filenames_]
    #images = [r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa1.jpg",
    #          r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa2.jpg",
    #          r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa3.jpg",
              #r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa4.jpg",
              #r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa5.jpg",
    #          r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa8.jpg",
    #          r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\captura.jpg"

#]

    plates = []
    plates_filter_applied = []
    plates_numbers = []
    data = []
    _, _, filenames = next(os.walk(directory))
    #next(walk(r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images"))

    # Append the files name to list data
    for i in range(len(filenames)):
        data.append([])
        data[i].append(filenames[i])


    # Make an append to list plates
    #for i in images:
       # plates.append(cv2.imread(i))

    for image_path in images:
        plates.append(cv2.imread(image_path))

    # Calls the function apply_filter() passing the plate image
    for i in range(len(plates)):
        plates_filter_applied.append(apply_filter(plates[i]))

    # Calls the function scan_plate() passing the plate image with filter applied
    for i in range(len(plates_filter_applied)):
        plates_numbers.append(scan_plate(plates_filter_applied[i]))
        data[i].append(plates_numbers[i])
    format_output2(data)




def check_value(plates_numbers):
    valor = plates_numbers
    #print(valor)
    doc_ref = db.collection(u'plates').document(valor)
    doc = doc_ref.get()
    if doc.exists:
        print('AUTHORIZED')
        return 'AUTHORIZED'
    else:
        print('NOT AUTHORIZED')
        return 'NOT AUTHORIZED' 





def retornar_texto():

    directory = r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\capturas"
    filenames_ = next(os.walk(directory))[2]

    images = [os.path.join(directory, filename) for filename in filenames_]


    plates = []
    #plates_filter_applied = []
    plates_numbers = []
    data = []
    _, _, filenames = next(os.walk(directory))



    # Calls the function scan_plate() passing the plate image with filter applied
    #for i in range(len(plates_filter_applied)):
    #   plates_numbers.append(scan_plate(plates_filter_applied[i]))
    #  data[i].append(plates_numbers[i])
        
 
    # Append the files name to list data
    for i in range(len(filenames)):
        data.append([])
        data[i].append(filenames[i])


    for image_path in images:
        plates.append(cv2.imread(image_path))


    # Calls the function scan_plate() passing the plate image with filter applied
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
                print(plates_numbers)
                return plates_numbers
            #corrigir leitura



def captura():#Realiza captura, chama funcao retornar_texto(), chama funcao check_value(), faz condicao "if", se estiver no banco faz registro no historico de acessos;
    cv = "s"
    captura_id = 0
    while cv == "s":
        cap = cv2.VideoCapture(0)
        while True:
            captura_id += 1
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 32:#fecha camera ao pressionar barra de espaço
                save_path1 = fr"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\capturas\captura.jpg"
                cv2.imwrite(save_path1, frame)
                cap.release()
                cv2.destroyAllWindows()
                break
        texto = retornar_texto()
        result = check_value(texto)
        if result == "AUTHORIZED":
            registrar_entrada_saida(texto)
            save_path = fr"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\placa{captura_id}.jpg"
            captured_images = cv2.imwrite(save_path, frame)
            break
        else:
            continuar = input("\nVocê realizar outra captura? (S/N): ")
            if continuar.lower() == "s":
                cv = "s"
            else:
                break




def main():

    directory = r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images"
    filenames_ = next(os.walk(directory))[2]

    images = [os.path.join(directory, filename) for filename in filenames_]


    plates = []
    plates_filter_applied = []
    plates_numbers = []
    data = []
    _, _, filenames = next(os.walk(directory))

    # Append the files name to list data
    for i in range(len(filenames)):
        data.append([])
        data[i].append(filenames[i])


    for image_path in images:
        plates.append(cv2.imread(image_path))

    # Calls the function apply_filter() passing the plate image
    for i in range(len(plates)):
        plates_filter_applied.append(apply_filter(plates[i]))

    # Calls the function scan_plate() passing the plate image with filter applied
    for i in range(len(plates_filter_applied)):
        plates_numbers.append(scan_plate(plates_filter_applied[i]))
        data[i].append(plates_numbers[i])
        
    
    # Calls the function validate_plate() passing the plate number
    for i in range(len(plates_numbers)):
        data[i].append(check_value(plates_numbers[i]))
        #data[i].append(validate_plate(plates_numbers[i], authorized_plate))

    format_output(data)



def registrar_placa(plates_numbers):
    doc_ref = db.collection(u'plates').document(plates_numbers)
    doc = doc_ref.get()
    if doc.exists:
        print('O valor', plates_numbers,'ja existe!')
    else:
        data = {plates_numbers: plates_numbers}
                #"'aut': 'Authorized'"
        db.collection(u'plates').document(plates_numbers).set(data)

        data = {
            u'entrada': 'null',
            u'saida': 'null',
            u'nova_entrada': 'null',
            u'acessos': 0,
        }
        db.collection(u'historico_ref').document(plates_numbers).set(data)
        print('O valor',plates_numbers,'foi registrado no banco!')



def registrar_entrada_saida(texto):
    plates_numbers = texto
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
    hist_ref(plates_numbers)

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
        print('Entrada registrada com sucesso!')
        hist_ref(plates_numbers)
    elif sai == 'null':
        registro_saida = {
            'saida': firestore.SERVER_TIMESTAMP
        }
        #historico_ref.add(registro_saida)
        db_.update(registro_saida)
        print('Saída registrada com sucesso!')
        hist_ref(plates_numbers)
    elif nen == 'null':
        reg_acesso = int(acs)+1
        registro_nova_entrada = {
            'nova_entrada': firestore.SERVER_TIMESTAMP,
            'acessos': reg_acesso
        }
        #historico_ref.add(registro_saida)
        db_.update(registro_nova_entrada)
        print('Já existem uma entrada e uma saída registradas.')
        print('Nova entrada registrada com sucesso!')
        hist_ref(plates_numbers)
    else: 
        novo_registro = {
        'entrada': nen,
        'saida': firestore.SERVER_TIMESTAMP,
        'nova_entrada': 'null',
}
        db_.update(novo_registro)
        print('Novo registro adicionado')
        print('Saída registrada com sucesso!')
        hist_ref(plates_numbers)





def deletar_placa(plates_numbers):
    db.collection(u'plates').document(plates_numbers).delete()
    db.collection(u'historico_ref').document(plates_numbers).delete()
    print('Placa deletada do banco!')




def relatorio_geral():
    print('Relatorio geral: ')
    placas = db.collection(u'plates').document()
    registros = db.collection(u'historico_ref').document()
    print(placas.get())
    print(registros.get())
    


            









while(True):
    relatorio_geral()
    #plate_numbers = 'LSN4149'
    #plate_numbers = (plate_numbers).upper()
    #registrar_placa(plate_numbers)
    #registrar_entrada_saida(plate_numbers)
    #deletar_placa(plate_numbers)
    #captura()
    break
    
    """plate_numbers = 'CSC-2013'
    registrar_placa(plate_numbers)
    registrar_entrada_saida(plate_numbers)
    #hist_ref(plate_numbers)
    #deletar_placa(plate_numbers)
    #TESTE_CHAMADA()"""
    """menu = int(input("\n\nPara fazer uma captura digite 1;\n"
        "Para verificar as placas autorizadas, digite 2;\n"
        "Para verificar as placas registradas, digite 3;\n"
        "\nO que você deseja fazer?: "))
    if menu == 1: captura()
    elif menu == 2: main()
    elif menu == 3: printar()
    else:
        break"""
