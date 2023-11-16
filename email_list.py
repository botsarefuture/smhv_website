from bson import ObjectId
from db_utils import db
from mail import list_join_email


email_collection = db["email_list"]

from datetime import datetime


def get_formatted_date():
    # Get the current date
    current_date = datetime.now()

    # Format the date as DD.MM.YYYY
    formatted_date = current_date.strftime("%d.%m.%Y")

    # Return the formatted date
    return formatted_date


def add_email(email, lang):
    if check_email(email) == False:
        data = {"email": email, "date": get_formatted_date(), "language": lang, "confirmed": False}
        
        try:
            result = email_collection.insert_one(data)
        
        except Exception as e:
            print(str(e))
            
            with open("to_list.txt", "a") as f:
                f.write('\n{"email": "%s", "language": "%s"}') % (email, lang)                
            return
        
        finally:
            list_join_email(lang, email, f"https://sinimustaahallitustavastaan.org/confirm_email/{result.inserted_id}")
        
def confirm_email(email_id):
    # Define the filter (condition to find the document to update)
    filter_condition = {"_id": ObjectId(email_id)}

    # Define the update operation
    update_operation = {
        "$set": {"confirmed": True}
    }

    # Perform the update
    email_collection.update_one(filter_condition, update_operation)
    
def check_email(email):
    # Define the filter condition
    filter_condition = {"email": email}

    # Check if any document matches the filter condition
    result = email_collection.find_one(filter_condition)

    # Return True if a matching document is found, else return False
    print(result)
    return result is not None

def get_emails():
    filter_condition = {"confirmed": True}
    
    result = email_collection.find(filter_condition)
    result_list = list(result)
    
    print(result_list)
    
    return result_list