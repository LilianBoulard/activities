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


    def __init__(self, title = None, lieu = None, theme = None, date = None, price = None) -> None:
        
        self.title = title #Str
        self.lieu = lieu #Str
        self.theme = theme #Str
        self.date = date #DateTime
        self.price = price #Bool or Range
        self.requete = None

    """
    Update
    """
    def update(self,tag,chaine):

        if tag == 'lieu':
            self.update_lieu(chaine)
        elif tag == 'theme':
            self.update_theme(chaine)
        elif tag == 'date':
            self.update_date(chaine)
        elif tag == 'price':
            self.update_price(chaine)

    def update_lieu(self,chaine):
        pass
    
    def update_theme(self,chaine):
        pass
    
    def update_date(self,chaine):
        pass
    
    def update_price(self,chaine):
        pass
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

        
