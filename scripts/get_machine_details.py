import platform

system = platform.system()
arch = platform.architecture()[0]
machine = platform.machine()

print(f'system={system}')
print(f'arch={arch}')
print(f'machine={machine}')


