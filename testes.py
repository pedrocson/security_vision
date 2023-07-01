import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"C:\Users\Pedro\Desktop\TCC2\license-plate-recognition-main\src\json_firebase.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()




print("Deixa eu ver...")
doc_ref = db.collection(u'plates').document(u'FUN-0972')

doc = doc_ref.get()
if doc.exists:
    #print(f'Document data: {doc.to_dict()}')
    print("Sim")
else:
    print("Não")



docs = db.collection(u'historico_ref').stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')