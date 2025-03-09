from SEC13F import SEC13F

"""
TODO Please check proper way of python unit test, just a stub here.
"""
c = SEC13F()

companies = ['BHLB','Apple Inc.','UBS','META','COST',"AMERICAN EXPRESS CO","ABBOTT LABORATORIES "]
for company in companies:
    print(c.cik_lookup(company))

