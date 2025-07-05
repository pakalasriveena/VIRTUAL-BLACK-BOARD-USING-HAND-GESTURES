import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data if not already present
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Convert the text to lowercase
    text = text.lower()
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.casefold() not in stop_words]
    
    # Lemmatization
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    
    # Join the words back into a single string
    processed_text = " ".join(lemmatized_words)
    
    return processed_text

def check_plagiarism():
    input_file_path = input_path_entry.get()
    dir_path = dir_path_entry.get()
    threshold = float(threshold_entry.get())

    if not input_file_path or not dir_path:
        messagebox.showerror("Error", "Please provide both input file and output directory paths.")
        return

    if not (0 <= threshold <= 1):
        messagebox.showerror("Error", "Similarity threshold must be between 0 and 1.")
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            file_text = f.read()
        
        input_file_sentences = sent_tokenize(file_text)
        
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        
        result_text.delete(1.0, tk.END)  # Clear the result text area
        
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                file_text2 = f.read()
            
            processed_file_text = preprocess_text(file_text)
            processed_file_text2 = preprocess_text(file_text2)
            
            # Calculate TF-IDF vectors
            tfidf = TfidfVectorizer().fit_transform([processed_file_text, processed_file_text2])
            
            # Calculate cosine similarity between the two texts
            cosine_sim = cosine_similarity(tfidf)[0][1]
            
            # Display similarity score in the result text area
            result_text.insert(tk.END, f"File: {file_name} - Similarity Score: {cosine_sim * 100:.2f}%\n")
            
            if cosine_sim >= threshold:
                output_file_path = os.path.join(dir_path, os.path.splitext(os.path.basename(file_path))[0] + "_plagiarised.txt")
                
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Similarity score: {cosine_sim * 100:.2f}%\n\n")
                    f.write("The following sentences are plagiarised:\n")
                    
                    plagiarised_sentences = []
                    
                    for input_sentence in input_file_sentences:
                        is_plagiarised = False
                        
                        for file_sentence in sent_tokenize(file_text2):
                            tfidf = TfidfVectorizer().fit_transform([input_sentence, file_sentence])
                            cosine_sim_sentence = cosine_similarity(tfidf)[0][1]
                            
                            if cosine_sim_sentence >= threshold:
                                is_plagiarised = True
                                break
                        
                        if is_plagiarised:
                            plagiarised_sentences.append(input_sentence)
                    
                    f.write("\n".join(plagiarised_sentences))
                    
                result_text.insert(tk.END, f"Plagiarism detected in file: {file_name}. Results saved to {output_file_path}.\n\n")
            else:
                result_text.insert(tk.END, f"No significant plagiarism detected in file: {file_name}.\n\n")
        
        # Show a message box indicating completion
        messagebox.showinfo("Completed", "Plagiarism check completed successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
window = tk.Tk()
window.title("Plagiarism Checker")

# Input file path label and entry
input_path_label = tk.Label(window, text="Input File Path:")
input_path_label.grid(row=0, column=0, sticky='W', padx=10, pady=10)

input_path_entry = tk.Entry(window, width=50)
input_path_entry.grid(row=0, column=1, padx=10, pady=10)

input_path_button = tk.Button(window, text="Browse", command=lambda: input_path_entry.insert(tk.END, filedialog.askopenfilename()))
input_path_button.grid(row=0, column=2, padx=10, pady=10)

# Directory path label and entry
dir_path_label = tk.Label(window, text="Directory Path:")
dir_path_label.grid(row=1, column=0, sticky='W', padx=10, pady=10)

dir_path_entry = tk.Entry(window, width=50)
dir_path_entry.grid(row=1, column=1, padx=10, pady=10)

dir_path_button = tk.Button(window, text="Browse", command=lambda: dir_path_entry.insert(tk.END, filedialog.askdirectory()))
dir_path_button.grid(row=1, column=2, padx=10, pady=10)

# Similarity threshold label and entry
threshold_label = tk.Label(window, text="Similarity Threshold:")
threshold_label.grid(row=2, column=0, sticky='W', padx=10, pady=10)

threshold_entry = tk.Entry(window, width=10)
threshold_entry.grid(row=2, column=1, padx=10, pady=10)
threshold_entry.insert(tk.END, "0.8")

# Check button
check_button = tk.Button(window, text="Check Plagiarism", command=check_plagiarism)
check_button.grid(row=3, column=0, columnspan=3, pady=20)

# Result text area
result_text = scrolledtext.ScrolledText(window, width=80, height=20, wrap=tk.WORD)
result_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

window.mainloop()