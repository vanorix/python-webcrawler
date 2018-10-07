import xmlrpclib

stub = xmlrpclib.ServerProxy('http://localhost:3000/SOII')

print stub.getWork()