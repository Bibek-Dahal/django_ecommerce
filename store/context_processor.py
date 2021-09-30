from.models import Catagory
def get_all_catagories(self):
    catagories = Catagory.objects.all()
    return {'catagories':catagories}
