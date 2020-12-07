import gc
gc.collect()

import streamlit as st
from transformers import pipeline, set_seed
from transformers.pipelines import TextGenerationPipeline

from google_trans_new import google_translator  
translator = google_translator()  

class TextGenerator:
    def __init__(self):
        self.generator: TextGenerationPipeline
        self.max_length = 300
        set_seed(1)

    def load_generator(self) -> None:
        self.generator = pipeline('text-generation', model='gpt2')

    def generate_text(self, starting_text: str) -> str:
        return self.generator(starting_text,
                              max_length=self.max_length,
                              num_return_sequences=1)[0]['generated_text']

@st.cache(allow_output_mutation=True)
def instantiate_generator():
    generator = TextGenerator()
    generator.load_generator()
    return generator

if __name__ == '__main__':
    st.title('GPT-2 em português, em teste')

    text_unlim = st.text_area("Escreva suas palavras ou frases abaixo e clique Ctrl + Enter")
    generator = translator.translate(text_unlim, lang_src= 'pt', lang_tgt='en') 
    generator = instantiate_generator()    
       
    if text_unlim:
        response = generator.generate_text(text_unlim)      
        result = translator.translate(response, lang_src= 'en', lang_tgt='pt') 
        st.markdown(f'Sua frase gpt-2: {result}')
       
    st.button("Clique para gerar nova frase")            
        

