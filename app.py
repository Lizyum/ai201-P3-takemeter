import gradio as gr
import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Point to your local model folder
MODEL_PATH = "./takemeter-model"

# Load local weights and tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
except Exception:
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# Your exact label mapping
ID_TO_LABEL = {0: "technical", 1: "experiential", 2: "strategy", 3: "noise"}


def classify_post(text):
    if not text.strip():
        return "Please enter a valid post.", "0.00%"

    # Tokenize input
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=512
    )

    # Compute prediction probabilities
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1).numpy()[0]

    pred_id = np.argmax(probs)
    return ID_TO_LABEL[pred_id].upper(), f"{probs[pred_id] * 100:.2f}%"


# Gradio Layout Configuration
demo = gr.Interface(
    fn=classify_post,
    inputs=gr.Textbox(
        lines=4, placeholder="Paste a Don't Starve Together forum post here..."
    ),
    outputs=[
        gr.Textbox(label="Predicted Category"),
        gr.Textbox(label="Confidence Level"),
    ],
    title="TakeMeter Classifier Engine",
    description="Enter text to see how the fine-tuned model categorizes the post's core intent.",
)

if __name__ == "__main__":
    demo.launch()