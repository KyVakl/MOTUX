import sys
from lxml import etree
import pickle
from common.Utils import Utils
from common.Parameters import Parameters

dictionnarieList = []

def getListOfWords(dicoEntry):
    inputList = dicoEntry.split() # Par défaut, la séparation se fait sur les espaces, ce qui est notre cas
    outputList = []

    # Certains mots, comme "100\-mètres" contiennent un '\'. Nous le supprimons
    for word in inputList:
        word = Utils.getNormalizedToUpperCaseWord(word)
        if Utils.isWordValid(word):
            outputList.append(word)

    return outputList


def addWords(wordsList):

    # On calcule la longueur du mot le plus grand    
    longestWordLength = 0
    for word in wordsList:
        if len(word) > longestWordLength:
            longestWordLength = len(word)

    # On prépare le tableau de dictionnaires de sortie:
    while len(dictionnarieList) < longestWordLength:
        dictionnarieList.append([])    

    # On rajoute chaque mot à sa liste (numérotée par longueur de mots)
    for word in wordsList:
        index = len(word) - 1 # Le premier index est 1
        if word not in dictionnarieList[index]:
            dictionnarieList[index].append(word)

# Cette fonction écrit les listes dans un fichier.
# Pour les relire, utiliser: itemlist = pickle.load(fp)
def writeSubDico(listOfWord, charsCount, folder):
    name = folder + '\\' + str(charsCount) + ".dico"
    with open(name, 'wb') as fp:
        pickle.dump(listOfWord, fp)

def readDico(inputPath, outputPath):
    print("Lecture du fichier " + inputPath)
    tree = etree.parse(inputPath)
    print("Le fichier " + inputPath + "a bien été lu")

    wordsList = tree.xpath("/dico/entry/lemma")

    index = 0
    for word in wordsList:
        addWords(getListOfWords(word.text))
        index = index + 1
        print('\r', end='') # On revient au début de la ligne
        print("Analyse en cours. " + str(int(100 * index / len(wordsList))) + " % effectué.", end="")
    
    print("") # On saute une ligne

    for i in range(0, len(dictionnarieList)):
        l = dictionnarieList[i]
        wordsCount = len(l)
        print("Le dictionnaire " + str(i) + " contient " + str(len(l)) + " mots de " + str(i + 1) + " caractères")
        if wordsCount >= Parameters.minimumWordsInDico():
            writeSubDico(l, i + 1, outputPath)

if __name__ == "__main__":

    # Le premier argument est le chemin vers CE programme
    # C'est donc le deuxième argument qui doit contenir le chemin vers le fichier xml d'entrée
    # Et le troisième le répertoire où écrire les sous-dictionnaires
    if len(sys.argv) < 3:
        print("Usage: python dico_generator.py chemin_vers_dictionnaire_xml repertoire_d_enregistrement_des_sous_dictionnaires")
        sys.exit(1)

    # Le premier argument est 0, donc le deuxième est 1, ...
    readDico(sys.argv[1], sys.argv[2])

