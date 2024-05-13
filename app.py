# Importation des modules nécessaires
from flask import Flask, render_template, Response
import cv2
import imageio

# Création de l'application Flask
app = Flask(__name__)

# Initialisation de la caméra
camera = cv2.VideoCapture(0)


# Fonction pour diffuser la vidéo en direct
def cctv_live():
    # Création d'un objet VideoWriter pour enregistrer la vidéo
    writer = imageio.get_writer('output.mp4', fps=20)
    while True:
        # Lecture de la trame de la caméra
        success, frame = camera.read()
        if not success:
            break
        else:
            # Écriture de la trame dans la vidéo
            writer.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # Conversion de la trame en bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        # Renvoi de la trame en tant que réponse
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # Fermeture de l'objet VideoWriter une fois terminé
    writer.close()


# Route pour la page d'accueil
@app.route('/')
@app.route('/index')
def index():
    # Rendu du template HTML pour la page d'accueil
    return render_template('index.html')


# Route pour le flux vidéo
@app.route('/video_feed')
def video_feed():
    # Renvoi du flux vidéo en tant que réponse
    return Response(cctv_live(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Point d'entrée principal
if __name__ == '__main__':
    # Démarrage de l'application Flask
    app.run(debug=True)
