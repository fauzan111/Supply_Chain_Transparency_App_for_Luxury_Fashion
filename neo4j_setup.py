"""
Neo4j Database Setup for Supply Chain Validator
Uses Neo4j Python driver to create an in-memory graph database
"""

from neo4j import GraphDatabase
import os

class Neo4jSetup:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        """Close the database connection"""
        self.driver.close()
    
    def create_schema(self):
        """Create the supply chain graph schema with constraints and indexes"""
        with self.driver.session() as session:
            # Create constraints for unique identifiers
            constraints = [
                "CREATE CONSTRAINT supplier_id IF NOT EXISTS FOR (s:Supplier) REQUIRE s.id IS UNIQUE",
                "CREATE CONSTRAINT material_id IF NOT EXISTS FOR (m:Material) REQUIRE m.id IS UNIQUE",
                "CREATE CONSTRAINT factory_id IF NOT EXISTS FOR (f:Factory) REQUIRE f.id IS UNIQUE",
                "CREATE CONSTRAINT certification_id IF NOT EXISTS FOR (c:Certification) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT collection_id IF NOT EXISTS FOR (col:Collection) REQUIRE col.id IS UNIQUE",
                "CREATE CONSTRAINT product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"✓ Created constraint: {constraint.split('FOR')[1].split('REQUIRE')[0].strip()}")
                except Exception as e:
                    print(f"Note: {str(e)}")
            
            # Create indexes for better query performance
            indexes = [
                "CREATE INDEX supplier_name IF NOT EXISTS FOR (s:Supplier) ON (s.name)",
                "CREATE INDEX material_type IF NOT EXISTS FOR (m:Material) ON (m.type)",
                "CREATE INDEX factory_location IF NOT EXISTS FOR (f:Factory) ON (f.location)",
                "CREATE INDEX certification_type IF NOT EXISTS FOR (c:Certification) ON (c.type)",
                "CREATE INDEX collection_year IF NOT EXISTS FOR (col:Collection) ON (col.year)"
            ]
            
            for index in indexes:
                try:
                    session.run(index)
                    print(f"✓ Created index: {index.split('FOR')[1].split('ON')[0].strip()}")
                except Exception as e:
                    print(f"Note: {str(e)}")
    
    def clear_database(self):
        """Clear all nodes and relationships from the database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✓ Database cleared")
    
    def verify_connection(self):
        """Verify database connection"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as num")
                record = result.single()
                if record and record["num"] == 1:
                    print("✓ Neo4j connection successful")
                    return True
        except Exception as e:
            print(f"✗ Neo4j connection failed: {str(e)}")
            return False
        return False

if __name__ == "__main__":
    # This will be used with a local Neo4j instance
    print("Neo4j Setup Module - Ready for initialization")
