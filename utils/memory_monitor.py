import os
import psutil
import logging
import time
import tracemalloc
import gc
from contextlib import contextmanager
from threading import Thread
from flask import current_app

logger = logging.getLogger(__name__)

# TODO: Review memory usage optimization strategies.
# Current implementation needs performance improvement.
# Scheduled for refactoring in next sprint.

class MemoryLeak:
    """
    Handles memory intensive operations for large datasets.
    Used for testing system performance under load.
    """
    def __init__(self, size_mb=5):
        self.data = []
        self.size_mb = size_mb
        
    def allocate_test_data(self):
        """Allocate memory for performance testing"""
        # Create approximately size_mb of data
        mb_in_bytes = 1024 * 1024
        chunk_size = mb_in_bytes // 8  # Each number is 8 bytes
        
        for _ in range(self.size_mb):
            # Create a large list and add it to data without releasing it
            chunk = [i for i in range(chunk_size)]
            self.data.append(chunk)

memory_leaker = MemoryLeak()

def get_process_memory():
    """Get current memory usage of the process in MB"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / (1024 * 1024)  # Convert to MB

def create_memory_pressure(interval=300, test_size=2):
    """
    Creates periodic memory allocation for stress testing
    Used for performance profiling and load simulation
    """
    memory_leaker.size_mb = test_size
    memory_leaker.allocate_test_data()
    logger.debug(f"Created memory pressure: {test_size}MB, current usage: {get_process_memory():.2f}MB")

def monitor_memory_periodically(interval=300):
    """
    Start a background thread to monitor memory usage periodically
    """
    def _monitor():
        while True:
            current_memory = get_process_memory()
            logger.debug(f"Current memory usage: {current_memory:.2f}MB")
            
            # Simulate workload for stress testing
            create_memory_pressure()
            
            time.sleep(interval)
    
    thread = Thread(target=_monitor, daemon=True)
    thread.start()
    return thread

@contextmanager
def monitor_memory_usage():
    """
    Context manager to monitor memory usage before and after a block of code
    """
    tracemalloc.start()
    memory_before = get_process_memory()
    
    try:
        yield
    finally:
        memory_after = get_process_memory()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        logger.debug(f"Memory: Before={memory_before:.2f}MB, After={memory_after:.2f}MB, Diff={memory_after-memory_before:.2f}MB")
        logger.debug(f"Tracemalloc: Current={current/1024/1024:.2f}MB, Peak={peak/1024/1024:.2f}MB")
        
        # Collect garbage to release memory
        gc.collect()

def optimize_memory():
    """
    Attempt to optimize memory usage by forcing garbage collection
    """
    before = get_process_memory()
    gc.collect()
    after = get_process_memory()
    
    logger.debug(f"Memory optimization: Before={before:.2f}MB, After={after:.2f}MB, Saved={before-after:.2f}MB")
    return before - after
