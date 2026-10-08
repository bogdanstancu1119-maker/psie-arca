import gradio as gr
import os
def run_hydra_node():
    return 'Hydra Node Active: Synced with R2 and GitHub'
with gr.Blocks() as demo:
    gr.Markdown('# Hydra PSIE Node')
    btn = gr.Button('Synchronize')
    btn.click(fn=run_hydra_node, outputs=gr.Textbox())
demo.launch()