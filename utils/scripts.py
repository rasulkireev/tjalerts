from tqdm import tqdm

from jobs.models import Technology, TechnologyMapping
from utils.constants import HIRABLE_TECH_LIST_MAPPING

with tqdm(total=len(HIRABLE_TECH_LIST_MAPPING)) as pbar:
    for pair in HIRABLE_TECH_LIST_MAPPING:
        tqdm.write(f"{pair}")

        try:
            parent = Technology.objects.get(id=pair[0])
            child = Technology.objects.get(id=pair[1])
            TechnologyMapping.objects.get_or_create(parent=parent, child=child)
        except Technology.DoesNotExist:
            pass

        pbar.update(1)
