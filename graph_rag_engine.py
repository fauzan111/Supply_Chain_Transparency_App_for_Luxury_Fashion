"""
GraphRAG Query Engine using LangChain
Translates natural language questions into graph queries
"""

import os
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from graph_database import GraphDatabase
import json

class GraphRAGEngine:
    """Graph Retrieval Augmented Generation Engine"""
    
    def __init__(self, db: GraphDatabase, model: str = "gpt-4.1-mini"):
        """Initialize the GraphRAG engine with database and LLM"""
        self.db = db
        self.llm = ChatOpenAI(model=model, temperature=0)
        
        # Get schema information
        self.schema = self._get_schema_description()
        
        # Create prompts
        self.query_prompt = self._create_query_prompt()
        self.answer_prompt = self._create_answer_prompt()
    
    def _get_schema_description(self) -> str:
        """Generate a human-readable schema description"""
        schema = self.db.get_schema()
        
        # Get sample nodes for each label
        node_descriptions = []
        for label in schema['node_labels']:
            nodes = self.db.get_all_nodes(label)
            if nodes:
                sample = nodes[0]
                properties = ', '.join(sample.keys())
                node_descriptions.append(f"  - {label}: {properties}")
        
        # Get relationship descriptions
        rel_descriptions = []
        for rel_type in schema['relationship_types']:
            rels = self.db.get_all_relationships(rel_type)
            if rels:
                sample = rels[0]
                from_node = self.db.nodes.get(sample['from'])
                to_node = self.db.nodes.get(sample['to'])
                if from_node and to_node:
                    rel_descriptions.append(
                        f"  - ({from_node['label']})-[{rel_type}]->({to_node['label']})"
                    )
        
        schema_text = f"""
Supply Chain Graph Schema:

Node Types:
{chr(10).join(node_descriptions)}

Relationship Types:
{chr(10).join(rel_descriptions)}

Total Nodes: {schema['node_count']}
Total Relationships: {schema['relationship_count']}
"""
        return schema_text
    
    def _create_query_prompt(self) -> ChatPromptTemplate:
        """Create a prompt to convert natural language to structured queries"""
        
        template = """You are an expert at converting natural language questions into structured graph database queries for a luxury fashion supply chain system.

{schema}

Given the question below, analyze what information is needed and create a structured query plan.

Question: {question}

Provide your response as a JSON object with these fields:
- "intent": What the user wants to know (e.g., "find suppliers", "trace materials", "verify certifications")
- "entities": List of entity types involved (e.g., ["Supplier", "Material"])
- "filters": Any specific filters mentioned (e.g., {{"year": "2024", "location": "Florence"}})
- "relationships": List of relationship types to traverse (e.g., ["PROVIDES", "SUPPLIED_TO"])
- "return_fields": What information to return

Response (JSON only):"""

        return ChatPromptTemplate.from_template(template)
    
    def _create_answer_prompt(self) -> ChatPromptTemplate:
        """Create a prompt to generate natural language answers from query results"""
        
        template = """You are a supply chain expert for luxury fashion brands. 

Question: {question}

Query Results:
{results}

Based on the query results above, provide a clear, professional answer to the question.
If the results are empty or insufficient, explain what information is missing.
Include specific details like names, locations, certifications, and dates when available.

Answer:"""

        return ChatPromptTemplate.from_template(template)
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Process a natural language question and return structured results
        
        Args:
            question: Natural language question about the supply chain
            
        Returns:
            Dictionary with query results and generated answer
        """
        
        # Step 1: Convert question to structured query plan
        messages = self.query_prompt.format_messages(
            schema=self.schema,
            question=question
        )
        query_plan_response = self.llm.invoke(messages).content
        
        try:
            query_plan = json.loads(query_plan_response)
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return valid JSON
            query_plan = {
                "intent": "general_query",
                "entities": [],
                "filters": {},
                "relationships": [],
                "return_fields": []
            }
        
        # Step 2: Execute graph queries based on the plan
        raw_results = self._execute_query_plan(query_plan)
        
        # Step 3: Generate natural language answer
        answer_messages = self.answer_prompt.format_messages(
            question=question,
            results=json.dumps(raw_results, indent=2)
        )
        answer = self.llm.invoke(answer_messages).content
        
        return {
            "question": question,
            "query_plan": query_plan,
            "raw_results": raw_results,
            "answer": answer.strip(),
            "result_count": len(raw_results)
        }
    
    def _execute_query_plan(self, query_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the structured query plan against the graph database"""
        
        intent = query_plan.get("intent", "")
        entities = query_plan.get("entities", [])
        filters = query_plan.get("filters", {})
        relationships = query_plan.get("relationships", [])
        
        results = []
        
        # Handle different query intents
        if "supplier" in intent.lower() or "Supplier" in entities:
            results.extend(self._query_suppliers(filters, relationships))
        
        if "material" in intent.lower() or "Material" in entities:
            results.extend(self._query_materials(filters, relationships))
        
        if "factory" in intent.lower() or "Factory" in entities:
            results.extend(self._query_factories(filters, relationships))
        
        if "certification" in intent.lower() or "Certification" in entities:
            results.extend(self._query_certifications(filters, relationships))
        
        if "collection" in intent.lower() or "Collection" in entities:
            results.extend(self._query_collections(filters, relationships))
        
        if "product" in intent.lower() or "Product" in entities:
            results.extend(self._query_products(filters, relationships))
        
        # If no specific intent matched, return all relevant data
        if not results:
            results = self._general_search(query_plan)
        
        return results
    
    def _query_suppliers(self, filters: Dict, relationships: List[str]) -> List[Dict]:
        """Query suppliers with optional filters and relationships"""
        suppliers = self.db.get_all_nodes('Supplier')
        
        # Apply filters
        if filters:
            suppliers = [s for s in suppliers if self._matches_filters(s, filters)]
        
        # Enrich with relationships if specified
        if relationships:
            for supplier in suppliers:
                supplier['relationships'] = self._get_node_relationships(supplier['id'], relationships)
        
        return suppliers
    
    def _query_materials(self, filters: Dict, relationships: List[str]) -> List[Dict]:
        """Query materials with optional filters and relationships"""
        materials = self.db.get_all_nodes('Material')
        
        if filters:
            materials = [m for m in materials if self._matches_filters(m, filters)]
        
        if relationships:
            for material in materials:
                material['relationships'] = self._get_node_relationships(material['id'], relationships)
        
        return materials
    
    def _query_factories(self, filters: Dict, relationships: List[str]) -> List[Dict]:
        """Query factories with optional filters and relationships"""
        factories = self.db.get_all_nodes('Factory')
        
        if filters:
            factories = [f for f in factories if self._matches_filters(f, filters)]
        
        if relationships:
            for factory in factories:
                factory['relationships'] = self._get_node_relationships(factory['id'], relationships)
        
        return factories
    
    def _query_certifications(self, filters: Dict, relationships: List[str]) -> List[Dict]:
        """Query certifications with optional filters and relationships"""
        certifications = self.db.get_all_nodes('Certification')
        
        if filters:
            certifications = [c for c in certifications if self._matches_filters(c, filters)]
        
        if relationships:
            for cert in certifications:
                cert['relationships'] = self._get_node_relationships(cert['id'], relationships)
        
        return certifications
    
    def _query_collections(self, filters: Dict, relationships: List[str]) -> List[Dict]:
        """Query collections with optional filters and relationships"""
        collections = self.db.get_all_nodes('Collection')
        
        if filters:
            collections = [c for c in collections if self._matches_filters(c, filters)]
        
        if relationships:
            for collection in collections:
                collection['relationships'] = self._get_node_relationships(collection['id'], relationships)
        
        return collections
    
    def _query_products(self, filters: Dict, relationships: List[str]) -> List[Dict]:
        """Query products with optional filters and relationships"""
        products = self.db.get_all_nodes('Product')
        
        if filters:
            products = [p for p in products if self._matches_filters(p, filters)]
        
        if relationships:
            for product in products:
                product['relationships'] = self._get_node_relationships(product['id'], relationships)
        
        return products
    
    def _general_search(self, query_plan: Dict) -> List[Dict]:
        """Perform a general search across all node types"""
        results = []
        
        for label in self.db.get_schema()['node_labels']:
            nodes = self.db.get_all_nodes(label)
            for node in nodes[:3]:  # Limit to 3 per type
                node['_type'] = label
                results.append(node)
        
        return results
    
    def _matches_filters(self, node: Dict, filters: Dict) -> bool:
        """Check if a node matches the given filters"""
        for key, value in filters.items():
            node_value = node.get(key, '')
            if isinstance(node_value, str) and isinstance(value, str):
                if value.lower() not in node_value.lower():
                    return False
            elif node_value != value:
                return False
        return True
    
    def _get_node_relationships(self, node_id: str, rel_types: List[str]) -> Dict[str, List]:
        """Get all relationships for a node, filtered by type"""
        relationships = {'outgoing': [], 'incoming': []}
        
        for rel in self.db.relationships:
            if rel['from'] == node_id and (not rel_types or rel['type'] in rel_types):
                to_node = self.db.nodes.get(rel['to'])
                if to_node:
                    relationships['outgoing'].append({
                        'type': rel['type'],
                        'to': rel['to'],
                        'to_label': to_node['label'],
                        'to_name': to_node['properties'].get('name', rel['to'])
                    })
            
            if rel['to'] == node_id and (not rel_types or rel['type'] in rel_types):
                from_node = self.db.nodes.get(rel['from'])
                if from_node:
                    relationships['incoming'].append({
                        'type': rel['type'],
                        'from': rel['from'],
                        'from_label': from_node['label'],
                        'from_name': from_node['properties'].get('name', rel['from'])
                    })
        
        return relationships
    
    def trace_supply_chain(self, product_id: str) -> Dict[str, Any]:
        """
        Trace the complete supply chain for a product
        Returns the full path from suppliers to final product
        """
        
        # Get the product
        product_node = self.db.nodes.get(product_id)
        if not product_node:
            return {"error": f"Product {product_id} not found"}
        
        trace = {
            "product": product_node['properties'],
            "factory": None,
            "materials": [],
            "suppliers": [],
            "certifications": []
        }
        
        # Find factory that manufactures this product
        for rel in self.db.relationships:
            if rel['to'] == product_id and rel['type'] == 'MANUFACTURES':
                factory_node = self.db.nodes.get(rel['from'])
                if factory_node:
                    trace['factory'] = factory_node['properties']
                    
                    # Find factory certifications
                    for cert_rel in self.db.relationships:
                        if cert_rel['from'] == rel['from'] and cert_rel['type'] == 'HAS_CERTIFICATION':
                            cert_node = self.db.nodes.get(cert_rel['to'])
                            if cert_node:
                                trace['certifications'].append(cert_node['properties'])
        
        # Find materials supplied to the factory
        if trace['factory']:
            factory_id = None
            for rel in self.db.relationships:
                if rel['to'] == product_id and rel['type'] == 'MANUFACTURES':
                    factory_id = rel['from']
                    break
            
            if factory_id:
                for rel in self.db.relationships:
                    if rel['to'] == factory_id and rel['type'] == 'SUPPLIED_TO':
                        material_node = self.db.nodes.get(rel['from'])
                        if material_node:
                            material_info = material_node['properties'].copy()
                            
                            # Find suppliers for this material
                            material_suppliers = []
                            for sup_rel in self.db.relationships:
                                if sup_rel['to'] == rel['from'] and sup_rel['type'] == 'PROVIDES':
                                    supplier_node = self.db.nodes.get(sup_rel['from'])
                                    if supplier_node:
                                        material_suppliers.append(supplier_node['properties'])
                            
                            material_info['suppliers'] = material_suppliers
                            trace['materials'].append(material_info)
                            
                            # Add suppliers to main list
                            trace['suppliers'].extend(material_suppliers)
        
        # Remove duplicates from suppliers
        seen = set()
        unique_suppliers = []
        for supplier in trace['suppliers']:
            supplier_id = supplier.get('id')
            if supplier_id not in seen:
                seen.add(supplier_id)
                unique_suppliers.append(supplier)
        trace['suppliers'] = unique_suppliers
        
        return trace


if __name__ == "__main__":
    # Test the GraphRAG engine
    from populate_data import populate_supply_chain_data
    
    db = GraphDatabase()
    populate_supply_chain_data(db)
    
    engine = GraphRAGEngine(db)
    
    # Test queries
    test_questions = [
        "Who supplies the leather for the 2024 collection?",
        "Which factories have ISO 9001 certification?",
        "What materials are used in the Prada Fall/Winter 2024 collection?"
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"Q: {question}")
        print(f"{'='*60}")
        result = engine.query(question)
        print(f"\nA: {result['answer']}")
        print(f"\nFound {result['result_count']} results")
