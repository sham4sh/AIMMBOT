from UserCSVData import UserCSVDataAccess
from algorithms.primaryAlgorithm import PrimaryAlgorithm
x = UserCSVDataAccess()
x.addFav('a','1231587',5)
x.addFav('a','1007028',4)
x.addFav('a','357413',3)
x.addFav('b','316654',5)
x.addFav('b','78346',3)
x.addFav('b','86893',4)
x.addFav('b','81573',4)
x.addFav('b','100758',4)

testing = PrimaryAlgorithm()
print(testing.get_top_n('a',10))
print(testing.get_top_n('b',10))

