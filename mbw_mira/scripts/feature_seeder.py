# -*- coding: utf-8 -*-
import json, os, pkgutil
import frappe

APP_MODULE = "MBW Mira"  # fallback nếu module data không cung cấp

MIRA_ROLES = [
    "Talent Recruiter",
    "Talent HR Manager",
    "Talent HR User",
]

# Map mặc định (nếu cần)
FAKE_ROLE_MAP = {
    # Campaign Features
    "mira_campaign_full_access":         ["Talent Recruiter"],
    "mira_campaign_creation":            ["Talent Recruiter", "Talent HR User"],
    "mira_campaign_view_only":           ["Talent HR Manager"],
    "mira_campaign_management":          ["Talent Recruiter", "Talent HR Manager"],
    "mira_campaign_file_management":     ["Talent Recruiter", "Talent HR User"],
    "mira_campaign_sharing":             ["Talent Recruiter", "Talent HR Manager"],
    "mira_campaign_reporting":           ["Talent Recruiter", "Talent HR Manager"],
    
    # Segment (Pool) Features
    "mira_segment_full_access":          ["Talent Recruiter"],
    "mira_segment_creation":             ["Talent Recruiter", "Talent HR User"],
    "mira_segment_view_only":            ["Talent HR Manager"],
    "mira_segment_management":           ["Talent Recruiter", "Talent HR Manager"],
    "mira_segment_delete":               ["Talent Recruiter"],
    "mira_segment_reporting":            ["Talent Recruiter", "Talent HR Manager"],
    "mira_segment_sync_ats":             ["Talent Recruiter"],
    
    # Talent Features
    "mira_talent_full_access":           ["Talent Recruiter"],
    "mira_talent_creation":              ["Talent Recruiter", "Talent HR User"],
    "mira_talent_view_only":             ["Talent HR Manager"],
    "mira_talent_management":            ["Talent Recruiter", "Talent HR Manager"],
    "mira_talent_delete":                ["Talent Recruiter"],
    "mira_talent_reporting":             ["Talent Recruiter", "Talent HR Manager"],
    "mira_talent_import":                ["Talent Recruiter", "Talent HR User"],
    "mira_talent_export":                ["Talent Recruiter", "Talent HR Manager", "Talent HR User"],
    
    # Campaign Template Features
    "mira_campaign_template_full_access":     ["Talent Recruiter"],
    "mira_campaign_template_creation":        ["Talent Recruiter", "Talent HR User"],
    "mira_campaign_template_view_only":       ["Talent HR Manager"],
    "mira_campaign_template_management":      ["Talent Recruiter"],
    "mira_campaign_template_delete":          ["Talent Recruiter"],
    "mira_campaign_template_use":             ["Talent Recruiter", "Talent HR Manager", "Talent HR User"],
    
    # Interaction Features
    "mira_interaction_full_access":      ["Talent Recruiter"],
    "mira_interaction_creation":         ["Talent Recruiter", "Talent HR User"],
    "mira_interaction_view_only":        ["Talent HR Manager"],
    "mira_interaction_management":       ["Talent Recruiter"],
    "mira_interaction_delete":           ["Talent Recruiter"],
    "mira_interaction_reporting":        ["Talent Recruiter", "Talent HR Manager"],
    "mira_interaction_analytics":        ["Talent Recruiter", "Talent HR Manager"],
    
    # Action Features
    "mira_action_full_access":           ["Talent Recruiter"],
    "mira_action_creation":              ["Talent Recruiter", "Talent HR User"],
    "mira_action_view_only":             ["Talent HR Manager"],
    "mira_action_management":            ["Talent Recruiter"],
    "mira_action_delete":                ["Talent Recruiter"],
    "mira_action_reporting":             ["Talent Recruiter", "Talent HR Manager"],
    "mira_action_execution":             ["Talent Recruiter", "Talent HR User"],
}

# ---------------------------- helpers ----------------------------
def _doctype_installed(doctype_name: str) -> bool:
    return bool(frappe.db.exists("DocType", doctype_name))

