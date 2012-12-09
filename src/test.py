import pyratemp

t = pyratemp.Template("Hello @!name!@. Age @!max(a1,a2)+a3!@")
#print t(({name="ho", a1=5, a2=2, a3=3})
print t(**{"name":"ho", "a1" : 5, "a2" : 2, "a3" : 3})
import difflib

k=' here val1 here val2 '
k2= 'here @!v1!@ here @!v2!@'
s =difflib.SequenceMatcher(lambda x: x==" ",k, k2)


