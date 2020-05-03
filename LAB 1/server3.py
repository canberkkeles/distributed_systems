import Pyro4
import random


@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        return "Hello, {arg1}. Today’s lucky number is: {arg2}.".format(arg1=name, arg2=random.randint(0, 10 ** 6))

@Pyro4.expose
class ResultMaker(object):
    def get_result(self,number):

        p = 82774018375762036230659850750851711854039699313175216914470363560945323457727
        a0 = 26748908084769669758664722731140522800875206292361297608046702271758631669759
        a1 = 59489944712712493230446426050522902095714591665803937192613571374709152682872
        a2 = 71257019652372732006624209284281187993740077445682918560838974809666187201576
        a3 = 55315635592811832356973556884353215645720087042315880077665613542569819620485
        a4 = 20411929856341763513465955098957309007252776763418101366798367886225234827183

        number = int(number)

        return str((a0 + number * a1 + number ** 2 * a2 + number ** 3 + a3 + number ** 4 * a4) % p)


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

uri = daemon.register(ResultMaker)
ns.register("example.result", uri)

print('ready')
daemon.requestLoop()
