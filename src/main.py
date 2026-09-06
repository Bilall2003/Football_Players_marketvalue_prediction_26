from eda import clean,insights
from model import model_training
from model_check import model_verify
from FE import feature_engineering

file_path=r"D:\Bilal folder\AIML\ML practice\playermarketvalue\football_ml_dataset.csv"

def mainfun():

    #load and clean file
    obj1=clean(file_path)

    # get insight
    # insights(obj1)
    
    obj2=feature_engineering(obj1)

    #model training
    obj3=model_training(obj2)
    
if __name__=="__main__":
    
    mainfun()
    
    

