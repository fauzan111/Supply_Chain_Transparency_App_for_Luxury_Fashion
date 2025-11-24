# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Set Up Environment

```bash
# Navigate to project directory
cd supply-chain-validator

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
```

**Note**: In this demo environment, the API key is already pre-configured.

### Step 4: Initialize Database

```bash
python src/populate_data.py
```

Expected output:
```
🔄 Populating supply chain database...
  ✓ Created supplier: Tuscany Leather Consortium
  ✓ Created supplier: Como Silk Mills
  ...
✅ Database populated successfully!
   - Total nodes: 28
   - Total relationships: 40
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎯 Try These Examples

### Example 1: Natural Language Query

1. Go to the **"Query Supply Chain"** tab
2. Enter: `"Who supplies the leather for the 2024 collection?"`
3. Click **"Query"**
4. View the AI-generated answer with supporting data

### Example 2: Validate Certifications

1. Go to the **"Validate Certifications"** tab
2. Select 2-3 certifications
3. Click **"Validate Selected Certifications"**
4. Review the AI assessment and confidence levels
5. See which certifications require human review

### Example 3: Trace a Product

1. Go to the **"Trace Products"** tab
2. Select a product (e.g., "Dionysus Leather Handbag")
3. Click **"Trace Supply Chain"**
4. View the complete supply chain from suppliers to final product

### Example 4: Browse Data

1. Go to the **"Browse Data"** tab
2. Select a data type (e.g., "Suppliers")
3. Expand any entry to see details and relationships

## 📊 Sample Queries to Try

### Supplier Queries
- `"Show me all suppliers in Florence, Italy"`
- `"Which suppliers have A+ sustainability rating?"`
- `"List suppliers that provide leather"`

### Material Queries
- `"What types of leather are available?"`
- `"Show me all organic materials"`
- `"Which materials have high sustainability?"`

### Factory Queries
- `"Which factories have ISO 9001 certification?"`
- `"Show me factories in Milan"`
- `"What is the capacity of Gucci Artisan Workshop?"`

### Certification Queries
- `"List all environmental certifications"`
- `"Which certifications expire in 2024?"`
- `"Show me all Made in Italy certifications"`

### Product Queries
- `"What products are in the Fall/Winter 2024 collection?"`
- `"Show me all handbags"`
- `"Which products are manufactured by Prada?"`

## 🔧 Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure you activated the virtual environment and installed all dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Streamlit won't start
**Solution**: Check if port 8501 is already in use:
```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Try again
streamlit run app.py
```

### Issue: OpenAI API error
**Solution**: Verify your API key is set correctly:
```bash
echo $OPENAI_API_KEY
```

### Issue: Database is empty
**Solution**: Re-run the population script:
```bash
python src/populate_data.py
```

## 📚 Next Steps

1. **Explore the Code**
   - `src/graph_database.py` - Graph database implementation
   - `src/graph_rag_engine.py` - Natural language query engine
   - `src/certification_validator.py` - Human-in-the-loop workflow
   - `app.py` - Streamlit frontend

2. **Customize the Data**
   - Edit `src/populate_data.py` to add your own suppliers, materials, etc.
   - Run the script again to reload the database

3. **Extend Functionality**
   - Add new node types
   - Create custom relationship types
   - Implement additional validation rules

4. **Deploy to Production**
   - Replace in-memory database with Neo4j
   - Add authentication
   - Set up monitoring and logging
   - Configure for scale

## 🎓 Learning Resources

### GraphRAG
- [LangChain Graph Documentation](https://python.langchain.com/docs/use_cases/graph/)
- [Neo4j Graph Academy](https://graphacademy.neo4j.com/)

### LangGraph
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Human-in-the-Loop Patterns](https://langchain-ai.github.io/langgraph/how-tos/human-in-the-loop/)

### Supply Chain Transparency
- [EU Digital Product Passport](https://ec.europa.eu/info/energy-climate-change-environment/standards-tools-and-labels/products-labelling-rules-and-requirements/sustainable-products/ecodesign-sustainable-products_en)
- [Leather Working Group](https://www.leatherworkinggroup.com/)

## 💡 Tips for Demos

1. **Start with Simple Queries**: Begin with straightforward questions to show basic functionality
2. **Show the Human-in-the-Loop**: Demonstrate how low-confidence certifications trigger human review
3. **Trace a Complete Product**: Use the tracing feature to show the full supply chain
4. **Highlight the Graph Structure**: Explain how relationships make queries more powerful
5. **Discuss Real-World Impact**: Connect to EU regulations and business needs

## 🎯 Interview Preparation

### Key Points to Emphasize
1. **GraphRAG vs. Traditional RAG**: Explain why graphs are better for supply chains
2. **Human-in-the-Loop**: Discuss importance for compliance and trust
3. **Scalability**: How this would scale to production (Neo4j cluster, caching, etc.)
4. **Business Value**: EU compliance, brand protection, sustainability reporting

### Demo Flow (5 minutes)
1. **Introduction** (30s): Explain the problem (EU Digital Product Passport)
2. **Natural Language Query** (1m): Show a complex query being answered
3. **Certification Validation** (1.5m): Demonstrate human-in-the-loop workflow
4. **Supply Chain Tracing** (1.5m): Trace a product from supplier to final product
5. **Q&A** (30s): Highlight technical skills and business impact

---

**Need Help?** Check the full README.md for detailed documentation.
