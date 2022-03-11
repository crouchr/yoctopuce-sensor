import platform

system = platform.system()
arch = platform.architecture()[0]
machine = platform.machine()

print(system)
print(arch)
print(machine)

