Parses json string in either of these two formats :

    [{} , {} , {} , {} ...]


    {}
    {}
    {}
    ...

and determine the location of top level objects.

If the json string is broken at EOF , then also returns the location of broken top level object at EOF.


