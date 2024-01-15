import json
from sklearn.model_selection import train_test_split

from apps.core.logger import Logger
from apps.core.file_operation import FileOperation
from apps.ingestion.load_validate import LoadValidate