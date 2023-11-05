def main(app, player, source):
    item = app.inventory.get_item_slot("Blanket")[0].item
    if item.state["worn"]:
        app.current_map.light_range = app.current_map.defaults["light_range"]
    else:
        app.current_map.light_range = 2
    item.state["worn"] = not item.state["worn"]
