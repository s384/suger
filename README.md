# suger
## Si van a usar esto en windows, ni pito idea de como montar python con django

#En linux
* Lo primero que debemos hacer es instalar el modulo venv, esto es para crear el entorno virtual en el cual instalaremos
los requisitos, es para no alterar otros proyectos realizados con python
~~~
sudo apt install python3-venv
~~~

* Ahora nos situamos en el directorio en el cual queremos tener alojado el entorno virtual y ejecutamos
~~~
python3 -m venv nombre-entorno-virtual
python3 -m venv suger
~~~

* Una vez listo esto activamos el entorno virtual
~~~
source suger/bin/activate
source directorio/donde/esta/alojado/el/entorno/virtual/bin/activate
~~~
### Esto debe hacerse cada primera vez que queramos trabajar con el proyecto, osea si prendo el pc para trabajar activo el
entorno virtual

* Clonamos el repositorio, este puede ser en otra carpeta, en la misma donde esta alojado el entorno virtual, yo prefiero
tener separado el proyecto con el entorno

~~~
cd ~/proyects
git clone https://github.com/s384/suger/
~~~

* Procedemos a instalar los requisitos
~~~
cd suger
pip install --upgrade pip
pip install -r requisitos.txt
~~~

* Con esto ya tenemos listo el proyecto para trabajar, para ejecutar el servidor de django ejectuamos
~~~
python manage.py runserver
~~~
### Este comando es el otro que debe ejecutarse cuando se trabaja con el proyecto, con esto ejecutamos el servidor web para visualizar los cambios
