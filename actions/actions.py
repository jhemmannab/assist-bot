# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from logging import Logger
from os import link
import pprint
from typing import Any, Text, Dict, List
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#

BaseUrl = 'https://docs.infoblox.com/rest/api/search/'
baseDocsUrl = 'https://docs.infoblox.com'


class ActionsHelpMessage(Action):

    def name(self) -> Text:
        return "action_help_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.latest_message['entities'][0]['value']

        dispatcher.utter_message(
            text=f"Please wait while we Search for your result !!!")

        return [SlotSet("query", query)]


class ActionSearch(Action):

    @staticmethod
    def getSearchQueryResult(query):
        url = f'{BaseUrl}?cql=siteSearch ~ "{query}"&start=0&limit=2'
        print(url)
        response = requests.get(url)
        resp_json = response.json()["results"]
        link = list()
        for resp in resp_json:
            link.append(f"{baseDocsUrl}{resp['content']['_links']['webui']}")
        return link

    def name(self) -> Text:
        return "action_show_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.get_slot("query")

        linkArr = ActionSearch.getSearchQueryResult(query)

        for link in linkArr:
            dispatcher.utter_message(
                text=f"Here is the top search result : [link]({link})")
        return []
