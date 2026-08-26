import logging

logger = logging.getLogger('automation-tool-65')

class ValidationError(Exception):
    pass

def validate_config(config: dict) -> bool:
    """Validate configuration dictionary for edge cases."""
    if not isinstance(config, dict):
        logger.error('Configuration must be a dictionary')
        raise ValidationError('Configuration must be a dictionary')
    
    required_keys = ['host', 'port', 'timeout']
    for key in required_keys:
        if key not in config:
            logger.error(f'Missing required configuration key: {key}')
            raise ValidationError(f'Missing required configuration key: {key}')
            
    if not isinstance(config['port'], int) or not (0 < config['port'] < 65536):
        logger.error('Port must be an integer between 1 and 65535')
        raise ValidationError('Port must be an integer between 1 and 65535')
        
    if not isinstance(config['timeout'], (int, float)) or config['timeout'] < 0:
        logger.error('Timeout must be a non-negative number')
        raise ValidationError('Timeout must be a non-negative number')
        
    logger.info('Configuration validated successfully')
    return True

def validate_payload(data: any) -> bool:
    """Validate incoming data payload against edge cases."""
    if data is None:
        logger.error('Payload cannot be None')
        raise ValidationError('Payload cannot be None')
        
    if isinstance(data, (str, list, dict)) and len(data) == 0:
        logger.warning('Payload is empty')
        return False
        
    return True
