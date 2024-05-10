import pytest
from adaptivecard.types import Backgroundimage
from adaptivecard.exceptions import *


class Test:
    def test_background_image(self):
        url = "https://images.ctfassets.net/sfnkq8lmu5d7/4Ma58uke8SXDQLWYefWiIt/3f1945422ea07ea6520c7aae39180101/2021-11-24_Singleton_Puppy_Syndrome_One_Puppy_Litter.jpg?w=1000&h=750&fl=progressive&q=70&fm=jpg"
        bg_image = Backgroundimage(url=url)
        with pytest.raises(ValueCheckError):
            bg_image.fill_mode = "covre"
        bg_image.fill_mode = "cover"
        bg_image.horizontal_alignment = "center"
        bg_image.to_dict()
