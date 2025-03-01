# -*- coding: utf-8 -*-
"""Simple_QnA_Bot_HF_Transformers_Gradio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-5PAyssk8neEKlh1ce6WXfnqwTzXH3aS

# **Simple QnA Bot using FLAN and Gradio**
In this assignment, you will build a rudimentary question answering bot using a pre-trained transformer along with Gradio, a library for building machine learning and data science demos and web applications.

## **Before we Begin - Using GPUs**
_Acc. to Wikipedia,_  
> A [graphics processing unit (GPU)](https://en.wikipedia.org/wiki/Graphics_processing_unit) is a specialized electronic circuit initially designed to accelerate computer graphics and image processing, but have later been used for non-graphic calculations involving embarrassingly parallel problems due to their parallel structure.  

Put simply, these are specialized hardware components that excel at performing an extremely large number of operations at once.<sup>*</sup>  
Their original application in graphic rendering largely involves them multiplying a large number of matrices with one another to figure out the colors that pixels on your screen should have, and as luck would have it<sup>**</sup>, this is exactly what we do when training and using neural networks.

Notes:
<details>
<summary>*</summary>
There are very significant conditions on the GPUs, the most crucial one being that all the operations its carrying out in parallel <b>must be the same</b>. It can add a billion pairs of numbers at once, and multiply a billion pairs at once, but it cannot do them both together. For more information, you can watch <a href="https://www.youtube.com/watch?v=xi-wTlVUZsQ"><b>this Youtube video</b></a>.
</details>
<details>
<summary>**</summary>
Its less luck, more that they both are heavily reliant on the same concepts of linear algebra.
</details>

### **Adding a GPU to your Colab instance**
Google Colab lets you use GPUs on your instance. To do this, you will need to change the runtime type of your Colab Notebook.

- First, find the arrow next to the **Connect/Session Info** button near the top-right, and click on it to reveal the drop-down. From the drop-down, click on **Change runtime type**.  
![](https://drive.google.com/uc?id=16azUrMW5dHnl81_yfRotwZ-Uk-9TAweE)

- In the **Change runtime type** dialog box, under **Hardware accelerator**, select **T4 GPU**. Then hit **Save**.  
![](https://drive.google.com/uc?id=1L7vVydEIBGPJg1i8Nd39IljgwEVcOXtK)

If you followed these steps correctly, then the **Connect/Session Info** button should have a T4 label next to them, and upon running the next cell you should see information related to the connected GPU.

#### **If you instead see** `/bin/bash: line 1: nvidia-smi: command not found`**, that would mean the instance does not have a GPU. Please ensure that your instance has a GPU before moving on.**
"""

!nvidia-smi

"""## **Install required libraries**
While Google Colab comes with many libraries pre-installed, we sometimes might need to use other libraries in our project.  
For this purpose, Google Colab provides a built-in shell command feature that allows you to run shell commands in a notebook cell. To run a shell command, you need to prefix it with an exclamation mark (!).  
We will use this feature to invoke `pip`, Python's default package installer, and install the necessary packages:
"""

! pip install -q transformers accelerate sentencepiece gradio

"""## **FLAN-T5-Large** (780M)


FLAN-T5 is a text-to-text LLM developed by Google Research. FLAN stands for “Fine-tuned LAnguage Net” T-5 stands for “Text-To-Text Transfer Transformer”. It is a comparitively light-weight model, with just 780 million parameters.

Here, a ***parameter*** refers to a trainable value in a model. Put simply, this means each and every value in the weight matrix of a fully connected layer, in the self-attention heads and so on will be considered a parameter. Thus a simple one layer neural network with an input layer or size $m$ and output layer of size $n$ will have $m\cdot n$ paramters.

While a parameter isn't a direct measure of a model's complexity or effeciency, it gives us an understanding of the size and resources that the model requires. Many well-known models like GPT-3, PaLM and LLaMA can sometimes have upwards of tens if not hunderds of **billions** of parameters, but these are too large for your standard Colab instance to handle.  

In this assignment, we'll be using Google's **FLAN-T5** as the LLM. At around 780M parameters, it is at a manageable size that your Colab instance should be able to run.
"""

from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large").to("cuda")

