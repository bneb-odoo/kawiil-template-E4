{
    "name": "ge01_team4",
    "summary": "Module #1",
    "description": """
    Create a filter for the products page that only shows products that are a motorcycle type
   """,
    'license': 'OPL-1',
    "summary": "Default motorcycle filter for products",
    "description": """Filters the products page to show products that are a motorcycle type 
    Task Id:342602 Dev: Odoo Team 4""",
    'license': 'OPL-1',
    'version': '0.1',
    'data': [
    'views/ge01_product_template_views.xml',
    ],
    "depends": ["motorcycle_registry","sale"],
    "author": "Odoo,Inc",
    "website": "www.odoo.com",
    "application": False,
}
