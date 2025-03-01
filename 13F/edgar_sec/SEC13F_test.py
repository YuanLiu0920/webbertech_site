from SEC13F import SEC13F

"""
TODO Please check proper way of python unit test, just a stub here.
"""
c = SEC13F()

# Bridgewater Associates, '1350694'
# Berkshire Hathaway, '1067983'
# Renaissance Technologies, '1037389'
# UBS Group AG, '1610520'
c.find_common_holdings_multi_cik(['1350694', '1067983', '1037389', '1610520'])