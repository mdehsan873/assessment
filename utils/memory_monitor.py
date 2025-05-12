import os
import psutil
import logging
import time
import tracemalloc
import gc
from contextlib import contextmanager
from flask import current_app

logger = logging.getLogger(__name__)

def get_process_memory():
    """Get current memory usage of the process in MB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert to MB

@contextmanager
def monitor_memory_usage():
    """
    Context manager to monitor memory usage before and after a block of code
    """
    # Start tracking memory usage
    memory_before = get_process_memory()
    
    try:
        yield
    finally:
        memory_after = get_process_memory()
        
        logger.debug(f"Memory: Before={memory_before:.2f}MB, After={memory_after:.2f}MB, Diff={memory_after-memory_before:.2f}MB")
        
        # Collect garbage to release memory
        gc.collect()

def optimize_memory():
    """
    Optimize memory usage by forcing garbage collection
    """
    before = get_process_memory()
    gc.collect()
    after = get_process_memory()
    
    logger.debug(f"Memory optimization: Before={before:.2f}MB, After={after:.2f}MB, Saved={before-after:.2f}MB")
    return before - after
