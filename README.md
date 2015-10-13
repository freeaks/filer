about:   
---   
an attempt at writing a file manager in pyqt, for linux or osx,   
with heavy influences from the Amiga Workbench and Directory Opus 5

file manager: [filer.py](https://raw.github.com/freeaks/filer/master/test-tree/screenshots/filer.png) <-- click for screenshot   
preference program: [prefs.py](https://raw.github.com/freeaks/filer/master/test-tree/screenshots/prefs.png)   
asl requester program: [requester.py](https://raw.github.com/freeaks/filer/master/test-tree/screenshots/asl_req.png)   


status:   
---   
alpha.   
it's working, but far from being feature complete,   
and there's almost no error checking yet.   


done:   
---
- file requester: browse filesystem, open directory or execute file   
- file manager:   display files, cleanup, dragndrop, copy, move,   
		  execute, select, multiselect, trash, open parent,   
		  create files and dirs, rename   
- preferences:    choose pattern, font color   
- global menu:    open file requester, preferences, quit, and    
		  all file manager actions listed above.   
		  


todo:   
---   
preferences:   
- adding and removing new icons (for filetypes)   
- activate the 'operation mode' selection (classic / dopus5 behavior)   


file manager:   
- create a dopus5-like file lister   
- create icon info window   
- create dialog to solve problem upon file operation (delete, overwrite, skip..)   

