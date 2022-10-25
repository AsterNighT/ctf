from pyads import ADS
file = "droste.jpg"
handler = ADS(file)
if handler.has_streams():
    for stream in handler:
        print(stream)

print(handler.get_stream_content("Zone.Identifier"))
