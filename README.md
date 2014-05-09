### Flurview
A simple python tool for creating an info dashboard in my hallway. It runs on an raspberry pi and is shown on an old 19'' TFT which is activated by a standard motion sensor (http://bit.ly/1j3lVSB).

![threeoptions_focused](https://dl.dropboxusercontent.com/u/2193334/Screenshot_Flurview.png)

### How it works

Flurview.py fetches some useful information on weather and traffic conditions as well as Google Calendar entries from the web and creates a html file to show the results in a concise fashion.

- Flurview.py (python script that creates index.html every ~60 sec.)
- index_template.html (template file with text markers that are replaced by Flurview.py)
- Flurview.html (master file - refreshes the index.html iframe every 45sec.)

### License

The MIT License (MIT)

Copyright (c) 2013 Conveyal

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
