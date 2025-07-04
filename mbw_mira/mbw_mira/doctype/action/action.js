// Copyright (c) 2025, MBWCloud Co. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Action', {
    refresh(frm) {
        if (frm.doc.status === "PENDING_MANUAL") {
            frm.add_custom_button("Đánh dấu đã xử lý", () => {
                frappe.prompt([
                    {
                        label: "Ghi chú",
                        fieldname: "note",
                        fieldtype: "Small Text"
                    }
                ], (values) => {
                    frappe.call({
                        method: "mbw_mira.api.complete_manual_action",
                        args: {
                            action_id: frm.doc.name,
                            note: values.note
                        },
                        callback: () => {
                            frappe.msgprint("Đã đánh dấu hoàn tất.");
                            frm.reload_doc();
                        }
                    });
                });
            });
        }
    }
});

