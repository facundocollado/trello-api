from flask import Flask, request
from trello import Trello
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    request_data = request.get_json()

    req_params = ["type", "title"]
    if all (k in request_data for k in req_params):
        trello = Trello()

        #Search for you latest board
        idBoard = json.loads(trello.get_all_boards())[-1]["id"]
        #Get the first list from that board 
        idList = json.loads(trello.get_board_lists(idBoard))[0]["id"]
        # Add a few test cards for the newly created labels
        # Categories are labels that won't show up on the front of cards.
        card = json.loads(trello.create_new_card(
            idBoard, 
            idList, 
            request_data["title"], 
            request_data["type"], 
            request_data["description"] if "description" in request_data else None, 
            request_data["category"] if "category" in request_data else None
            ))

        return "\n New card available at: " + card["shortUrl"] + "\n"

    return "\n Missing parameters. Type and Title are required. \n"

'''
Local setup, this function will create the requested labels for cards.
'''
@app.route('/set-up', methods=['GET'])
def set_up():
        trello = Trello()
        
        idBoard = json.loads(trello.get_all_boards())[-1]["id"]
        #create default labels
        issueId = trello.labels['issue'] = json.loads(trello.new_label(idBoard, "issue", "yellow"))["id"]
        bugId = trello.labels['bug'] = json.loads(trello.new_label(idBoard, "bug", "orange"))["id"]
        taskID = trello.labels['task'] = json.loads(trello.new_label(idBoard, "task", "green"))["id"]

        print("Adding labels for issues \n")
        trello.store_labelId("issue", str(issueId))
        print("Adding labels for bugs \n")
        trello.store_labelId("bug", str(bugId))
        print("Adding labels for tasks \n")
        trello.store_labelId("task", str(taskID))

        return "Local setup completed, you can now start creating new cards!"
        
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)