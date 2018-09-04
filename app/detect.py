"""Module contenant la classe DetectVisage"""
import os
import sys
import cv2


class DetectVisage:
    """
    Classe gerant le detecteur de visages
    Utilise le mdele pre-entraine haarcascade_frontalface_default.xml
    Methodes :
       load_model
       detect
    """

    def __init__(self):
        self.filtre = ''
        self.charge_model()

    def charge_model(self):
        """
        Cette methode charge le modele de detection dans une variable de notre classe DetectVisage
        """

        root_path = os.path.dirname(sys.modules['__main__'].__file__)
        model_path = os.path.join(root_path, 'models')
        self.filtre = cv2.CascadeClassifier(
            os.path.join(model_path, 'haarcascade_frontalface_default.xml'))

    def detect(self, path_image):
        """
        Cette methode effectue la detection a partir du modele charge precedement
        Parametre:
          path_image : chemin vers l'image sur laquelle on souhaite faire une detection
        """

        print(path_image)
        image = cv2.imread(path_image)
        image_niveaux_gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = self.filtre.detectMultiScale(image_niveaux_gris)
        return False if len(face) == 0 else True
