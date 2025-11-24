# Technical Architecture

## System Overview

The Supply Chain Validator is built on a **GraphRAG** (Graph Retrieval Augmented Generation) architecture, combining graph databases, large language models, and human-in-the-loop workflows to provide intelligent supply chain transparency.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                      (Streamlit Frontend)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │  Query   │ │ Validate │ │  Trace   │ │  Browse  │          │
│  │   Tab    │ │   Tab    │ │   Tab    │ │   Tab    │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└────────┬──────────────────────┬─────────────────────────────────┘
         │                      │
         │                      │
    ┌────▼──────────────┐  ┌───▼────────────────────┐
    │  GraphRAG Engine  │  │ Certification Validator │
    │   (LangChain)     │  │     (LangGraph)         │
    │                   │  │                         │
    │ ┌───────────────┐ │  │ ┌─────────────────────┐│
    │ │ Query Prompt  │ │  │ │  State Machine      ││
    │ │  Generator    │ │  │ │  - Assess           ││
    │ └───────┬───────┘ │  │ │  - Auto Approve     ││
    │         │         │  │ │  - Human Review     ││
    │ ┌───────▼───────┐ │  │ │  - Process Feedback ││
    │ │  LLM (GPT-4)  │ │  │ │  - Finalize         ││
    │ └───────┬───────┘ │  │ └─────────────────────┘│
    │         │         │  │                         │
    │ ┌───────▼───────┐ │  │ ┌─────────────────────┐│
    │ │ Query Executor│ │  │ │  Confidence Scorer  ││
    │ └───────┬───────┘ │  │ └─────────────────────┘│
    │         │         │  │                         │
    │ ┌───────▼───────┐ │  │ ┌─────────────────────┐│
    │ │Answer Generator│ │  │ │  Memory Checkpoints ││
    │ └───────────────┘ │  │ └─────────────────────┘│
    └────────┬──────────┘  └───┬────────────────────┘
             │                 │
             └────────┬────────┘
                      │
              ┌───────▼────────┐
              │ Graph Database │
              │  (In-Memory)   │
              │                │
              │ ┌────────────┐ │
              │ │   Nodes    │ │
              │ │ - Supplier │ │
              │ │ - Material │ │
              │ │ - Factory  │ │
              │ │ - Cert     │ │
              │ │ - Product  │ │
              │ └────────────┘ │
              │                │
              │ ┌────────────┐ │
              │ │Relationships│ │
              │ │ - PROVIDES │ │
              │ │ - SUPPLIED │ │
              │ │ - HAS_CERT │ │
              │ └────────────┘ │
              └────────────────┘
```

## Component Details

### 1. Graph Database Layer

**File**: `src/graph_database.py`

**Responsibilities**:
- Store nodes and relationships in memory
- Execute Cypher-like queries
- Manage graph schema
- Provide CRUD operations

**Key Classes**:
```python
class GraphDatabase:
    - create_node(label, properties)
    - create_relationship(from_id, to_id, type, properties)
    - execute_cypher(query)
    - get_all_nodes(label)
    - get_all_relationships(type)
```

**Data Model**:
```
Nodes: {node_id: {label: str, properties: dict}}
Relationships: [{from: id, to: id, type: str, properties: dict}]
```

**Performance Characteristics**:
- **Node Lookup**: O(1) - Hash table
- **Relationship Traversal**: O(R) - Linear scan (R = total relationships)
- **Pattern Matching**: O(N*R) - Worst case
- **Memory**: ~1KB per node, ~500B per relationship

**Scalability Considerations**:
- Current: In-memory, single-threaded
- Production: Neo4j cluster with:
  - Read replicas for query distribution
  - Write master for consistency
  - Indexes on frequently queried properties
  - Estimated capacity: 10M+ nodes, 100M+ relationships

### 2. GraphRAG Engine

**File**: `src/graph_rag_engine.py`

**Responsibilities**:
- Convert natural language to structured queries
- Execute graph queries
- Generate natural language responses
- Trace supply chains

**Architecture**:

```
User Question
     │
     ▼
