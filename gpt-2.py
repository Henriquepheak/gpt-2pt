import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from transformers import pipeline, set_seed
from transformers.pipelines import TextGenerationPipeline

from googletrans import Translator
translator = Translator()

class TextGenerator:
    def __init__(self):
        self.generator: TextGenerationPipeline
        self.max_length = 300
        set_seed(1)

    def load_generator(self) -> None:  
        self.generator = pipeline('text-generation', model='gpt2')
      
    def generate_text(self, text_unlim: str) -> str:
        return self.generator(text_unlim,
                              max_length=self.max_length,
                              num_return_sequences=1)[0]['generated_text']

@st.cache(allow_output_mutation=True)
def instantiate_generator():
    generator = TextGenerator()
    generator.load_generator()
    return generator

if __name__ == '__main__':
    st.title('GPT-2 em português')

    text_unlim = st.text_area("Escreva suas palavras ou frases abaixo", "Escreva aqui e clique Ctrl+Del")
    generator = translator.translate(text_unlim, src= 'pt',dest='en')							
    generator = instantiate_generator()

    if text_unlim:
        response = generator.generate_text(text_unlim)
        result = translator.translate(response, src= 'en',dest='pt')
        st.markdown(f'Completed phrase: {result}')

