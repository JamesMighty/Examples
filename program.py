from nodeThree import Three
import resolver

while True:
    inp = input("> ")
    todo = resolver.Resolve(Three, inp=inp, allResolvedMatches=[], lastMatch=0, doPrintUnresolved=True)[0]
    #print(todo)
    outp = resolver.Do(todo,inp)
    print(outp)
    


# Zkus do konzole napsat neco jako: Ahoj, jak se mas? nebo Ahoj, kolik je hodin?