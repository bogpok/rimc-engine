import os
from rimc_engine import open_apply_save
from rimc_engine import recipes_collection


import datetime

def main():
    path = "orig/"    
    
    print(os.listdir(path))
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            # Get the current timestamp
            current_timestamp = round(datetime.timestamp(datetime.now())/10)
            print(current_timestamp)
            print(recipes_collection)
            open_apply_save(f, suffix=str(current_timestamp), recipe=recipes_collection["GOLD"], keep_original_size=True)
            open_apply_save(f, suffix=str(current_timestamp)+"S", recipe=recipes_collection["SUPR"], keep_original_size=True)

        

if __name__ == "__main__":
    main()