frappe.listview_settings['Mira Interaction'] = {
    onload(listview) {
        listview.page.add_action_item(__('My Button'), function() {
            let selected = listview.get_checked_items(); // lấy các item đã chọn
            if(selected.length === 0){
                frappe.msgprint(__('Please select at least one record'));
                return;
            }

            // xử lý logic
            frappe.msgprint(__('Selected records: ' + selected.map(d => d.name).join(', ')));
        });
        listview.page.add_inner_button('Tạo Interaction Test', () => {
            frappe.prompt([
                {
                    label: 'Talent',
                    fieldname: 'talent_id',
                    fieldtype: 'Link',
                    options: 'Mira Talent',
                    reqd: 1
                },
                {
                    label: 'Campaign',
                    fieldname: 'campaign_id',
                    fieldtype: 'Link',
                    options: 'Mira Campaign',
                    reqd: 1
                },
                {
                    label: 'Channel',
                    fieldname: 'channel',
                    fieldtype: 'Select',
                    options: [
                        'Email', 'Facebook', 'Zalo', 'SMS', 'Call',
                        'Landing Page', 'Website', 'Tiktok',
                        'LinkedIn', 'Chatbot', 'Form', 'Other'
                    ].join('\n'),
                    reqd: 1
                },
                {
                    label: 'Interaction Type',
                    fieldname: 'interaction_type',
                    fieldtype: 'Select',
                    options: [
                        'EMAIL_OPENED','ON_LINK_CLICK','PAGE_VISITED',
                        'FORM_SUBMITTED','FB_COMMENT','FB_REACTION',
                        'ZALO_CLICK','SMS_REPLIED','CALL_COMPLETED'
                    ].join('\n'),
                    reqd: 1
                }
            ], (values) => {
                frappe.call({
                    method: "mbw_mira.mbw_mira.doctype.mira_interaction.mira_interaction.create_fake_interaction",
                    args: values,
                    callback(r) {
                        if (!r.exc) {
                            frappe.msgprint("Đã tạo Interaction test");
                            listview.refresh();
                        }
                    }
                });
            }, "Tạo Interaction Test");
        });
    }
}
