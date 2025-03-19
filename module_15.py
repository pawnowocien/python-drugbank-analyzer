# Zrealizować punkt 6 tak, aby możliwe było wysłanie id leku na Twój serwer, który zwróci
# wynik w odpowiedzi (skorzystaj z fastapi i uvicorn; wystarczy zademonstrowanie przesłania
# danych metodą POST, przez Execute w dokumentacji)
from fastapi import FastAPI
from pydantic import BaseModel

from utils import get_drugs, get_id, get_pathways


DATA_SOURCE = None     # W razie potrzeby można zmienić źródło danych

app = FastAPI()

class PathCountRequest(BaseModel):
    drug_id: str

# Generuje słownik id leku - liczba szlaków
def gen_database(data=None):
    path_count = {}
    for drug in get_drugs(data):
        pathways = get_pathways(drug)
        drug_id = get_id(drug)
        if pathways is not None:
            path_count[drug_id] = len(pathways)
        else:
            path_count[drug_id] = 0
    return path_count

database = gen_database(DATA_SOURCE)
@app.post("/")
def index(request:PathCountRequest) -> dict:
    drug_id = request.drug_id
    if drug_id in database:
        return { drug_id: database[drug_id] }
    return { drug_id: None }    # Jeśli lek jest nieprawidłowy zwracamy null