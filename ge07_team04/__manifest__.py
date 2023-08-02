{
    "name": "Motorcycle Registry : Registry from Sale Order",
    "summary": "Links new registry with delivered motorcycles",
    "description": """
    Motorcycle Registry : Registry from Sale Order \n
    Modifies motorcycle Sales Orders so that a new motorcycle.registry entry
    is made automatically when delivery to final customer is confirmed (picking). \n
    Task Id:3426906 \n
    Dev: Odoo Team 4
    """,
    "license": "OPL-1",
    "version": "1.0.0",
    "depends": ["ge06_team04","sale"],
    "data": [
        "views/motorcycle_registry_inherit.xml",
        "views/stock_lot_views.xml",
    ],
    "author": "Odoo,Inc.",
    "website": "www.odoo.com",
}
