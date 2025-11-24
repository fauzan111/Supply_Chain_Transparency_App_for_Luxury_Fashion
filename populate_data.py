"""
Populate Supply Chain Graph Database with Realistic Italian Luxury Fashion Data
Includes suppliers, materials, factories, certifications, collections, and products
"""

from graph_database import GraphDatabase
from datetime import datetime

def populate_supply_chain_data(db: GraphDatabase):
    """Populate the database with comprehensive supply chain data"""
    
    print("🔄 Populating supply chain database...")
    
    # Clear existing data
    db.clear()
    
    # ==================== SUPPLIERS ====================
    suppliers = [
        {
            'id': 'SUP001',
            'name': 'Tuscany Leather Consortium',
            'location': 'Florence, Italy',
            'country': 'Italy',
            'type': 'Leather Supplier',
            'established': '1947',
            'employees': '250',
            'sustainability_rating': 'A+'
        },
        {
            'id': 'SUP002',
            'name': 'Como Silk Mills',
            'location': 'Como, Italy',
            'country': 'Italy',
            'type': 'Textile Supplier',
            'established': '1920',
            'employees': '180',
            'sustainability_rating': 'A'
        },
        {
            'id': 'SUP003',
            'name': 'Biella Wool Producers',
            'location': 'Biella, Italy',
            'country': 'Italy',
            'type': 'Wool Supplier',
            'established': '1885',
            'employees': '320',
            'sustainability_rating': 'A'
        },
        {
            'id': 'SUP004',
            'name': 'Veneto Textile Group',
            'location': 'Venice, Italy',
            'country': 'Italy',
            'type': 'Textile Supplier',
            'established': '1965',
            'employees': '150',
            'sustainability_rating': 'B+'
        },
        {
            'id': 'SUP005',
            'name': 'Marche Leather Artisans',
            'location': 'Marche, Italy',
            'country': 'Italy',
            'type': 'Leather Supplier',
            'established': '1978',
            'employees': '95',
            'sustainability_rating': 'A'
        }
    ]
    
    for supplier in suppliers:
        db.create_node('Supplier', supplier)
        print(f"  ✓ Created supplier: {supplier['name']}")
    
    # ==================== MATERIALS ====================
    materials = [
        {
            'id': 'MAT001',
            'name': 'Premium Calf Leather',
            'type': 'Leather',
            'origin': 'Italian Calves',
            'grade': 'A+',
            'tanning_method': 'Vegetable Tanning',
            'color_options': 'Natural, Black, Brown',
            'sustainability': 'High'
        },
        {
            'id': 'MAT002',
            'name': 'Mulberry Silk',
            'type': 'Silk',
            'origin': 'Italian Silkworms',
            'grade': 'A',
            'weight': '19 momme',
            'finish': 'Charmeuse',
            'sustainability': 'High'
        },
        {
            'id': 'MAT003',
            'name': 'Merino Wool',
            'type': 'Wool',
            'origin': 'Italian Merino Sheep',
            'grade': 'Superfine',
            'micron': '17-19',
            'treatment': 'Organic',
            'sustainability': 'Very High'
        },
        {
            'id': 'MAT004',
            'name': 'Cashmere',
            'type': 'Wool',
            'origin': 'Mongolian Goats',
            'grade': 'Grade A',
            'ply': '2-ply',
            'softness': 'Ultra Soft',
            'sustainability': 'Medium'
        },
        {
            'id': 'MAT005',
            'name': 'Exotic Python Leather',
            'type': 'Leather',
            'origin': 'Certified Python Farms',
            'grade': 'A',
            'treatment': 'Chrome Tanning',
            'pattern': 'Natural Scale',
            'sustainability': 'Regulated'
        },
        {
            'id': 'MAT006',
            'name': 'Organic Cotton',
            'type': 'Cotton',
            'origin': 'Italian Organic Farms',
            'grade': 'GOTS Certified',
            'thread_count': '300',
            'finish': 'Mercerized',
            'sustainability': 'Very High'
        }
    ]
    
    for material in materials:
        db.create_node('Material', material)
        print(f"  ✓ Created material: {material['name']}")
    
    # ==================== FACTORIES ====================
    factories = [
        {
            'id': 'FAC001',
            'name': 'Gucci Artisan Workshop',
            'location': 'Florence, Italy',
            'country': 'Italy',
            'type': 'Leather Goods Manufacturing',
            'capacity': '50000 units/year',
            'employees': '450',
            'certifications': 'ISO 9001, ISO 14001'
        },
        {
            'id': 'FAC002',
            'name': 'Prada Manufacturing Hub',
            'location': 'Milan, Italy',
            'country': 'Italy',
            'type': 'Handbag & Accessories',
            'capacity': '75000 units/year',
            'employees': '620',
            'certifications': 'ISO 9001, SA 8000'
        },
        {
            'id': 'FAC003',
            'name': 'Bottega Veneta Atelier',
            'location': 'Vicenza, Italy',
            'country': 'Italy',
            'type': 'Leather Weaving',
            'capacity': '30000 units/year',
            'employees': '280',
            'certifications': 'ISO 9001, LWG Gold'
        },
        {
            'id': 'FAC004',
            'name': 'Loro Piana Textile Mill',
            'location': 'Biella, Italy',
            'country': 'Italy',
            'type': 'Textile & Garment',
            'capacity': '100000 units/year',
            'employees': '380',
            'certifications': 'ISO 9001, OEKO-TEX'
        }
    ]
    
    for factory in factories:
        db.create_node('Factory', factory)
        print(f"  ✓ Created factory: {factory['name']}")
    
    # ==================== CERTIFICATIONS ====================
    certifications = [
        {
            'id': 'CERT001',
            'name': 'Made in Italy',
            'type': 'Origin Certification',
            'issuing_body': 'Italian Ministry of Economic Development',
            'valid_from': '2020-01-01',
            'valid_until': '2025-12-31',
            'verification_url': 'https://madeinitaly.gov.it',
            'confidence_level': 'High'
        },
        {
            'id': 'CERT002',
            'name': 'LWG Gold Rating',
            'type': 'Environmental Certification',
            'issuing_body': 'Leather Working Group',
            'valid_from': '2022-06-01',
            'valid_until': '2025-06-01',
            'verification_url': 'https://www.leatherworkinggroup.com',
            'confidence_level': 'High'
        },
        {
            'id': 'CERT003',
            'name': 'GOTS Organic',
            'type': 'Organic Certification',
            'issuing_body': 'Global Organic Textile Standard',
            'valid_from': '2021-03-15',
            'valid_until': '2026-03-15',
            'verification_url': 'https://global-standard.org',
            'confidence_level': 'High'
        },
        {
            'id': 'CERT004',
            'name': 'CITES Permit',
            'type': 'Wildlife Trade Certification',
            'issuing_body': 'Convention on International Trade in Endangered Species',
            'valid_from': '2023-01-01',
            'valid_until': '2024-12-31',
            'verification_url': 'https://cites.org',
            'confidence_level': 'Medium'
        },
        {
            'id': 'CERT005',
            'name': 'ISO 9001:2015',
            'type': 'Quality Management',
            'issuing_body': 'International Organization for Standardization',
            'valid_from': '2020-09-01',
            'valid_until': '2026-09-01',
            'verification_url': 'https://www.iso.org',
            'confidence_level': 'High'
        },
        {
            'id': 'CERT006',
            'name': 'SA 8000',
            'type': 'Social Accountability',
            'issuing_body': 'Social Accountability International',
            'valid_from': '2021-11-01',
            'valid_until': '2025-11-01',
            'verification_url': 'https://sa-intl.org',
            'confidence_level': 'High'
        }
    ]
    
    for cert in certifications:
        db.create_node('Certification', cert)
        print(f"  ✓ Created certification: {cert['name']}")
    
    # ==================== COLLECTIONS ====================
    collections = [
        {
            'id': 'COL001',
            'name': 'Spring/Summer 2024',
            'year': '2024',
            'season': 'SS',
            'brand': 'Gucci',
            'theme': 'Renaissance Revival',
            'launch_date': '2024-02-15'
        },
        {
            'id': 'COL002',
            'name': 'Fall/Winter 2024',
            'year': '2024',
            'season': 'FW',
            'brand': 'Prada',
            'theme': 'Urban Elegance',
            'launch_date': '2024-09-20'
        },
        {
            'id': 'COL003',
            'name': 'Cruise 2024',
            'year': '2024',
            'season': 'Cruise',
            'brand': 'Bottega Veneta',
            'theme': 'Mediterranean Dreams',
            'launch_date': '2024-05-10'
        }
    ]
    
    for collection in collections:
        db.create_node('Collection', collection)
        print(f"  ✓ Created collection: {collection['name']}")
    
    # ==================== PRODUCTS ====================
    products = [
        {
            'id': 'PROD001',
            'name': 'Dionysus Leather Handbag',
            'sku': 'GG-DIO-2024-001',
            'category': 'Handbag',
            'price_eur': '2500',
            'collection': 'Spring/Summer 2024',
            'made_in': 'Italy'
        },
        {
            'id': 'PROD002',
            'name': 'Galleria Saffiano Tote',
            'sku': 'PR-GAL-2024-045',
            'category': 'Tote Bag',
            'price_eur': '3200',
            'collection': 'Fall/Winter 2024',
            'made_in': 'Italy'
        },
        {
            'id': 'PROD003',
            'name': 'Intrecciato Woven Clutch',
            'sku': 'BV-INT-2024-023',
            'category': 'Clutch',
            'price_eur': '1800',
            'collection': 'Cruise 2024',
            'made_in': 'Italy'
        },
        {
            'id': 'PROD004',
            'name': 'Cashmere Overcoat',
            'sku': 'LP-CAS-2024-012',
            'category': 'Outerwear',
            'price_eur': '4500',
            'collection': 'Fall/Winter 2024',
            'made_in': 'Italy'
        }
    ]
    
    for product in products:
        db.create_node('Product', product)
        print(f"  ✓ Created product: {product['name']}")
    
    # ==================== RELATIONSHIPS ====================
    print("\n🔗 Creating relationships...")
    
    # Supplier -> Material relationships
    relationships = [
        ('SUP001', 'MAT001', 'PROVIDES', {'since': '2015', 'volume': 'High'}),
        ('SUP001', 'MAT005', 'PROVIDES', {'since': '2018', 'volume': 'Low'}),
        ('SUP002', 'MAT002', 'PROVIDES', {'since': '2010', 'volume': 'High'}),
        ('SUP003', 'MAT003', 'PROVIDES', {'since': '2005', 'volume': 'Very High'}),
        ('SUP003', 'MAT004', 'PROVIDES', {'since': '2012', 'volume': 'Medium'}),
        ('SUP004', 'MAT006', 'PROVIDES', {'since': '2019', 'volume': 'Medium'}),
        ('SUP005', 'MAT001', 'PROVIDES', {'since': '2020', 'volume': 'Medium'}),
        
        # Material -> Factory relationships
        ('MAT001', 'FAC001', 'SUPPLIED_TO', {'quantity': '5000 sq meters', 'frequency': 'Monthly'}),
        ('MAT001', 'FAC002', 'SUPPLIED_TO', {'quantity': '7500 sq meters', 'frequency': 'Monthly'}),
        ('MAT001', 'FAC003', 'SUPPLIED_TO', {'quantity': '3000 sq meters', 'frequency': 'Bi-weekly'}),
        ('MAT002', 'FAC004', 'SUPPLIED_TO', {'quantity': '2000 meters', 'frequency': 'Weekly'}),
        ('MAT003', 'FAC004', 'SUPPLIED_TO', {'quantity': '10000 kg', 'frequency': 'Monthly'}),
        ('MAT004', 'FAC004', 'SUPPLIED_TO', {'quantity': '1500 kg', 'frequency': 'Quarterly'}),
        ('MAT005', 'FAC002', 'SUPPLIED_TO', {'quantity': '500 skins', 'frequency': 'Quarterly'}),
        ('MAT006', 'FAC004', 'SUPPLIED_TO', {'quantity': '5000 meters', 'frequency': 'Monthly'}),
        
        # Factory -> Product relationships
        ('FAC001', 'PROD001', 'MANUFACTURES', {'lead_time': '45 days', 'batch_size': '500'}),
        ('FAC002', 'PROD002', 'MANUFACTURES', {'lead_time': '30 days', 'batch_size': '1000'}),
        ('FAC003', 'PROD003', 'MANUFACTURES', {'lead_time': '60 days', 'batch_size': '300'}),
        ('FAC004', 'PROD004', 'MANUFACTURES', {'lead_time': '90 days', 'batch_size': '200'}),
        
        # Product -> Collection relationships
        ('PROD001', 'COL001', 'PART_OF', {'featured': 'Yes'}),
        ('PROD002', 'COL002', 'PART_OF', {'featured': 'Yes'}),
        ('PROD003', 'COL003', 'PART_OF', {'featured': 'Yes'}),
        ('PROD004', 'COL002', 'PART_OF', {'featured': 'No'}),
        
        # Certification relationships
        ('SUP001', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-06-15'}),
        ('SUP001', 'CERT002', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2022-11-20'}),
        ('SUP002', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-03-10'}),
        ('SUP003', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-01-05'}),
        ('SUP003', 'CERT003', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2021-08-22'}),
        ('SUP004', 'CERT003', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2022-04-18'}),
        ('SUP005', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-09-30'}),
        
        ('FAC001', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-07-12'}),
        ('FAC001', 'CERT005', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2020-09-15'}),
        ('FAC002', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-05-20'}),
        ('FAC002', 'CERT005', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2021-02-10'}),
        ('FAC002', 'CERT006', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2021-11-05'}),
        ('FAC003', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-08-18'}),
        ('FAC003', 'CERT002', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2022-06-25'}),
        ('FAC004', 'CERT001', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2023-04-14'}),
        ('FAC004', 'CERT005', 'HAS_CERTIFICATION', {'verified': 'Yes', 'verified_date': '2020-10-08'}),
        
        ('MAT005', 'CERT004', 'REQUIRES_CERTIFICATION', {'status': 'Active', 'renewal_date': '2024-12-31'}),
    ]
    
    for from_id, to_id, rel_type, props in relationships:
        db.create_relationship(from_id, to_id, rel_type, props)
        print(f"  ✓ Created: {from_id} -[{rel_type}]-> {to_id}")
    
    # Print summary
    schema = db.get_schema()
    print(f"\n✅ Database populated successfully!")
    print(f"   - Node labels: {', '.join(schema['node_labels'])}")
    print(f"   - Relationship types: {', '.join(schema['relationship_types'])}")
    print(f"   - Total nodes: {schema['node_count']}")
    print(f"   - Total relationships: {schema['relationship_count']}")
    
    return db

if __name__ == "__main__":
    db = GraphDatabase()
    populate_supply_chain_data(db)
    
    # Export to JSON for backup
    db.export_to_json('/home/ubuntu/supply-chain-validator/data/supply_chain_graph.json')
    print("\n💾 Database exported to: data/supply_chain_graph.json")
