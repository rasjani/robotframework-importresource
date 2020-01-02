ImportResource
==============

Tool to import robot framewort resource files from installed python packages.

For example, if you want to distribute the keyword files via pip packages, place those 
files into a package within folder "rf-resources" and then, within the testdata:

```robotframework
Library   ImportResource  resources=yourpackagename;anotherpackage
```


See https://github.com/rasjani/robotframework-importresource-testdata for example package
used during acceptance tests on how to package your robotframework resource files.
