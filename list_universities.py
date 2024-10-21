import json
import os
import csv

def load_json_data():
    try:
        folder_path = input("Enter the folder path where the JSON file is located: ")
        file_path = os.path.join(folder_path, 'paramveer_adoptions.json')
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found in the specified directory.")
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except json.JSONDecodeError as json_error:
        print(f"Error decoding JSON: {json_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

data = load_json_data()


def save_adoptions_to_csv(adoptions_data, file_name):
    try:
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['adoption_id', 'date', 'quantity', 'book_id', 'isbn', 'title', 'category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for adoption in adoptions_data:
                book = adoption['book']
                writer.writerow({
                    'adoption_id': adoption['id'],
                    'date': adoption['date'],
                    'quantity': adoption['quantity'],
                    'book_id': book['id'],
                    'isbn': book['isbn10'],
                    'title': book['title'],
                    'category': book['category']
                })
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

save_adoptions_to_csv(data[0]['adoptions'], 'paramveer_adoptions.csv')


def list_universities_by_state(data, state_name):
    universities = [record['university']['name'] for record in data if record['university']['state'] == state_name]
    if universities:
        print(f"Universities in {state_name}:")
        for university in universities:
            print(university)
    else:
        print(f"No universities found in {state_name}.")

list_universities_by_state(data, 'Illinois')


def list_books_by_category(data, chosen_category, output_file):
    books_in_category = []
    
    for record in data:
        for adoption in record['adoptions']:
            if adoption['book']['category'] == chosen_category:
                books_in_category.append(adoption['book']['title'])
    
    if books_in_category:
        with open(output_file, 'w') as f:
            for book in books_in_category:
                f.write(f"{book}\n")
        print(f"Books in the {chosen_category} category have been saved to {output_file}.")
    else:
        print(f"No books found in the {chosen_category} category.")

list_books_by_category(data, 'Business', 'business_books.txt')