"""## **Using the Transformer**
There are 3 simple steps to getting the transfomer to generate a response:
1. Tokenize your input string
1. Pass your tokenized input to the model, with any other modifiers that the model might take (<u>ex.</u> the maximum length of the output)
1. Decode your output logits to get the generated output string
"""

def generate(input_text):
  input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")
  output = model.generate(input_ids, max_length=100)
  return tokenizer.decode(output[0], skip_special_tokens=True)

"""Let's test the model on some inputs:
#### Translation
"""

input_text = """translate English to French: How much do the tomatoes cost?"""
generate(input_text)

"""#### Simple Facts"""

input_text = """Please answer the following question.
What is the boiling point of water in °F?"""
generate(input_text)

"""#### Mathematical Reasoning"""

input_text = """
Answer the following question by reasoning step by step.
The cafeteria had 23 apples. If they used 20 for lunch and bougth 6 more, how many apples do they have?
"""
generate(input_text)

"""The above results are not coreect hence these mistakes have to be resolved further and a more robust system will be developed.

#### Logical Reasoning
"""

input_text = """
Q: Can Mozart have a conversation with Kanye West?
Give the rationale before answering
"""
generate(input_text)

input_text = """
"Premise: Alberto is the CTO of a top NLP company. Hypothesis: Alberto is a tech expert. Does the premise entail the hypothesis?"
"""

generate(input_text)

input_text = """
Q: Answer the following yes/no question by
reasoning step-by-step.
Can you write a whole Haiku in a single tweet?
A:"""
generate(input_text)

"""#### Custom Knowledge"""

input_text = """
Summarize the following text: The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.
"""
generate(input_text)

input_text = """
Generate a question for the following text: The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.
"""
generate(input_text)

"""The above prompt clearly states that the model is robust enough for reverse engineering the questions and hence denotes that information here is not localized as in flowing in a single direction

#### Sentiment Analysis
"""

input_text = """
Q: Which statement is sarcastic?
Options:
(A) Congratulations on finishing the assignment!
(B) Congratulations on finally releasing Week 4, why you should've taken another week to do it!
A: Let's think step by step.
"""
generate(input_text)

"""As you might have seen, while the model generates coherent replies, it is not really capable of more involved logical or emotional analysis. It makes up facts, and is confidently incorrect with mathematics.  
However, now understanding the general structure behind these models, you may have a new-found appreciation for even its simplest abilities.  

Let us now create a simple GUI to let us interact with this model more easily.

## **GUI with Gradio**
[**Gradio**](https://www.gradio.app/) is an open-source Python library that is used to build machine learning and data science demos and web applications.

With Gradio, you can quickly create a beautiful user interface around your machine learning models or data science workflow and let people "try it out" by dragging-and-dropping in their own images, pasting text, recording their own voice, and interacting with your demo, all through the browser.

Here, I have created a simple GUI for our text generation model using Gradio.

The [`Interface`](https://www.gradio.app/docs/interface) is a high-level component, that manages the creation and updation of the whole GUI.

It takes 3 mandatory parameters: a function that takes all the inputs from the UI (<u>ex.</u> a prompt, image) and returns a single output (a response) or a tuple of expected outputs; the inputs; and the outputs.  
It also has other optional arguments to add or change stuff to the UI (title, example inputs, themes, etc.).

For our use, all we require is a field for text input along with a place for our output. To achieve this, we use two [`Textbox`](https://www.gradio.app/docs/textbox) components, one for input and the other for the output.

We also set a custom title and include a few example prompts for people to get started with using the model.
"""

import gradio as gr

# Examples are a nested array, with each inner array contiaining all the values
# corresponing to each input field for the example. In our case, since we have
# only one input field, we may just use an array of strings instead

examples = [
  ["Answer the following question by detailing your reasoning: Are Pokemons alive?"],
  ["Q: Can Barack Obama have a conversation with George Washington? Give the rationale before answering."],
  ["Summarize the following text: Peter and Elizabeth took a taxi to attend the night party in the city. While in the party, Elizabeth collapsed and was rushed to the hospital. Since she was diagnosed with a brain injury, the doctor told Peter to stay besides her until she gets well. Therefore, Peter stayed with her at the hospital for 3 days without leaving."],
  ["Translate to German: I love eating flan!"],
  ["Generate a cooking recipe to make a cheesecacke:"],
  ["Premise:  At my age you will probably have learnt one lesson. Hypothesis:  It's not certain how many lessons you'll learn by your thirties. Does the premise entail the hypothesis?"],
  ["Answer the following question by reasoning step by step. The cafeteria had 23 apples. If they used 20 for lunch and bought 6 more, how many apples do they have?"]
]

