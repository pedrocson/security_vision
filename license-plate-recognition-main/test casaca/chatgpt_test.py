from flask import Flask, render_template, Response
import cv2
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    """Rota para renderizar a página inicial."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


def gen_frames():  
    """Gerar quadros para o streaming de vídeo."""
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # Lê o quadro da câmera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            



@app.route('/capture')
def capture():
    """Rota para capturar uma imagem estática da webcam e processá-la com o Pytesseract."""
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    if success:
        cv2.imwrite('capture.jpg', frame)
        
    image_path = 'capture.jpg'
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    

    return text, render_template('result.html', text=text)




@app.route('/video_feed')
def video_feed():
    """Rota para o streaming de vídeo. Será a src do tag de vídeo no HTML."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')





