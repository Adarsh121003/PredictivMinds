import logging
import json
from datetime import datetime
from pathlib import Path


class MahaGovAILogger:
    """Professional logging system with activity tracking"""

    def __init__(self):
        Path("logs").mkdir(exist_ok=True)

        self.logger = logging.getLogger("MahaGovAI")
        self.logger.setLevel(logging.INFO)

        # File handlers
        file_handler = logging.FileHandler('logs/app.log')
        error_handler = logging.FileHandler('logs/errors.log')
        error_handler.setLevel(logging.ERROR)
        console_handler = logging.StreamHandler()

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)

    def log_api_request(self, endpoint: str, method: str, data: dict, ip: str):
        """Log API requests for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'ip_address': ip,
            'action': 'API_REQUEST'
        }
        self.logger.info(f"API Request: {endpoint} from {ip}")
        self._save_activity_log(log_entry)

    def log_prediction(self, model_name: str, input_data: dict, output: dict, ip: str):
        """Log model predictions for compliance"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'model': model_name,
            'ip_address': ip,
            'district': input_data.get('district', 'unknown'),
            'action': 'MODEL_PREDICTION',
            'success': output.get('success', False)
        }
        self.logger.info(
            f"Prediction: {model_name} for {input_data.get('district')}")
        self._save_activity_log(log_entry)

    def log_error(self, error: Exception, context: str):
        """Log errors with context"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'action': 'ERROR'
        }
        self.logger.error(f"Error in {context}: {str(error)}")
        self._save_activity_log(log_entry)

    def log_data_access(self, user_role: str, data_type: str, action: str, ip: str):
        """Log data access for security audit"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_role': user_role,
            'data_type': data_type,
            'action': action,
            'ip_address': ip,
            'category': 'DATA_ACCESS'
        }
        self.logger.info(f"Data Access: {user_role} accessed {data_type}")
        self._save_activity_log(log_entry)

    def log_file_upload(self, filename: str, file_size: int, domain: str, ip: str):
        """Log file uploads"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'filename': filename,
            'file_size_mb': round(file_size / (1024*1024), 2),
            'domain': domain,
            'ip_address': ip,
            'action': 'FILE_UPLOAD'
        }
        self.logger.info(
            f"File Upload: {filename} ({log_entry['file_size_mb']} MB)")
        self._save_activity_log(log_entry)

    def _save_activity_log(self, log_entry: dict):
        """Save to activity log file for audit"""
        activity_log_path = Path('logs/activity_log.jsonl')
        with open(activity_log_path, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')


# Global logger instance
logger = MahaGovAILogger()
