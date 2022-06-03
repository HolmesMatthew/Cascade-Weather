# Cascade-Weather

For when Googles not good enough

> capstone project for PDX code guild

## Project Overview

Weather/News app. The goal behind Cascade Weather is to create a weather and news app using `Open Weather Map api` and `New York Times api`. The app will also be using `ip-api` to get the users current location. The user will have access to current and forecast weather data as well as the ability to search by zip code

## Features

- Locational weather data
- Four day forecast
- Weather data by zip

## Data Model

#### Home page

- Get locational data
  - pass data to weather api
- Load weather
  - pass weather data threw django view
  - pass final data to HMTL

#### Search

- Get Zip code
  - verify zip code
  - pass zip code to weather api
- Load weather
  - pass weather data threw django view
  - pass final data to HMTL

---

## Schedule

### Week one

> Initialize api's

- start django project
- connect to ip-api
- connect to open weather maps
- connect to new york times api

### Week Two

> Build home view

- sort threw weather data
- assign data to variables
- start displaying weather data

### Week Three

> Search Functionality and styling

- work on home page styling (bootstrap)
- build django view for search function

### Week Four

> Finish styling

- Finish styling
- Make last minute corrections/additions
