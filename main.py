from crosshair import Crosshair
import json

def main():
    with open("config.json", "r") as f:
        config = json.loads(f.read())

    try:
        c = Crosshair(config["color"], (config["thickness"], config["length"], config["offset"]), config["set_pixel_fps"])
    except Exception as e:
        print("Missing {}. Using default settings.".format(e))
        c = Crosshair()

    c.create_crosshair_matrix()
    c.save_crosshair_png()
    c.draw_crosshair_pixels()

if __name__ == "__main__":
    main()
