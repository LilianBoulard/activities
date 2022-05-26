"""
Implements a request between the output of NLTK and the Redis database.

4 attributs:
    -Name
    -Tag
    -Price
    -localisation
"""


from ast import Str


class Request:


    def __init__(self, title = None, emplacement = None, theme = None, date = None, price = None) -> None:
        
        self.title = title #Str
        self.emplacement = emplacement #Str
        self.theme = theme #Str
        self.date = date #DateTime
        self.price = price #Bool or Range
        self.requete = None


    """
    DB connection
    """
    
    """
    Name Function
    """
    def set_title_event(self, titre) -> None:       
        self.title =titre
    
    def get_title_event(self) -> Str:
        return self.title
    

    

    """
    Date function
    """

    """
    Localisation function
    """

    """
    Tag function
    """
    
    