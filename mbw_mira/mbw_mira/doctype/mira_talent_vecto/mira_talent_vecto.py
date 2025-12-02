# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import ast
import frappe
import json
from frappe.model.document import Document
from mbw_mira.utils.ai import get_vector_embeddings
from mbw_mira.utils.embedding import compare_vector_with_list


class MiraTalentVecto(Document):

	def on_update(self):
		try:
			if self.summary_text:
				frappe.enqueue(
                        "mbw_mira.mbw_mira.doctype.mira_talent_vecto.mira_talent_vecto.set_vecto_and_compare",
                        queue="default",
                        doc=self.as_dict()
                    )
		except Exception as e:
			frappe.log_error(f"Lỗi compare {str(e)}")
			pass
	
def safe_parse_vector(value):
    """Trả về list[float] bất kể input là string JSON hay list."""
    if value is None:
        return None

    # Nếu là string JSON -> parse
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            frappe.log_error("Invalid JSON vector", value)
            return None

    # Nếu đã là list -> trả về luôn
    if isinstance(value, list):
        return value

    return None

def set_vecto_and_compare(doc):
    embedding_vector= get_vector_embeddings([json.dumps(doc.summary_text)])
    if embedding_vector:
        frappe.db.set_value("Mira Talent Vecto",doc.name, 'embedding_vector',json.dumps(embedding_vector[0]))

        compare_talent_pool_vecto(doc.mira_talent)


def compare_talent_pool_vecto(talent_id):
    # Lấy vector của talent
    embedding_str = frappe.db.get_value(
        "Mira Talent Vecto",
        {"mira_talent": talent_id},
        "embedding_vector"
    )
    target = safe_parse_vector(embedding_str)

    # Lấy list vector pool
    pool = frappe.get_all("Mira Pool Vecto", fields=["embedding_vector"])
    list_vec = [safe_parse_vector(item["embedding_vector"]) for item in pool]

    # loại bỏ vector None
    list_vec = [x for x in list_vec if x]

    score = compare_vector_with_list(target, list_vec)
    return score
	