def ensure_roles():
    print("=== Ensure MIRA Roles ===")
    for role_name in MIRA_ROLES:
        if frappe.db.exists("Role", role_name):
            # Không ghi đè settings của role đã tồn tại để tránh xung đột với các app khác
            print(f"• Role exists: {role_name} (skipping update)")
        else:
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 0,
                "home_page": ""
            }).insert(ignore_permissions=True)
            print(f"✔ Created Role: {role_name}")

def _perm_row_from_json(p: dict) -> dict:
    def f(k): return 1 if int(p.get(k, 0) or 0) else 0
    return {
        "doctype_name": p.get("doctype"),
        "is_select": f("read"),
        "is_create": f("create"),
        "is_email":  f("email"),
        "is_export": f("export"),
        "is_read":   f("read"),
        "is_delete": f("delete"),
        "is_report": f("report"),
        "is_share":  f("share"),
        "is_write":  f("write"),
        "is_print":  f("print"),
        "is_import": f("import"),
    }

def _upsert_feature_from_file(feature: dict, module_label: str):
    dn = feature["feature_name"]
    if frappe.db.exists("MBW Feature Settings", dn):
        doc = frappe.get_doc("MBW Feature Settings", dn)
        is_new = False
    else:
        doc = frappe.get_doc({"doctype": "MBW Feature Settings", "feature_name": dn})
        is_new = True

    doc.label = feature.get("label") or dn
    doc.description = feature.get("description") or ""
    doc.is_active = 1 if int(feature.get("is_active", 1) or 1) else 0
    doc.module = module_label or APP_MODULE  # lưu module tại Feature

    # replace child
    doc.set("permissions", [])
    for p in feature.get("permissions", []) or []:
        doc.append("permissions", _perm_row_from_json(p))

    if is_new:
        doc.insert(ignore_permissions=True)
        print(f"✔ Inserted Feature: {dn} (module={doc.module})")
    else:
        doc.save(ignore_permissions=True)
        print(f"↺ Updated Feature: {dn} (module={doc.module})")

def ensure_docperm_for_feature(feature: dict, roles: list):
    """Tạo Custom DocPerm từ feature.permissions → gắn cho Role."""
    for p in feature.get("permissions", []) or []:
        dt = p.get("doctype")
        if not dt:
            continue
        for role in roles:
            exists = frappe.db.exists("Custom DocPerm", {"role": role, "parent": dt})
            if not exists:
                docperm = frappe.get_doc({
                    "doctype": "Custom DocPerm",
                    "parent": dt,
                    "parentfield": "permissions",
                    "parenttype": "DocType",
                    "role": role,
                    "read": int(p.get("read", 0)),
                    "write": int(p.get("write", 0)),
                    "create": int(p.get("create", 0)),
                    "delete": int(p.get("delete", 0)),
                    "email": int(p.get("email", 0)),
                    "export": int(p.get("export", 0)),
                    "report": int(p.get("report", 0)),
                    "share": int(p.get("share", 0)),
                    "print": int(p.get("print", 0)),
                    "import": int(p.get("import", 0)),
                })
                docperm.insert(ignore_permissions=True)
                print(f"✔ Added DocPerm: {dt} ↔ {role}")
            else:
                print(f"• DocPerm exists: {dt} ↔ {role}")

def ensure_feature_role_link(feature_name: str, role_name: str):
    key = {"feature_name": feature_name, "role": role_name}
    print('========================= key: ', key, flush=True)
    if not frappe.db.exists("MBW Feature Role Permission", key):
        print('========================= 3 ', key, flush=True)
        frappe.get_doc({
            "doctype": "MBW Feature Role Permission",
            "feature_name": feature_name,
            "role": role_name,
            "is_active": 1,
        }).insert(ignore_permissions=True)
        print(f"✔ Linked: {feature_name} ↔ {role_name}")
    else:
        print(f"• Link exists: {feature_name} ↔ {role_name}")

