import csv
import os
import ast
import pandas as pd
from googletrans import Translator
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL for image handling
import threading
import sys
from scrapers import (
    webscrape1,
    webscrape2,
    webscrape3,
    webscrape4,
    webscrape5,
    webscrape6,
    webscrape7,
    webscrape8,
    webscrape9,
)

# Function to write scraped content to CSV
def save_to_csv(data, file_name='./files/extracted_articles.csv'):
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)  # Create the directory if it doesn't exist
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["content"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving to CSV: {e}")

# Main scraping function
def main(url, start_date, end_date):
    print(f"Starting scraping process for URL: {url}")
    content = []

    try:
        # Define eligible URLs for each scraper
        if url in [
            "https://agencia.petrobras.com.br/sustentabilidade",
            "https://agencia.petrobras.com.br/institucional"
        ]:
            print("Using webscrape1 for scraping...")
            # Loop through the URLs for webscrape1
            urls = [
                "https://agencia.petrobras.com.br/sustentabilidade",
                "https://agencia.petrobras.com.br/institucional",
                
            ]
            for url in urls:
                response = webscrape1.scrape_url_web1(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://eneva.com.br/sala-de-imprensa/noticias/?cat=83",
            "https://eneva.com.br/sala-de-imprensa/noticias/?cat=59",
            "https://eneva.com.br/sala-de-imprensa/noticias/?cat=58",
            "https://eneva.com.br/sala-de-imprensa/noticias/?cat=60",
            "https://eneva.com.br/sala-de-imprensa/noticias/?cat=57"
        ]:
            print("Using webscrape2 for scraping...")
            # Loop through the URLs for webscrape2
            urls = [
                "https://eneva.com.br/sala-de-imprensa/noticias/?cat=83",
                "https://eneva.com.br/sala-de-imprensa/noticias/?cat=59",
                "https://eneva.com.br/sala-de-imprensa/noticias/?cat=58",
                "https://eneva.com.br/sala-de-imprensa/noticias/?cat=60",
                "https://eneva.com.br/sala-de-imprensa/noticias/?cat=57"
            ]
            for url in urls:
                response = webscrape2.scrape_url_web2(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://totalenergies.com.br/blog"
        ]:
            print("Using webscrape3 for scraping...")
            # Loop through the URLs for webscrape3
            urls = [
                "https://totalenergies.com.br/blog"
            ]
            for url in urls:
                response = webscrape3.scrape_url_web3(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://english.elpais.com/usa/",
            "https://english.elpais.com/international/",
            "https://english.elpais.com/economy-and-business/",
            "https://english.elpais.com/science-tech/",
            "https://english.elpais.com/health/",
            "https://english.elpais.com/technology/",
            "https://english.elpais.com/climate/",
            "https://english.elpais.com/people/",
            "https://english.elpais.com/lifestyle/",
            "https://english.elpais.com/opinion/",
            "https://english.elpais.com/sports/"
        ]:
            print("Using webscrape4 for scraping...")
            # Loop through the URLs for webscrape4
            urls = [
                "https://english.elpais.com/usa/",
                "https://english.elpais.com/international/",
                
            ]
            for url in urls:
                response = webscrape4.scrape_url_web4(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://infomercado.pe/ultimas-noticias/",
            "https://infomercado.pe/actualidad/",
            "https://infomercado.pe/negocios/emprendimientos/",
            "https://infomercado.pe/negocios/",
            "https://infomercado.pe/tendencias/",
            "https://infomercado.pe/utilidades/"
        ]:
            print("Using webscrape5 for scraping...")
            # Loop through the URLs for webscrape5
            urls = [
                "https://infomercado.pe/ultimas-noticias/",
                "https://infomercado.pe/actualidad/",
              
            ]
            for url in urls:
                response = webscrape5.scrape_url_web5(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://www.lapatria.com/manizales",
            "https://www.lapatria.com/caldas",
            "https://www.lapatria.com/eje-cafetero",
            "https://www.lapatria.com/sucesos",
            "https://www.lapatria.com/deportes",
            "https://www.lapatria.com/opinion",
            "https://www.lapatria.com/denuncie",
            "https://www.lapatria.com/economia",
            "https://www.lapatria.com/politica",
            "https://www.lapatria.com/entretenimiento",
            "https://www.lapatria.com/cultura",
            "https://www.lapatria.com/ciencias",
            "https://www.lapatria.com/tecnologia",
            "https://www.lapatria.com/educacion",
            "https://www.lapatria.com/salud",
            "https://www.lapatria.com/medioambiente",
            "https://www.lapatria.com/nacional",
            "https://www.lapatria.com/internacional",
            "https://www.lapatria.com/social",
            "https://www.lapatria.com/publirreportaje"
        ]:
            print("Using webscrape6 for scraping...")
            # Loop through the URLs for webscrape6
            urls = [
                "https://www.lapatria.com/manizales",
                "https://www.lapatria.com/caldas",
               
            ]
            for url in urls:
                response = webscrape6.scrape_url_web6(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://www.mch.cl/categoria/negocios-industria/comunidades/",
            "https://www.mch.cl/categoria/negocios-industria/inversiones/"
        ]:
            print("Using webscrape8 for scraping...")
            # Loop through the URLs for webscrape8
            urls = [
                "https://www.mch.cl/categoria/negocios-industria/comunidades/",
                "https://www.mch.cl/categoria/negocios-industria/inversiones/"
            ]
            for url in urls:
                response = webscrape8.scrape_url_web8(url, start_date, end_date)
                content.append(response)

        elif url in [
            "https://unitel.bo/",
            "https://unitel.bo/noticias/seguridad",
           
        ]:
            print("Using webscrape9 for scraping...")
            # Loop through the URLs for webscrape9
            urls = [
                "https://unitel.bo/",
                "https://unitel.bo/noticias/seguridad",
                "https://unitel.bo/noticias/salud",
           
            ]
            for url in urls:
                response = webscrape9.scrape_url_web9(url, start_date, end_date)
                content.append(response)

        else:
            messagebox.showerror("Error", "No eligible scraper found for the provided URL.")
            return

    except Exception as e:
        messagebox.showerror("Error", f"Error during scraping: {e}")
        return

    if content:
        print("Scraping complete. Content fetched:")
        print(content)

        # Prepare data to save
        data = {"content": content}
        save_to_csv(data)
    else:
        messagebox.showerror("Error", "No content found.")


# Function to extract content from structured string
def extract_content(content):
    try:
        # Attempt to parse the content as a Python literal structure
        data_list = ast.literal_eval(content)
        
        # Check the structure and extract 'Content' appropriately
        if isinstance(data_list, list):
            if all(isinstance(item, dict) for item in data_list):
                # Simple list of dictionaries
                return [item.get('Content', '[No Content]') for item in data_list]
            elif isinstance(data_list[0], list):
                # List of lists with dictionaries inside
                flat_list = [entry for sublist in data_list for entry in sublist]
                return [item.get('Content', '[No Content]') for item in flat_list if isinstance(item, dict)]
        else:
            print("Parsed content is not in expected list format.")
            return ["[Non-list content structure]"]
        
    except Exception as e:
        print(f"Error parsing content: {e}")
        return ["[Parsing error]"]

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

# Function to extract and translate content
def extract_and_translate(output_file, translated_file, language_choice):
    try:
        # Load the CSV file
        df = pd.read_csv('./files/extracted_articles.csv')
        # Apply the updated extraction function
        df['Extracted Content'] = df['content'].apply(extract_content)

        # Write the extracted content to a text file
        with open(output_file, 'w', encoding='utf-8') as f:
            for index, content_list in enumerate(df['Extracted Content'], start=1):
                f.write(f"All Contents Founded in Date range:\n")  # Label each article
                for item_index, content in enumerate(content_list, start=1):
                    f.write(f"Article ({item_index}) Content:\n{content}\n")
                f.write('\n')

        print(f"Extracted content written to {output_file}.")

        # Translate the content and write to a translated file
        with open(translated_file, 'w', encoding='utf-8') as f:
            for index, content_list in enumerate(df['Extracted Content'], start=1):
                f.write(f"Article {index} Translations:\n")  # Label each article
                translated_contents = translate_content(content_list, language_choice)
                for item_index, translated_content in enumerate(translated_contents, start=1):
                    f.write(f"Translated Content {item_index}:\n{translated_content}\n")
                f.write('\n')

        print(f"Translated content written to {translated_file}.")

    except Exception as e:
        print(f"Error processing content: {e}")

# Function to run scraping and translation based on user input
def run_scraping():
    # Check and delete existing files before starting a new run
    if os.path.exists('./files/extracted_articles.csv'):
        os.remove('./files/extracted_articles.csv')
    if os.path.exists('./files/extracted_content.txt'):
        os.remove('./files/extracted_content.txt')
    if os.path.exists('./files/translated_content.txt'):
        os.remove('./files/translated_content.txt')

    # Get input from the user
    user_url = url_entry.get().strip()
    if not user_url:
        messagebox.showerror("Error", "No URL provided!")
        return

    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()
    language_choice = language_entry.get().strip().lower()

    if language_choice not in ['en', 'pt', 'es']:
        messagebox.showerror("Error", "Invalid language choice. Please enter 'en', 'pt', or 'es'.")
        return

    # Disable the button to prevent multiple clicks
    run_button.config(state=tk.DISABLED)

    # Show loading
    loading_label.pack()
    root.update_idletasks()  # Update the UI to show loading label

    # Start a new thread for scraping to keep the GUI responsive
    threading.Thread(target=scrape_and_translate, args=(user_url, start_date, end_date, language_choice)).start()

def scrape_and_translate(user_url, start_date, end_date, language_choice):
    main(user_url, start_date, end_date)

    # File paths for content processing
    output_file = './files/extracted_content.txt'
    translated_file = translated_file_entry.get().strip()  # Use user input for translated file

    # Extract and translate content
    extract_and_translate(output_file, translated_file, language_choice)

    loading_label.pack_forget()  # Hide loading
    run_button.config(state=tk.NORMAL)  # Re-enable the button

    messagebox.showinfo("Success", "Scraping and translation completed!")
    
#     # Option to restart
#     if messagebox.askyesno("Continue", "Do you want to Scrape More?"):
#         restart_application()

# def restart_application():
#     global root
#     root.quit()
#     os.execl(sys.executable, sys.executable, *sys.argv)

# Create the Tkinter GUI
# Create the Tkinter GUI
root = tk.Tk()
root.title("Article Scraper With Translations")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

# Load background image
background_image = Image.open(r"C:\bot\art-scrap\main\imagess\2.jpg")  # Adjust path as necessary
background_image = background_image.resize((700, 400))  # Resize to fit the window
bg_image = ImageTk.PhotoImage(background_image)

# Create a label for the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Title label
title_label = tk.Label(root, text="Web Scraper and Translator", font=("Arial", 16), bg="#FFFFFF", fg="#000080")
title_label.pack(pady=5)

# Direct URL Input
tk.Label(root, text="URL Input:", bg="#FFFFFF", font=("Arial", 8, "bold")).pack(anchor='w', padx=10)
url_entry = tk.Entry(root, width=40, bd=2, relief="groove")
url_entry.pack(pady=5, padx=10, anchor='w')  # Adjusted for left alignment

# Date range inputs
tk.Label(root, text="From Date (YYYY-MM-DD):", bg="#FFFFFF", font=("Arial", 8, "bold")).pack(anchor='w', padx=10)
start_date_entry = tk.Entry(root, width=40, bd=2, relief="groove")
start_date_entry.pack(pady=5, padx=10, anchor='w')  # Adjusted for left alignment

tk.Label(root, text="To Date (YYYY-MM-DD):", bg="#FFFFFF", font=("Arial", 8, "bold")).pack(anchor='w', padx=10)
end_date_entry = tk.Entry(root, width=40, bd=2, relief="groove")  # Add border with groove style
end_date_entry.pack(pady=5, padx=10, anchor='w')# Adjusted for left alignment

# Language choice input
tk.Label(root, text="Translation Language (en For English, pt For Portuguese, es For Spanish):", bg="#FFFFFF", font=("Arial", 8, "bold")).pack(anchor='w', padx=10)
language_entry = tk.Entry(root, width=40, bd=2, relief="groove")
language_entry.pack(pady=5, padx=10, anchor='w')  # Adjusted for left alignment

# Loading label (hidden initially)
loading_label = tk.Label(root, text="Scraping... Please wait.", bg="#FFFFFF", fg="#000080")
loading_label.pack_forget()

# Entry for translated file output
tk.Label(root, text="Give Name Output File:", bg="#FFFFFF", font=("Arial", 8, "bold")).pack(anchor='w', padx=10)
translated_file_entry = tk.Entry(root, width=40, bd=2, relief="groove")
translated_file_entry.pack(pady=5, padx=10, anchor='w')  # Adjusted for left alignment

# Run button
run_button = tk.Button(root, text="Run The Bot", command=run_scraping, bg="#f3b157", fg="white", font=("Arial", 8, "bold"), bd=2, relief="groove",width=34)
run_button.pack(pady=5,padx=10, anchor='w')

# Run the application
root.mainloop()

