from typing import List, Dict

# Record class representing the data for each record
class Record:
    """
    Record class representing the data for each record
    """
    def __init__(self, date, category, amount, message, _id = None):
        """
        Initialize a new record

        Args:
            date (str): Records date
            category (str): Records category
            amount (float): Records amount
            message (str): Records description
        """
        # Importin generate_hex_id() to give each record a unique id 
        from ..utils.model_utils import generate_hex_id
        self._id = _id if _id else generate_hex_id()
        self.date = date
        self.category = category
        self.amount = amount
        self.message = message
    
    
    # A static method for converitng a dictionary type data of Record class into a list for further use
    @staticmethod    
    def _unjsonfy(data: Dict) -> List:
        """Converting Dict format Record data into List

        Args:
            data (Dict): Dictionary of Record data (stored in the JSON db as a value of it's _id)
            {
                "date": "date_value",
                "category": "category_value",
                "amount": "amount_value",
                "message": "message_value"}

        Raises:
            ValueError: In case the Dict is incorrect, or misses some main Record Args  

        Returns:
            List: List of data in following format [date, category, amount, message]
        """
        if isinstance(data, dict) and all(key in data for key in ['date', 'category', 'amount', 'message']):
            return [data['date'], data['category'], data['amount'], data['message']]
        else:
            raise ValueError("Invalid data format for unjsonfy method")
    
    
    # Same as previuos method, but extended to have the _id of the Record
    # (Will be depricated in further versions) 
    @staticmethod    
    def _unjsonfy_extended(data: Dict) -> List:
        """Converting Dict format Record data into List

        Args:
            data (Dict): Dictionary of Record data (stored in the JSON db as a value of it's _id)
            {
                "id": "id_value",
                "date": "date_value",
                "category": "category_value",
                "amount": "amount_value",
                "message": "message_value"}

        Raises:
            ValueError: In case the Dict is incorrect, or misses some main Record Args  

        Returns:
            List: List of data in following format [_id, date, category, amount, message]
        """
        if isinstance(data, dict) and all(key in data for key in ['id', 'date', 'category', 'amount', 'message']):
            return [data["id"], data['date'], data['category'], data['amount'], data['message']]
        else:
            raise ValueError("Invalid data format for extended unjsonfy method")
    
    
    # A method for converting a Record to a Dict for storing in JSON DB
    def _jsonfy(self) -> Dict:
        """Converts Record to Dict for easier use with JSON DB file

        Returns:
            Dict: {
                "date": "date_value",
                "category": "category_value",
                "amount": "amount_value",
                "message": "message_value"}
        """
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "message": self.message
        }
    
        
    # A method for manging the data of Record     
    def _data(self) -> List:
        """Returns main Record's data in a List format

        Returns:
            List: [date, category, amount, message]
        """
        return [self.date, self.category, self.amount, self.message]
    
    
    # Same as previuos method, but extended to have the _id of the Record
    # (Will be depricated in further versions) 
    def _data_extended(self) -> List:
        """Returns main Record's data in a List format

        Returns:
            List: [_id, date, category, amount, message]
        """
        return [self._id, self.date, self.category, self.amount, self.message]
    
    