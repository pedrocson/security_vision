

## Procedimento para executar o aplicativo:

--Para executar este aplicativo, você deve ter python, flask, OpenCV, Thread, pytesseract, os, e firebase instalados.
Para instalar a biblioteca pytesseract você precisa intalar o programa Thesseract-OCR, disponível em: https://github.com/tesseract-ocr/tessdoc.


Em seguida, execute um comando pip para fazer a instalação de cada uma das bibliotecas:

pip install opencv-python;
pip install flask;
pip install pytesseract;
pip install firebase-admin;
pip install os;
pip install Thread;

#Modificar os diretórios de acordo com o seu computador:
path_pytesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
cred = credentials.Certificate(r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\src\json_firebase.json")
directory = r"C:\Users\Pedro\Desktop\teste\Reconhecimento de placa - Security_Vision\shots"



--Para inciar a aplicação, execute o código e depois pressione a tecla ctrl e clique em cima do link http://127.0.0.1:5000/ que irá aparecer no terminal python;
Ou então copie e cole http://127.0.0.1:5000/ em seu navegador de internet favorito e pronto.

--Por favor, leia minha postagem no medium para obter uma explicação detalhada: https://medium.com/@pedro.motta124/security-vision-sistema-web-para-controlar-o-acesso-de-ve%C3%ADculos-em-condom%C3%ADnios-88ab7efb6910

