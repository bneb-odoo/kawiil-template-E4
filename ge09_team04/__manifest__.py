{
    "name": "ge09_team04",
    "summary": "Captures motorcycle repair order data automatically",
    "description": """Modifies repair order so that whenever a motorcycle is
    assigned to a repair order, its motorcycle registry information (vin, owner,
    sale order, product id, mileage) gets copied automatically and adds a smart button 
    to the motorcycle registry view form to acces the repair history of the motorcycle.
    Task Id:3427355 Dev: Odoo Team 4""",
    "license": 'OPL-1',
    "version": "1.0.0",
    "data": [
    "views/repair_views.xml",
    "views/motorcycle_registry_views.xml",
    ],
    "depends": ["ge07_team04","repair"],
    "author": "Odoo,Inc.",
    "website": "www.odoo.com",
    "application": False,
}
