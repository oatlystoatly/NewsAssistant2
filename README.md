------------------------------------------
BOB BOT - Intelligent Assistant Prototype
------------------------------------------
This is my project status, setup and development record.

## PROJECT OVERVIEW

Bob Bot is an interactive assistant prototype, developed to explore how an intelligence assistant should explore ambiguity, user intent and conversational context in an example of an AI assisted information retrieval. 

The project investigates how an agent can clarify ambigious requests, respect user preferences and provide explanations for its source selection decisions without making assumptions.

## PROJECT

The current implementation is a functional, rule-based prototype with a browser-based conversational interface developed using Streamlit. This is developed through 'bob_bot.py' ad 'app.py', however, developed analysis can be found through the documents section. 

-------------
FUNCTIONALITY
-------------

## DEVELOPED FUNCTIONALITY

- Keyword-based intent and entity recognition.
- Identification of explicit, inferred and missing request information.
- Selective clarification of ambiguous source preferences.
- Selection of multiple source categories.
- Individual article selection and preview.
- Date-based recency filtering.
- Warnings for superseded information.
- Academic suitability warnings for social media sources.
- Conversational context retention within an active session.
- User-confirmed reuse of previous source preferences.
- Feedback, correction and source-selection explanations.

## SIMULATED FUNCTIONALITY

The prototype uses a controlled local corpus of five fictional Markdown source files representing news, academic and social media sources. 

The source content is simulated and not genuine. 

The intelligent interpretation is simulated using predefined rules and keyword analysis matching rather than a LLM, as the project focuses on error handling rather than the LLM model. 

It is a simulated instance of a user interacting with their personalised AI agent. This is why intergration with an LLM was deferred as it would need to be personalised, which is unrealistic to make examinable to an unknown user within the time frame.

## DEFERRED FUNCTIONALITY

- Live news retrieval.
- Integration with a personalised LLM.
- General-purpose natural-language understanding.
- Persistent memory across independent sessions.
- Wider source coverage and non simmulated source verification.
- Further interface development and user evaluation.

## TECHNOLOGY STACK 

Technology | Purpose

Python 3.14.2| Request interpretation, context management and retrieval logic
Streamlit 1.67.0 | Interactive browser-based interface and session management
Markdown | Controlled source corpus and development documentation
CSS | Visual styling of the conversational interface
VS Code | Development environment
GitHub | Version control and project documentation
ChatGPT | AI-assisted development and design support, not the running prototype.

------------------------
## RUNNING THE PROTOTYPE
------------------------
REQUIREMENTS
- Python 3.12.2 
- Streamlit 1.67.0

SETUP
1. Clone or download this repository
2. Open the project folder in a terminal or VS Code
3. Install the dependencies using python3 -m pip install -r requirements.txt
(If this does not work install streamlit)
4. Run python3 -m streamlit run app.py
5. Open the local browser address provided by Streamlit.

In terminal version
python3 bob_bot.py

NO API key or external service for news is needed.

## WARNING 
Depending on your operating system and python installation you may need to use python instead of python3

-----------------------
## EXAMPLE INTERACTIONS
-----------------------
The prototype supports three principal interaction scenarios:

An ambiguous request concerning the Selly Oak bin strikes, requiring clarification of source preferences.

A request for all available news articles, including potentially superseded information.

A recognised question about Black Sabbath for which the local corpus contains no supporting evidence.

Further examples explore recency filtering, conversational context and academic suitability warnings.

## DEVELOPMENT RECORD

The prototype was developed incrementally, beginning with interaction design and a controlled source corpus before progressing to Python-based interaction logic and a Streamlit interface.

It originally had one simulated py files which is included in the xtras folder.

<>

## TESTING AND EVALUATION

Testing focuses on whether the prototype responds appropriately to predefined user requests and interaction scenarios.

The test record documents expected behaviour, observed behaviour, identified problems and subsequent improvements.

See /docs/02_TEST_RECORD.d

-------------
AI ASSISTANCE
-------------

ChatGPT was used to support the development of the prototype, including discussions of system architecture, Python implementation, contextual memory, source filtering, warning messages and Streamlit integration.

CoPilot was used to help with git submissions and prototype development as well as working through directories.

AI-generated suggestions were adapted throughout development to reflect the intended interaction design.

The final implementation, storyboards, markdown files, logic and reasoning and  design decisions remain the responsibility of the project author.

----------
ADDITIONAL 
----------
PROJECT FILES

Context Map — Initial context and assumptions.

Test Record — Functional testing and evaluation.

Interaction Design — Developed interaction scenarios and alternative paths.

System Design — System architecture and design decisions.

/docs/test_case_photos/ — Visual evidence of developed testing.

Sources/ — Fictional local news source corpus.

xtras - This includes the simulation example to show progression

Additional Diagrams - These provide visual examples of the flow charts and reasoning.

## REFERENCES AND ACKNKOWLEDGEMENTS

Python — programming language and standard libraries.

Streamlit — framework used to develop the conversational interface.

ChatGPT (OpenAI) — assistance with Python development, debugging, interaction design and documentation.

Lab teaching materials — adapted for the initial context mapping exercise and doc design inputs.

LucidChart - All charts are made on Lucid chart but not using the AI feature.

Canva -- All storyboards are made on canva, not using the AI feature, the only exemption is some of the design/pitcure 'elements' can be sourced from AI from the way that it is drawn.

The source corpus contains fictional material created for simulation purposes and does not represent genuine published articles.

Academic literature informing the design is referenced in the accompanying assignment report.


## SUBMITTED VERSION
- Repository 
https://github.com/oatlystoatly/NewsAssistant2/tree/main
- Submitted commit or release