from rimc_engine import open_apply_save, Recipe, recipes_collection
import os
from datetime import datetime


def main():
    path = "orig/"    
    
    print(os.listdir(path))
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            # Get the current timestamp
            current_timestamp = round(datetime.timestamp(datetime.now())/10)
            print(current_timestamp)
            print(recipes_collection)
            open_apply_save(f, suffix=str(current_timestamp), recipe=recipes_collection["GOLD"])
            open_apply_save(f, suffix=str(current_timestamp)+"S", recipe=recipes_collection["SUPR"])

        

if __name__ == "__main__":
    main()