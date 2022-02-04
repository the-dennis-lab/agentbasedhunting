# Agent Based Modeling of hunting   

I made an arena-like environment for agents (mice) to get towards other agents (crickets) which produce noise. I started to link their behaviors (crickets do not chirp if the mouse recently moved) but let the project sit due to other priorities.


## How to Run

Launch the model:
```
    $ conda activate abm
    $ cd src
    $ python crickethunt/server.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

=======
* Launch the visualization
```
< from the src folder >
$ mesa runserver
```
* Visit your browser: http://127.0.0.1:8521/
* In your browser hit *run*

## TODO
- build test set
- make all buttons work
- update hexmap
- make notebook that auto-generates hex maps 

=======
* Launch the visualization
```
$ mesa runserver
```
* Visit your browser: http://127.0.0.1:8521/
* In your browser hit *run*
