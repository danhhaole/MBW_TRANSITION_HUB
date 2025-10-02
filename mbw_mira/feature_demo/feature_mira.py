import json
import os
import pkgutil
import frappe
from typing import Dict, List, Optional, Any

APP_MODULE = "MBW Mira"  # fallback nếu module data không cung cấp

# Định nghĩa các vai trò chính trong hệ thống
MIRA_ROLES = {
    "marketing_admin": "Marketing Admin",
    "recruiter": "Recruiter",
    "hiring_manager": "Hiring Manager",
    "hr_manager": "HR Manager",
    "hr_user": "HR User"
}

# Ánh xạ vai trò với các tính năng tương ứng
FEATURE_ROLE_MAP = {
    # Marketing Admin - Toàn quyền hệ thống
    "data_source_management": [MIRA_ROLES["marketing_admin"]],
    "template_management": [MIRA_ROLES["marketing_admin"]],
    "campaign_full_access": [MIRA_ROLES["marketing_admin"]],
    "job_opening_management": [MIRA_ROLES["marketing_admin"]],
    "campaign_reporting": [MIRA_ROLES["marketing_admin"]],
    
    # Recruiter - Tạo và quản lý chiến dịch
    "campaign_creation": [MIRA_ROLES["recruiter"], MIRA_ROLES["hr_manager"]],
    "campaign_execution": [MIRA_ROLES["recruiter"], MIRA_ROLES["hr_manager"]],
    "applicant_pool_management": [MIRA_ROLES["recruiter"], MIRA_ROLES["hr_manager"]],
    
    # Hiring Manager - Chỉ xem và báo cáo
    "campaign_view_only": [MIRA_ROLES["hiring_manager"], MIRA_ROLES["hr_user"]],
    
    # HR Manager - Quyền HR cao cấp
    "hr_full_access": [MIRA_ROLES["hr_manager"]],
    
    # HR User - Quyền HR cơ bản
    "hr_basic_access": [MIRA_ROLES["hr_user"]]
}

# Định nghĩa các nhóm quyền
ROLE_GROUPS = {
    "marketing_team": [
        MIRA_ROLES["marketing_admin"]
    ],
    "recruitment_team": [
        MIRA_ROLES["recruiter"],
        MIRA_ROLES["hr_manager"]
    ],
    "hiring_team": [
        MIRA_ROLES["hiring_manager"],
        MIRA_ROLES["hr_user"]
    ]
}
def _doctype_installed(doctype_name: str) -> bool:
    """Kiểm tra xem một DocType đã được cài đặt chưa"""
    return bool(frappe.db.exists("DocType", doctype_name))

def ensure_roles():
    """Đảm bảo tất cả các vai trò đã được tạo trong hệ thống"""
    print("=== Đang khởi tạo vai trò MBW Mira ===")
    
    for role_key, role_name in MIRA_ROLES.items():
        desk_access = 1 if role_key in ["marketing_admin", "recruiter", "hr_manager"] else 0
        home_page = "/app" if role_key in ["marketing_admin", "recruiter", "hr_manager"] else ""
        
        if not frappe.db.exists("Role", role_name):
            # Tạo mới vai trò
            role_doc = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": desk_access,
                "home_page": home_page,
                "search_bar": 1,
                "notifications": 1,
                "list_sidebar": 1,
                "bulk_actions": 1,
                "view_switcher": 1,
                "form_sidebar": 1,
                "timeline": 1,
                "dashboard": 1
            })
            role_doc.insert(ignore_permissions=True)
            print(f"✔ Đã tạo vai trò: {role_name}")
        else:
            # Cập nhật vai trò hiện có
            role_doc = frappe.get_doc("Role", role_name)
            update_needed = False
            
            if role_doc.desk_access != desk_access:
                role_doc.desk_access = desk_access
                update_needed = True
                
            if role_doc.home_page != home_page:
                role_doc.home_page = home_page
                update_needed = True
            
            if update_needed:
                role_doc.save(ignore_permissions=True)
                print(f"• Đã cập nhật vai trò: {role_name}")
            else:
                print(f"✓ Vai trò đã tồn tại: {role_name}")

