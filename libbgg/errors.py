
class InvalidInputError(Exception):
    pass

class APICallError(Exception):

    def __init__(self , msg , url):
        Exception.__init__(self , msg)
        self.url = url

