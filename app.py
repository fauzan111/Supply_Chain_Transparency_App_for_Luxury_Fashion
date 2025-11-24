"""
Supply Chain "Made in Italy" Validator
Streamlit Frontend Application

A GraphRAG application for luxury fashion supply chain transparency
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from graph_database import GraphDatabase
from populate_data import populate_supply_chain_data
from graph_rag_engine import GraphRAGEngine
from certification_validator import CertificationValidator

# Page configuration
st.set_page_config(
    page_title="Supply Chain Validator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff; /* Changed from #1f1f1f to white for better contrast */
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
    }
    .certification-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .badge-high {
        background-color: #d4edda;
        color: #155724;
    }
    .badge-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    .badge-low {
        background-color: #f8d7da;
        color: #721c24;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db' not in st.session_state:
    with st.spinner("🔄 Initializing supply chain database..."):
        st.session_state.db = GraphDatabase()
        populate_supply_chain_data(st.session_state.db)
        st.session_state.engine = GraphRAGEngine(st.session_state.db)
        st.session_state.validator = CertificationValidator(st.session_state.db)
        st.session_state.query_history = []

# Header
st.markdown('<div class="main-header">🏭 Supply Chain "Made in Italy" Validator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">GraphRAG for Luxury Fashion Supply Chain Transparency</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/0066cc/ffffff?text=Supply+Chain+Validator", use_container_width=True)
    
    st.markdown("### 📊 Database Statistics")
    schema = st.session_state.db.get_schema()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nodes", schema['node_count'])
        st.metric("Suppliers", len(st.session_state.db.get_all_nodes('Supplier')))
        st.metric("Materials", len(st.session_state.db.get_all_nodes('Material')))
    with col2:
        st.metric("Relationships", schema['relationship_count'])
        st.metric("Factories", len(st.session_state.db.get_all_nodes('Factory')))
        st.metric("Certifications", len(st.session_state.db.get_all_nodes('Certification')))
    
    st.markdown("---")
    st.markdown("### 🎯 Features")
    st.markdown("""
    - 🔍 **Natural Language Queries**
    - 🤖 **AI-Powered Analysis**
    - ✅ **Certification Validation**
    - 👤 **Human-in-the-Loop**
    - 📈 **Supply Chain Tracing**
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This application demonstrates **GraphRAG** (Graph Retrieval Augmented Generation) 
    for supply chain transparency in luxury fashion, addressing EU Digital Product Passport requirements.
    """)

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Query Supply Chain", 
    "✅ Validate Certifications", 
    "📈 Trace Products",
    "📊 Browse Data",
    "📚 Query History"
])

# Tab 1: Query Supply Chain
with tab1:
    st.markdown("### 🔍 Natural Language Supply Chain Queries")
    st.markdown("Ask questions about suppliers, materials, factories, certifications, and products.")
    
    # Example queries
    with st.expander("💡 Example Queries"):
        st.markdown("""
        - Who supplies the leather for the 2024 collection?
        - Which factories have ISO 9001 certification?
        - What materials are used in the Prada Fall/Winter 2024 collection?
        - Show me all suppliers in Florence, Italy
        - Which certifications does Tuscany Leather Consortium have?
        - List all products manufactured by Gucci Artisan Workshop
        - What is the sustainability rating of Biella Wool Producers?
        """)
    
    # Query input
    query = st.text_input(
        "Enter your question:",
        placeholder="e.g., Who supplies the leather for the 2024 collection?",
        key="query_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        query_button = st.button("🚀 Query", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()
    
    if query_button and query:
        with st.spinner("🤔 Analyzing your question..."):
            result = st.session_state.engine.query(query)
            
            # Save to history
            st.session_state.query_history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'query': query,
                'result': result
            })
            
            # Display answer
            st.markdown("### 💬 Answer")
            st.success(result['answer'])
            
            # Display query plan
            with st.expander("🔧 Query Analysis"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Intent:**")
                    st.info(result['query_plan'].get('intent', 'N/A'))
                    
                    st.markdown("**Entities:**")
                    entities = result['query_plan'].get('entities', [])
                    if entities:
                        for entity in entities:
                            st.markdown(f"- {entity}")
                    else:
                        st.markdown("None specified")
                
                with col2:
                    st.markdown("**Filters:**")
                    filters = result['query_plan'].get('filters', {})
                    if filters:
                        st.json(filters)
                    else:
                        st.markdown("None applied")
                    
                    st.markdown("**Relationships:**")
                    rels = result['query_plan'].get('relationships', [])
                    if rels:
                        for rel in rels:
                            st.markdown(f"- {rel}")
                    else:
                        st.markdown("None specified")
            
            # Display raw results
            with st.expander(f"📋 Raw Data ({result['result_count']} results)"):
                if result['raw_results']:
                    st.json(result['raw_results'])
                else:
                    st.warning("No data found")

# Tab 2: Validate Certifications
with tab2:
    st.markdown("### ✅ Certification Validation with Human-in-the-Loop")
    st.markdown("AI-powered certification validation with human review for uncertain cases.")
    
    # Get all certifications
    all_certs = st.session_state.db.get_all_nodes('Certification')
    
    st.markdown("#### Select Certifications to Validate")
    
    # Create a grid of certifications
    cols = st.columns(2)
    selected_certs = []
    
    for idx, cert in enumerate(all_certs):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"**{cert['name']}**")
                st.caption(f"Type: {cert['type']}")
                st.caption(f"Valid until: {cert['valid_until']}")
                if st.checkbox(f"Select {cert['id']}", key=f"cert_{cert['id']}"):
                    selected_certs.append(cert['id'])
                st.markdown("---")
    
    if st.button("🔍 Validate Selected Certifications", type="primary", disabled=len(selected_certs) == 0):
        with st.spinner("🤖 Validating certifications..."):
            results = st.session_state.validator.validate_all_certifications_for_query(
                query="Manual certification validation",
                certification_ids=selected_certs
            )
            
            summary = st.session_state.validator.get_certification_summary(results)
            
            # Display summary
            st.markdown("### 📊 Validation Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total", summary['total_certifications'])
            with col2:
                st.metric("Auto-Approved", summary['auto_approved'], delta="High Confidence")
            with col3:
                st.metric("Human Approved", summary['human_approved'], delta="Medium Confidence")
            with col4:
                st.metric("Rejected", summary['rejected'], delta="Low Confidence", delta_color="inverse")
            
            # Display individual results
            st.markdown("### 📋 Validation Results")
            for result in results:
                status = result['validation_status']
                confidence = result['confidence_level']
                
                # Determine badge color
                if confidence == "High":
                    badge_class = "badge-high"
                    icon = "✅"
                elif confidence == "Medium":
                    badge_class = "badge-medium"
                    icon = "⚠️"
                else:
                    badge_class = "badge-low"
                    icon = "❌"
                
                with st.expander(f"{icon} {result['certification_name']} - {status.upper()}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Type:** {result['certification_type']}")
                        st.markdown(f"**Issuing Body:** {result['issuing_body']}")
                        st.markdown(f"**Valid Until:** {result['valid_until']}")
                        st.markdown(f"**Verification URL:** [{result['verification_url']}]({result['verification_url']})")
                    with col2:
                        st.markdown(f'<div class="certification-badge {badge_class}">{confidence} Confidence</div>', unsafe_allow_html=True)
                        st.markdown(f"**Status:** {status}")
                    
                    st.markdown("**AI Assessment:**")
                    st.info(result['ai_assessment'])
                    
                    if result['human_feedback'] != "Not required - High confidence":
                        st.markdown("**Human Feedback:**")
                        st.warning(result['human_feedback'])

# Tab 3: Trace Products
with tab3:
    st.markdown("### 📈 Complete Supply Chain Tracing")
    st.markdown("Trace the full supply chain from suppliers to final product.")
    
    # Get all products
    all_products = st.session_state.db.get_all_nodes('Product')
    
    product_names = {p['id']: p['name'] for p in all_products}
    selected_product = st.selectbox(
        "Select a product to trace:",
        options=list(product_names.keys()),
        format_func=lambda x: product_names[x]
    )
    
    if st.button("🔍 Trace Supply Chain", type="primary"):
        with st.spinner("🔄 Tracing supply chain..."):
            trace = st.session_state.engine.trace_supply_chain(selected_product)
            
            if 'error' in trace:
                st.error(trace['error'])
            else:
                # Product info
                st.markdown("### 👜 Product Information")
                product = trace['product']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Product", product['name'])
                with col2:
                    st.metric("SKU", product['sku'])
                with col3:
                    st.metric("Price", f"€{product['price_eur']}")
                
                st.markdown(f"**Collection:** {product['collection']}")
                st.markdown(f"**Category:** {product['category']}")
                st.markdown(f"**Made in:** {product['made_in']}")
                
                # Factory info
                if trace['factory']:
                    st.markdown("### 🏭 Manufacturing")
                    factory = trace['factory']
                    with st.container():
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"**Factory:** {factory['name']}")
                            st.markdown(f"**Location:** {factory['location']}")
                            st.markdown(f"**Type:** {factory['type']}")
                        with col2:
                            st.markdown(f"**Capacity:** {factory['capacity']}")
                            st.markdown(f"**Employees:** {factory['employees']}")
                
                # Materials info
                if trace['materials']:
                    st.markdown("### 🧵 Materials")
                    for material in trace['materials']:
                        with st.expander(f"📦 {material['name']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Type:** {material['type']}")
                                st.markdown(f"**Origin:** {material.get('origin', 'N/A')}")
                                st.markdown(f"**Grade:** {material.get('grade', 'N/A')}")
                            with col2:
                                st.markdown(f"**Sustainability:** {material.get('sustainability', 'N/A')}")
                            
                            if material.get('suppliers'):
                                st.markdown("**Suppliers:**")
                                for supplier in material['suppliers']:
                                    st.markdown(f"- {supplier['name']} ({supplier['location']})")
                
                # Suppliers info
                if trace['suppliers']:
                    st.markdown("### 🏢 Suppliers")
                    cols = st.columns(min(len(trace['suppliers']), 3))
                    for idx, supplier in enumerate(trace['suppliers']):
                        with cols[idx % 3]:
                            st.markdown(f"**{supplier['name']}**")
                            st.caption(f"📍 {supplier['location']}")
                            st.caption(f"⭐ Rating: {supplier.get('sustainability_rating', 'N/A')}")
                
                # Certifications info
                if trace['certifications']:
                    st.markdown("### ✅ Certifications")
                    cert_cols = st.columns(min(len(trace['certifications']), 4))
                    for idx, cert in enumerate(trace['certifications']):
                        with cert_cols[idx % 4]:
                            st.markdown(f"**{cert['name']}**")
                            st.caption(f"Valid: {cert['valid_until']}")

# Tab 4: Browse Data
with tab4:
    st.markdown("### 📊 Browse Supply Chain Data")
    
    data_type = st.selectbox(
        "Select data type:",
        ["Suppliers", "Materials", "Factories", "Certifications", "Collections", "Products"]
    )
    
    # Map selection to node label
    label_map = {
        "Suppliers": "Supplier",
        "Materials": "Material",
        "Factories": "Factory",
        "Certifications": "Certification",
        "Collections": "Collection",
        "Products": "Product"
    }
    
    label = label_map[data_type]
    nodes = st.session_state.db.get_all_nodes(label)
    
    st.markdown(f"#### {data_type} ({len(nodes)} total)")
    
    # Display as cards
    for node in nodes:
        with st.expander(f"📌 {node.get('name', node.get('id'))}"):
            # Display all properties
            for key, value in node.items():
                if key != 'id':
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            
            # Show relationships
            rels = st.session_state.engine._get_node_relationships(node['id'], [])
            if rels['outgoing'] or rels['incoming']:
                st.markdown("**Relationships:**")
                if rels['outgoing']:
                    st.markdown("*Outgoing:*")
                    for rel in rels['outgoing']:
                        st.markdown(f"- {rel['type']} → {rel['to_name']} ({rel['to_label']})")
                if rels['incoming']:
                    st.markdown("*Incoming:*")
                    for rel in rels['incoming']:
                        st.markdown(f"- {rel['from_name']} ({rel['from_label']}) → {rel['type']}")

# Tab 5: Query History
with tab5:
    st.markdown("### 📚 Query History")
    
    if st.session_state.query_history:
        for idx, item in enumerate(reversed(st.session_state.query_history)):
            with st.expander(f"🕐 {item['timestamp']} - {item['query'][:50]}..."):
                st.markdown(f"**Question:** {item['query']}")
                st.markdown(f"**Answer:** {item['result']['answer']}")
                st.markdown(f"**Results Found:** {item['result']['result_count']}")
    else:
        st.info("No queries yet. Try asking a question in the 'Query Supply Chain' tab!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Supply Chain "Made in Italy" Validator</strong></p>
    <p>Built with GraphRAG, LangChain, LangGraph, and Streamlit</p>
    <p>Demonstrating EU Digital Product Passport compliance for luxury fashion</p>
</div>
""", unsafe_allow_html=True)
