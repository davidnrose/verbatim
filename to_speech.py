import torch
# import TTS

# def generate_audio(text="This is the opening paragraph of an academic article turned into a podcast"):
#     tts = TTS.model_name("tts_models/en/ljspeech/fast_pitch")
#     tts.tts_to_file(text=text, file_path="./output/audio_1.wav")


### --- ChatTTS --- ###
import ChatTTS
import torchaudio
import torch
from IPython.display import Audio
import ffmpeg

chat = ChatTTS.Chat()
chat.load(source="huggingface", compile=False)

text_input = [r"This article describes an emergent logic of accumulation in the networked sphere, ‘surveillance capitalism,’ and considers its implications for ‘information civilization.’ The institutionalizing practices and operational assumptions of Google Inc. are the primary lens for this analysis as they are rendered in two recent articles authored by Google Chief Economist Hal Varian. Varian asserts four uses that follow from computer-mediated transactions: ‘data extraction and analysis,’ ‘new contractual forms due to better monitor ing,’ ‘personalization and customization,’ and ‘continuous experiments.’ An examination of the nature and consequences of these uses sheds light on the implicit logic of surveillance capitalism and the global architecture of computer mediation upon which it depends. This architecture produces a distributed and largely uncontested new expression of power that I christen: ‘Big Other.’ It is constituted by unexpected and often illegible mechanisms of extraction, commodification, and control that effectively exile persons from their own behavior while producing new markets of behavioral prediction and modification. Surveil lance capitalism challenges democratic norms and departs in key ways from the centuries long evolution of market capitalism.",]

# torchaudio.utils.ffmpeg_utils.get_audio_encoders()

print(torchaudio.list_audio_backends())

audio_array = chat.infer(text_input,)
filepath_save = r"C:\Users\mosel\PycharmProjects\article_labelling\some_output.wav"
torchaudio.save(filepath_save, torch.from_numpy(audio_array), 24000, format="wav")

Audio(audio_array[0], rate=24_000, autoplay=True)