import os
import cv2
from lib.filters import get_grayscale, thresholding, pytesseract
from lib.format_output import format_output
from lib.format_output2 import format_output2


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


def hist_ref(plate_numbers):
    db_ = db.collection(u'historico_ref').document(plate_numbers)
    
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

        print(f"\n",plate_numbers,":")
        print("Acessos:", a)
        print("Entrada:", e)
        print("Saida:", s)
        print("Nova Entrada:", ne,"\n")


def apply_filter(plate):
    gray = get_grayscale(plate)
    thresh = thresholding(gray)
    return thresh



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


def check_value(plate_number):
    print(plate_number)
    valor = plate_number

    doc_ref = db.collection(u'plates').document(valor)

    doc = doc_ref.get()
    if doc.exists:
        return 'AUTHORIZED'
    else:
        return 'NOT AUTHORIZED'
    


def captura():
    cv = "s"
    captura_id = 0
    while cv == "s":
        cap = cv2.VideoCapture(0)
        while True:
            captura_id += 1
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 32:
                save_path = fr"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\images\captura{captura_id}.jpg"
                captured_image = cv2.imwrite(save_path, frame)
                cap.release()
                cv2.destroyAllWindows()
                break
        continuar = input("\nVocê deseja capturar outra placa? (S/N): ")
        if continuar.lower() == "s":
            cv = "s"
        else:
            return main()  # Chama a função main diretamente, não precisa retorná-la







def main():

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
        
    
    # Calls the function validate_plate() passing the plate number
    for i in range(len(plates_numbers)):
        data[i].append(check_value(plates_numbers[i]))
        #data[i].append(validate_plate(plates_numbers[i], authorized_plate))
    format_output(data)


def registrar_placa(plates_numbers):

    data = {plates_numbers: plates_numbers}
    db.collection(u'plates').document(plates_numbers).set(data)

    data = {
        u'entrada': 'null',
        u'saida': 'null',
        u'nova_entrada': 'null',
        u'acessos': 0,
    }
    db.collection(u'historico_ref').document(plates_numbers).set(data)
    return 'Registrado no banco!'



def registrar_entrada_saida():
    db_ = db.collection(u'historico_ref').document(u'CSC-2013')
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


    plates_numbers = 'CSC-2013'
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


while(True):

    #plates_numbers = 'CSC-2013'
    #registrar_placa(plates_numbers)
    #registrar_entrada_saida()
    #TESTE_CHAMADA()
    menu = int(input("\n\nPara fazer uma captura digite 1;\n"
        "Para verificar as placas autorizadas, digite 2;\n"
        "Para verificar as placas registradas, digite 3;\n"
        "\nO que você deseja fazer?: "))
    if menu == 1: captura()
    elif menu == 2: main()
    elif menu == 3: printar()
    else:
        break
