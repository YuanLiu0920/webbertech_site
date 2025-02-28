from secedgar.cik_lookup import CIKLookup
import json
lookups = CIKLookup(['aapl', 'msft', 'Facebook','Berkshire Hathaway', 'Bridgewater Associates', 'Renaissance Technologies', 'UBS Group AG' ],
                    user_agent="Name (email)")

print(lookups.__dict__)