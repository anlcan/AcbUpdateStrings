## ACBUpdateStrings

My humble attempt to replace genstrings update strategy, which is according
 to [Apple documentation] ( https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/LoadingResources/Strings/Strings.html)
works as follows

    The first time you run the genstrings tool, it creates a set of new strings files
    for you. Subsequent runs replace the contents of those strings files with the
    current string entries found in your source code. For subsequent runs, it is a
    good idea to save a copy of your current strings files before running genstrings.
    You can then diff the new and old versions to determine which strings were
    added to (or changed in) your project. You can then use this information to
    update any already localized versions of your strings files, rather than replacing
    those files and localizing them again
    
   
So, instead of going through that you can run generate.py to upate your localizable strings

First download and make *generate.py* script executable
```bash
curl 'https://raw.githubusercontent.com/anlcan/AcbUpdateStrings/master/generate.py' -o /usr/local/bin/generate.py && chmod u+x /usr/local/bin/generate.py
```
Second, go to your project directory and run generate.py with source folder as first argument and existing localizable strings file as second

```bash   
# this command will generate a new Localizable.strings file in current directory, 
# with new strings appended at the bottom
generate.py . ./Supporting\ Files/en.lproj/Localizable.strings 
``` 
       
For more complete solution, you can check 
- [Localizable Strings merge](http://www.loc-suite.org/) paid app
- [Localization Suite] (http://www.loc-suite.org/)
