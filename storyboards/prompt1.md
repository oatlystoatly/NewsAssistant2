# Build an interactive chatbot prototype called Bob Bot

Create a simple, functional web-based chatbot prototype called **Bob Bot** for a university human–AI interaction design project.

The purpose is to demonstrate how a news assistant handles ambiguous user requests, asks for clarification, allows users to control source selection, and explains its decisions.

**This is a controlled design simulation, not a real AI news service.**

## 1. Initial screen

When the website opens, show a clean, minimal chatbot interface.

- Title: **Bob Bot**
- Subtitle: *A news assistant that asks rather than assumes.*
- A large, initially empty conversation area.
- At the bottom, a blank text input with the placeholder: **Ask Bob Bot a question...**
- A Send button.
- No preloaded messages, sample questions, suggested prompts or automatic chatbot greeting.
- The user must type the first message themselves.

Use a simple, professional design resembling a modern messaging application. Make it responsive for desktop and mobile.

## 2. Technical requirements

- Do not connect to the internet.
- Do not use external news APIs, search engines, AI models, OpenAI APIs or live retrieval.
- Do not fetch news articles from websites.
- Do not require authentication or a database.
- All responses and news records must be hard-coded locally.
- Use local React state to manage the conversation.
- Build a working interactive prototype, not just static mockups.
- Label any example news records as **simulated sources**, not verified articles.
- Do not automatically use previous conversation history to determine a user's preferences.

## 3. Main scenario: Selly Oak bin strikes

The primary demonstration begins when the user types:

**"Give me updates on the Selly Oak Bin strikes"**

Bob Bot should recognise:

- Topic: Selly Oak bin strikes
- Location: Selly Oak, Birmingham
- Requested information: Updates
- Source preference: Not specified
- Purpose: Not specified
- Recency: Recent information implied

The important point is that Bob Bot must **not automatically select social media or any other source type** just because the user asked for "updates".

Instead, Bob Bot should respond:

**"What sort of update source would you like? You can choose news sources, academic sources or social media."**

Show three clickable source-selection options:

- News sources
- Academic sources
- Social media

Also allow the user to type a response instead of clicking.

The user should be able to select more than one source category if desired.

## 4. When the user selects News sources

Bob Bot should acknowledge the choice:

**"You've selected news sources. I'll use the available simulated news records for the Selly Oak bin strikes."**

Then display two fictional, locally stored example records:

**BBC News — Simulated source**
Title: *Birmingham bin strike dispute continues*
Date: 15 November 2026
Summary: *An illustrative news record describing ongoing industrial action and its effect on waste collection.*

**ITV News — Simulated source**
Title: *Residents respond to disruption in Birmingham waste collections*
Date: 18 November 2026
Summary: *An illustrative news record describing local responses to collection disruption.*

These are fabricated records for interaction testing. Do not imply that BBC or ITV actually published these articles.

Display each record in a simple source card showing the source name, article title, publication date and summary.

After presenting the results, Bob Bot should ask:

**"Are these sources satisfactory for your request?"**

Show buttons:

- Yes
- No, change sources

If the user selects Yes, Bob Bot should acknowledge the feedback.

If the user selects No, change sources, Bob Bot should reopen the source-selection options without requiring the user to restart the conversation.

## 5. Other source selections

If the user selects Academic sources or Social media, show a corresponding simulated record from the local dataset.

For example:

**Academic source — Simulated**
Title: *Industrial action and municipal waste services: An illustrative case study*
Date: 2024

**Social media — Simulated**
Platform: TikTok
Title: *Local discussion about Selly Oak bin collections*
Date: 19 November 2026

Make clear that these records are fictional demonstrations.

Allow the user to change their selection at any point.

## 6. Second scenario: Outdated information

Recognise the user message:

**"I want you to give me all the news articles you have on the current Selly Oak Bin Strikes for a report"**

In this scenario, the user has explicitly requested **all** available news articles.

Bob Bot should display the two recent simulated news records, plus one older fictional record:

**CNN — Simulated historical source**
Title: *Previous waste collection dispute in Birmingham*
Date: 10 February 2020
Summary: *An illustrative historical article about an earlier dispute.*

Clearly distinguish the older record visually and explain:

**"I've included this older record because you asked for all available news articles. However, it was published in 2020 and may not be relevant to the current dispute."**

If the user asks:

**"Why did you include the old article?"**

Bob Bot should respond:

**"You requested all available news articles, so I included the older record rather than silently excluding it. I've shown its publication date so you can decide whether it is relevant to your report."**

This scenario demonstrates transparency and respecting explicit user instructions.

## 7. Third scenario: Unsupported information

Recognise the message:

**"How many members are there in the Birmingham Black Sabbath band? I am writing a report on them."**

Bob Bot should respond:

**"I don't have any supporting information about Black Sabbath in my available local sources, so I can't give you a reliable answer from this dataset."**

Do not generate a number from general knowledge.

Do not search the internet.

This demonstrates how the assistant responds when its available evidence is insufficient.

## 8. Source options and user control

Source preferences should be accessible for every request, even when Bob Bot does not need to ask a clarification question.

Add a small **Source preferences** control near the chat input or in the chat header.

When clicked, it should allow the user to select:

- News
- Academic
- Social media

Use these preferences for the current request only unless the user explicitly changes them.

Clarification should be triggered when the missing information is important to fulfilling the request. Do not ask unnecessary questions when the request is already sufficiently clear.

## 9. Interaction behaviour

Implement a simple local, rule-based conversation system.

It should:

1. Read the user's typed message.
2. Check whether it matches one of the three designed scenarios.
3. Identify relevant keywords and request conditions.
4. Ask for clarification when needed.
5. Wait for the user's choice before displaying results.
6. Present simulated sources with dates.
7. Accept feedback and allow correction.
8. Display a clear limitation message when no supporting records exist.

Do not pretend that the prototype contains a working large language model. The responses are simulated.

For unrelated messages, Bob Bot should politely explain that this prototype currently supports a limited set of demonstration scenarios.

## 10. Visual design

Keep the interface minimal and realistic.

- White or light-grey background.
- Clear distinction between user and Bob Bot messages.
- Rounded message bubbles.
- Subtle blue accent colour.
- Source cards integrated into the conversation.
- Small, unobtrusive label: **Offline design prototype — simulated responses**
- Simple clickable clarification buttons.
- No dashboard, complex navigation or unnecessary pages.

The chatbot must open with a completely blank conversation and a question input, so the interaction can be demonstrated naturally from the beginning.

## 11. What this prototype should demonstrate

The website should visibly demonstrate these design principles:

- The agent does not automatically assume missing user preferences.
- Users can explicitly select and correct source preferences.
- Clarification happens when necessary.
- Source selection and publication dates are transparent.
- The system respects explicit requests while identifying potentially outdated information.
- The system acknowledges when its local dataset cannot support an answer.

Prioritise functional interaction and faithful simulation of these three scenarios over adding unrelated features.