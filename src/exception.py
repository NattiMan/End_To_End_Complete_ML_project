import sys
import os

from src.logger import logging



def create_error_message_from_exception(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return (f"An error has happened in the file {file_name} at line {line_number}. The error message is : {str(error)}")




class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = create_error_message_from_exception(error_message, error_detail=error_detail)
        

    def __str__(self):
        return self.error_message
    


