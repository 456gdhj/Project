import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        location = location.lower()
        loc_index = -1
        if location in __data_columns:
            loc_index = __data_columns.index(location)

        x = np.zeros(len(__data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_index >= 0:
            x[loc_index] = 1

        return round(__model.predict([x])[0], 2)
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __data_columns = [col.lower() for col in __data_columns]  # Normalize to lowercase
        __locations = __data_columns[3:]

    if __model is None:
        with open('./artifacts/bangalore_home_price_model.pickle', 'rb') as f:
            __model = pickle.load(f)

    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))  # unknown location
    print(get_estimated_price('Ejipura', 1000, 2, 2))   # known location
