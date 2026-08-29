import logging

class TaskHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def process(self, tasks):
        # Handle edge case: no tasks or invalid type
        if not tasks:
            self.logger.warning("No tasks provided")
            return []

        if not isinstance(tasks, list):
            self.logger.error("Tasks must be a list")
            return []

        results = []

        for i, task in enumerate(tasks):
            try:
                if not isinstance(task, dict):
                    raise TypeError("Each task must be a dictionary")
                action = task.get("action")
                if not action:
                    raise ValueError("Task must have an action")
                if action == "divide":
                    a = task.get("a")
                    b = task.get("b")
                    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                        raise ValueError("Operands must be numbers")
                    if b == 0:
                        raise ZeroDivisionError("Division by zero edge case")
                    res = a / b
                elif action == "concat":
                    s1 = task.get("s1", "")
                    s2 = task.get("s2", "")
                    if not isinstance(s1, str) or not isinstance(s2, str):
                        raise ValueError("Strings required for concat")
                    res = s1 + s2
                else:
                    raise ValueError(f"Unknown action: {action}")
                results.append({"task": task, "result": res, "status": "ok"})
            except (ValueError, ZeroDivisionError, TypeError) as e:
                self.logger.error(f"Error in task {i}: {e}")
                results.append({"task": task, "error": str(e), "status": "error"})
            except Exception as e:
                self.logger.error(f"Unexpected error in task {i}: {e}")
                results.append({"task": task, "error": str(e), "status": "error"})
        return results

if __name__ == "__main__":
    h = TaskHandler()
    tasks = [
        {"action": "divide", "a": 10, "b": 2},
        {"action": "divide", "a": 5, "b": 0},
        {"action": "divide", "a": "x", "b": 2},
        {"action": "concat", "s1": "hello", "s2": " world"},
        {"action": "concat", "s1": 123, "s2": "test"},
        {"action": "foo"},
        {},
        None,
    ]
    print(h.process(tasks))