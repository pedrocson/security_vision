import cv2
    # Captura a imagem da webcam
cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    # Aguarda a tecla 'q' ser pressionada para encerrar a captura
    if cv2.waitKey(1) & 0xFF == 32:
        break
save_path = r"C:\Users\Pedro\Desktop\TCC2\testes\Placas\placa.png"
cv2.imwrite(save_path,frame)
    # Libera os recursos:
cap.release()
cv2.destroyAllWindows()



