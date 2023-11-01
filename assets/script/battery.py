def main(app, player, source):
    from assets import load_asset

    flashlight = app.inventory.get_item_slot("Flashlight")[0]

    if flashlight is None:
        app.clear_alerts()
        load_asset("script", "cannot_use.py", app=app, player=player, source="battery")
        return False
    else:
        if flashlight.item.state["charge"] == 0:
            flashlight.item.state["charge"] = flashlight.item.state["max_charge"]
            app.clear_alerts()
            app.current_scenes.append(load_asset("scene", "battery_use.scn", app=app))
            return True
        else:
            app.clear_alerts()
            app.current_scenes.append(
                load_asset("scene", "battery_no_use.scn", app=app)
            )
            return False
