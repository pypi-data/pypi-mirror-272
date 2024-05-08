import pickle
from pathlib import Path

import typer
from sentence_transformers import SentenceTransformer, util, CrossEncoder

import warnings

# Suppress FutureWarning
warnings.simplefilter(action="ignore", category=FutureWarning)

app = typer.Typer()


class SearchEngine:
    def __init__(self):
        self.bi_encoder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
        self.bi_encoder.max_seq_length = 256
        self.top_k = 32
        self.cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

        with open(Path(__file__).parent / "data/my-embeddings.pkl", "rb") as fIn:
            cache_data = pickle.load(fIn)
            self.passages = cache_data["sentences"]
            self.corpus_embeddings = cache_data["embeddings"]
            self.json = cache_data["json"]

    def search(self, query):
        print("Input question:", query)

        question_embedding = self.bi_encoder.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(question_embedding, self.corpus_embeddings, top_k=self.top_k)
        hits = hits[0]

        cross_inp = [[query, self.passages[hit["corpus_id"]]] for hit in hits]
        cross_scores = self.cross_encoder.predict(cross_inp)

        for idx in range(len(cross_scores)):
            hits[idx]["cross-score"] = cross_scores[idx]

        print("\n-------------------------\n")
        print("Top-3 Bi-Encoder Retrieval hits")
        hits = sorted(hits, key=lambda x: x["score"], reverse=True)
        for i, hit in enumerate(hits[0:3]):
            text = self.passages[hit["corpus_id"]]  # .replace("\n", " ")
            # json_data = self.json[hit["corpus_id"]]
            # {hit["score"] }
            print(f"{i + 1}. {text[:500]}", "..." if len(text) > 500 else "")


engine = SearchEngine()


@app.command()
def search(query: list[str]):
    print("searching...")
    engine.search(query=" ".join(query))


if __name__ == "__main__":
    app()
