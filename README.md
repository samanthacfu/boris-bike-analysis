# Analysis of London's Bike Sharing Program\
("Boris Bikes" / Santander Cycles)

This repo contains some basic analyses of publicly available data on London's main bike sharing program, Boris Bikes. The data is part of Transport for London's Open Data initiative and can be found [here.](http://cycling.data.tfl.gov.uk/)

## Motivation
I like biking! And bike-sharing initiatives!
But mostly these analyses were an attempt at data journalism on the future of bike-sharing, published [here](http://publicspherejournal.com/2018/01/bike-sharing-the-future-of-urban-transportation/).

## Description
- download_data
  - Script that downloads csvs of trip data from the TfL page
- get_station_data
  - Script that gets a list of all bike stations and lat/lons from the TfL API
- import_data
  - Script to import csvs into a dataframe
- clean_and_analyze
  - Script to clean data & perform some basic analyses
- create_xx_maps
  - Script to create maps visualizing some of the data
