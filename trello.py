import requests
import json
import os
from pathlib import Path

'''
Trello api class for some of the functionalities available from Atlassian
Further info for request and API instructions can be found at: 
https://developer.atlassian.com/cloud/trello/rest/api-group-actions/
'''
class Trello:

    headers = {
        "Accept": "application/json"
    }
    labels = {}
    query = {}

    #we take values from the credential file and set up the class global variables
    def __init__(self):

        global_vars = {}
        with open('credentials.txt', "r") as f:
            global_vars = json.load(f)
            self.query["key"] = global_vars["key"]
            self.query["token"] = global_vars["token"]
            self.labels = global_vars["labels"]
            f.close()
        

    def store_labelId(self, label: str, id: str):

        global_vars = None
        with open('credentials.txt', "r") as f:
            global_vars = json.load(f)
            f.close()
            
        if global_vars is not None:
            with open('credentials.txt', "w") as f:
                #append the new label
                global_vars["labels"][label] = id
                #write the new labels into the file making them available everywhere
                f.write(json.dumps(global_vars, sort_keys=False, indent=4, separators=(",", ": ")))
                f.close()

    #Get all of the boards that belong to your user.
    def get_all_boards(self):
        
        url = "https://api.trello.com/1/members/me/boards"
        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=self.query
        )
        return response.text

    #Get specific board info.
    def get_bard_info(self, idBoard: str):

        url = "https://api.trello.com/1/boards/" + idBoard
        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=self.query
        )
        return response.text


    def new_board(self, name: str):
        
        url = "https://api.trello.com/1/boards/"
        query = {}
        query['key'] = self.query['key']
        query['token'] = self.query['token']
        query["name"] = name

        response = requests.request(
            "POST",
            url,
            headers=self.headers,
            params=query
        )
        return response.text

    '''
    Create a new Label on a Board.
    idLabel : string
    name: string
    color: string
    '''
    def new_label(self, idBoard: str, name: str, color: str):
        url = "https://api.trello.com/1/boards/" + idBoard + "/labels"
        
        query = {}
        query['key'] = self.query['key']
        query['token'] = self.query['token']
        query['name'] = name
        query['color'] = color

        response = requests.request(
            "POST",
            url,
            params=query
        )

        return response.text
    

    def get_board_lists(self, idBoard: str):
        url = "https://api.trello.com/1/boards/" + idBoard + "/lists"

        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=self.query
        )
        return response.text

    def new_list(self, idBoard: str, name: str):
        url = "https://api.trello.com/1/boards/" + idBoard + "/lists"

        query = {}
        query['key'] = self.query['key']
        query['token'] = self.query['token']
        query["name"] = name

        response = requests.request(
            "POST",
            url,
            headers=self.headers,
            params=query
        )
        return response.text

    '''
    Creates a new card given a board Id
    idList: string
    name: string
    desc: string
    label: string
    category: string
    '''
    def create_new_card(self, idBoard:str, idList: str, name: str, label: str, desc: str = None, category: str = None):
        url = "https://api.trello.com/1/cards"

        query = {}
        query['key'] = self.query['key']
        query['token'] = self.query['token']
        query["idList"] = idList
        query["name"] = name
        query["desc"] = desc if desc is not None else None
        
        query["idLabels"] = [self.labels[label] if label in self.labels else None]
        
        if category is not None:
            query["idLabels"].append(json.loads(self.new_label(idBoard, category, "null"))["id"])
        
        response = requests.request(
            "POST",
            url,
            headers=self.headers,
            params=query
        )
        return response.text