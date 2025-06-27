import sys

def error_message_detail(error_message,error_detail:sys)->str:
    _,_,exc_tb=error_detail.exc_info()
    filename=exc_tb.tb_frame.f_code.co_filename
    lineno=exc_tb.tb_lineno
    error_message=f"Error occurred in script: {filename} at line number: {lineno} with error message: {error_message}"
    return error_message
    
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail)
    def __str__(self):
        return self.error_message