import os

from cl_tasks.storage.file_store import FileTaskStore
# from taskcli.storage.cosmos_store import CosmosTaskStore  # later

def get_store():
    use_cosmos = os.getenv("USE_COSMOS", "false").lower() == "true"
    if use_cosmos:
        from cl_tasks.storage.cosmos_store import CosmosTaskStore
        return CosmosTaskStore()
    return FileTaskStore()