title = "Response Generation Model - FLAN"

# The function that takes the text input and generates a text output
def process_input(text):
 return generate(text)

model_gui = gr.Interface(
  process_input,
  gr.Textbox(lines=3,label="Input"),
  gr.Textbox(lines=3, label="FLAN T5"),
  title=title,
  examples=examples
)
model_gui.launch()

"""## **Text Generation Demo with GPT-2**
You will now use the knowledge from the previous model demonstration to build a text generation demo using GPT-2, that takes an input sequence of words, and builds upon it.

$$
\text{The sky is}\rightarrow\text{The sky is the limit. Don't limit yourself.}
$$
"""

# <START>
#Set this to true only when you're ready to move on to this section
remove_model = True
# <END>
assert remove_model

del model         # Delete refernces to model
del tokenizer     # Delete references to tokenizer
model_gui.close() # Close model's server (note that the GUI will still be visible, but non-functional)

"""Instead of writing all the code required to harness the power of the transformer, we will instead use **pipelines**, abstractions that offer a simple API for many specific tasks such as Named Entity Recognition, sentiment analysis, image classification, and even text generation."""

from transformers import pipeline
# download & load GPT-2 model
text_generator = pipeline('text-generation', model='gpt2',device_map='auto')

"""The text generator pipeline takes a prompt as an input, and returns a list of dicts (corresponding to the value of `num_return_sequences`) that contain the generated text under the `generated_text` key.

```python
[
  {'generated_text': "The sky is the limit. Don't ..."},
  ...
]
```
Top-k sampling along with temperature has been implemented, and you can vary the values of these LLM hyper-parameters to see how it affects the generated output.
"""

import warnings
warnings.filterwarnings("ignore") # To supress sequential runs warnings that the text_generator issues

# <START>
top_k = 10
temperature = 0.9
max_length = 100

input = "To be honest, neural networks"
# <END>

sentences = text_generator(input, do_sample=True, top_k=top_k, temperature=temperature, max_length=max_length, num_return_sequences=3)

print("="*50)
for sentence in sentences:
  print(sentence['generated_text'])
  print("="*50)

"""###Important conclusions
Top-k sampling is a technique used to control the quality and diversity of the generated text by limiting the number of potential next tokens.

Temperature is a hyperparameter that controls the randomness of predictions by scaling the logits.

High k with high temperature: Maximizes diversity and creativity, potentially at the expense of coherence and relevance

Now, create a GUI for this text generation model. It should contain:

- Numerical input fields for `top_k` and `max_length`
- A slider from $0$ to $1$ for `temperature`
- A text input field for the prompt, and a text output field for the generated text (only generate the one text you plan to display)

The inference function should take all the input values, and return the generated text
"""

def generate_text(input_text, top_k, max_length, temperature):
    return text_generator(input_text, do_sample=True, top_k=top_k, temperature=temperature, max_length=max_length, num_return_sequences=1)[0]['generated_text']

# Gradio Interface
title = "Text Generative Pipeline Models"

with gr.Blocks() as text_gen_gui:
    with gr.Tab("Input and hyper-parameter tuning"):
        gr.Markdown("## Text Generative Pipeline Models")

        input_text = gr.Textbox(label="Input prompt")
        top_k = gr.Number(value=50, label="Top-k", precision=0,elem_id="top_k")
        max_length = gr.Number(value=100, label="Max Length", precision=0)
        temperature = gr.Slider(0.1, 1.0, value=0.7, step=0.01, label="Temperature (Relevance meter)")

        generate_button = gr.Button("Generate Text")
        output_text = gr.Textbox(label="Generated Text")

        generate_button.click(
            fn=generate_text,
            inputs=[input_text, top_k, max_length, temperature],
            outputs=output_text
        )
##Further we can add a button for viewing different outputs produced via changing the [0] in return statement can be done via adding another input.

text_gen_gui.launch()

remove_text_gen_gui = True
text_gen_gui.close() # Close model's server (note that the GUI will still be visible, but non-functional)

