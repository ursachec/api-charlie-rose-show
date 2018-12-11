Old API I built a long long while ago. Put it here in case it's interesting to anyone. Beware, best coding practices were not followed.


# api-charlie-rose

A collection of scripts plus an API that may be helpful when building a client for viewing Charlie Rose Shows.

## Features:
- Map html files downloaded from www.charlierose.com to database entries
```
python content-handler.py
```

- Run a REST-ful API that presents database entries for Charlie Rose shows
```
python app.py
```

------------------------------------------------------------------------------------------


## Installation

1. Check out the repository ( ``` git clone https://github.com/ursachec/api-charlie-rose.git ``` )

2. Install virtualenv ( http://flask.pocoo.org/docs/installation/#virtualenv )

3. Install required python Modules ( *the project uses python 2.7* ) 
 
- BeautifulSoup
- Flask
- MySQL Connector/Python

## Usage

### Running the API

The following command will start a webserver with a default listening port on http://0.0.0.0:5000/ .

```
python app.py
```

To check if the content delivery is working: 
- Open http://0.0.0.0:5000/shows/all in a browser.
- Check the Content-Type header, It should be *application/json*.
- Check if the show contents from your database are being displayed.
- Update the db-credentials from ```app/config/db.py``` . To keep the credentials out of your public repository, you may want to run ```git update-index --assume-unchanged app/config/db.py```


### Populating your DB with content

- Download html files of your favourite shows from www.chalierose.com and save them all in one directory.
- In *content-handler.py*, make sure ```handleShowsFromDirectory(directory)``` points to the directory you saved the files to.
- Run ```python content-handler.py```. The content from the html files should be saved to the database.

## Links
Should you not be familiar with The Charlie Rose Show, it is an incredible knowledge source, take a few minutes to check it out:

- http://en.wikipedia.org/wiki/Charlie_Rose_(TV_show)
- www.charlierose.com

## Technical explanation

[![Technica explanation of how the API works](https://raw.github.com/ursachec/api-charlie-rose-show/master/img/technical_charlie_rose.png)](#app)
