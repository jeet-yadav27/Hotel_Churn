import sys
import traceback

class CustomException(Exception):
    def __init__(self, error_message, error_detail=None):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail=None):
        # Get traceback from the exception if provided, else from sys.exc_info()
        if error_detail is not None:
            # Use traceback object from the exception
            tb = error_detail.__traceback__
        else:
            # Get current exception info
            _, _, tb = sys.exc_info()

        if tb is not None:
            file_name = tb.tb_frame.f_code.co_filename
            line_number = tb.tb_lineno
            return f"Error in {file_name}, line {line_number}: {error_message} | Details: {str(error_detail)}"
        else:
            return f"{error_message} | Details: {str(error_detail)}"

    def __str__(self):
        return self.error_message
