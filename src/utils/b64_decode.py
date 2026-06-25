import base64
import binascii
import logging

logger = logging.getLogger(__name__)

def b64_decode(b64_str: str) -> str:
    # Type validation for incoming external data
    if not isinstance(b64_str, (str, bytes)):
        logger.error(f"Invalid data type received: {type(b64_str)}")
        return ""

    if isinstance(b64_str, bytes):
        try:
            b64_str = b64_str.decode('utf-8')
        except UnicodeDecodeError:
            logger.warning("Failed to decode incoming bytes to UTF-8 string")
            return ""
        
    # Strip whitespace and newlines from the base64 string    
    b64_str = b64_str.strip()
    
    try:
        # Strict base64 decoding
        decoded_bytes = base64.b64decode(b64_str, validate=True)
        return decoded_bytes.decode('utf-8')
        
    except (binascii.Error, UnicodeDecodeError) as e:
        # Log the error 
        logger.warning(f"Failed to decode external base64 payload: {e}")
        return b64_str