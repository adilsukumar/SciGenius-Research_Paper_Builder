import gradio as gr
from src.api import app as fastapi_app

# This file is specifically for deploying to Hugging Face Spaces (Gradio SDK) for free.
# Gradio is built on FastAPI. By mounting an empty Gradio block, Hugging Face 
# will run our FastAPI app on its powerful free tier without requiring Docker or a Credit Card.

with gr.Blocks() as gradio_ui:
    gr.Markdown("# SciGenius Backend is Running!")
    gr.Markdown("The API is accessible at `/api`. This UI is just a placeholder to keep the Hugging Face Space active.")

# Mount the dummy Gradio UI onto our real FastAPI app
app = gr.mount_gradio_app(fastapi_app, gradio_ui, path="/")
