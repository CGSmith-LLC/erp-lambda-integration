require('dotenv').config();
var Odoo = require('odoo-xmlrpc');
var odoo = new Odoo({
    url: process.env.ODOO_URL,
    db: process.env.ODOO_DB,
    username: process.env.ODOO_USERNAME,
    password: process.env.ODOO_PASSWORD
});


// Connect to Odoo
odoo.connect(function (err) {
    if (err) { return console.log(err); }

    var innerParams = [];
    innerParams.push({
        'name': 'Name of crm.lead.name',
        'active': 1,
        'contact_name': 'chris+nodejs@email.com',
        'type': 'lead',
        'website': 'https://www.email.com/En-US/eus/eusdatadetails/1401403', // @todo this is the response ID!
        'user_email': 'chris+user_email@email.com',
        'street': '123 Main Street',
        'street2': '',
        'zip': '53149',
        'city': 'Mukwonago',
        'phone': '555-555-5555',
        'won_status': 'pending',
        'state_id': 10, // @todo need to have a lookup for state IDs
        'display_name': 'Lead from Website'
    })


    var params = [];
    params.push(innerParams);

    // Save new crm.lead
    odoo.execute_kw('crm.lead', 'create', params, function (err, value) {
        if (err) { return console.log(err); }

        console.log('Result:', value);
    });
});
