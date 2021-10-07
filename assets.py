import os

def _asset(asset_name: str, pardir:str="", relative:bool=False) -> str:
    if pardir:
        asset_name = f"{pardir}/{asset_name}"

    asset_name = f"assets/{asset_name}"

    if relative:
        asset_name = os.path.abspath(asset_name)

    return asset_name

def construct_background_filename(colour: str, w: int, h: int, relative:bool=False):
    return _asset("{}x{}-{}-solid-color-background.jpg".format \
            (w, h, "-".join(colour.strip().split())),pardir="backgrounds", relative=relative)

class Assets:

    image_icon = _asset("image.png")
    logo = _asset("logo.png")
    background = _asset("brass.jpg")