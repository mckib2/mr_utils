'''PMU_Type enum.'''

PMU_Type = dict()
# PMU_Type = {
#     'END': 0x01FF0000,
# 	'ECG1': 0x01010000,
# 	'ECG2': 0x01020000,
# 	'ECG3': 0x01030000,
# 	'ECG4': 0x01040000,
# 	'PULS': 0x01050000,
# 	'RESP': 0x01060000,
# 	'EXT1': 0x01070000,
# 	'EXT2': 0x01080000
# }

PMU_Type_inverse = {v: k for k, v in PMU_Type.items()}
