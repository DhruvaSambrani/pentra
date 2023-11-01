def pause(time, clock):
    for i in range(time):
        clock.tick(30)


def get_scene_id(name, app):
    return next(
        (idx for idx, scene in enumerate(app.current_scenes) if scene.name == name),
        -1,
    )


def clear_alerts(app):
    app.current_scenes = list(
        filter(lambda scene: scene.name != "ALERT", app.current_scenes)
    )
