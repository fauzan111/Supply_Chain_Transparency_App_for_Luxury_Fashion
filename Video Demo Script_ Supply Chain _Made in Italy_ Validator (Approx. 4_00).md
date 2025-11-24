# Video Demo Script: Supply Chain "Made in Italy" Validator (Approx. 4:00)

This script is designed for a professional, 3-5 minute portfolio video. Use the Streamlit application (accessible via the provided URL) for the live demo sections.

---

## 🎬 Scene 1: Introduction & Problem Statement (0:00 - 0:30)

| Time | Visuals | Talking Points |
|---|---|---|
| 0:00 | Title Card: "Supply Chain 'Made in Italy' Validator" | **(Energetic, Professional Tone)** |
| 0:05 | Transition to a graphic of a luxury handbag/product. | **"The luxury fashion industry is facing a massive challenge: transparency."** |
| 0:10 | Show a graphic of the EU flag and "Digital Product Passport." | "Upcoming EU regulations, like the **Digital Product Passport**, demand complete, verifiable traceability for every product. For brands like Gucci and Prada, this means instantly answering: *'Who supplied the leather for this handbag?'* and *'Is that supplier's certification still valid?'*" |
| 0:20 | Transition to the Streamlit app's main page. | "This is the **Supply Chain 'Made in Italy' Validator**, a **GraphRAG** application I built to solve this problem." |

---

## 🎬 Scene 2: Architecture & Key Technologies (0:30 - 1:15)

| Time | Visuals | Talking Points |
|---|---|---|
| 0:30 | Show the Architecture Diagram (from ARCHITECTURE.md). | "The core challenge is that supply chains are complex networks. That's why I chose a **GraphRAG** architecture." |
| 0:40 | Highlight the Graph Database (Neo4j concept). | "Instead of a traditional database, we use a graph to map relationships between **Suppliers, Materials, Factories, and Certifications**. This makes complex queries simple." |
| 0:50 | Highlight LangChain/GraphRAG Engine. | "I used **LangChain** to build a **GraphRAG Engine** that translates natural language questions into graph queries, retrieving relationship-aware context." |
| 1:00 | Highlight LangGraph/Certification Validator. | "And critically, I used **LangGraph** to implement a **Human-in-the-Loop** workflow, ensuring compliance and trust for high-stakes decisions like certification validation." |
| 1:10 | Transition to the Query tab. | "Let's see it in action." |

---

## 🎬 Scene 3: Demo - Natural Language Query (1:15 - 2:15)

| Time | Visuals | Talking Points |
|---|---|---|
| 1:15 | Type the first query into the Query tab. | **"Imagine a compliance officer needs to verify a material source."** |
| 1:20 | **Query**: "Who supplies the leather for the 2024 collection?" | "I can ask a complex, multi-hop question in plain English: **'Who supplies the leather for the 2024 collection?'**" |
| 1:30 | Show the AI's Answer. | "The AI instantly returns a professional answer: **'The Tuscany Leather Consortium in Florence, Italy supplies premium calf leather...'**" |
| 1:40 | Expand the "Query Analysis" section. | "But the real power is under the hood. The **GraphRAG Engine** parsed my question into a structured query plan, identifying the intent, entities, and relationships needed to traverse the graph." |
| 1:50 | Scroll through the Raw Data. | "It then executed that plan against the graph, retrieving all the relevant data points—the supplier, the material, the factory, and the collection details." |
| 2:00 | **Key Takeaway**: Show the speed and accuracy. | "This is the power of GraphRAG: **fast, accurate, relationship-aware answers** that a traditional database struggles to provide." |

---

## 🎬 Scene 4: Demo - Human-in-the-Loop Validation (2:15 - 3:15)

| Time | Visuals | Talking Points |
|---|---|---|
| 2:15 | Switch to the "Validate Certifications" tab. | "Now, let's look at the **Human-in-the-Loop** feature, which is essential for compliance." |
| 2:25 | Select a few certifications (e.g., Made in Italy, CITES Permit). | "I'll select a few certifications and run the validation workflow." |
| 2:35 | Show the Validation Summary. | "The **LangGraph** state machine takes over. It uses AI to assess the confidence of each certification." |
| 2:45 | Click to expand an **Auto-Approved (High Confidence)** result. | "For a high-confidence certification, like **'Made in Italy,'** the AI auto-approves it, providing a full audit trail." |
| 2:55 | Click to expand a **Rejected/Pending (Low Confidence)** result (e.g., CITES Permit). | "But for a low-confidence case—perhaps a CITES permit that is about to expire—the system flags it, sets the status to **'Rejected,'** and provides a detailed AI assessment of the concerns." |
| 3:05 | **Key Takeaway**: Emphasize compliance. | "This ensures that high-stakes decisions are always reviewed by a human operator, providing a **verifiable audit trail** for regulators." |

---

## 🎬 Scene 5: Demo - Supply Chain Tracing & Conclusion (3:15 - 4:00)

| Time | Visuals | Talking Points |
|---|---|---|
| 3:15 | Switch to the "Trace Products" tab. | "Finally, let's see the complete **Digital Product Passport** in action." |
| 3:20 | Select a product (e.g., "Dionysus Leather Handbag") and click "Trace." | "I can trace the **Dionysus Handbag** back to its origin." |
| 3:30 | Scroll through the trace results (Factory, Materials, Suppliers, Certifications). | "We instantly see the manufacturing factory, the specific materials used, the suppliers for those materials, and all relevant certifications—a complete, end-to-end view of the supply chain." |
| 3:40 | Transition back to a closing slide with key skills. | "This project demonstrates my expertise in **GraphRAG**, **LangGraph state machines**, **Neo4j integration**, and building **production-ready full-stack applications**." |
| 3:50 | Final Call to Action (Text on screen: "View Code on GitHub," "Read the Blog Post"). | "Thank you for watching. The full code, architecture deep-dive, and a detailed blog post are available in the links below." |
| 4:00 | End. | |

---
**Next Steps for User:**
1. Record the screen following the visuals and talking points.
2. Use the provided URL for the live demo.
3. Edit the video to match the timing and add professional music/graphics.
4. Upload to YouTube/Vimeo.
