from typing import List, Union, Any
from swarmauri.core.chunkers.IChunker import IChunker

class FixedLengthChunker(IChunker):
    """
    Concrete implementation of IChunker that divides text into fixed-length chunks.
    
    This chunker breaks the input text into chunks of a specified size, making sure 
    that each chunk has exactly the number of characters specified by the chunk size, 
    except for possibly the last chunk.
    """

    def __init__(self, chunk_size: int):
        """
        Initializes a new instance of the FixedLengthChunker class with a specific chunk size.

        Parameters:
        - chunk_size (int): The fixed size (number of characters) for each chunk.
        """
        self.chunk_size = chunk_size

    def chunk_text(self, text: Union[str, Any], *args, **kwargs) -> List[str]:
        """
        Splits the input text into fixed-length chunks.

        Parameters:
        - text (Union[str, Any]): The input text to be chunked.
        
        Returns:
        - List[str]: A list of text chunks, each of a specified fixed length.
        """
        # Check if the input is a string, if not, attempt to convert to a string.
        if not isinstance(text, str):
            text = str(text)
        
        # Using list comprehension to split text into chunks of fixed size
        chunks = [text[i:i+self.chunk_size] for i in range(0, len(text), self.chunk_size)]
        
        return chunks