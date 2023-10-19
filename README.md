# gPit - An open-pit optimisation tool
<p align="center">
  <a href="#">
    <img src="https://img.shields.io/github/license/GuilhermeMene/gPit?style=for-the-badge" style="max-width:100%;" alt="License">
  </a>
  <a href="#">
    <img src="https://img.shields.io/github/repo-size/GuilhermeMene/gPit?style=for-the-badge" style="max-width:100%;" alt="Repo Size">
  </a>

_____________

#### About

The gPit is a tool for open-pit mining otimisation. 

The main features of the gPit are: 
* EPV and Cut-Off calculations 
* Ultimate Pit Limit by using (Hochbaum, 2008 -  pseudoflow algorithm)
* Revenue Factor analysis by incremental RF 
* Ultimate Pit Limit mesh creation
* Calculation of the NPV and open-pit volumes

#### Dependencies
Some libraries are required to run the gPit software: 

* pandas  
* numpy
* pyvista
* scipy
* networkx
* pseudoflow
* meshio

A list of all libraries used under development of the gPit is provided in [Requirements] (https://github.com/GuilhermeMene/gPit/blob/main/requirements.txt)

#### References 
Dorit S. Hochbaum, 2008. "The Pseudoflow Algorithm: A New Algorithm for the Maximum-Flow Problem," Operations Research, INFORMS, vol. 56(4), pages 992-1009, August.

Part of the gPit tool is based on the 2020 Avalos code distributed under an MIT license: 

Avalos, S., Ortiz, JM (2020) A guide for pit optimization with Pseudoflow in python, Predictive Geometallurgy and Geostatistics Lab, Queen's University, Annual Report 2020 [Git Repo](https://code.engineering.queensu.ca/geomet-group/2020-pseudoflow-python)

#### License
The gPit is a free software licensed under [MIT License] (https://github.com/GuilhermeMene/gPit/blob/main/LICENSE)


