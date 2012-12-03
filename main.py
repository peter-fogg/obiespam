#!/usr/bin/env python

import obiespam

messages = ["""Serbian kibo number key Bosnia Putin UMTS ISEC CBNRC national
information infrastructure Osama munitions Jyllandsposten Montenegro
doctrine Aldergrove""",
"""sweep data haven JUWTF Janet Reno Mena government $400 million in gold
bullion Glock radar Merlin Osama BROMURE John Kerry jihad threat
""", 
"""
Ft. Knox Rumsfeld BLU-97 A/B SHA CipherTAC-2000 dictionary United
Nations propaganda InfoSec AFSPC Bush Wired MDA bce clandestine SRI
"""]
obiespam.spam(messages, times=2, wait=4)
