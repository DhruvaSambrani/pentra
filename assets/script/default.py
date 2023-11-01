def main(app, player, source):
    import scriptable

    app.current_scenes.append(
        scriptable.Scriptable(
            [
                "WHITE TRANSPARENT -n ALERT",
                "print 'TF you want me to do with this item bro?' -l 400x400",
                "pause 60",
            ],
            app,
            False,
        )
    )
