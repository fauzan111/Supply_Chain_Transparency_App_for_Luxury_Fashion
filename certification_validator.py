"""
LangGraph Human-in-the-Loop Workflow for Certification Validation
Implements approval workflow when AI is uncertain about certifications
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from graph_database import GraphDatabase
import json
from datetime import datetime

# Define the state structure
class CertificationState(TypedDict):
    """State for certification validation workflow"""
    query: str
    certification_data: dict
    confidence_level: str  # "High", "Medium", "Low"
    validation_status: str  # "pending", "approved", "rejected", "auto_approved"
    ai_assessment: str
    human_feedback: str
    final_result: dict
    requires_human_review: bool


class CertificationValidator:
    """Human-in-the-loop certification validation workflow"""
    
    def __init__(self, db: GraphDatabase, model: str = "gpt-4.1-mini"):
        """Initialize the certification validator"""
        self.db = db
        self.llm = ChatOpenAI(model=model, temperature=0)
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
        
        # Memory saver for checkpoints
        self.memory = MemorySaver()
        
        # Compile the graph with checkpointing
        self.app = self.workflow.compile(checkpointer=self.memory)
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        
        # Create a new graph
        workflow = StateGraph(CertificationState)
        
        # Add nodes
        workflow.add_node("assess_certification", self._assess_certification)
        workflow.add_node("auto_approve", self._auto_approve)
        workflow.add_node("request_human_review", self._request_human_review)
        workflow.add_node("process_human_feedback", self._process_human_feedback)
        workflow.add_node("finalize_result", self._finalize_result)
        
        # Set entry point
        workflow.set_entry_point("assess_certification")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "assess_certification",
            self._should_request_human_review,
            {
                "auto_approve": "auto_approve",
                "human_review": "request_human_review"
            }
        )
        
        # Add edges
        workflow.add_edge("auto_approve", "finalize_result")
        workflow.add_edge("request_human_review", "process_human_feedback")
        workflow.add_edge("process_human_feedback", "finalize_result")
        workflow.add_edge("finalize_result", END)
        
        return workflow
    
    def _assess_certification(self, state: CertificationState) -> CertificationState:
        """Assess the certification data using AI"""
        
        cert_data = state["certification_data"]
        
        # Create assessment prompt
        prompt = ChatPromptTemplate.from_template("""
You are a certification expert for luxury fashion supply chains. Assess the following certification data.

Certification Information:
{cert_info}

Analyze this certification and provide:
1. Confidence Level (High/Medium/Low) - based on:
   - Validity dates (is it current?)
   - Issuing body reputation
   - Verification URL availability
   - Data completeness

2. Assessment - A brief explanation of your confidence level

3. Concerns - Any red flags or issues (if any)

