'''
Parallel translation of xlsx files using pandas (test file)
Author: Pranav Dalvi
'''

import pandas as pd
import re

def load_model_m2m_v2():
    print("Running m2m-v2")
    from IndicTrans2.inference.engine import Model
    global m2m_model
    m2m_model = Model(ckpt_dir='../../models_udaan_indic/m2m-v2', model_type="fairseq")


def translate_text(text, src_lang, trans_lang):
    try:
        translated_text = m2m_model.translate_paragraph(text, src_lang, trans_lang)
    except Exception as e:
        # If translation fails, try translating individual tokens
        print(f"Error translating text: {e}")
        translated_text = ''
        tokens = re.split(r'[,]', text)
        tokens = [token.strip() for token in tokens if token.strip()]  # Remove empty strings and trim whitespace
        translated_tokens = []

        for token in tokens:
            try:
                translated_token = m2m_model.translate_paragraph(token, src_lang, trans_lang)
                translated_tokens.append(translated_token)
            except Exception as e:
                print(f"Error translating token '{token}': {e}")
                translated_tokens.append('')  # Handle translation failure for individual tokens

        translated_text = ', '.join(translated_tokens)

    return translated_text

def translate_excel(input_file, output_file, src_lang, trans_lang):
    df = pd.read_excel(input_file)

    # Assuming text data is in column 'A'
    df['Translated'] = df['Original'].apply(lambda x: translate_text(x, src_lang, trans_lang))

    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    input_file = 'input.xlsx'
    output_file = 'output.xlsx'
    src_lang = 'en'  
    trans_lang = 'hi' 
    translation_function = en2indic_bob_model.translate_paragraph  # Replace with your translation function

    translate_excel(input_file, output_file, src_lang, trans_lang, translation_function)
