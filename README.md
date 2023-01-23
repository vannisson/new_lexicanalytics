# Lexicanalytics Web 🔎📄
Lexicanalytics is a web plataform to support linguistics and education researchers/professionals on extracting relevant lexical info from texts.

## What is underneath? ⚙️
While the previous version of Lexicanalytics was developed in Java, this one is a web service running over a **flask** backend server and **react-components/nodejs** client-side frontend.

## What it does? 📝

* Extraction of data from texts, such as lexical density and diversity, mean, mode and number of words and lines.

* Morphological analysis of the words of the productions.

* Data visualization in the shape of graphs.

## How to make it work? 🧑🏼‍💻
While the project isn't online, it is encapsulated in docker containers and run with docker-compose. To run locally, one just needs to clone this repository:

`$ git clone https://github.com/vannisson/lexicanalyticsWeb.git`

and build the images using:

`$ docker-compose build`

having created the images, run the servers using:

`$ docker-compose up`