Respond in JSON format:
{{
    "confidence_level": "High|Medium|Low",
    "assessment": "your assessment here",
    "concerns": ["concern 1", "concern 2"] or []
}}
""")
        
        messages = prompt.format_messages(
            cert_info=json.dumps(cert_data, indent=2)
        )
        
        response = self.llm.invoke(messages).content
        
        try:
            assessment = json.loads(response)
        except json.JSONDecodeError:
            assessment = {
                "confidence_level": "Low",
                "assessment": "Unable to parse AI response",
                "concerns": ["JSON parsing error"]
            }
        
        # Check if certification is expired
        if "valid_until" in cert_data:
            try:
                valid_until = datetime.strptime(cert_data["valid_until"], "%Y-%m-%d")
                if valid_until < datetime.now():
                    assessment["confidence_level"] = "Low"
                    assessment["concerns"].append("Certification has expired")
            except:
                pass
        
        # Update state
        state["confidence_level"] = assessment["confidence_level"]
        state["ai_assessment"] = assessment["assessment"]
        state["requires_human_review"] = assessment["confidence_level"] in ["Medium", "Low"]
        
        # Add concerns to assessment
        if assessment["concerns"]:
            state["ai_assessment"] += f"\n\nConcerns: {', '.join(assessment['concerns'])}"
        
        return state
    
    def _should_request_human_review(self, state: CertificationState) -> Literal["auto_approve", "human_review"]:
        """Decide whether human review is needed"""
        if state["requires_human_review"]:
            return "human_review"
        return "auto_approve"
    
    def _auto_approve(self, state: CertificationState) -> CertificationState:
        """Auto-approve high confidence certifications"""
        state["validation_status"] = "auto_approved"
        state["human_feedback"] = "Not required - High confidence"
        return state
    
    def _request_human_review(self, state: CertificationState) -> CertificationState:
        """Request human review for uncertain certifications"""
        state["validation_status"] = "pending"
        
        # In a real application, this would trigger a notification to a human operator
        # For this demo, we'll simulate the request
        print("\n" + "="*60)
        print("🚨 HUMAN REVIEW REQUIRED")
        print("="*60)
        print(f"\nQuery: {state['query']}")
        print(f"\nCertification: {state['certification_data'].get('name', 'Unknown')}")
        print(f"Confidence Level: {state['confidence_level']}")
        print(f"\nAI Assessment:\n{state['ai_assessment']}")
        print("\n" + "="*60)
        
        return state
    
    def _process_human_feedback(self, state: CertificationState) -> CertificationState:
        """Process feedback from human operator"""
        
        # In a real application, this would wait for actual human input
        # For demo purposes, we'll simulate approval based on confidence level
        
        if state.get("human_feedback") and state["human_feedback"] != "":
            # Human feedback was provided
            if "approve" in state["human_feedback"].lower():
                state["validation_status"] = "approved"
            else:
                state["validation_status"] = "rejected"
        else:
            # Simulate human decision
            if state["confidence_level"] == "Medium":
                state["validation_status"] = "approved"
                state["human_feedback"] = "Approved after manual verification"
            else:
                state["validation_status"] = "rejected"
                state["human_feedback"] = "Rejected - requires further investigation"
        
        return state
    
    def _finalize_result(self, state: CertificationState) -> CertificationState:
        """Finalize the validation result"""
        
        cert_data = state["certification_data"]
        
        state["final_result"] = {
            "certification_name": cert_data.get("name", "Unknown"),
            "certification_type": cert_data.get("type", "Unknown"),
            "validation_status": state["validation_status"],
            "confidence_level": state["confidence_level"],
            "ai_assessment": state["ai_assessment"],
            "human_feedback": state.get("human_feedback", "None"),
            "issuing_body": cert_data.get("issuing_body", "Unknown"),
            "valid_until": cert_data.get("valid_until", "Unknown"),
            "verification_url": cert_data.get("verification_url", "Not provided")
        }
        
        return state
    
    def validate_certification(self, query: str, certification_id: str, 
                              human_feedback: str = None) -> dict:
        """
        Validate a certification with optional human-in-the-loop
        
        Args:
            query: The original query that led to this certification
            certification_id: ID of the certification to validate
            human_feedback: Optional human feedback (for resuming workflow)
            
        Returns:
            Validation result dictionary
        """
        
        # Get certification data from database
        cert_node = self.db.nodes.get(certification_id)
        if not cert_node:
            return {
                "error": f"Certification {certification_id} not found",
                "validation_status": "error"
            }
        
        cert_data = cert_node['properties']
        
        # Create initial state
        initial_state = {
            "query": query,
            "certification_data": cert_data,
            "confidence_level": "",
            "validation_status": "pending",
            "ai_assessment": "",
            "human_feedback": human_feedback or "",
            "final_result": {},
            "requires_human_review": False
        }
        
        # Run the workflow
        config = {"configurable": {"thread_id": certification_id}}
        
        try:
            # Execute the workflow
            result = self.app.invoke(initial_state, config)
            return result["final_result"]
        except Exception as e:
            return {
                "error": str(e),
                "validation_status": "error"
            }
    
    def validate_all_certifications_for_query(self, query: str, 
                                             certification_ids: list) -> list:
        """
        Validate multiple certifications for a query
        
        Args:
            query: The original query
            certification_ids: List of certification IDs to validate
            
        Returns:
            List of validation results
        """
        results = []
        
        for cert_id in certification_ids:
            result = self.validate_certification(query, cert_id)
            results.append(result)
        
        return results
    
    def get_certification_summary(self, results: list) -> dict:
        """Generate a summary of certification validation results"""
        
        summary = {
            "total_certifications": len(results),
            "auto_approved": 0,
            "human_approved": 0,
            "rejected": 0,
            "high_confidence": 0,
            "medium_confidence": 0,
            "low_confidence": 0,
            "certifications": results
        }
        
        for result in results:
            status = result.get("validation_status", "unknown")
            confidence = result.get("confidence_level", "unknown")
            
            if status == "auto_approved":
                summary["auto_approved"] += 1
            elif status == "approved":
                summary["human_approved"] += 1
            elif status == "rejected":
                summary["rejected"] += 1
            
            if confidence == "High":
                summary["high_confidence"] += 1
            elif confidence == "Medium":
                summary["medium_confidence"] += 1
            elif confidence == "Low":
                summary["low_confidence"] += 1
        
        return summary


if __name__ == "__main__":
    # Test the certification validator
    from populate_data import populate_supply_chain_data
    
    db = GraphDatabase()
    populate_supply_chain_data(db)
    
    validator = CertificationValidator(db)
    
    # Test with different certifications
    print("\n" + "="*60)
    print("Testing Certification Validation Workflow")
    print("="*60)
    
    # Test 1: High confidence certification (Made in Italy)
    print("\n\n1. Testing HIGH confidence certification...")
    result1 = validator.validate_certification(
        query="Verify Made in Italy certification",
        certification_id="CERT001"
    )
    print(f"\nResult: {json.dumps(result1, indent=2)}")
    
    # Test 2: Medium confidence certification (CITES - expires soon)
    print("\n\n2. Testing MEDIUM confidence certification...")
    result2 = validator.validate_certification(
        query="Verify CITES permit for exotic materials",
        certification_id="CERT004"
    )
    print(f"\nResult: {json.dumps(result2, indent=2)}")
    
    # Test 3: Validate multiple certifications
    print("\n\n3. Testing multiple certifications...")
    results = validator.validate_all_certifications_for_query(
        query="Verify all certifications for Tuscany Leather Consortium",
        certification_ids=["CERT001", "CERT002"]
    )
    
    summary = validator.get_certification_summary(results)
    print(f"\nSummary: {json.dumps(summary, indent=2)}")
