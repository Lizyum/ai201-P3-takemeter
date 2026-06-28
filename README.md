# ai201-P3-takemeter

TakeMeter is a custom NLP classification system featuring a regularized, fine-tuned DistilBERT sequence classifier optimized for intent detection within the *Don't Starve Together* (DST) gaming community. The system parses dense, jargon-heavy community forum data and maps individual posts to a structured 4-dimensional taxonomy to differentiate actionable optimization, software system diagnostics, narrative storytelling, and low-substance community clutter.

---

## 📌 Project Taxonomy At-A-Glance

The system enforces a strict, single-label categorization boundary across the following distinct text classifications:

* **Technical:** Text explicitly targeting software stability, performance degradation, hardware inputs, or unintended mechanical game-engine bugs.
* **Strategy:** Actionable, educational content optimized for gameplay efficiency, including kiting parameters, mathematical recipes, and logical sequencing.
* **Experiential:** Relatable, narrative-driven player experiences, casual community commentary, and cooperative relationship dynamics void of optimization data.
* **Noise:** Low-substance text consisting of community memes, text-based sarcasm, hyper-expressive venting, or knee-jerk emotional rants.
---

## Hyperparameter Justification & Optimization Strategy

### 1. Epochs & Tracking the Sweet Spot
I set the training duration to **5 epochs** after watching how the model converged during my initial trial-and-error runs. My main cue was tracking the validation loss alongside accuracy; I looked for the exact inflection point where the validation loss flattened out and stopped dropping. I stopped at 5 epochs because it gave the model enough passes to adapt to the community's unique vernacular without running it so long that it began blindly memorizing the training samples.

### 2. Batch Size Reduction for Granular Learning
I chose to scale the batch size down from **16 to 10** to force more frequent weight updates per epoch. Because my dataset is small (~200 examples), a large batch size meant the model wasn't adjusting its parameters often enough to catch subtle context. Lowering the batch size gave the model more granular optimization steps, which was essential for parsing edge cases where identical keywords (like game-specific nouns such as *"Crockpot"*) appeared across entirely different categories, like strategy guides versus casual stories.

### 3. Balancing Learning Rate and Regularization (Weight Decay)
I pushed the learning rate up to **$3 \times 10^{-5}$** because the baseline model was too conservative and needed a stronger nudge to prioritize domain-specific patterns. However, I knew a faster learning rate on a small dataset risks creating hyper-confident, brittle decision boundaries. To balance this, I intentionally paired it with an elevated weight decay of **0.05**. This combination allowed the model to rapidly pick up on the *Don't Starve Together* slang while forcing its internal weights to stay lean, preventing it from becoming over-confident on niche training phrases so it could handle the unseen test set.

## Evaluation Report


## Error Analysis & Pattern Recognition

An evaluation of the 12 misclassified test instances revealed three consistent linguistic bottlenecks where the fine-tuned model struggled to separate vocabulary from context.

