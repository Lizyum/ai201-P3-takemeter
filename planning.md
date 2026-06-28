# planning.md

## Community: Don't Starve Together
I have chosen the **Don't Starve Together (DST)** gaming community. DST is an excellent fit for a text classification task because its brutal survival mechanics and steep learning curve split the player base into wildly distinct behavioral archetypes. 

Discourse ranges from beginners desperately seeking basic survival mechanics to hardcore veterans min-maxing daily resource yields, running parallel to a highly emotional community layer that reacts to character reworks with sarcasm, hyperbole, or toxicity. The core challenge of this classifier is separating objective, actionable signal (bugs and high-level strategy) from subjective, conversational noise (personal anecdotes and knee-jerk rants), which requires parsing deep community slang and context that a generic base model will naturally struggle with.

---

## Labels

### 1. Technical & Anomalous
* **Definition:** Posts focused explicitly on software stability, performance issues, or unintended mechanical exploits where the game engine behaves in a broken or unnatural way.
* **Priority Rule:** If a post outlines a gameplay guide or optimization tactic but relies entirely on manipulating system glitches, pathing freezes, or broken collision spaces (marked by keywords like *"hit box"*, *"infinitely farm"*, *"exploit"*), it must be classified here rather than under Strategy.
* **Example 1:** *"Every time I hammer down a burnt Jubilantern Post, my game instantly crashes to desktop on the new patch."*
* **Example 2:** *"If you drop a lureplant exactly on this biome tile boundary, its pathing breaks and it won't spawn eyeplants, completely disabling the hound wave."*

### 2. Experiential & Social
* **Definition:** Relatable, narrative-driven posts centered on personal player experiences, casual opinions, aesthetic preferences, or cooperative relationships, completely devoid of objective optimization data.
* **Priority Rule:** If a post contains structural fluff, personal observation, or a narrative recounting of an event (e.g., *"my friend ran in circles"*), it belongs here—even if the user accidentally mentions a correct kiting pattern or encounters an engine bug during their story. The overarching presence of conversational fluff overrides any secondary strategic or technical value.
* **Example 1:** *"Me and my dad just started a world and we love basing near the Beefalo; it feels so cozy and safe even if it's a long trek for wood."*
* **Example 2:** *"I honestly just love playing Wendy because Abigail keeps me company and clears out spider nests while I pick flowers."*

### 3. Strategy, Analytical & Instructive
* **Definition:** Intent-driven, educational text aiming to optimize gameplay by providing accurate mechanics, recipes, kiting guides, or character breakdown statistics.
* **Priority Rule (Sarcasm Tie-Breaker):** Genuine strategy must maintain an earnest, objective instructional intent, typically supported by exact numbers, recipes, or logical sequencing without emotional framing. If a post provides complex instructions but relies on highly informal slang frameworks (e.g., starting with *"Bro..."*, ending with *"Trust me"*), features blatant tonal contradictions, or advocates for a universally known low-tier constraint (e.g., unarmored Wes runs) without a highly data-backed justification, it drops into Hyperbole & Noise.
* **Example 1:** *"To kill Deerclops easily as a beginner, hit him 2 times with a Hambat, then immediately walk back to dodge his freeze AOE."*
* **Example 2:** *"You get up to 4 random item drops per week just by being active on a server; the first drop happens at 15 minutes, the second at 2 hours. Source: Klei Forums."*

### 4. Hyperbole & Noise
* **Definition:** Low-substance text consisting of community memes, jokes, text-based sarcasm, or knee-jerk emotional rants that lack literal or actionable utility.
* **Priority Rule:** If a post uses highly exaggerated idioms (e.g., *"vanished into thin air"*, *"fundamentally broken"*, *"literal garbage"*), it is immediately classified here. This holds true even if the user frames their frustration as a software error (user error masquerading as a bug) or dresses their joke up to look like structural strategy.
* **Example 1:** *"Omg this new Willow rework is complete trash, the devs literally hate their own players and ruined the game, uninstalled."*
* **Example 2:** *"Me watching the Dragonfly burn down our entire base on day 20 🤡💀"*

---

## Example Edge Cases

