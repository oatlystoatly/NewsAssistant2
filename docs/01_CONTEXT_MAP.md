## User and System Context

Context | Information | Design implication

1. User goal
Information: Retrieve relevant information	
Design implementation: Identify the purpose of the request

2. Topic
Information: Selly Oak bin strikes	
Design implication: Filter relevant sources

3. Location
Information: Selly Oak, Birmingham	
Design Implication: Establish geographical relevance and topic

4. Source preference	
Information: News, academic or social media	
Design implication: Clarify when unspecified

5. Recency
Information: Recent, historical or unrestricted
Design implication: Filter using source dates

6. Purpose	
Information: Report, assignment or general interest
Design implication: Provide appropriate source warnings

7. Conversation history	
Information: Previous requests and preferences	
Design Implication: Retain relevant context without automatically applying historical preferences

## Assumptions
- The user may not communicate their full intention initially.
- Previous preferences may not reflect current requirements.
- Recent information is defined as information from the last 30 days.
- System only recognises keywords

## System constraints
- Limited, fictional source corpus.
- Rule-based interpretation rather than genuine AI reasoning.
- Session-based memory.
- No live internet retrieval.

## Design response
The system addresses uncertainty through selective clarification, visible source options, contextual memory, transparent filtering and opportunities for user correction.