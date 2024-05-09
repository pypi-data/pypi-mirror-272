import os
from typing import List

from faster_whisper import WhisperModel
from pytube import YouTube


def youtube_url_to_mp3(video_url: str):
    """
    Youtube Url to mp3

    args:
        video_url(str): Youtube video url of the model to transcibe

    """
    # url input from user
    yt = YouTube(str(video_url))

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # check for destination to save file
    destination = "."

    # download the file
    out_file = video.download(output_path=destination)

    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)

    # result of success
    print(yt.title + " has been successfully downloaded.")

    # Print the name of the file
    print(new_file)
    return new_file


def run_whisper(mp3: str):
    # Run on GPU with FP16
    model = WhisperModel(
        "large-v3", device="cpu", compute_type="int8"
    )

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(mp3, beam_size=5)

    print(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )

    for segment in segments:
        print(
            f"[{segment.start:.2f}s -> {segment.end:.2f}s]"
            f" {segment.text}"
        )

    return segments, info


def youtube_urls_to_text(
    urls: List[str],
):
    """
    Converts YouTube video URLs to text captions and saves them to a file.

    Args:
        urls (List[str]): A list of YouTube video URLs.
        new_file_name (str, optional): The name of the file to save the captions to. Defaults to "captions.txt".

    Returns:
        str: The name of the file where the captions are saved.
    """
    for url in urls:
        mp3 = youtube_url_to_mp3(url)
        new_file_name = f"{url}.txt"

        # Get the captions from the mp3
        segments, info = run_whisper(mp3)

        # Write the captions to a file
        with open(new_file_name, "w") as f:
            for segment in segments:
                f.write(
                    f"[{segment.start:.2f}s -> {segment.end:.2f}s]"
                    f" {segment.text}\n"
                )

        # Remove the mp3 file
        os.remove(mp3)

    return new_file_name
