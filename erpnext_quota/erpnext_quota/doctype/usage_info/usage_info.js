// Copyright (c) 2020, Havenir Solutions Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Usage Info', {
	setup: function (frm){
		frm.disable_save();
	},
	onload_post_render: function (frm){
		frm.disable_save();
		frm.call('get_usage_info').then( r => {
			if(r.message){
				frm.doc.users_allowed = r.message[0]
				frm.doc.active_users = r.message[1]
				frm.doc.space_allowed = r.message[2]
				frm.doc.used_space = r.message[3]
				frm.doc.company_allowed = r.message[4]
				frm.doc.active_company = r.message[5]
				frm.refresh_field('users_allowed')
				frm.refresh_field('active_users')
				frm.refresh_field('space_allowed')
				frm.refresh_field('used_space')
				frm.refresh_field('company_allowed')
				frm.refresh_field('active_company')
			}
		})
	},
	refresh: function(frm) {
		frm.disable_save();
		
	}
});
