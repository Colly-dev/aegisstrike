"""
AegisStrike - Task Manager
Manages concurrent tasks, thread pools, and task scheduling.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any

class TaskManager:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers

    def run_tasks(self, func: Callable, items: List[Any], *args) -> List[Any]:
        """Run a function concurrently over a list of items."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(func, item, *args): item for item in items}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    pass
        return results
