import pandas as pd
import ast
from googletrans import Translator

# Load the CSV file
input_file = './files/extracted_articles.csv'
df = pd.read_csv(input_file)

# Function to extract 'Content' from the structured string
def extract_content(content):
    try:
        data_list = ast.literal_eval(content)
        if isinstance(data_list, list):
            if all(isinstance(item, dict) for item in data_list):
                return [item.get('Content', '[No Content found]') for item in data_list]
            elif isinstance(data_list[0], list):
                flat_list = [entry for sublist in data_list for entry in sublist]
                return [item.get('Content', '[No Content found]') for item in flat_list if isinstance(item, dict)]
            else:
                return ["Invalid nested list structure."]
        else:
            return ["Non-list content structure."]
        
    except Exception as e:
        print(f"Error parsing content: {e}")
        return ["Parsing error."]

# Function to translate content with segmentation
def translate_content(content_list, target_language='en', max_length=5000):
    translator = Translator()
    translated_list = []
    
    for content in content_list:
        try:
            if content and isinstance(content, str):
                segments = [content[i:i+max_length] for i in range(0, len(content), max_length)]
                translated_segments = []
                for segment in segments:
                    translation = translator.translate(segment, dest=target_language)
                    translated_segments.append(translation.text)
                translated_list.append(" ".join(translated_segments))
            else:
                translated_list.append("[No content available for translation]")
        except Exception as e:
            print(f"Error translating content: {e}")
            translated_list.append("[Translation error]")
    
    return translated_list

# Apply the extraction function to the 'content' column
df['Extracted Content'] = df['content'].apply(extract_content)

# Write the extracted content to a text file
output_file = 'extracted_content.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for index, content_list in enumerate(df['Extracted Content'], start=1):
        f.write(f"Article {index}:\n")
        for item_index, content in enumerate(content_list, start=1):
            f.write(f"Content {item_index}:\n{content}\n")
        f.write('\n')

print(f"Extracted content written to {output_file}.")

# Translate content and write to a translated file
translated_file = 'translated_content.txt'
with open(translated_file, 'w', encoding='utf-8') as f:
    for index, content_list in enumerate(df['Extracted Content'], start=1):
        translated_contents = translate_content(content_list, target_language='en')
        f.write(f"Article {index} Translations:\n")
        for item_index, translated_content in enumerate(translated_contents, start=1):
            f.write(f"Translated Content {item_index}:\n{translated_content}\n")
        f.write('\n')

print(f"Translated content written to {translated_file}.")
