from dataclasses import dataclass


@dataclass
class Item:
    name: str
    max_stack: int
    lore: str


# money
coin = Item(
    "Coin",
    64,
    """This small piece of a copper and gold alloy is the
official Pecunia currency.""",
)

# logs
oak_log = Item("Oak Log", 64, """The trunk of a tree called "Oak".""")
spruce_log = Item("Spruce Log", 64, """Christmas Tree""")
birch_log = Item("Birch Log", 64, """This is a white thing with black dots.""")

# raw ores
raw_iron = Item("Raw Iron", 64, """It's a useful pebble.""")
raw_gold = Item("Raw Gold", 64, """That is a really precious pebble.""")
raw_copper = Item(
    "Raw Copper",
    64,
    """Copper is far more useful than you think.
""",
)
raw_dark_steel = Item(
    "Raw Dark Steel",
    64,
    """It is not a regular pebble
at all.""",
)

# ingots
iron_ingot = Item(
    "Iron Ingot",
    64,
    """Iron is used in the manufacture of many
objects, it is most often drawn from the subsoil in the form of ore.""",
)
gold_ingot = Item(
    "Gold Ingot",
    64,
    """Gold is a precious metal.
It is rare and naturally has a golden yellow color.""",
)
copper_ingot = Item(
    "Copper Ingot",
    64,
    """Golden red metal,
very good conductor of electricity.""",
)
dark_steel_ingot = Item(
    "Dark Steel Ingot",
    64,
    """This weird gloomy ingot
is really hard...""",
)

# food

apple = Item("Apple", 64, """Common red fruit which is juicy and sweet.""")
bread = Item("Bread", 64, """Bread is pain. La douleur est le pain.""")
carrot = Item("Carrot", 64, """Orange treasure.""")

# potatoes
potato = Item("Potato", 64, """Solanum tuberosum bonum est.""")
jacket_potato = Item("Jacket Potato", 64, """or Baked Potato...""")
poisonous_potato = Item(
    "Poisonous Potato",
    64,
    """Eating poisonous things
is not quite good for health""",
)

# berries
blueberry = Item("Blue Berry", 64, """Blue and juicy.""")
purpleberry = Item(
    "Purple Berry",
    64,
    """Açai Berries ? Black Currants ? Blackberries ? Elderberries ?
Gooseberries ? Huckleberries ? Jamun Berries ? Luma Berries ? Maqui Berries ?
Mulberries ? Olallieberries ? Riberries ? Salal Berries ? Serviceberries ?
Sherbet Berries ?""",
)
redberry = Item("Red Berry", 64, """Red and sweet.""")

# meats

# chicken
chicken = Item(
    "Raw Chicken",
    64,
    """Do not eat this raw meat, it could be
poisonous.""",
)
cooked_chicken = Item(
    "Raw Chicken",
    64,
    """Cooked chicken is more nutritious
and tastes better than raw chicken.""",
)

# beef
beef = Item("Raw Beef", 64, """Cow cruelly eliminated in an atrocious way.""")
steak = Item("Steak", 64, """Cow cooked mercilessly in fiery flames.""")

# mutton
mutton = Item("Raw Mutton", 64, """Dead Sheep""")
cooked_mutton = Item("Cooked Mutton", 64, """Heated Dead Sheep""")

# fish
fish = Item("Raw Fish", 64, """Aquatic Steak.""")
cooked_fish = Item("Cooked Fish", 64, """Cooked Aquatic Steak.""")
