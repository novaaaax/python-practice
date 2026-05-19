import simpy

completed_tasks = []
def task(env, ID, duration):
    yield env.timeout(duration)
    completed_tasks.append(ID)

fiber_count = int(input("Enter the number of fibers: "))

task_1 = fiber_count * 2

env = simpy.Environment()
env.process(task(env, 'Task 1', 5))
env.process(task(env, 'Task 2', 3))
env.run()
print("Completed tasks:", completed_tasks)
