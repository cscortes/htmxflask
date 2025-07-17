# htmxflask
All the HTMX examples redone using a FLASK server backend.  

To see the original HTMX samples, go to 
https://htmx.org/examples/. 

The idea is to create server and client side examples 
that will display the full amount of effort required.

* Since HTMX is in flux I will be using developmental version of HTMX.  
* The most current version of HTMX is 2.0.6.

## Client Side Notes:

* Example of how to use HTMX in your web pages:

```html
<script src="https://unpkg.com/htmx.org@2.0.6/dist/htmx.min.js"></script>
<script>
  // Minimal configuration for educational examples
  htmx.config.historyEnabled = false;
  htmx.config.allowEval = false;
  htmx.config.allowScriptTags = false;
</script>
```
 
 ## Server Side Notes:
 
 To "run" the python side myapp.py you need to have flask installed and possibly other
 modules. PIPENV is what you need to get it install and run.
 
 **pipenv install**
 
CD into one of the Major directories and you can "run" the flask server with:

**pyenv shell**

**python myapp.py**

This will setup your server on localhost:5000.  

Open a browsers, and in the url bar type:

http://localhost:5000 


 
 
