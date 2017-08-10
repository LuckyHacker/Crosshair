from crosshair import Crosshair
import json
import threading

def reload_crosshair(c = None):
    if c:
        c.allow_draw = False

    with open("config.json", "r") as f:
        config = json.loads(f.read())

    try:
        c = Crosshair(config["color"], (config["thickness"], config["length"], config["offset"]), config["set_pixel_fps"])
    except Exception as e:
        print("Missing {}. Using default settings.".format(e))
        c = Crosshair()

    c.create_crosshair_matrix()
    c.save_crosshair_png()
    c_thread = threading.Thread(target=c.draw_crosshair_pixels)
    c_thread.daemon = True
    c_thread.start()
    return c


def update_config(key, value):
    with open("config.json", "r") as f:
        config = json.loads(f.read())

    if key == "color":
        config[key] = value
    else:
        config[key] = int(value)


    with open("config.json", "w") as f:
        f.write(json.dumps(config))

def main():
    c = reload_crosshair()
    commands = ["thickness", "length", "offset", "color", "set_pixel_fps"]
    command = ""
    while command != "exit":
        command = input("crosshair> ")

        try:
            key, value = command.split(" ")
            if key in commands:
                update_config(key, value)
        except:
            if command not in ("exit", ""):
                print("Invalid command")

        c = reload_crosshair(c)

if __name__ == "__main__":
    main()
