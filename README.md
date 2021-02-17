# Project Title

alaitp-co-occurrence-matrix

## Author

* **Junpeng He** - *Initial work* - [junpenghe.com](https://junpenghe.com)

## Main Feature
* get most correlated words for a given word by word category.
* this is no longer a runtime app, it will calculate the matrix and persist matrix data in the database.
* at runtime job-description-api will fetch the database to get the matrix data

## Related Modules
* job-description-api(get the persisted matrix data from database)

## Built With

* [Python 3.7](https://www.python.org/) - The programming language used
* [Flask](https://flask.palletsprojects.com/) - The web framework used


