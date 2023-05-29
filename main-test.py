from src.image_handler import image_compression, image_reading

if __name__ == "__main__":
    image_compression(
        image_reading("data/A2.png"), use_genetic_algorithm=True, debug=True
    )
