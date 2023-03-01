// Copyright (c) 2020, Havenir Solutions Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Usage Info', {
	setup: function (frm){
		frm.disable_save();
	},
	onload_post_render: function (frm){
		frm.disable_save();
		frm.call('get_usage_info').then( r => {
			frm.refresh();
		})
	},
	refresh: function(frm) {
		frm.disable_save();
	}
});


frappe.ui.form.on('Quota Document Limit Detail', {
	document_limit_add: function (frm, cdt, cdn){
		frm.set_query('document_type', 'document_limit', () => {
			return {
				filters: {
					issingle: 0,
					istable: 0,
					module: ["!=", "Core"],
					name: ["NOT IN", "Email Queue", "Notification Log"]
				}
			}
		})
	}
});