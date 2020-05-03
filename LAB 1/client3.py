import Pyro4

num = input("Input an integer: ").strip()
res_maker = Pyro4.Proxy("PYRONAME:example.result")
print(res_maker.get_result(num))
