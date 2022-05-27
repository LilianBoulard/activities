"""
Implements a request between the output of NLTK and the Redis database.

4 attributs:
    -Name
    -Tag
    -Price
    -localisation
"""


from datetime import datetime
import json


class Request:


    def __init__(self, title = None, emplacement = None, theme = None, date = None, price = None) -> None:
        
        self.title = title #Str
        self.emplacement = emplacement #Str
        self.theme = theme #Str
        self.date = date #DateTime
        self.price = price #Bool or Range
        self.requete = None


    """
    DB connection && Request building
    """

    
    
    """
    Name Function
    """
    def set_title_event(self, titre) -> None:       
        self.title =titre
    
    def get_title_event(self) -> str:
        return self.title

    """
    Date function
    """
    def set_Date(self, Date :str) -> None:
        nDate = datetime(Date)
        """if nDate < datetime.now().strftime("%d/%b/%Y"):
            return ERROR"""
        self.date = nDate
    
    """
    Localisation function
    """
    def set_localisation(self, localisation) -> None:
        if type(localisation) == int :
            self.emplacement = "(Arrondissement)"+localisation
        elif type(localisation) == str:
            self.emplacement = "(Ville)"+localisation

    """
    Tag function
    """
    def get_theme(self, theme):
        if type(theme) != type([]):
            theme = [theme]
        file = open('theme.json')
        data = json.load(file)

        check = all(item in data.values() for item in theme)

        if check:
            return theme
        else:
            return "Error"

        
