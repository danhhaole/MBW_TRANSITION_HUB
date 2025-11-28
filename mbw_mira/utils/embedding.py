import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import frappe
from frappe import _

def compare_vector_with_list(target_vec, vector_list, top_k=None):
    target = np.array(target_vec).reshape(1, -1)
    vectors = np.array(vector_list)

    scores = cosine_similarity(target, vectors)[0]

    # Nếu có threshold
    if top_k is not None:
        return float(max(scores)) if max(scores) >= top_k else 0.0

    return [{"index": i, "score": float(s)} for i, s in enumerate(scores)]
