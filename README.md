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
    
   
So, instead of going through that you run generate.py with your project directory as first parameter 
and existing strings file as second:

    ```
    # assuming:  
    # 1 python is installed 
    # 2 you downloaded generate.py and stored it in your Documents folder
    # 3 you are in your project root directory
    
    # this command will generate an new Localizable.strings file in current directory, 
    # with new strings appended at the bottom
    python generate.py . /Supporting\ Files/en.lproj/Localizable.strings 
    ``` 
       