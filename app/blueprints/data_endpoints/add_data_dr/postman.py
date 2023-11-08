import requests
import json
import datetime
class Postman:
    def __init__(self,API_email,password,name,orgID):
        self.API_email = API_email
        self.password = password
        self.name = name
        self.orgID =orgID

        self.url_v1 = "https://api.machinemax.com/v1/iso/Fleet/1"
        self.headers_v1 = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.authenticate()
                }
        # for count in range(1,36):
        #     self.url_v1 = f"https://api.machinemax.com/v1/iso/Fleet/{count}"
        #     self.GET()
    def GET(self):
        self.response = requests.get(self.url_v1, headers=self.headers_v1)
        if self.response.status_code != 200:
            print(f"postman.py: Error with requests status code {self.response.status_code}")
            return {}
        else:
            self.response = self.response.text
            self.response = json.loads(self.response)
            self.fleet = self.response['Fleet']['Equipment']

            fleet_dictionary = {}
            for equipment in self.fleet:
                equipment = dict(equipment)
                #Syntax for self.get details is (dictionary,key) - note equipment['EquipmentHeader'] is a dictionary

                api_calls = []
                for datetime_key in equipment.keys():
                    try:
                        datetime_dict = {
                            datetime_key : equipment[datetime_key]["datetime"]
                                         }
                        api_calls.append(datetime_dict)
                        #This will only append keys with "datetime" child keys
                    except:
                        pass

                api_calls_datetime_format = [(key, datetime.datetime.fromisoformat(value.rstrip("Z"))) for item in api_calls for key, value in item.items()]
                latest_call_tuple = max(api_calls_datetime_format, key=lambda x: x[1])

                messy_equip_dict = equipment['EquipmentHeader']
                clean_equip_dict = \
                    {self.equipment_header(messy_equip_dict, 'SerialNumber'):
                         {'Asset ID': self.equipment_header(messy_equip_dict, 'EquipmentID'),
                          'Model': self.equipment_header(messy_equip_dict, 'SerialNumber'),
                          "OEM": self.equipment_header(messy_equip_dict, 'OEMName'),
                          'Latest Call Type': latest_call_tuple[0],
                          'Latest Call':latest_call_tuple[1],
                          'API Calls':api_calls
                          }
                     }
                fleet_dictionary = fleet_dictionary | clean_equip_dict
            return {'name':self.name, 'orgID':self.orgID, 'fleet':fleet_dictionary}

    def authenticate(self):
        self.url_authenticate = "https://api.machinemax.com/v1/auth/authenticate"
        self.headers_authenitcate = {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.32.3",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        self.body_authenitcate = {
                               "email": self.API_email,
                               "password": self.password
                                 }
        self.body_authenitcate = json.dumps(self.body_authenitcate)

        try:
            with open("token.txt") as file_token:
                timestamp_str, prev_string = file_token.read().split('\n', 1)
                last_generated_time = datetime.datetime.fromisoformat(timestamp_str)
                if (datetime.datetime.now() - last_generated_time).seconds < 25 * 60:
                    print("postman.py: Using old token",prev_string)
                    return prev_string

        except (FileNotFoundError, ValueError):
               pass

        response_authenticate = requests.post(self.url_authenticate, headers=self.headers_authenitcate, data=self.body_authenitcate)
        response_authenticate = response_authenticate.json()['idToken']
        with open('token.txt', "w") as f:
            f.write(f"{datetime.datetime.now().isoformat()}\n")
            f.write(response_authenticate)
        print("postman.py: Creating new token")
        return response_authenticate

    def equipment_header(self,dictionary,key):
        try:
            return dictionary[key]
        except:
            return f"No {key}"

    def update_database(self):

        pass

