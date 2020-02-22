// Copyright (c) 2020, Havenir Solutions Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Usage Info', {
	refresh: function(frm) {
		frm.call('get_usage_info').then( r => {
			if(r.message){
				frm.doc.users_allowed = r.message[0]
				frm.doc.active_users = r.message[1]
				frm.doc.space_allowed = r.message[2]
				frm.doc.used_space = r.message[3]
				frm.refresh_field('users_allowed')
				frm.refresh_field('active_users')
				frm.refresh_field('space_allowed')
				frm.refresh_field('used_space')
			}
		})
	}
});
