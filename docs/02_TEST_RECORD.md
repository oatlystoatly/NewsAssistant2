
IMPORTANT
Requests such as 'all news' must be made unindependently, as it is simulated to have access to all internet articles, it would be undrealistic to show all news possible.


-------------------
Testing methodology
-------------------

The prototype is evaluated using scenario-based functional testing and simulated interaction walkthroughs.

Each test examines whether the developed system responds appropriately to a predefined user request or interaction sequence.

A controlled corpus of five fictional sources labeled 'sources' is used to ensure that the expected retrieval outcomes can be identified in advance.

Testing focuses on intent, clarification, source selection, recency filtering,transparency and unsupported-answer handling.

Each test records the user input, expected behaviour, observed behaviour, result and any identified limitations. Where changes are made following a failed test, the interaction is repeated to evaluate the revised implementation.

This evaluation assesses the functionality of the prototype rather than establishing its effectiveness with a wider population of users.


---------------------------

## T01 — Ambiguity
- Input: Give me updates on the Selly Oak bin strikes
- Expected: Requests source clarification rather than assuming a category.
- Observed: Bobot acsks what sort of updates I would like.
- Result: Correct

## T02 — Multiple categories
- Input: Select a, b
- Expected: Returns matching news and academic sources.
- Observed: It responds with the two selections available, BBC news and ITV news.
- Result: Correct

## T03 — All news
- Input: Show all news on Selly Oak bin strikes
- Expected: Returns BBC, ITV and CNN.
- Observed: "I cannot understand that request within this simulation. Please rephrase or choose a supported source option."
- Result: Incorrect

I then changed and improved this.

- Input: Give me all news on Selly Oak bin strikes
- Expected:  Returns BBC, ITV and CNN.
- Observed:  Returns BBC, ITV and CNN.
- Result: Correct

## T04 — Recent news
- Input: Show all recent news on Selly Oak BIn strikes
- Expected: Returns BBC and ITV; excludes CNN.
- Observed: Returns BBC and ITV, it excludes CNN
- Result: Correct

## T05 — Historical news
- Input: Show historical news
- Expected: Returns CNN only.
- Observed: Returns CNN only
- Result: Correct

## T06 — All sources
- Input: Show all sources
- Expected: Returns all five records.
- Observed: Returns all sources
- Result: Correct

## T07 — Recent sources
- Input: Show all recent sources
- Expected: Returns all records except CNN.
- Observed: Returns all records except CNN.
- Result: Correct

## T08 — Transparency
- Input: Why did you include the outdated article?
- Expected: Explains inclusion of CNN after it is opened.
- Observed: Explains the reasoning, see the screenshot.
- Result: Correct

## T09 — Correction
- Input: exclude outdated
- Expected: Revises results and removes CNN.
- Observed: Removes CNN
- Result: Correct

## T10 — Contextual memory
- Input: Initial report request → Show all recent news
- Expected: Retains the topic and report purpose.
- Observed: Correct, see above tests.
- Result: Correct

## T11 — Unacademic warning
- Input: Initial report request → Select c → Open TikTok
- Expected: Displays a source suitability warning.
- Observed: Displays the source with the suitability warning
- Result: Correct

## T12 — Warning relevance
- Input: Request without academic purpose → Open TikTok
- Expected: Displays TikTok without the academic-specific warning.
- Observed: Displays Tiktok without the warning.
- Result: Correct

## T13 — Historical preferences
- Input: New ambiguous request → use previous
- Expected: Reuses source categories only after confirmation.
- Observed: Only works for 'use previous' not 'previous'
- Result: Correct

## T14 — Unsupported request
- Input: How many members are there in Black Sabbath?
- Expected: Recognises the topic but declines to provide an unsupported answer.
- Observed: Says it is not supported in the information it has
- Result: Correcy

## T15 — Unrecognised request
- Input: Tell me about quantum physics
- Expected: Explains that the request is not understood within the simulation.
- Observed: Explains that the request is not understood within the simulation.
- Result: Correct

## T16 — Reset
- Input: reset
- Expected: Clears active context and previous preferences.
- Observed: Active context and history is cleared
- Result: Correct

## T17 — Interface and session
- Input: Send several messages through Streamlit
- Expected: Messages remain visible and active context survives normal app reruns.
- Observed: All screenshots
- Result: Correct