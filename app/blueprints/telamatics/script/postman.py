import json
import requests
import pprint
def main(sourceList,orgID):
    #sourceList = ["KOMTRAX","HITACHI","HITACHIV2","TRACKUNIT","TRACKUNITV2","JCB","CAT","CATV2","VOLVO","VOLVOV2","DOOSAN","DOOSANV1","TEREX","BELL","CASE","LIEBHERR","BOMAG","BAUER","KOBELCO","LIUGONG","JOHN_DEERE","HYUNDAI","PROEMION","ENIGMA","VOLVOHAULASSIST"]

    dictionary = Postman(sourceList,orgID)
    #Returns the form {Serial:{AssetID:Value,{Fuel:Value,..}, SerialSerial:{AssetID:Value,{Fuel:Value,..}}
    return(dictionary.getData())

class Postman:
    def __init__(self,sourceList,orgID):
        self.url = "https://api.machinemax.com/v1/portal/admin/machines/import?key=AIzaSyAfX6H-JT5Bbn-frgjABdzLxCM6SGhd4YI"
        self.headers = {
            "Content-Type": "text/plain",
            "User-Agent": "PostmanRuntime/7.32.3",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        self.sourceList = sourceList
        self.orgID = orgID
        self.returnDictionary = {}


    def getData(self):
        for source in self.sourceList:
            self.data = {
                "organisationId": self.orgID,
                "source": source,
                "dry": "TRUE"
            }

            self.data = json.dumps(self.data)
            response = requests.post(self.url, headers=self.headers, data=self.data)
            response = response.text.strip("\n").strip(' ')
            if response == '{"created":[],"updated":[],"conflicts":[],"dry":true,"unassociated":[]}':
                 pass
            elif "Unknown source" in response:
                pass
            else:

                unassociated = json.loads(response)['unassociated']
                for equipment in unassociated:
                    externalID = equipment['external_id']
                    equipmentInfo = json.loads(equipment['info'])
                    serial = self.getDictValue(equipmentInfo,'serial_number')
                    make = self.getDictValue(equipmentInfo,'make')
                    equipmentID = self.getDictValue(equipmentInfo,'equipment_id')
                    model = self.getDictValue(equipmentInfo,'model')
                    equipmentDict = {serial: { "Make": make, "Equipment ID": equipmentID, 'External ID':externalID, 'Model':model, 'Unassociated':'True', 'Source':source}}
                    self.returnDictionary = self.returnDictionary | equipmentDict


        return(self.returnDictionary)

    def getDictValue(self, equipmentInfo, key):
        try:
            return equipmentInfo[key]
        except:
            return ''


