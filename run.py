"""
Interface console/detecteur
Usage : python -m detect_visage.run -h
"""
import getopt
import sys
from detect_visage.app.detect import DetectVisage


def usage():
    print("python -m detect_visage.run -i <chemin_vers_image>")
    print("ou")
    print("python -m detect_visage.run --image <chemin_vers_image>")


try:
    opts, args = getopt.getopt(sys.argv[1:], 'h:i:', ['help', 'image'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

chemin_image = ''
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(1)
    elif opt in ('-i', '--image'):
        chemin_image = arg

detecteur = DetectVisage()
if detecteur.detect(chemin_image):
    print("Visage detecte !")
else:
    print("Pas de visage")
