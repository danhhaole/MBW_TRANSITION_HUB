import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import frappe
from frappe import _

def compare_vector_with_list(target_vec, vector_list, top_k=None):
    """
    So sánh 1 vector với danh sách nhiều vector (cosine similarity).

    Args:
        target_vec (list[float]): vector cần so sánh
        vector_list (list[list[float]]): danh sách vector
        top_k (int, optional): nếu muốn lấy top K kết quả

    Returns:
        list[dict]: danh sách {index, score}, sắp xếp giảm dần
    """

    if not target_vec:
        frappe.throw(_("Target vector cannot be empty"))

    if not vector_list:
        frappe.throw(_("Vector list cannot be empty"))

    # kiểm tra chiều dài vector
    vector_len = len(target_vec)
    for i, v in enumerate(vector_list):
        if len(v) != vector_len:
            frappe.throw(
                _("Vector at index {0} has different length").format(i)
            )

    # reshape đúng chuẩn sklearn
    a = np.array(target_vec).reshape(1, -1)
    b = np.array(vector_list)

    # tính similarity
    scores = cosine_similarity(a, b)[0]   # output là mảng 1 chiều

    # map index → score
    results = [
        {"index": idx, "score": float(score)}
        for idx, score in enumerate(scores)
    ]

    # sort giảm dần
    results.sort(key=lambda x: x["score"], reverse=True)

    # nếu chỉ lấy top K
    if top_k:
        return results[:top_k]

    return results
