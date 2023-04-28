import os

from datetime import datetime

from moviepy import editor


class ImageConcatenator:
    def __init__(self, image_dir: str, duration: float, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

        self.image_dir = image_dir
        self.duration = duration

    def get_images_between_dates(self):
        images = [f for f in os.listdir(self.image_dir) if f[-4:] == ".png"]

        image_clips = []

        for image in images:
            im_date = datetime.strptime(image[:10], "%Y-%m-%d")

            if self.end_date >= im_date >= self.start_date:
                image_clips.append(editor.ImageClip(f"{self.image_dir}/{image}").set_duration(self.duration))

        return image_clips

    def compile(self, filepath):
        image_clips = self.get_images_between_dates()
        video = editor.concatenate(image_clips, method="compose")
        video.write_videofile(filepath, fps=60)


def main():
    duration = float(input("Enter each clip's duration: "))
    start_date_str = input("Enter the start date in the format MM-DD-YYYY: ")
    end_date_str = input("Enter the end date in the format MM-DD-YYYY: ")

    start_date = datetime.strptime(start_date_str, "%m-%d-%Y")
    end_date = datetime.strptime(end_date_str, "%m-%d-%Y")

    ic = ImageConcatenator(
        f"{os.getenv('APPDATA')}/.minecraft/screenshots",
        duration, start_date, end_date
    )

    ic.compile("output.mp4")


if __name__ == "__main__":
    main()
