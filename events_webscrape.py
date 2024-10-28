import os
import requests
from dotenv import load_dotenv
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import webscrape

url = "https://events.sjsu.edu/calendar"
soup = None

load_dotenv()

def scrapeEvents():
    try:
        # finds the structure containing only the current day's events
        eventsToday = soup.find('div', class_="em-card-group em-card-group--small")
        events = [div for div in eventsToday.find_all('div') if div.parent == eventsToday]
        events_data = [] # a list of dictionaries data of each event
        
        # Structure is defined as:
        # [Event Title, Event Date, Event Location, Event Tag, Event Image]
        for event in events:
            event_card_id = event.get('class')[1:] # ex: ['em-event-45493027815300', 'em-event-instance-45493027927995']
            title = event.find('h3', class_="em-card_title").text.strip()
            date = event.find('p', class_="em-card_event-text").text.strip()
            if len(event.find_all('p', class_="em-card_event-text")) >= 2: # checking if location exists for event to avoid IndexError
                location = event.find_all('p', class_="em-card_event-text")[1].text.strip()
            tag = event.find('a', class_="em-card_tag")
            if tag: # not all events have tags, if it does, get the text
                tag = tag.text.strip()
            img_src = event.find('img')['src'].strip() # ex: https://localist-images.azureedge.net/photos/47670022594355/card/a47b3e7c3ff4c51c544a0dd82ad6bd27cc6f685e.jpg

            # print(f"Event id: {event_card_id}")
            # print(f"Event title: {title}")
            # print(f"Event date: {date}")
            # print(f"Event location: {location}")
            # print(f"Event tag: {tag}")
            # print(f"Event image: {img_src}\n\n")

            events_data.append({
                "event_card_id": event_card_id,
                "title": title,
                "date": date,
                "location": location,
                "tag": tag,
                "img_src": img_src
            })
        print(f'Saved: {events_data[-1]}')

        return events_data
    
    except Exception as e:
        print("Error scraping events:", e)
        return None



def saveToMongo(db, events_data):
    if db is not None and events_data:
        try:
            collection = db['events']
            print(collection)
            for event in events_data:
                print(event)
                existing_event = collection.find_one({'event_card_id': event['event_card_id']})

                # if event already exists
                if existing_event:
                    print("Found event")
                    # if there are changes to the event, update it
                    if existing_event != event:
                        collection.update_one({'event_card_id': event['event_card_id']}, {'$set': event})
                        print("Event updated")
                    
                
                else:
                    print("Inserting...")
                    collection.insert_one(event)
            print("data saved to db")
                
        except Exception as e:
            print("Error saving to mongo: ", e)
            return None


if __name__ == "__main__":
    soup = webscrape.initializeSoup(url)
    if soup:
        events_data = scrapeEvents()
        client, db = webscrape.connectToMongo()
        if db is not None:
            saveToMongo(db, events_data)
        if client:
            client.close()