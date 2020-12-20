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
