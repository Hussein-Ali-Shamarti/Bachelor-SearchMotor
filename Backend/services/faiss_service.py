# Dette skriptet initialiserer FAISS-indeksen ved å laste den fra disk eller bygge den på nytt 
# basert på embeddings lagret i databasen. Returnerer selve indeksen og tilhørende artikkel-IDer.


from faiss_helper import load_or_rebuild_faiss_index

def init_faiss_index():
    """Loads or rebuilds the FAISS index and returns the index along with IDs."""
    index, ids = load_or_rebuild_faiss_index()
    if index is None:
        print("FAISS index is empty! No embeddings found in the database.")
    return index, ids