### Edge Case 1: Sarcastic/Hyperbolic Strategy ("The Expert Facade")
* **The Ambiguity:** A post uses highly specific game terms and mechanics (e.g., *"Just fight Dragonfly without armor on Day 2, it's totally fine"*), making it structurally look like **Strategy**, but the intent is purely sarcastic/destructive (**Noise**).
* **Handling Strategy:** I will enforce a strict annotation rule based on *literal correctness and structural data*. True **Strategy** must contain an objective instructional intent, often marked by numerical steps, recipes, or logical sequencing. If a post lacks actionable accuracy and uses emotionally extreme modifiers, it will be classified as **Noise**.

### Edge Case 2: Personal Complaining vs. Software Failure
* **The Ambiguity:** A player complaining about a mechanic being unfair or frustrating (e.g., *"Hounds spawning on day 6 is completely broken and unplayable"*). This blends the frustration of **Noise** with the topic of game stability.
* **Handling Strategy:** I will classify this based on *systemic intent*. If the text describes a deviation from intended software behavior (a literal glitch, crash, or sequence break), it is annotated as **Technical & Anomalous**. If it describes intended game design that the player simply dislikes or finds too hard, it will be annotated as **Experiential & Social** (if conversational) or **Noise** (if highly hyperbolic/toxic).

---

### Applied Labeling Decisions (Milestone 3 Edge Cases)

To test these boundaries, I encountered three specific data points during the dataset review that proved exceptionally difficult to classify. Below is the documentation of my final decisions for each:

#### 1. The "Nuclear Bomb Mod" Suggestion
* **The Post:** *"Can somebody PLEASE make a high quality nuclear bomb modpack, with a nuclear bomb, a whole screen light up thingy, a countdown, bunkers, and like aftereffects like terrain turning into goo or something, and slime monsters and radiation and stuff... PLEASE make a nuke mod that's actually good quality..."*
* **The Difficulty:** On the surface, this reads like a genuine modding suggestion, which a standard classifier might loop into *Technical* or *Strategy* because it discusses game additions. However, *Don't Starve Together* is a gothic, wilderness survival sandbox; dropping a nuclear weapon into the mechanics is completely exaggerated, structurally non-serious, and knee-jerk. 
* **My Decision:** **Hyperbole & Noise**. Because the suggestion lacks literal or actionable utility for core gameplay and relies on highly dramatic formatting ("PLEASE"), it fits the pattern-match for community noise rather than structural strategy.

#### 2. Settings Modification vs. Optimization Guide
* **The Post:** *"Automatic health adjust can scale the game for single player for boss hp. Too many items plus gives you 1 hit kill commands if you just want to skip it."*
* **The Difficulty:** This post straddles the line between *Strategy* and *Technical*. It mentions specific ways to handle boss HP, which looks like an instructive strategy guide at first glance. 
* **My Decision:** **Technical & Anomalous**. I classified this as technical because the user isn't explaining an in-game combat strategy or kiting pattern. Instead, they are describing how to change a server setting and utilize backend developer commands to alter how the software scales. It is an instruction on system configuration rather than gameplay optimization.

#### 3. Item Component Bragging
* **The Post:** *"I on my new world have like 3 walking cane, 5 tam'o'shaders and 6 pan flutes all from gifts"*
* **The Difficulty:** This data point contains heavy strategic keywords—listing top-tier items like walking canes, Tam o' Shanters, and pan flutes alongside exact numerical counts. A basic keyword match would immediately yank this into *Strategy*.
* **My Decision:** **Experiential & Social**. Looking past the specific item names, the true intent of the player is to share a personal narrative about their luck with the game's daily skin/gift drop system. There is no instructional sequencing or analytical advice being offered; it is a purely relatable, narrative-driven observation of their world state.

---

## Data Collection Sources

### Sourcing Strategy
I will collect data across three distinct, targeted platforms to naturally capture our label archetypes:
1. **Official Klei DST Bug Tracker:** Primary source for the **Technical & Anomalous** label.
2. **Steam Game Discussion Board & Reviews:** Primary source for **Experiential & Social** (general discussion), and **Strategy, Analytical, & Instructive** commentary.
3. **r/dontstarvetogether Subreddits:** Primary source for **Hyperbole & Noise** (filtering by helpful negative reviews) and **Strategy, Analytical & Instructive** (filtering by flairs like `Guide`, `Tip`, or searching advanced terms like `Crockpot efficiency`).

