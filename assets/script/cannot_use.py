def main(app, player, source):
    import scriptable

    app.current_scenes.append(
        scriptable.Scriptable(
            [
                "WHITE TRANSPARENT -n ALERT",
                "print 'I dont see how I can use this.' -l 400x400",
                "pause 60",
            ],
            app,
            False,
        )
    )

    return False
