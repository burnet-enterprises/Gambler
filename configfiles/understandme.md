Proxy params has a special paramter sourced from https://framkant.org/2017/09/flask_script_name/
To reverse proxy successfuly you must have X-SCRIPT-NAME in the Proxy paramters as located in the file then label the folder.

Apache example
<Location "/test_subdir">
    ProxyPass "http://localhost:8081" 
    X-SCRIPT-NAME "/test_subdir"
</Location>

Nginx Example

proxy_set_header X-SCRIPT-NAME "/";


To make sure sure you can redirect on the home page for the docs a hack is necessary.  This is the steps for the hack until Sphinx allows relative links.
1. Make Build the documentation
2. Replace the docs/build/html/Home.html with the following:
<html>
<head><meta http-equiv="Refresh" content="0; url='..'" />
</head>
<body> <a href="..">Go Home</a> </body></html>

