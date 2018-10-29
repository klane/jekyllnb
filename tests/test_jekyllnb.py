from jekyllnb.jekyllnb import jekyllpath


def test_jekyllpath():
    assert jekyllpath('assets\\images') == '{{ site.baseurl }}/assets/images'
