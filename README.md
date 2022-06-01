<br />
<p align="center">
  <a href="https://github.com/DaDebias/cool_programmer_tshirts2.0">
    <img src="book.png" alt="Logo" width=150 height=150>
  </a>
  
  <h1 align="center">Exam Project: Data Science</h1> 
  <h3 align="center">MSc Cognitive Science 2022</h3> 


  <p align="center">
    Thea Rolskov Sloth & Astrid Sletten Rybner
    <br />
    <a 
    Aarhus University
    a>
    <br />
  </p>
</p>


## Project information
This repository contains code for reproducing our analysis regarding gender representation in English literature from the nineteenth and twentieth century. 


## Repository structure
An overview of the scripts used for the analysis can be found below.  

| Folder | Description|
|--------|:-----------|
```data_exploration``` | data exploration  
```meta``` | metadata files for analyzed texts 
```src```| main analysis scripts
```output``` | output folder for the different scripts 
```timeseries```| scripts for timeseries analysis


## Usage
To reproduce the analysis, you need to first clone this repository:

```
git clone https://github.com/thearol/data-science-x-am
cd /cool_programmer_tshirts2.0
pip install -r requirements.txt
```

You then need to download the full Project Gutenberg corpus via [The Standardized Project Gutenberg Corpus](https://github.com/pgcorpus/gutenberg).

To analyze the same texts used in this analysis, the full corpus can then be filtered down using the metadata files in the ```meta``` folder. The txt files of the books should then be placed in a folder named ```data```

Subsequently, the two main analysis can be run with: 
``` 
python /src/gender-counts.py 
python /src/bodydescriptions.py 
```
The first script will extract a count of all male and female pronouns from each book. 
The second script locates all bodyparts and their owners, as well as any adjectives describing the bodypart. 
The output files are saved to the output folder. 


## Contact details
If you have any questions regarding the project itself or the code implementation, feel free to contact us via e-mail: [Thea Rolskov Sloth](mailto:201706833@post.au.dk) & [Astrid Sletten Rybner](mailto:201808935@post.au.dk)

## Acknowledgements
We would like to give special thanks to the following:
* [Erin Davis](https://github.com/erdavis1/GenderedDescriptions) for project inspiration.
* [Project Gutenberg](https://www.gutenberg.org/) for providing acces to the many digitized works analyzed in this project. 
* [The Standardized Project Gutenberg Corpus](https://github.com/pgcorpus/gutenberg) for creating a pipeline for accessing the most current version of the books in Project Gutenberg. 
