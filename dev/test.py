def unique(arr: list):
    for i in range(len(arr) - 1):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return False
    return True


unique([{"type":"equipment", "data": "test"}, {"data": "test", "type": "equipment"}])
pass
