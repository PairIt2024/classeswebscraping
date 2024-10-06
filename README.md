# Web Scraping Project

## Overview

This project is designed to scrape class schedules from the San Jose State University (SJSU) website for the Fall 2024 semester. The scraped data includes essential information about each class, which is then stored in a MongoDB database for easy retrieval and management.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Data Structure](#data-structure)
- [License](#license)

## Features

- Scrapes class schedules from the SJSU website.
- Stores class data in a MongoDB database.
- Prevents duplicate entries by checking for existing records.
- Updates existing records if there are changes in the class information.

## Technologies Used

- Python
- BeautifulSoup (for HTML parsing)
- Requests (for HTTP requests)
- PyMongo (for MongoDB interactions)
- dotenv (for environment variable management)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
