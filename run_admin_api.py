from core.logger import get_logger
from admin_api.src.settings import get_settings
from admin_api.src.main import start_admin

settings = get_settings()
logger = get_logger(settings.log_filename)


if __name__ == "__main__":
    start_admin()