def setup_role_profiles():
    """Thiết lập các hồ sơ vai trò (Role Profiles)"""
    print("\n=== Thiết lập hồ sơ vai trò ===")
    
    for profile_name, roles in ROLE_GROUPS.items():
        profile_doc = {
            "doctype": "Role Profile",
            "role_profile": f"MBW {profile_name.replace('_', ' ').title()}",
            "roles": [{"role": role} for role in roles]
        }
        
        if not frappe.db.exists("Role Profile", profile_doc["role_profile"]):
            frappe.get_doc(profile_doc).insert(ignore_permissions=True)
            print(f"✔ Đã tạo hồ sơ: {profile_doc['role_profile']}")
        else:
            doc = frappe.get_doc("Role Profile", profile_doc["role_profile"])
            doc.roles = profile_doc["roles"]
            doc.save()
            print(f"• Đã cập nhật hồ sơ: {profile_doc['role_profile']}")

def get_user_roles(user: str = None) -> List[str]:
    """Lấy danh sách vai trò của người dùng"""
    if not user:
        user = frappe.session.user
    
    roles = frappe.get_roles(user)
    return [r for r in roles if r in MIRA_ROLES.values()]

def has_feature_access(feature_name: str, user: str = None) -> bool:
    """Kiểm tra xem người dùng có quyền truy cập tính năng không"""
    if not user:
        user = frappe.session.user
    
    if frappe.session.user == "Administrator":
        return True
        
    user_roles = get_user_roles(user)
    allowed_roles = FEATURE_ROLE_MAP.get(feature_name, [])
    
    return any(role in user_roles for role in allowed_roles)

def get_all_features() -> List[Dict[str, Any]]:
    """Lấy danh sách tất cả các tính năng"""
    features_dir = os.path.join(os.path.dirname(__file__), "..", "config")
    features_file = os.path.join(features_dir, "featureMira.json")
    
    try:
        with open(features_file, "r") as f:
            data = json.load(f)
            return data.get("modules", [{}])[0].get("features", [])
    except Exception as e:
        frappe.log_error(f"Lỗi khi đọc file tính năng: {str(e)}")
        return []

def get_user_features(user: str = None) -> List[Dict[str, Any]]:
    """Lấy danh sách các tính năng mà người dùng có quyền truy cập"""
    if not user:
        user = frappe.session.user
    
    all_features = get_all_features()
    user_features = []
    
    for feature in all_features:
        if has_feature_access(feature["feature_name"], user):
            user_features.append(feature)
    
    return user_features

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

def _upsert_feature_from_file(feature: dict, module_feature_mira: str):
    dn = feature["feature_name"]
    if frappe.db.exists("MBW Feature Settings", dn):
        doc = frappe.get_doc("MBW Feature Settings", dn)
        is_new = False
    else:
        doc = frappe.new_doc("MBW Feature Settings")
        doc.feature_name = dn
        is_new = True

    doc.feature_name = dn
    doc.label = feature.get("label", dn)
    doc.description = feature.get("description", "")
    doc.module = module_feature_mira
    doc.is_active = 1 if int(feature.get("is_active", 0) or 0) else 0

    # Permissions
    doc.set("permissions", [])
    for p in feature.get("permissions", []):
        if not _doctype_installed(p.get("doctype")):
            print(f"  ! Skip permission for missing doctype: {p.get('doctype')}")
            continue
        perm_data = _perm_row_from_json(p)
        doc.append("permissions", perm_data)

    # Roles - Skip for now as field may not exist

    if is_new:
        doc.insert(ignore_permissions=True)
        print(f"✔ Created Feature: {dn}")
    else:
        doc.save(ignore_permissions=True)
        print(f"~ Updated Feature: {dn}")

def ensure_features_role_link(feature_name:str, role_name:str):
    key = {"feature_name": feature_name, "role": role_name}
    if not frappe.db.exists("MBW Feature Role Permission", key):
        frappe.get_doc(
            {
                "doctype": "MBW Feature Role Permission",
                "feature_name": feature_name,
                "role": role_name,
                "is_active": 1,
            }
        ).insert(ignore_permissions=True)
        print(f"✔ Linked: {feature_name} ↔ {role_name}")
    else:
        print(f"• Link exists: {feature_name} ↔ {role_name}")