### 1. First-Person Narrative Dominance (Pronoun Biases)
* **The Problem:** The model over-indexed on first-person pronouns (*"I," "my," "we"*). 
* **Example Case:** When a user wrote, *"If Wanda has something in her hand... I tried holding a walking cane..."* (Error #1), the text was a literal, actionable software glitch report (**Technical**). However, because it was delivered via personal anecdote, the model incorrectly weighted the narrative structure over the technical context and predicted **Experiential**.

### 2. Keyword Sensitivity Over Context
* **The Problem:** Hard system terminology instantly overrode casual sentiment.
* **Example Case:** In Error #11, a player casually discussing how they prefer playing with friends was labeled **Technical** simply because the text included infrastructure buzzwords like *"public server"* and *"private server."* The model lacks the contextual depth to distinguish between *discussing* a server connection choice (Experiential) and *troubleshooting* one (Technical).

### 3. Emotion and Hyperbole Overlap
* **The Problem:** Expressive language or venting was continuously flattened into pure spam or clutter.
* **Example Case:** When players shared shocking timeline events (*"i was shocked lol i didnt expect a fat catcoon day 38 destroying n stealing my food"* — Error #4), the emotional intensity triggered a **Noise** classification. The model struggled to differentiate between active, destructive community toxicity (**Noise**) and high-energy, narrative game summaries (**Experiential**).

Example 1: If Wanda has something in her hand, she cannot interact with a Mysterious Dirt Pile on a hunt. I tried holding a walking cane and one of the new items. Neither would work, but if her hands were empty, it would be fine.

Analysis: This post was classified as experiential but the content is actually bringing up a technical issue. The character is not able to interact with game components as intended, so this is a Technical post.

Example 2: Spider and Beefalo items are the things that I have had to install mods to clear out in very long term lobbies. I cant think of any other item in the game thats "too abundant". Razors but I dont think that fits what you were asking

Analaysis: This is a singular tip that a user expresses through their personal experience handling a niche annoyance. The thoroughness does not meet expectations for Strategy posts so it should be classified as Experiential

Example 3: only 5 gunpowder, each knight has 900 hp, 1 gunpowder does 200 damage, 5 gp = 1k damage. ill try 4gp with 2 slurtle whatever to deal 900 damage precisely, hope it works. Im playing as WX78.

Analysis: this post was inaccurately labeled technical, probably due to the presence of numbers and mention of game compoenents but the sequence and lack of a clear problem make this a strategy to accomplish something rather than address unexpected behavior.

Overall, there may be some inconsistencies with annotations between experiential/technical/strategy as the intent of posts that make posts distinct is shrouded by social and sometimes technical jargon that can even throw off a human if they don't abide by the categorization defintion closely. A solution to this probelm is accumulating more examples of strategic comments that follow a linear progression of advice, more technical examples that clearly demonstrate the surfacing of unexpected behavior using simple language or numbers, and ruling out the rest as experiential as the model is already doing a good job recalling noise, which can be lumpeod iwth experiential as they serve the same purpose of contributing to social interaction and community engagement.

# TakeMeter Evaluation Report: Baseline vs. Fine-Tuned Model

This report details the performance transition from a zero-shot base model to a regularized fine-tuned sequence classifier optimized for the *Don't Starve Together* community.

---

## 📊 Performance Metrics

### 1. Overall Accuracy Summary
* 🎯 **Baseline Model Accuracy:** $56.67\%$ (Evaluated on 30 parseable test responses)
* 🎯 **Fine-Tuned Model Accuracy:** $60.00\%$ (Evaluated on 30 pristine test items)
* 📈 **Net Improvement:** $+3.33\%$ accuracy gain over the baseline configuration.

---

### 2. Comparative Per-Class Metrics

Below is a detailed comparison showcasing how the underlying predictive behavior shifted from the generic baseline model to the specialized domain model.

| Label Name | Baseline Precision | Baseline Recall | Baseline F1 | Fine-Tuned Precision | Fine-Tuned Recall | Fine-Tuned F1 | Test Support |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Technical & Anomalous** | $0.86$ | $0.75$ | $0.80$ | $0.67$ | $0.75$ | $0.71$ | 8 |
| **Experiential & Social** | $0.36$ | $0.57$ | $0.44$ | $0.40$ | $0.29$ | $0.33$ | 7 |
| **Strategy & Instructive**| $0.50$ | $0.62$ | $0.56$ | $0.62$ | $0.62$ | $0.62$ | 8 |
| **Hyperbole & Noise** | $1.00$ | $0.29$ | $0.44$ | $0.62$ | $0.71$ | $0.67$ | 7 |

* **Macro Averages (Fine-Tuned):**
  * Precision: $0.58$ | Recall: $0.59$ | F1-Score: $0.58$ (Refer to file `image_ea1c54.png`)
* **Macro Averages (Baseline):**
  * Precision: $0.68$ | Recall: $0.56$ | F1-Score: $0.56$ (Refer to file `image_ea1f04.png`)

---

### 3. Fine-Tuned Model Confusion Matrix (Text-Readable Format)

This text-based grid reflects the exact breakdown of the fine-tuned model's predictions on the 30-post test set (Visual reference available in file `image_ea1f23.png`). Rows indicate the true user intent; columns represent what the model predicted.

| True \ Predicted Label | Technical & Anomalous | Experiential & Social | Strategy & Instructive | Hyperbole & Noise |
| :--- | :---: | :---: | :---: | :---: |
| **Technical & Anomalous** | **6** | 0 | 2 | 0 |
| **Experiential & Social** | 3 | **2** | 1 | 1 |
| **Strategy & Instructive**| 0 | 2 | **5** | 1 |
| **Hyperbole & Noise** | 0 | 1 | 1 | **5** |

## 🧪 Baseline Model Methodology

### 1. Baseline Prompt Configuration
The baseline performance metrics were evaluated using a zero-shot prompting strategy on the base model. The system prompt explicitly defined the four target categories, established strict guardrails for mutual exclusivity, provided context-specific examples from the *Don't Starve Together* community, and enforced a rigid, single-word string output format.

```text
You are classifying posts from the Don't Starve Together (DST) gaming community for the TakeMeter project.
Assign each post to exactly one of the following categories based on its primary structural purpose and intent.

Technical: Posts focused explicitly on software stability, performance issues, or unintended mechanical exploits where the game engine behaves in a broken or unnatural way.
Example: "Every time I hammer down a burnt Jubilantern Post, my game instantly crashes to desktop on the new patch."

Experiential: Relatable, narrative-driven posts centered on personal player experiences, casual opinions, aesthetic preferences, or cooperative relationships, completely devoid of objective optimization data.
Example: "Me and my dad just started a world and we love basing near the Beefalo; it feels so cozy and safe even if it's a long trek for wood."

Strategy: Intent-driven, educational text aiming to optimize gameplay by providing accurate mechanics, recipes, kiting guides, or character breakdown statistics.
Example: "To kill Deerclops easily as a beginner, hit him 2 times with a Hambat, then immediately walk back to dodge his freeze AOE."

Noise: Low-substance text consisting of community memes, jokes, text-based sarcasm, or knee-jerk emotional rants that lack literal or actionable utility.
Example: "Omg this new Willow rework is complete trash, the devs literally hate their own players and ruined the game, uninstalled."

Respond with ONLY the exact label name from the list of valid labels below. Do not include quotes, punctuation, markdown formatting, or any explanation.

Valid labels:
Technical
Experiential
Strategy
Noise
```

---

## 🔍 Deep-Dive Error Analysis

A structural review of the misclassified test instances shows that the model is struggling heavily with the boundary separating **Technical**, **Strategy**, and **Experiential** posts whenever slang and specific in-game inventory terms collide.

### Example 1: Pronoun Bias Masking Software Bugs
* **The Post:** *"If Wanda has something in her hand, she cannot interact with a Mysterious Dirt Pile on a hunt. I tried holding a walking cane and one of the new items. Neither would work, but if her hands were empty, it would be fine."*
* **Labels:** True: `technical` | Predicted: `experiential` (Confidence: 0.41)
* **Why it Failed:** The data point describes an active game-breaking bug where a specific character cannot interact with a core mechanic. However, the author chose to deliver this via an anecdotal, first-person narrative framework (*"I tried holding..."*, *"her hands were empty"*). The fine-tuned model over-indexed on these casual narrative cues, entirely missing the core technical defect.

### Example 2: Niche Troubleshooting vs. Casual Sharing
* **The Post:** *"Spider and Beefalo items are the things that I have had to install mods to clear out in very long term lobbies. I cant think of any other item in the game thats "too abundant". Razors but I dont think that fits what you were asking"*
* **Labels:** True: `experiential` | Predicted: `technical` (Confidence: 0.48)
* **Why it Failed:** This post captures a player sharing a casual observation regarding server item abundance. Because the user includes strong technical system markers like *"install mods"* and *"long term lobbies,"* the model bypassed the relaxed, narrative structure of the sentence and immediately misclassified the post as a hardware/software report.

### Example 3: Arithmetic & Inventory Nouns Overriding Strategy Intent
* **The Post:** *"only 5 gunpowder, each knight has 900 hp, 1 gunpowder does 200 damage, 5 gp = 1k damage. ill try 4gp with 2 slurtle whatever to deal 900 damage precisely, hope it works. Im playing as WX78."*
* **Labels:** True: `strategy` | Predicted: `technical` (Confidence: 0.37)
* **Why it Failed:** This post relies heavily on mathematical variables, resource metrics (*"900 hp," "200 damage"*), and character codes (*"WX78"*). Because the model was fine-tuned to watch for dense, system-level metrics to isolate bugs, it falsely assumed this math was a technical software profile rather than what it actually is: a highly analytical sequencing strategy to minimize explosive waste.

---

## 🏁 Critical Takeaways & Strategic Future Adjustments

### 1. The Single-Label Taxonomy Constraint
The primary challenge in achieving perfect classification is not annotation quality, but rather the structural limitation of a single-label taxonomy. Real-world community discourse is natively multi-layered; a player will frequently log a valid software bug (`Technical`) while delivering it inside a casual, personal anecdote (`Experiential`). Because the current system forces a mutually exclusive choice, the model is forced to split the difference on posts that legitimately belong to multiple categories. The bottleneck lies in forcing a single-label constraint onto multi-intent human conversation.

### 2. Programmatic Fixes for a V2 System
To push past this classification ceiling, future iterations of TakeMeter require three concrete data revisions:
1.  **Linear Strategy Templates:** Accumulate a more diverse array of strategy examples that specifically follow a strict, linear progression of actionable instruction.
2.  **Simplified Technical Features:** Inject explicit examples of technical logs where the language isolating unexpected software behavior is simple and unclouded by narrative elements.
3.  **Label Condensation:** Given that the model successfully separated **Hyperbole & Noise** (jumping significantly to a $0.71$ F1-Score compared to baseline recall errors), we can structurally merge the *Noise* and *Experiential* categories. In a real-world moderation dashboard, both serve an identical purpose: fueling general social interaction and community engagement, rather than documenting code bugs or metadata optimization.

---

## 📋 Sample Classifications

Below are example posts processed through the final fine-tuned model, demonstrating its real-world inference behavior and prediction confidence.

| Post Content | Predicted Label | Confidence Score | Evaluation & Rationale |
| :--- | :---: | :---: | :--- |
| Wigfrid died for willow and willow avenged her. So touching 😓🥀 | `Noise` | `0.54` | **Correct Prediction:** This prediction is reasonable because the model successfully bypassed the game vocabulary and accurately flagged the expressive, hyperbolic emotional cues as community noise. |
| "He's probably clicking to attack, and then clicking next to the enemy and it makes him run. F to auto-shoot hostile mobs, Control-F to shoot the closest neutral mob. If you are using keys and not mouse clicks to fight, you shouldn't be 'running towards' anything. You can also upgrade Walter's slingshot so it has greater range. Not knowing how to use keybinds has been a big thing I've seen turn off new players. Just try kill a butterfly only using your mouse. not a fun time." | `Technical` | `0.44` | **Correct Prediction:** The model successfully identified this post as Technical, correctly recognizing that the text is clarifying expected software behavior to address a user's confusion about a systemic input failure. The low confidence score ($36\%$) accurately reflects how difficult this boundary is, as the model had to sift through heavy combat and strategy vocabulary to isolate the underlying focus on hardware keybinds. |
| "Either memorize a lot of recipes or use some combination of full hunger restoring foods - plenty of options for this but Meaty Stew+one other decent food(Like Meatballs) goes a decent way. You can also just power through it with high value individual foods if you have the resources, like just eating Meaty Stews until you're full, and then eating after the penalty has worn off. Set up an Automatic Volt Goat farm early - this can get you plenty of passive Volt Goat Horns early. You do need to go to the Lunar Isle to get an Anenemy to set one up, but it's not too difficult to manage and you can also pilfer the other resources while you're there(Stone Fruit makes for great and easy filler, along with Kelp, both of which you can get there). If you're unlucky with random seeds..." | `Strategy` | `0.8` | **Correct Prediction:** The model confidently caught this post ($80\%$ confidence) because it perfectly matches the true strategic intent, picking up on the highly explicit instructional steps, resource math, and specific progression advice (like setting up an "Automatic Volt Goat farm early"). |

---

## 🧠 High-Level Taxonomy Reflection: Intent vs. Boundary Reality

### What I Intended to Capture
My original objective with the TakeMeter taxonomy was to isolate clear intent boundaries within the community discourse: mapping raw data optimization to `Strategy`, infrastructure/bug anomalies to `Technical`, personal player narratives to `Experiential`, and low-value clutter to `Noise`.

### What the Model Actually Captured (The Decision Boundary Gap)
Instead of capturing the high-level semantic *intent* of a player's post, the model's internal decision boundaries ultimately overfitted to underlying structural styles and linguistic delivery:

* **Overfitting to Narrative Pronouns:** The model heavily overfitted to first-person framing (*"I," "my," "we"*). Rather than reading the core problem of a post, the presence of a narrative voice automatically pulled the model toward an `Experiential` classification, effectively blinding it to technical or strategic data delivered via a personal anecdote.
* **Overfitting to Systems Jargon:** The model overfitted to infrastructure keywords (*"servers," "mods," "lobbies"*). Even when a player was casually conversing about their setup, the model treated these phrases as high-priority features for a `Technical` classification.
* **What it Missed (Contextual Intent):** The model fundamentally missed the nuanced boundary where technical vocabulary intersects with strategy. Because it relies heavily on keyword token patterns rather than deep logical reasoning, it struggled to recognize that numerical resource calculations are instructional strategies rather than software scaling metrics.

---

## 📝 Specification Reflection

The process of drafting the initial project specification sheet was highly instrumental in guiding the system's design, though real-world data constraints forced minor adjustments during implementation.

* **How the Spec Guided Implementation:** Writing out the theoretical edge cases and boundary conditions in the specification sheet ahead of time forced me to pre-determine how to handle ambiguous community posts. This proactive scoping gave me a rigorous, standardized framework to lean on as I manually curated the dataset, ensuring a much higher level of data quality and consistency from the very beginning. It established clear project boundaries that directly anchored my hyperparameter and optimization choices.
* **How Implementation Diverged from the Spec:** While the specification sheet planned for discrete, mutually exclusive data classes, the actual dataset implementation revealed a far tighter linguistic overlap between `Strategy` and `Technical` categories than anticipated. In practice, I had to allow for more flexible boundary definitions—such as treating hardware keybind adjustments as technical profiling rather than strategic gameplay—to adapt to how the community actually communicates.

---

## 🤖 AI Usage Disclosure & Collaboration

All 200 dataset instances used to train TakeMeter were manually reviewed and annotated from scratch to guarantee ground-truth integrity. However, AI assistance was systematically leveraged during the scoping, stress-testing, and error-analysis phases of the project.

### Instance 1: Label Verification & Capability Stress-Testing
* **Directives Given:** I directed Gemini to evaluate a subset of data using my taxonomy definitions to test its baseline zero-shot classification performance. I also directed it to generate adversarial, synthetic boundary posts that intentionally blended categories.
* **Artifacts Produced:** The AI produced a set of predicted labels and a collection of highly ambiguous, complex mock posts designed to challenge the edge cases of the taxonomy definitions.
* **Modifications & Overrides:** I completely overrode the AI's labeling approach. The agent failed to accurately internalize and apply the strict label constraints to the nuances of *Don't Starve Together* slang. However, I used its failed attempts and synthetic boundary posts to drastically tighten my manual labeling guidelines, sharpening the mutual exclusivity between categories.

### Instance 2: Automated Error-Analysis & Pattern Recognition
* **Directives Given:** Following the evaluation of the final fine-tuned model, I provided the AI with the raw logs of the 12 misclassified test set instances and directed it to surface structural patterns among the errors.
* **Artifacts Produced:** The AI isolated three clear linguistic bottlenecks: a systemic bias toward first-person narrative pronouns, an over-activation on infrastructure keywords, and a tendency to mistake conversational hyperbole for toxic noise.
* **Modifications & Overrides:** I accepted the core patterns surfaced by the AI but heavily modified the technical framing to align with my project constraints. Instead of treating these patterns as unfixable flaws, I used them to formulate concrete programmatic solutions for a V2 system—specifically mapping out the data templates needed to clear up the boundaries between `Strategy` and `Technical` text.


## 🚀 Deployed Interface

TakeMeter includes a locally deployable, web-based interface built with **Gradio** that allows content moderators to classify Don't Starve Together forum posts using the fine-tuned model.

The application automatically downloads the latest version of the model from the project's public Hugging Face repository the first time it is launched. After the initial download, the model is cached locally for faster subsequent startups.

> **Note:** The fine-tuned model is hosted on Hugging Face Hub rather than in this repository because the model checkpoint exceeds GitHub's file size limits. The application downloads the model automatically when it is first run.

### How to Run the App Locally

1. **Set Up a Virtual Environment (Recommended)**
To prevent dependency conflicts with your global Python installation, initialize a clean virtual environment within the root of your project directory:

* **On macOS and Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

* **On Windows (PowerShell):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```



2. **Install Dependencies:** Cleanly install all required machine learning frameworks and interface dependencies using the repository's configuration file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Boot the Server**: Run the deployment script from the root of your local workspace directory:
    ```bash
    python app.py
    ```

4. **Access the App**: Open your web browser and navigate to the local link outputted in your terminal (typically http://127.0.0.1:7860).

### How the Application Works

1. Paste a Don't Starve Together forum post into the input text box.
2. The application tokenizes the text using the same tokenizer employed during model training.
3. The fine-tuned DistilBERT classifier predicts one of four categories:
   - **Technical**
   - **Experiential**
   - **Strategy**
   - **Noise**
4. The interface displays the predicted category along with the model's confidence score.

## 🤗 Model

The fine-tuned DistilBERT model used by TakeMeter is hosted on Hugging Face Hub and is downloaded automatically the first time the application is launched.

**Model Repository:** https://huggingface.co/lizyum/takemeter-model