┌─────────────────────────────────┐
│  Query Understanding (LLM)      │
│  Input: Question + Schema       │
│  Output: Structured Query Plan  │
│  {                              │
│    intent: "find suppliers"     │
│    entities: ["Supplier"]       │
│    filters: {location: "Italy"} │
│    relationships: ["PROVIDES"]  │
│  }                              │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  Query Execution                │
│  - Filter nodes by label        │
│  - Apply property filters       │
│  - Traverse relationships       │
│  - Collect results              │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│  Answer Generation (LLM)        │
│  Input: Question + Results      │
│  Output: Natural Language Answer│
└─────────────────────────────────┘
```

**Key Methods**:
```python
class GraphRAGEngine:
    - query(question: str) -> dict
        └─> _create_query_prompt()
        └─> llm.invoke(prompt)
        └─> _execute_query_plan(plan)
        └─> _create_answer_prompt()
        └─> llm.invoke(answer_prompt)
    
    - trace_supply_chain(product_id: str) -> dict
        └─> Find factory (MANUFACTURES)
        └─> Find materials (SUPPLIED_TO)
        └─> Find suppliers (PROVIDES)
        └─> Find certifications (HAS_CERTIFICATION)
```

**LLM Integration**:
- **Model**: GPT-4.1-mini (fast, cost-effective)
- **Temperature**: 0 (deterministic)
- **Prompts**: Structured with schema context
- **Token Usage**: ~500-1000 tokens per query

### 3. Certification Validator

**File**: `src/certification_validator.py`

**Responsibilities**:
- Assess certification confidence
- Implement human-in-the-loop workflow
- Manage validation state
- Generate audit trails

**LangGraph State Machine**:

```
                    START
                      │
                      ▼
            ┌─────────────────┐
            │ Assess          │
            │ Certification   │
            │ (AI Analysis)   │
            └────────┬────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    High Confidence         Medium/Low
         │                   Confidence
         ▼                       │
┌────────────────┐               ▼
│ Auto Approve   │      ┌────────────────┐
└────────┬───────┘      │ Request Human  │
         │              │ Review         │
         │              └────────┬───────┘
         │                       │
         │                       ▼
         │              ┌────────────────┐
         │              │ Process Human  │
         │              │ Feedback       │
         │              └────────┬───────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Finalize Result │
            └────────┬────────┘
                     │
                     ▼
                    END
```

**State Definition**:
```python
class CertificationState(TypedDict):
    query: str
    certification_data: dict
    confidence_level: str  # "High", "Medium", "Low"
    validation_status: str  # "pending", "approved", "rejected"
    ai_assessment: str
    human_feedback: str
    final_result: dict
    requires_human_review: bool
```

**Confidence Scoring**:
```python
Factors:
- Validity dates (expired = Low)
- Issuing body reputation (known = +1)
- Verification URL (present = +1)
- Data completeness (all fields = +1)

Scoring:
- High: All factors positive, not expired
- Medium: 2-3 factors positive
- Low: <2 factors positive OR expired
```

**Checkpoint System**:
- Uses `MemorySaver` for state persistence
- Each certification has unique thread_id
- Enables pause/resume for human review
- Supports audit trail reconstruction

### 4. Streamlit Frontend

**File**: `app.py`

**Responsibilities**:
- User interface
- Session state management
- Real-time updates
- Data visualization

**Architecture**:

```
Session State
├── db: GraphDatabase
├── engine: GraphRAGEngine
├── validator: CertificationValidator
└── query_history: List[dict]

Tabs
├── Query Supply Chain
│   ├── Input: Natural language question
│   ├── Process: engine.query(question)
│   └── Output: Answer + Query plan + Raw data
│
├── Validate Certifications
│   ├── Input: Selected certification IDs
│   ├── Process: validator.validate_all_certifications()
│   └── Output: Validation summary + Individual results
│
├── Trace Products
│   ├── Input: Product ID
│   ├── Process: engine.trace_supply_chain(product_id)
│   └── Output: Complete supply chain visualization
│
├── Browse Data
│   ├── Input: Node type selection
│   ├── Process: db.get_all_nodes(label)
│   └── Output: Expandable cards with relationships
│
└── Query History
    ├── Input: (automatic)
    ├── Process: session_state.query_history
    └── Output: Historical queries and results
