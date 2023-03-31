import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import asyncio
from server_start import main
asyncio.run(main())
