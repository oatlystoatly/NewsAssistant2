Architecture and source selection reasoning.

1. Purpose
2. System components
    - user interface
    - contxt manager
    - retrieval component
    - clarification component
    - source filter

-------
Purpose
-------

The News assistant finds information on topics for the user on any topic. The hardware not expressed is access to the internet, link to most search engines and a working LLM. 

-----------------
System Components
-----------------

User interface: The user interface recieved questions and messages. It also presents clarification options when there is ambiguity with the message.


Context manager: It controls the topic from the user message, user preferences on the type of source and the research purpose from the user. For example, the topic would be 'Bin strikes', user preferences if social media source or news source, and the research purpose as 'report'. 

Retrieval component: This identifies relevant documents from the local corpus using the context manager (ie.e. the topic and user preferences).

Clarification component: Identifies missing or ambiguous source preferences.

Source filter: Selects documents matching the user's preferences and recency requirements.

Evidence display: Presents the answer alongside supporting sources and dates.