def _load_feature_data() -> dict:
    """
    Ưu tiên import module Python (mbw_ats.config.featureMira).
    Fallback: tìm JSON trong app (mbw_ats/config/featureMira.json) để dev tiện soát.
    """
    # 1) import Python module
    try:
        from mbw_mira.config.featureMira import FEATURES_MIRA

        if isinstance(FEATURES_MIRA, dict) and FEATURES_MIRA.get("modules"):
            return FEATURES_MIRA
    except Exception as e:
        print(f"[feature_seeder] WARN: cannot import FEATURES_MIRA from module: {e}")

    # 2) fallback: JSON trong app
    json_path = frappe.get_app_path("mbw_mira", "mbw_mira", "config", "featureMira.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # 3) fallback cuối: resource package
    try:
        raw = pkgutil.get_data("mbw_mira", "mbw_mira/config/featureMira.json")
        if raw:
            return json.loads(raw.decode("utf-8"))
    except Exception:
        pass

    raise FileNotFoundError(
        "Không tìm thấy FEATURES_MIRA (module) hoặc featureMira.json trong app"
    )


def _iter_features(data: dict):
    """Yield (feature_dict, module_feature_mira)"""
    global APP_MODULE
    if data.get("feature_mira"):
        APP_MODULE = data["feature_mira"]

    modules = data.get("modules", []) or []
    for m in modules:
        module_feature_mira = (
            data.get("feature_mira") or APP_MODULE
        )  # dùng feature_mira app (“MBW MIRA”) làm module cho Feature
        for feature in m.get("features", []) or []:
            yield feature, module_feature_mira


# ---------------------------- public APIs ----------------------------
def seed():
    """Roles → Features (import từ module Python) → Links. Không cần tham số."""
    ensure_roles()

    need = [
        "MBW Feature Settings",
        "MBW Feature Setting Detail",
        "MBW Feature Role Permission",
    ]
    missing = [dt for dt in need if not _doctype_installed(dt)]
    if missing:
        print("⏭️ Skip seeding features: missing DocTypes ->", ", ".join(missing))
        print(
            "👉 bench migrate rồi chạy lại: bench --site <yoursite> execute mbw_mira.scripts.feature_seeder.seed"
        )
        return {"skipped_missing_doctypes": missing}

    data = _load_feature_data()
    print("=== Read features from Python module: mbw_mira.config.featureMira ===")
    print(f"APP_MODULE (from data['feature_mira']) = {data.get('feature_mira') or APP_MODULE}")

    print("=== Upsert Features ===")
    feature_names = []
    for feature, module_feature_mira in _iter_features(data):
        _upsert_feature_from_file(feature, module_feature_mira)
        feature_names.append(feature["feature_name"])

    print("=== Link Feature ↔ Role ===")
    linked_count = 0
    for fname, roles in FEATURE_ROLE_MAP.items():
        if fname not in feature_names:
            print(f"  ! Skip linking: Feature '{fname}' not found in features list")
            continue
            
        for role in roles:
            ensure_features_role_link(fname, role)
            linked_count += 1
            print(f"  ✓ Linked: {fname} → {role}")

    frappe.db.commit()
    print(f"✅ DONE seed. Linked {linked_count} feature-role pairs")
    return {
        "features": feature_names,
        "linked_count": linked_count,
        "roles": list(MIRA_ROLES.values())
    }


def print_payload():
    """In payload đọc từ module Python (KHÔNG ghi DB)."""
    data = _load_feature_data()
    module_feature_mira = data.get("feature_mira") or APP_MODULE

    features_payload = []
    for feature, _module in _iter_features(data):
        features_payload.append(
            {
                **feature,
                "module": module_feature_mira,
                "permissions": [
                    _perm_row_from_json(p) for p in feature.get("permissions", []) or []
                ],
            }
        )

    print("=== ROLES ===")
    print(json.dumps(MIRA_ROLES, ensure_ascii=False, indent=2))
    print("\n=== MBW Feature Settings (from module) ===")
    print(json.dumps(features_payload, ensure_ascii=False, indent=2))

    print("\n=== MBW Feature Role Permission (links; map mặc định) ===")
    links = []
    for feature_name, roles in FEATURE_ROLE_MAP.items():
        # Chỉ thêm các feature có trong features_payload
        if not any(f.get("feature_name") == feature_name for f in features_payload):
            continue
            
        for role in roles:
            links.append({
                "doctype": "MBW Feature Role Permission",
                "feature_name": feature_name,
                "role": role,
                "is_active": 1,
            })
    
    print(json.dumps(links, ensure_ascii=False, indent=2))
    
    return {
        "feature_count": len(features_payload), 
        "link_count": len(links),
        "roles": list(MIRA_ROLES.values())
    }
