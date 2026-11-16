import json
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parent
enc_path = BASE_DIR.parent / "encounters.json"

def getEncounter(type = "random"):
    with open(enc_path, "r") as file:
            data = json.load(file)
    random.seed(None)
    if(type =="random"):
          number = random.randint(0, len(data) -1)
          if(number ==0):
                type ="social"
          if(number ==1):
                type ="combat"
          if(number ==2):
                type ="hazard"
          if(number ==3):
                type ="puzzle"
          print(type)
        
          
    number = random.randint(0, len(data[type]) -1)
    #print(data[type][number])
    return data[type][number]



#type = "hazard"
#getEncounter(type)