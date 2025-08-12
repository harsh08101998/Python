import base64


hh = '{\"event\":\"media\",\"stream_sid\":\"d449637026985e4791a92db2d148173h\",\"sequence_number\":\"20\",\"media\":{\"chunk\":\"19\",\"timestamp\":\"360\",\"payload\":\"sP+U/CT6RPjE90T4JPnk+tT8PP/MApwGvAdcBlwEbAMcBFwFXAXcA2QBFP4k++T4xPfE90T4pPlk+5T9xADcBBwH3AYcBdwD3ANcBdwFnASsAvD/tPwk+kT4xPfE9+T4ZPok/Nz+jALcBZwGXAXcA2wDnAQcBtwFXASsAaz+pPuk+UT4RPjk+OT5ZPt0/aQAXAQcBlwFnAOsAkwDHAWcBZwErAIAABT9pPpk+eT4JPkk+qT7NP2g/0wD3AXcBRwEbAJMApwDHAWcBAwDtADU/WT7pPnk+CT5JPpk+/T8HP9sApwFnAZcBWwDbAJMA5wE3ARMA0QBdP6k+6T5pPhE+CT5ZPrk+9T9xACcBJwGHAZcBOwCDAOcBFwFnASsAuD/9Pyk+iT5pPjk+OT5ZPvU/Cz/rALcBVwG3AQsA6wCnAM=\"}}'

coded_string=hh["payload"]
print(base64.b64decode(coded_string))
