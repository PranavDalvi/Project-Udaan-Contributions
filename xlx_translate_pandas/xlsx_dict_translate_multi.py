'''
Multi Parallel translation of xlsx files using pandas
Author: Pranav Dalvi
'''
import pandas as pd
import re
import os
import glob
from nltk.tokenize import PunktSentenceTokenizer

def load_model_m2m_v2():
    print("Running m2m-v2")
    from IndicTrans2.inference.engine import Model
    global m2m_model
    m2m_model = Model(ckpt_dir='../../models_udaan_indic/m2m-v2', model_type="fairseq")

def load_model_en2indic_v2():
  print("Running en2indic-v2")
  from IndicTrans2.inference.engine import Model
  global en2indic_model
  en2indic_model = Model(ckpt_dir='../../models_udaan_indic/en-indic-v2', model_type="fairseq")

def translate_text(text, src_lang, trans_lang):
    print(f"Input: {text}")
    if text == "":
        print("Skipping Cell as no text found")
        return ""
    if src_lang == "eng_Latn":
        max_seq_len=256
        try: 
            translated_text = en2indic_model.translate_paragraph(text, src_lang, trans_lang)
        except:
            try:
                translated_tokens = []
                tokenizer = PunktSentenceTokenizer()
                tokens = tokenizer.tokenize(text)

                for token in tokens:
                    translated_token = en2indic_model.translate_paragraph(token, src_lang, trans_lang)
                    translated_tokens.append(translated_token)
                translated_text = ' '.join(translated_tokens)
            except:
                # split sentence on comma
                translated_text = ''
                translated_tokens = []
                tokens = re.split(r'[,]', text)
                tokens = [token.strip() for token in tokens if token.strip()]  # Remove empty strings and trim whitespace

                for token in tokens:
                    translated_token = en2indic_model.translate_paragraph(token, src_lang, trans_lang)
                    translated_tokens.append(translated_token)
                
                translated_text = ', '.join(translated_tokens)

    elif src_lang != "eng_Latn" and trans_lang != "eng_Latn":
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

def translate_excel(input_file, output_file, src_lang, trans_lang_list):
    # if src_lang == "eng_Latn":
    # load_model_en2indic_v2()
    # elif src_lang != "eng_Latn" and trans_lang != "eng_Latn":
    load_model_m2m_v2()
        
    df = pd.read_excel(input_file)

    for trans_lang in trans_lang_list:
        df[f'{trans_lang} Machine Translated'] = df['Meaning'].apply(lambda x: translate_text(x, src_lang, trans_lang) if pd.notnull(x) else '')

    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    input_directory = '/home/*.xlsx'
    src_lang = 'hin_Deva'
    trans_lang_list = ['kas_Arab', 'eng_Latn']  

    input_files = sorted(glob.glob(input_directory))
    for input_file in input_files:
        file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f'/home/{file_name_without_extension}_translated.xlsx'
        print(f"\nTranslating: {input_file}\n")
        translate_excel(input_file, output_file, src_lang, trans_lang_list)
    
