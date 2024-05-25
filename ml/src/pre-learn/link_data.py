import os
import glob

def make_dataset(studies_folder, masks_folder):
    """Создает набор данных, который связывает КТ-снимки и их маски.

    Аргументы:
        `studies_folder`: путь к папке, содержащей КТ-снимки.
        `masks_folder`: путь к папке, содержащей маски.

    Возвращает:
        Список кортежей, где каждый кортеж содержит путь к КТ-снимку и путь
        к его соответствующей маске.
    """

    # Получаем список всех КТ-снимков.
    studies_paths = glob.glob(os.path.join(studies_folder, "*.nii.gz"))

    # Создаем список для хранения связанных путей КТ-снимка и масок.
    linked_paths = []

    # Перебираем КТ-снимки.
    for study_path in studies_paths:

        # Получаем имя файла КТ-снимка.
        study_filename = os.path.basename(study_path)

        # Получаем соответствующее имя файла маски.
        fname = study_filename.split(".")
        fname[0] += "_mask"
        mask_filename = ".".join(fname)
        mask_path = os.path.join(masks_folder, mask_filename)

        # Проверяем, существует ли файл маски.
        if os.path.exists(mask_path):
            # Добавляем пути КТ-снимка и маски в список связанных путей.
            linked_paths.append((study_path, mask_path))
        else:
            linked_paths.append((study_path, None))

    return linked_paths

def get_existing():
    # Получаем пути к папкам с исследованиями и масками.
    masks_folder = "data/masks/"
    linked_paths = []
    for i in range(5):
        studies_folder = f"data/studies/CT-{i}"
        # Создаем набор данных.
        linked_paths.append(make_dataset(studies_folder, masks_folder))

    # Печатаем длину набора данных.
    existing = []
    for paths in linked_paths[1]:
        if paths[1]:
            existing.append(paths)
    
    return existing

if __name__ == "__main__":
    # Получаем пути к папкам с исследованиями и масками.
    masks_folder = "data/masks/"
    linked_paths = []
    for i in range(5):
        studies_folder = f"data/studies/CT-{i}"
        # Создаем набор данных.
        linked_paths.append(make_dataset(studies_folder, masks_folder))

    # Печатаем длину набора данных.
    for paths in linked_paths[1]:
        if paths[1]:
            print(paths)
    for i in range(5):
        print(f"CT-{i} содержит {sum([1 if a[1] is not None else 0 for a in linked_paths[i]])} связанных пар КТ-снимков и масок.")
        print(f"CT-{i} содержит {sum([0 if a[1] is not None else 1 for a in linked_paths[i]])} КТ-снимков без маски.")
