# This makes init run only once
execute if entity @a unless data storage dp_conv:init {"init":true} run function converter_datapack:init
execute if entity @a run data merge storage dp_conv:init {"init":true}

# Handles giving credit sign
execute if data storage dp_conv:init {"sign":true} run give @a minecraft:oak_sign{BlockEntityTag:{Text1:'{"text":"Converted to","clickEvent":{"action":"run_command","value":"tellraw @a [\\"\\",{\\"text\\":\\"The datapack in this map was converted to command blocks using NICO_THE_PRO\'s commands-converter tool! You can learn more on how it works by clicking \\",\\"color\\":\\"green\\"},{\\"text\\":\\"-> here <-\\",\\"bold\\":true,\\"color\\":\\"dark_green\\",\\"clickEvent\\":{\\"action\\":\\"open_url\\",\\"value\\":\\"https://github.com/rotolonico/Commands-Converter\\"}}]"},"color":"green"}',Text2:'{"text":"commands by","color":"green"}',Text3:'{"text":"NICO_THE_PRO","color":"green"}',Text4:'{"text":"[Learn more]","bold":true,"color":"dark_green"}'},display:{Name:'{"text":"Epic Sign :D"}'}}
data merge storage dp_conv:init {"sign":false}
