------------------
DEVELOPMENT RECORD
------------------

Stage |	Development	| Reason for change	What to check or evidence

1. 	Context map and interaction scenarios
	- Identify ambiguity and user requirements
    - Original design documents
2.	Controlled Markdown corpus	
    - Isolate source-selection behaviour from live retrieval
    - Five source files and metadata
3.	Initial Python prototype
    - Develop functional interactions
    - Early terminal interactions
4.	Clarification and source categories
    - Avoid assuming the user's preferred source
    - Ambiguous request walkthrough
5.	Individual article selection
    - Increase user control over retrieved information
    - Numbered source selection
6. Recency filtering
    - Prevent outdated information appearing as recent evidence	
    - CNN inclusion and exclusion tests
7. Contextual memory	
    - Prevent loss of topic and purpose during follow-ups
    - Multi-turn conversation
8. Academic suitability warnings	
    - Make source limitations visible
    - TikTok report scenario
9. Streamlit integration
    - Improve accessibility and conversational presentation	
    - Browser screenshots
10. Testing and refinement	
    - Identify functional and interaction limitations	
    - Completed test record

## INDEPTH ANALYSIS OF DEVELOPMENT

1. Context map and interaction scenarios

I initially created a context map and interaction scenarios through story boarding and planning. This was inspired by the labs from week 1-4, also seen as a template for docs 01-04. 

During development I focused on fixing a small problem, therefore the focus on the story boards and scenarios are more detailed than the news assistance design. I did not aim for a complete solve of AI personalised assistance but rather a change in computer assumption making over user design, influenced by what I learnt in lectures.

2. Controlled Markdown corpus	

I created orginally three simulated mark down sources and labelled them corpus: accademic, bbc news, tiktok. This emulates real life sources that students would want to use. 

The use of the actual names, show how throughout the process I understood that connection to the LLM would be a deffered feature, otherwise I would have to clarify more explicitly that these are fake examples of code.

I then developed the itv news source to all there to be multiple types of one source, and all the use to choose between two types. 

I then developed the ccn news source. I wanted to test the use case of someone asking for information and needed the LLM to decipher that this is outdated text. Therefore I set a date as a metadata in each feature to add a superceding function from the agent. 

Finally I developed the peaky blinders md, as I needed to prove that the agent could collect the correct topic type.

3. Initial Python prototype

The initial python prototype was an interminal simulation rather than the planned browser screen. I decided to develop this rather than just doing the simple md folder route because I wanted a visual representation of my work and check that my logic made sense. 

This can be found in /xtras/simulation.py

4. Clarification and source categories

This was developed through a series of testing and playing around with the new developed bob_bot.py. To check that clarification worked, I provided multiple ambigious and non real prompt suggestions.

5. Individual article selection

I decided to improve traditional article selections by increasing the user input and decision making. This was inspired from what I learnt in lectures as I learnt more about ambiguity and personal control decisions improving trust from the user if they have more control on the final output. 

6. Recency filtering

This was developed through making the CNN exclusion tests. I identified that requesting all available news sources could conflict with a user's requirement for recent information. The system initially treated the quantity of sources and their recency as closely related requirements.

A configurable 30-day recency threshold was introduced alongside the superseded metadata field. This was intended to prevent historical information from being presented as current evidence while allowing the user to intentionally retrieve historical sources.

7. Contextual memory 

This allows multi turn conversations and the option to go back to the previou state when filtering through different sources. 

However, this could be developed further and improved as in some cases, for example, after a large amount of input it may not remember information. This is mainly because it believes it in a different state.

8. Academic suitability warnings

This was developed specifically for the Tiktok scenario. I did not want you to not be able to access sources, but also warn the content of said sources.

9. Streamlit integration

This improved accessibility and conversation presentation. This allowed problems that I found such as how the metadata of sources were presented to be identified and fixed. 

10. Testing and refinement

This can be seen in the test record. 