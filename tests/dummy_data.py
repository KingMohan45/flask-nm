completed_tasks = []
incomplete_tasks = []
for i in range(1, 11):
    completed_tasks.append({
        'task': 'task' + str(i),
        'is_complete': True,
    })
    incomplete_tasks.append({
        'task': 'task' + str(10+i),
        'is_complete': False
    })