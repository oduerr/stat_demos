
Task: Extract CSS to a shared file (keep JS inline)

Target file to modify: docs/linear_regression_nn.html
New file to create: docs/shared/demo-shell.css
Do not touch any other files.

Goals
	1.	Move the entire <style> … </style> block from docs/linear_regression_nn.html into docs/shared/demo-shell.css verbatim (no changes to rules/selectors).
	2.	In the HTML <head>, replace the removed <style> tag with:
    
```
<link rel="stylesheet" href="./shared/demo-shell.css">
```
	3.	Keep all JavaScript inline inside the HTML. No external JS files, no CDN links.
	4.	The page must work offline when opened from the file system and look identical.

Steps
	1.	Create folder docs/shared/ if it doesn’t exist.
	2.	Copy the entire contents of the current <style> tag into docs/shared/demo-shell.css.
	3.	Remove the <style> tag from the HTML and add the <link> tag shown above.
	4.	Do not change IDs/classes or any markup/JS.
	5.	Save both files.