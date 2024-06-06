from pprint import pprint

from ultralytics import YOLO, settings


pprint(settings)
# settings.update({"datasets_dir": "C:\\back up\\DeepL_om\\ml\\data"})
# settings.update({"runs_dir": "C:\\back up\\DeepL_om\\ml\\runs"})
# pprint(settings)


# model = YOLO("weights/v8medium_50epoch.pt")


# # Evaluate the model (obtain predictions)
# results = model.val(save_txt=True, save_conf=False, save_crop=False)

# # Loop through predictions and calculate Dice scores
# pprint(results)