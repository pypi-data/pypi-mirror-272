import os
import logging
import logging.handlers
import inspect

class CUserLogger:
    _logger_instance = None
    ins_count = 0

    @classmethod
    def getInstance(cls, task_id):
        """防止多日志对象初始化"""
        if cls._logger_instance is None:
            cls._logger_instance = cls(task_id)
        return cls._logger_instance

    def __init__(self, task_id):
        CUserLogger.ins_count += 1
        self.task_id = task_id
        # self.node_id = node_id

        self.handler = Handler(task_id)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        self.formatter = logging.Formatter(
            "[%(asctime)s] - %(levelname)s - TaskId: %(task_id)s - %(message)s"
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        log_dir = './logs'
        os.makedirs(log_dir, exist_ok=True)
        fh = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'userLog.log'),
            # maxBytes=10 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 添加控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    @classmethod
    def queryInstanceCnt(cls):
        return cls.ins_count

    def log(self, level, msg):
        frame = inspect.currentframe().f_back.f_back  # 获取调用日志方法的堆栈帧，向上回溯两层
        filename = inspect.getfile(frame)
        lineno = frame.f_lineno
        self.logger.log(level, f"{filename}:{lineno} - {msg}")

    def debug(self, msg):
        self.log(logging.DEBUG, msg)

    def info(self, msg):
        self.log(logging.INFO, msg)

    def warning(self, msg):
        self.log(logging.WARNING, msg)

    def error(self, msg):
        self.log(logging.ERROR, msg)

    def critical(self, msg):
        self.log(logging.CRITICAL, msg)

    def setTask(self, task_id):
        self.task_id = task_id
        self.handler.task_id = task_id

    def clearTask(self):
        self.handler.task_id = '无任务'

class Handler(logging.Handler):
    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

    def emit(self, record):
        try:
            record.task_id = self.task_id  # Add task_id to the record
            self.format(record)
        except Exception:
            self.handleError(record)