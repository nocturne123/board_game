import arcade

SCREEN_TITLE = "Test Map"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

TILE_SCALING = 3


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera_sprites = None

        # A non-scrolling camera that can be used to draw GUI elements
        self.camera_gui = None

        # Keep track of the score
        self.score = 0

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Setup the Cameras
        self.camera_sprites = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "resources/tiled_maps/board_map.json"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep track of the score
        self.score = 0

        # Set up the player, specifically placing it at these coordinates.
        # src = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        # self.player_sprite = arcade.Sprite(src, CHARACTER_SCALING)
        # self.player_sprite.center_x = 128
        # self.player_sprite.center_y = 128
        # self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff
        # Create the 'physics engine'
        # self.physics_engine = arcade.PhysicsEnginePlatformer(
        #   self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        # )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Activate the game camera
        self.camera_sprites.use()

        # Draw our Scene
        # Note, if you a want pixelated look, add pixelated=True to the parameters
        self.scene.draw(pixelated=True)

        # Activate the GUI camera before drawing GUI elements
        self.camera_gui.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            start_x=10,
            start_y=10,
            color=arcade.csscolor.WHITE,
            font_size=18,
        )

    def on_resize(self, width, height):
        """Resize window"""
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
