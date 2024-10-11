{
    'name': 'Marbeya Products',
    'version': '1.0',
    
    'depends': ['base', 'product', 'purchase', 'stock', 'sale'],
    'description': """
This is customized version of products that fits MarbeyaUG factory
    """,
    'data': [
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        # 'views/report_purchase_order_inherit.xml',
        
    ],
    'demo': [
        
    ],
    
    'application': True,
    'installable': True,
   
    'license': 'LGPL-3',
}
