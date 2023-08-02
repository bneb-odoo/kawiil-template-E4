{
    "name": "Portal Account creation",
    "summary": "Portal extension to allow customer account creation",
    "description": """ 
    Modifies motorcycle Registry to trigger the creation of a portal user account whenever a motorcycle 
    registry is created (automated on delivery validation, ge07_team04) and owner has no 
    existing portal account. Once created sends an email invitation to the portal.
    Task id: 3427361 Dev: Odoo Team4""",
    "version": "1.0.0",
    "category": "Kawiil/Web",
    "license": 'OPL-1',
    "depends": ["ge07_team04", "mail"],
    "data":[
    "views/email_template.xml"
    ],
    "author": "Odoo, Inc",
    "website": "www.odoo.com",
}
