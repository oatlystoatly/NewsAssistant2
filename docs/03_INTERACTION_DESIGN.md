Developed screens, user choices and system responses. User conversation.

Structure of walkthrough: 
1. Scenario and user goal.
2. Initial ambiguous request
3. System context and interpretation
4. Initial retrieval and candidate sources
5. Clarification interaction
6. User selection and source filtering
7. Final answer and supporting evidence
8. Feedback and correction
9. Alternative interaction paths
10. Evaluation and limitations

---------
Interaction 1: Ambiguity and clarification

SCENARIO: The user is trying to research about local news on the Selly Oak bin strikes. However the user is unclear with their input. 

<State 1: User intention>
Initial ambigious request: 
Userinput: "Give me updates on the Selly Oak Bin strikes" 

Explanation:
The user wants to write a report on the Selly Oak bin strikes. There is an undisclosed request that the sources are reputable news sources or academic sources. Previous chat history suggests that the user only wants to use.

<State 2: System interpretation and context.>
*Intent* 'update_search'
*Entities Extracted*
    * Topic: Bin strikes
    * Type of source: Any
    * Area: Selly Oak, Birmingham
    * Use: Ambigious
    * Date: Recent

Explanation:
The user has not specified that they want 'news' and rather there is a search for the key word 'Updates'. This previously caused a system selection of the tiktokuser123 source in the corpus, as the source has the word 'Update' in it compared to other sources. However, the system knows that if use is ambigious and the type of source is ambigious. Therefore the agent asks for clarification. 

<State 3: Clarification>
Output: "What sort of update source would you like? News sources, academic sources or social media?" 

Explanation:
See '04_SYSTEM_DESIGN' for clarification on the type of language used. The agent asks for clarification as the design has found that the question is ambigious. The system proposes three signifiers for the user to select, giving more control for the user.


<State 4: Source Selection>
Userinput: *Selects 'News sources'

*Intent* 'news_search'
*Entities Extracted*
    * Topic: Bin strikes
    * Type of source: News articles
    * Area: Selly Oak, Birmingham
    * Use: Ambigious
    * Date: Recent

Explanation:
The user selects the 'News source option', the agent now can select between the BBC_news, itv_news and bbc_news. The CNN option is denied as the previous word 'updates' suggests that the user wants recent news. A possible improvement is that the use is still ambigious, however it may not be needed as the type of source is clear and 'updates' suggests that it is recent. 

<State 5: System Response>

Output: 
"Here are recent news sources for you on the current Birmingham Bin Strikes:
BBC News: Waste Collection disruption
Date: 15/11/26

ITV News: MP Bob Dylan on Waste Collection disruption in Selly Oak.
Date: 15/11/26"

Explanation:
The agent then provides two sources, filtering if they are recent and news sources. It shows the date of the source, where it is from, and the title to show it is relevant.

<State 6: Feedback>
Output: "Are the sources satisfactory?"

UserInput: "Yes"

Explanation:
The agent asks a clarifying question at the end to check if the user is satisfied with the output. This allows feedback to the agent, but maintains control from the user, who can change and clarify if needed. 


DESIGN RATIONAL
**Success criteria:**
- Publication dates are visible.
- Source and Title are visible
- The older CNN example is not presented as current evidence and tiktokuser is not presented as evidence. 
- The explanation distinguishes historical relevance from current relevance.

LIMITATIONS OF DESIGN
The use of it is still ambigious from the user. The user could want academic sources instead or want both academic and news sources, for example a research paper on strikes and a news article. Therefore it may not be good to only allow one option selected. This limitation is mitigated by the feedback prompt, however this can also be improved to possible "Do you want any other sources".

------------
Interaction 2: Outdated information

SCENARIO: The user is trying to research about local news on the Selly Oak bin strikes. However the user wants all possible news stories, including irrelevant data ones. 

<State 1: User intention>
Userinput: "I want you to give me all the news articles you have on the current Selly Oak Bin Strikes for a report"

Explanation:
The user wants any news article relating to the Selly Bin strikes. This includes the outdated CNN article, which is not useful for the report, however it is relevant to the Selly Oak strikes. 


<State 2: System interpretation and context.>
Intent* 'news_search_formal'
*Entities Extracted*
    * Topic: Bin strikes
    * Type of source: News
    * Area: Selly Oak, Birmingham
    * Use: Formal report
    * Date: Any


Explanation: The system will output any news source that it has related to the Selly Oak bin strikes. It is flagged that the CNN news source is outdated. 

<State 3: Source Selection>

*Entities Extracted*
    * Topic: Bin strikes
    * Type of source: News
    * Area: Selly Oak, Birmingham
    * Use: Formal report
    * Date: Any

Explanation: The user has specifically requested all sources that the agent has available
Therefore the sources then selected by the agent is:
- BBC_News
- CNN_News
- ITV_News
The date of the sources are also clarified as well. CNN may be superceded in information, therefore it is still outputted with clarification that this is an outdated source.

<State 4: System Response>

Output: 
"Here are all the news sources for you on the current Birmingham Bin Strikes:
BBC News: Waste Collection disruption
Date: 15/11/26

ITV News: MP Bob Dylan on Waste Collection disruption in Selly Oak.
Date: 15/11/26"

CNN News: Early Report on Waste Disposal
Date: 15/11/2020
Important: This article may not be relevant as it is dated to 2020. 

Explanation:
As the system allows the CNN article to be superceded, the agent clarifies why it may not be relevant. However it is important to not hide information explicitly asked by the user.


<State 5: Feedback>
UserInput: "Why did you give this article if it is outdated?"
*UserIntent*: Clarification of choices

Output: "You asked for all sources available. You may want to site how atmospheres have changed between years."

Explanation:
The agent provides a positive explanation as to why they have suggested the CNN News source. 

DESIGN RATIONAL
**Success criteria:**
- Publication dates are visible.
- Source and Title are visible
- Only news areticles are presented.
- The explanation distinguishes historical relevance from current relevance and provides transparancy to the user. 

LIMITATIONS OF DESIGN
The design assumes that the user does not want the CNN article or is making a mistake. It assumes that the user cannot get all the required information from simply displaying the date of source.


------
Interaction 3: Unsupported Information


SCENARIO: The user is asking about the band 'Black Sabbath, a birmingham band but nothing to do with the sources the agent currently has.

<State 1: User intention>
Userinput: "How many members are there in the Birmingham Black Sabbath band? I am writing a report on them."

Explanation:
The user is asking a valid question, however the agent does not have the current answer to this.

<State 2: System interpretation and context.>
*Intent* 'BlackSabbath_band'
*Entities Extracted*
    * Topic: BlackSabbath
    * Type of source: Any
    * Area: Birmingham
    * Use: Formal report
    * Date: Any

Explanation: The agent correctly identifies the entities needed to answer this question and searches it's files for anything to do with the BlackSabbath birmingham band.

<State 3: System Selection>
The system searched its files in corpus for any information on the band, however there is none. It then decides to clarify that it does not have any information at the moment. 

<State 4: System Response>

Output: 
"I do not have any information on 'The Black Sabbath' in my files. Therefore I am unable to give a reliable answer."

Explanation:
The system is clear that they cannot answer this question. It regurgitates the topic 'Black Sabbath' back to the user to clarify it has identified the topic and there is not an input issue.


DESIGN RATIONAL
**Success criteria:**
- System is clear what limits it has to the user and does not provide unneccessary information.

LIMITATIONS OF DESIGN
The agent could be expanded to all google searches to help solve the problem for the user, however this is limited to the access it has. This is only an example case scenario however.  

