from app.blueprints.telamatics.script import excelImport
from app.blueprints.telamatics.script import postman
from app.blueprints.telamatics.script import sourceChecker

def main(file,orgID):
    #file = 'excelTest.csv'
    source = ["KOMTRAX","HITACHI","HITACHIV2","TRACKUNIT","TRACKUNITV2","JCB","CAT","CATV2","VOLVO","VOLVOV2","DOOSAN","DOOSANV1","TEREX","BELL","CASE","LIEBHERR","BOMAG","BAUER","KOBELCO","LIUGONG","JOHN_DEERE","HYUNDAI","PROEMION","ENIGMA","VOLVOHAULASSIST"]
    org = "32afd2bd-7bad-4618-a0df-1dcc1b8fdaa2"

    excelDict = excelImport.main(file)
    postmanDict = postman.main(source,orgID)
    return (sourceChecker.main(excelDict,postmanDict))



def main_but_no_import(excelDict,orgID):

    source = ["KOMTRAX","HITACHI","HITACHIV2","TRACKUNIT","TRACKUNITV2","JCB","CAT","CATV2","VOLVO","VOLVOV2","DOOSAN","DOOSANV1","TEREX","BELL","CASE","LIEBHERR","BOMAG","BAUER","KOBELCO","LIUGONG","JOHN_DEERE","HYUNDAI","PROEMION","ENIGMA","VOLVOHAULASSIST"]
    postmanDict = postman.main(source,orgID)
    return (sourceChecker.main(excelDict,postmanDict))
