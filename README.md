# Manufacturers Products Database [The computing and IT project - Open University]Manufacturers Products Database [The computing and IT project - Open University]

The final module of my Open University qualification.

In collaboration with a fashion retail startup company, I created an application to gather fashion product data at scale from the web, automatically classify the data, persist it and expose it through a web UI with different search features, including image reverse search.

The application consists of the following components:

- A scraping framework to gather product data and images
- A third party AI based image classification system to classify and augment product data with features based on a custom taxonomy.
- A web application to store and retrieve data, either by parameter or reverse image search. 

Tech stack used:

- Scrapy (Scraping Framework)
- Django (Web Application)
- Tensor Flow for image vectorisation and Spotify's Annoy to calculate approximate nearest neighbours (Reverse Image Search)
- Service runs in docker compose