### Target Metrics & Underrepresentation Mitigation
* **Target Volume:** 40–50 examples per label, aiming for a highly balanced baseline dataset of **160–200 total hand-annotated rows**. 
* **Mitigation Plan:** If a specific label is underrepresented after evaluating the first 200 raw posts collected, I will pivot from random sampling to **targeted keyword indexing**. For example, if *Technical* is lacking, I will explicitly query the forums for terms like `"crash"`, `"glitch"`, `"unhandled exception"`, or `"exploit"`. If *Strategy* is lacking, I will target specific item/boss data terms like `"frame data"`, `"recipe"`, or `"HP breakdown"` to boost that label's numbers before training.

---

## Evaluation Metrics

### Beyond Base Accuracy
While overall accuracy tells us how the model performs macroscopically, it is insufficient because a model can mask severe blind spots by over-performing on an easy label (like *Noise* or *Experiential*) while completely failing on a nuanced one (like *Technical* vs *Strategy*). To combat this, I will evaluate the following:

* **Per-Class Precision:** Out of all posts the model *claims* are Strategy, how many actually are? This ensures the tool doesn't dilute useful insights with casual chatter.
* **Per-Class Recall:** Out of all actual Technical bugs posted, how many did the model successfully catch? This is crucial if a developer wants to ensure no real bug reports are dropped.
* **Confusion Matrix Analysis:** I will specifically map the misclassifications between *Strategy* and *Noise* to evaluate if the fine-tuning successfully taught the model to detect sarcasm/hyperbole over raw keyword counting.

### Definition of Success
A **90% per-class accuracy across all four categories** will serve as the baseline threshold for production deployment. This means the model can confidently separate community noise from actionable development insights, rendering it a genuinely useful tool for community managers and QA teams.


## AI Tool Plan

### 1. Label Stress-Testing
To validate and refine my taxonomy boundaries before starting manual annotation, I will use an LLM to stress-test my definitions.
* **Prompt Strategy:** I will provide the AI with my current definitions for **Strategy** vs. **Noise** and **Technical** vs. **Experiential**, then instruct it to generate 5–10 highly ambiguous boundary posts (e.g., highly technical sarcasm or subjective complaints about intended balancing).
* **Refinement Process:** If the AI generates posts that cannot be cleanly categorized using my existing rules, I will immediately update the handling strategies in my `planning.md` edge cases prior to beginning data collection.

### 2. Annotation Assistance
I will utilize an LLM to pre-label the collected dataset.
* **Tool & Model Selection:** : Gemini 3.5 Flash via Web Interface
* **Verification & Disclosure Tracking:** To maintain strict data integrity and comply with AI disclosure requirements, I will structure my raw dataset with a dedicated `label` column. Every single automated label will be manually reviewed, verified, and corrected by me.

### 3. Failure Analysis
Post-evaluation, I will use an AI tool to perform an audit on the model's errors to discover blind spots that aggregate macro metrics might hide.
* **Analytical Workflow:** I will compile all misclassified instances from the test set into a structured prompt containing the `True Label`, `Predicted Label`, and the `Post Text`. I will task the AI with identifying linguistic, structural, or keyword-based patterns causing the confusion (e.g., determining if the model is over-indexing on character names like *Willow* or *Maxwell*).
* **Human Verification:** I will verify the AI-generated error patterns by manually cross-referencing them against my confusion matrix and calculating the exact error frequencies for the flagged keywords or structural patterns to confirm they are statistically significant.

## Baseline Metrics Evaluation

### Reflection on Zero-Shot Performance

When I looked at the initial baseline metrics, two clear failure modes stood out immediately: the model struggled heavily with low precision on Experiential posts and poor recall on Noise posts. 

I noticed that the zero-shot model has a strong native bias toward pronouns and social cues. The moment a post contained personal anecdotes like *"me and my dad"* or casual phrases like *"we started a world,"* the model defaulted to labeling it as *Experiential*. It completely missed the bigger picture—even when the actual core intent of the post was to lay out an objective *Strategy* guide. It essentially treated the Experiential category as a generic dumping ground for any conversational text.

The *Noise* category revealed the exact opposite problem. While the model had $100\%$ precision—meaning it was never wrong when it actually chose to label something as Noise—it allowed a massive $71\%$ of actual noise posts to slip right past it. Looking closer at the data, the baseline model was incredibly rigid; it seemed to require glaring, unmistakable formatting clues like heavy emoji usage (`🤡💀`) or extreme keywords like *"uninstalled"* to flag a post as noise. Because it lacked community context, it was completely blind to text-based community sarcasm, rants, and subtle doomposting, often misclassifying them into other categories.

---





