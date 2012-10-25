pysnips
=======

Python code snippets. Suggestions for improvements are highly encouraged.

template.py
-----------

My starting template when creating new python CLI functions


callfunc.py
-----------

Useful function to link optparse/parseargs with a "main" function. Saves repeating parameter names.


fnctlexamples.py
----------------

Because I can never remember how to make an existing file non-blocking.


a_star.py
---------

Collegue at work asked for a good "little project" to learn intermediate-to-advanced Python
features. Using A* to solve the 15-puzzle is something I keep reimplementing to just
about the same thing for myself. So, that's what I suggested, and here's my current
implementation.

loggerexamples.py
-----------------

Python's 'logging' module is awesome. Python's documentation for the module is less so; it
really needs some examples on how to piece things together if you're not using basicConfig
or the logging config modules. First example is a "basicConfig" ish thing for sending
stuff to the local syslog.