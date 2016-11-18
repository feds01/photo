class Fatal(Exception):
    pass

"""
class Config(BaseException):
    def __init__(self, error_code, old_definition):
        self.error_code = error_code
        self.old_definition = old_definition
        self.correct_value = "\\"

    def IncorrectVariableValue(self):
            print("Config was not compiled correctly.")
            print("Error Code: " + self.error_code)
            print("variable definition " ,self.old_definition, " -> ", self.correct_value)
"""