```

**State Management**:
```python
# Initialize once per session
if 'db' not in st.session_state:
    st.session_state.db = GraphDatabase()
    populate_supply_chain_data(st.session_state.db)
    st.session_state.engine = GraphRAGEngine(st.session_state.db)
    st.session_state.validator = CertificationValidator(st.session_state.db)
    st.session_state.query_history = []
```

**Performance Optimization**:
- Lazy initialization (only on first access)
- Session state caching (avoid re-initialization)
- Minimal re-renders (use keys strategically)
- Async operations where possible

## Data Flow Examples

### Example 1: Natural Language Query

```
User: "Who supplies the leather for the 2024 collection?"
  │
  ▼
[GraphRAG Engine]
  │
  ├─> LLM: Convert to query plan
  │   {
  │     intent: "find suppliers",
  │     entities: ["Supplier", "Material"],
  │     filters: {type: "Leather", year: "2024"},
  │     relationships: ["PROVIDES", "SUPPLIED_TO"]
  │   }
  │
  ├─> Execute query plan
  │   - Get all Supplier nodes
  │   - Filter by relationships to Leather materials
  │   - Filter by year in collection
  │   - Collect: Tuscany Leather Consortium, Marche Leather Artisans
  │
  └─> LLM: Generate answer
      "The Tuscany Leather Consortium in Florence, Italy supplies
       premium calf leather with A+ grade and LWG Gold certification
       for the 2024 collections..."
```

### Example 2: Certification Validation

```
User: Validates "CITES Permit" (CERT004)
  │
  ▼
[Certification Validator]
  │
  ├─> State: assess_certification
  │   - LLM analyzes certification data
  │   - Checks validity dates
  │   - Result: confidence_level = "Low" (expired)
  │
  ├─> Decision: should_request_human_review?
  │   - Low confidence → "human_review"
  │
  ├─> State: request_human_review
  │   - Print notification
  │   - Set validation_status = "pending"
  │
  ├─> State: process_human_feedback
  │   - (Simulated) Human rejects
  │   - Set validation_status = "rejected"
  │
  └─> State: finalize_result
      - Generate final_result dict
      - Return to user
```

### Example 3: Supply Chain Tracing

```
User: Traces "Dionysus Leather Handbag" (PROD001)
  │
  ▼
[GraphRAG Engine]
  │
  ├─> Find product node
  │   PROD001: {name: "Dionysus Leather Handbag", ...}
  │
  ├─> Traverse: (Factory)-[MANUFACTURES]->(Product)
  │   FAC001: Gucci Artisan Workshop
  │
  ├─> Traverse: (Material)-[SUPPLIED_TO]->(Factory)
  │   MAT001: Premium Calf Leather
  │
  ├─> Traverse: (Supplier)-[PROVIDES]->(Material)
  │   SUP001: Tuscany Leather Consortium
  │
  ├─> Traverse: (Supplier)-[HAS_CERTIFICATION]->(Certification)
  │   CERT001: Made in Italy
  │   CERT002: LWG Gold Rating
  │
  └─> Return complete trace
      {
        product: {...},
        factory: {...},
        materials: [{...}],
        suppliers: [{...}],
        certifications: [{...}]
      }
