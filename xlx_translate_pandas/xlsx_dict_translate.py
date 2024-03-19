'''
Parallel translation of xlsx files using pandas
Author: Pranav Dalvi
'''

import pandas as pd
import re
import os
import glob

def load_model_m2m_v2():
    print("Running m2m-v2")
    from IndicTrans2.inference.engine import Model
    global m2m_model
    m2m_model = Model(ckpt_dir='../../models_udaan_indic/m2m-v2', model_type="fairseq")


def translate_text(text, src_lang, trans_lang):
    print(f"Input: {text}")
    if not text.strip():
        return ''
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
    load_model_m2m_v2()
    df = pd.read_excel(input_file)

    df['Translated'] = df['Original'].apply(lambda x: translate_text(x, src_lang, trans_lang))

    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    input_directory = '/home/*.xlsx'
    src_lang = "san_Deva"
    trans_lang = "kan_Knda"

    input_files = glob.glob(input_directory)
    for input_file in input_files:
        file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f'/home/{file_name_without_extension}_{trans_lang}.xlsx'
        print(f"Translating: {input_file}")
        translate_excel(input_file, output_file, src_lang, trans_lang)
