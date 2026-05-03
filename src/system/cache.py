import json
import os


class PathCache:
    def __init__(self, file_path=None):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        default_path = os.path.join(project_root, "output", "path_cache.json")

        self.file_path = file_path or default_path
        self.storage = {}
        self.disk_storage = self._load_disk_storage()

    def _key_to_string(self, key):
        return ",".join(str(value) for value in key)

    def _load_disk_storage(self):
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_disk_storage(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as file:
            json.dump(self.disk_storage, file, indent=2)

    def has(self, key):
        key_string = self._key_to_string(key)
        return key in self.storage or key_string in self.disk_storage

    def get(self, key, grid=None):
        if key in self.storage:
            return self.storage[key]

        if grid is None:
            return None

        key_string = self._key_to_string(key)
        positions = self.disk_storage.get(key_string)
        if not positions:
            return None

        path = []
        for x, y in positions:
            if not grid.in_bounds(x, y):
                return None
            path.append(grid.get_node(x, y))

        self.storage[key] = path
        return path

    def set(self, key, path):
        self.storage[key] = path
        self.disk_storage[self._key_to_string(key)] = [
            [node.x, node.y]
            for node in path
        ]
        self._save_disk_storage()

    def clear(self):
        self.storage.clear()

    def clear_all(self):
        self.storage.clear()
        self.disk_storage.clear()
        self._save_disk_storage()