# ---------------------------- load data (Phương án 2) ----------------------------
def _load_feature_data() -> dict:
    """
    Ưu tiên import module Python (mbw_mira.config.featureMira).
    Fallback: tìm JSON trong app (mbw_mira/config/featureMira.py) để dev tiện soát.
    """
    # 1) import Python module
    try:
        from mbw_mira.config.featureMira import FEATURES_MIRA
        if isinstance(FEATURES_MIRA, dict) and FEATURES_MIRA.get("modules"):
            return FEATURES_MIRA
    except Exception as e:
        print(f"[feature_seeder] WARN: cannot import FEATURES_DATA from module: {e}")

    # 2) fallback: JSON trong app
    json_path = frappe.get_app_path("mbw_mira", "mbw_mira", "config", "featureMira.py")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # 3) fallback cuối: resource package
    try:
        raw = pkgutil.get_data("mbw_mira", "mbw_mira/config/featureMira.py")
        if raw:
            return json.loads(raw.decode("utf-8"))
    except Exception:
        pass

    raise FileNotFoundError("Không tìm thấy FEATURES_DATA (module) hoặc featureATS.json trong app")

def _iter_features(data: dict):
    """Yield (feature_dict, module_label)"""
    global APP_MODULE
    if data.get("label"):
        APP_MODULE = data["label"]

    modules = data.get("modules", []) or []
    for m in modules:
        module_label = data.get("label") or APP_MODULE  # dùng label app (“MBW ATS”) làm module cho Feature
        for feature in m.get("features", []) or []:
            yield feature, module_label

# ---------------------------- public APIs ----------------------------
def seed():
    """Roles → Features (import từ module Python) → Links + Custom DocPerm."""
    ensure_roles()

    need = [
        "MBW Feature Settings",
        "MBW Feature Setting Detail",
        "MBW Feature Role Permission",
    ]
    missing = [dt for dt in need if not _doctype_installed(dt)]
    if missing:
        print("⏭️ Skip seeding features: missing DocTypes ->", ", ".join(missing))
        print("👉 bench migrate rồi chạy lại: bench --site <yoursite> execute mbw_mira.scripts.feature_seeder.seed")
        return {"skipped_missing_doctypes": missing}

    data = _load_feature_data()
    print("=== Read features from Python module: mbw_mira.config.featureATS ===")
    print(f"APP_MODULE (from data['label']) = {data.get('label') or APP_MODULE}")

    print("=== Upsert Features ===")
    feature_names = []
    for feature, module_label in _iter_features(data):
        _upsert_feature_from_file(feature, module_label)
        feature_names.append(feature["feature_name"])

    print("=== Link Feature ↔ Role & Sync DocPerm ===")
    for fname, roles in FAKE_ROLE_MAP.items():
        print('========================= fname: ', fname, flush=True) 
        print('========================= roles: ', roles, flush=True)
        if fname not in feature_names:
            continue
        for r in roles:
            print(">>>>>>>>>>>>>>>2")
            # Link role ↔ feature
            ensure_feature_role_link(fname, r)
            print('========================= 3', flush=True)

            # Tìm feature detail trong data để sync DocPerm
            for module in data.get("modules", []):
                print('========================= 4', flush=True)
                for f in module.get("features", []):
                    print('========================= 5', flush=True)
                    if f["feature_name"] == fname:
                        ensure_docperm_for_feature(f, [r])
                        break

    frappe.db.commit()
    print("✅ DONE seed")
    return {"features": feature_names}


def print_payload():
    """In payload đọc từ module Python (KHÔNG ghi DB)."""
    data = _load_feature_data()
    module_label = data.get("label") or APP_MODULE

    features_payload = []
    for feature, _module in _iter_features(data):
        features_payload.append({
            **feature,
            "module": module_label,
            "permissions": [_perm_row_from_json(p) for p in feature.get("permissions", []) or []],
        })

    print("=== ROLES ===")
    print(json.dumps(MIRA_ROLES, ensure_ascii=False, indent=2))
    print("\n=== MBW Feature Settings (from module) ===")
    print(json.dumps(features_payload, ensure_ascii=False, indent=2))

    print("\n=== MBW Feature Role Permission (links; map mặc định) ===")
    links = [
        {"doctype": "MBW Feature Role Permission", "feature_name": fname, "role": role, "is_active": 1}
        for fname, roles in FAKE_ROLE_MAP.items()
        for role in roles
        if any(f["feature_name"] == fname for f in features_payload)
    ]
    print(json.dumps(links, ensure_ascii=False, indent=2))
    return {"feature_count": len(features_payload), "link_count": len(links)}