```

## Security Considerations

### Current Implementation
- **No authentication**: Demo application
- **In-memory data**: No persistence
- **API keys**: Pre-configured in environment

### Production Requirements
1. **Authentication & Authorization**
   - User authentication (OAuth 2.0)
   - Role-based access control (RBAC)
   - API key management

2. **Data Security**
   - Encryption at rest (Neo4j Enterprise)
   - Encryption in transit (TLS)
   - Audit logging

3. **API Security**
   - Rate limiting
   - Input validation
   - SQL/Cypher injection prevention

4. **Compliance**
   - GDPR compliance (data privacy)
   - SOC 2 Type II (security controls)
   - ISO 27001 (information security)

## Performance Characteristics

### Current Scale
- **Nodes**: 28
- **Relationships**: 40
- **Query Time**: <1s (in-memory)
- **LLM Latency**: 1-3s per call

### Production Scale Estimates

| Metric | Current | Production | Scaling Strategy |
|--------|---------|------------|------------------|
| Nodes | 28 | 10M+ | Neo4j sharding |
| Relationships | 40 | 100M+ | Relationship indexes |
| Concurrent Users | 1 | 1000+ | Load balancer + replicas |
| Query Latency | <1s | <2s | Caching + indexes |
| LLM Calls | Unlimited | Rate-limited | Queue + batching |

### Optimization Strategies

1. **Database**
   - Index frequently queried properties
   - Use relationship indexes for traversals
   - Implement query result caching (Redis)
   - Partition large graphs

2. **LLM**
   - Cache common queries
   - Batch similar requests
   - Use smaller models for simple tasks
   - Implement request queuing

3. **Frontend**
   - Server-side rendering for initial load
   - Lazy loading for large datasets
   - WebSocket for real-time updates
   - CDN for static assets

## Deployment Architecture

### Development
```
Local Machine
├── Python 3.11 + venv
├── In-memory database
├── Streamlit dev server
└── OpenAI API (cloud)
```

### Production
```
Cloud Infrastructure (AWS/GCP/Azure)
│
├── Load Balancer
│   └─> SSL/TLS termination
│
├── Application Tier (Kubernetes)
│   ├── Streamlit pods (3+ replicas)
│   ├── API pods (5+ replicas)
│   └── Worker pods (for async tasks)
│
├── Database Tier
│   ├── Neo4j cluster (1 write, 2+ read replicas)
│   └── Redis cache
│
├── AI Services
│   ├── OpenAI API (external)
│   └── LangChain Hub (external)
│
└── Monitoring & Logging
    ├── Prometheus (metrics)
    ├── Grafana (dashboards)
    └── ELK Stack (logs)
```

## Technology Choices Rationale

### Why In-Memory Database (for demo)?
- ✅ Fast development
- ✅ No external dependencies
- ✅ Easy to demonstrate
- ❌ Not production-ready

### Why Neo4j (for production)?
- ✅ Industry-standard graph database
- ✅ Powerful Cypher query language
- ✅ Excellent performance for graph traversals
- ✅ Enterprise support and tooling

### Why LangChain?
- ✅ Abstracts LLM complexity
- ✅ Prompt management
- ✅ Chain composition
- ✅ Large ecosystem

### Why LangGraph?
- ✅ State machine for complex workflows
- ✅ Checkpoint system for human-in-the-loop
- ✅ Better than simple if/else logic
- ✅ Visualizable and debuggable

### Why Streamlit?
- ✅ Rapid prototyping
- ✅ Python-native (no JavaScript)
- ✅ Built-in state management
- ✅ Easy deployment
- ❌ Limited customization vs. React

## Future Architecture Enhancements

### Phase 1: Production-Ready (3 months)
- Replace in-memory DB with Neo4j
- Add authentication and authorization
- Implement caching layer (Redis)
- Set up monitoring and alerting
- Deploy to cloud (Kubernetes)

### Phase 2: Scale (6 months)
- Implement microservices architecture
- Add message queue (RabbitMQ/Kafka)
- Implement async processing
- Add real-time notifications
- Integrate with external APIs

### Phase 3: Advanced Features (12 months)
- Blockchain integration for immutability
- Machine learning for anomaly detection
- Predictive analytics
- Mobile application
- Multi-tenant support

---

**Note**: This architecture is designed to be both demonstrable (for portfolio) and scalable (for production). The current implementation prioritizes clarity and ease of understanding over performance optimization.
