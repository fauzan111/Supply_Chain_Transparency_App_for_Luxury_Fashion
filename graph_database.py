"""
In-Memory Graph Database for Supply Chain Validator
Simulates Neo4j functionality with Cypher-like query interface
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

class GraphDatabase:
    """In-memory graph database with Cypher-like query support"""
    
    def __init__(self):
        self.nodes = {}  # {node_id: {label: str, properties: dict}}
        self.relationships = []  # [{from: id, to: id, type: str, properties: dict}]
        self.node_counter = 0
        
    def create_node(self, label: str, properties: Dict[str, Any]) -> str:
        """Create a node with label and properties"""
        node_id = properties.get('id', f"{label}_{self.node_counter}")
        self.node_counter += 1
        
        self.nodes[node_id] = {
            'label': label,
            'properties': properties
        }
        return node_id
    
    def create_relationship(self, from_id: str, to_id: str, rel_type: str, properties: Dict[str, Any] = None):
        """Create a relationship between two nodes"""
        if from_id not in self.nodes or to_id not in self.nodes:
            raise ValueError(f"Node not found: {from_id} or {to_id}")
        
        self.relationships.append({
            'from': from_id,
            'to': to_id,
            'type': rel_type,
            'properties': properties or {}
        })
    
    def execute_cypher(self, query: str) -> List[Dict[str, Any]]:
        """Execute a Cypher-like query and return results"""
        query = query.strip()
        
        # Handle MATCH queries
        if query.upper().startswith('MATCH'):
            return self._execute_match(query)
        
        # Handle CREATE queries
        elif query.upper().startswith('CREATE'):
            return self._execute_create(query)
        
        # Handle simple RETURN queries
        elif query.upper().startswith('RETURN'):
            return [{'result': 'OK'}]
        
        return []
    
    def _execute_match(self, query: str) -> List[Dict[str, Any]]:
        """Execute MATCH queries"""
        results = []
        
        # Parse simple patterns like: MATCH (s:Supplier) RETURN s
        # or MATCH (s:Supplier)-[:PROVIDES]->(m:Material) RETURN s, m
        
        # Extract node patterns
        node_pattern = r'\((\w+):(\w+)(?:\s*\{([^}]+)\})?\)'
        rel_pattern = r'-\[:(\w+)\]->'
        
        nodes_match = re.findall(node_pattern, query)
        rels_match = re.findall(rel_pattern, query)
        
        if not nodes_match:
            return results
        
        # Simple single node query
        if len(nodes_match) == 1 and not rels_match:
            var_name, label, props = nodes_match[0]
            
            # Filter nodes by label
            matching_nodes = [
                {var_name: {'id': nid, **node['properties']}}
                for nid, node in self.nodes.items()
                if node['label'] == label
            ]
            
            # Apply property filters if specified
            if props:
                prop_filters = self._parse_properties(props)
                matching_nodes = [
                    n for n in matching_nodes
                    if all(n[var_name].get(k) == v for k, v in prop_filters.items())
                ]
            
            results = matching_nodes
        
        # Relationship query
        elif len(nodes_match) >= 2 and rels_match:
            var1, label1, props1 = nodes_match[0]
            var2, label2, props2 = nodes_match[1]
            rel_type = rels_match[0]
            
            # Find matching relationships
            for rel in self.relationships:
                if rel['type'] != rel_type:
                    continue
                
                from_node = self.nodes.get(rel['from'])
                to_node = self.nodes.get(rel['to'])
                
                if not from_node or not to_node:
                    continue
                
                if from_node['label'] == label1 and to_node['label'] == label2:
                    results.append({
                        var1: {'id': rel['from'], **from_node['properties']},
                        var2: {'id': rel['to'], **to_node['properties']},
                        'relationship': rel['type']
                    })
        
        return results
    
    def _execute_create(self, query: str) -> List[Dict[str, Any]]:
        """Execute CREATE queries"""
        # This is a simplified implementation
        return [{'result': 'Created'}]
    
    def _parse_properties(self, props_str: str) -> Dict[str, Any]:
        """Parse property string like 'name: "Leather", type: "Material"'"""
        props = {}
        pairs = props_str.split(',')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                props[key] = value
        return props
    
    def get_all_nodes(self, label: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all nodes, optionally filtered by label"""
        if label:
            return [
                {'id': nid, **node['properties']}
                for nid, node in self.nodes.items()
                if node['label'] == label
            ]
        return [
            {'id': nid, 'label': node['label'], **node['properties']}
            for nid, node in self.nodes.items()
        ]
    
    def get_all_relationships(self, rel_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all relationships, optionally filtered by type"""
        if rel_type:
            return [r for r in self.relationships if r['type'] == rel_type]
        return self.relationships
    
    def clear(self):
        """Clear all data from the database"""
        self.nodes = {}
        self.relationships = []
        self.node_counter = 0
    
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema information"""
        labels = set(node['label'] for node in self.nodes.values())
        rel_types = set(rel['type'] for rel in self.relationships)
        
        return {
            'node_labels': list(labels),
            'relationship_types': list(rel_types),
            'node_count': len(self.nodes),
            'relationship_count': len(self.relationships)
        }
    
    def export_to_json(self, filepath: str):
        """Export database to JSON file"""
        data = {
            'nodes': self.nodes,
            'relationships': self.relationships
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_from_json(self, filepath: str):
        """Import database from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.nodes = data.get('nodes', {})
        self.relationships = data.get('relationships', [])


# Global database instance
db = GraphDatabase()

if __name__ == "__main__":
    # Test the database
    db = GraphDatabase()
    
    # Create test nodes
    supplier_id = db.create_node('Supplier', {
        'id': 'SUP001',
        'name': 'Tuscany Leather Co.',
        'location': 'Florence, Italy'
    })
    
    material_id = db.create_node('Material', {
        'id': 'MAT001',
        'name': 'Premium Calf Leather',
        'type': 'Leather'
    })
    
    # Create relationship
    db.create_relationship(supplier_id, material_id, 'PROVIDES')
    
    # Test query
    results = db.execute_cypher('MATCH (s:Supplier) RETURN s')
    print(f"Query results: {results}")
    
    schema = db.get_schema()
    print(f"Schema: {schema}")
