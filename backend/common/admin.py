from django.db.models.fields.files import ImageFieldFile


def header_with_image(
    title: str, subtitle: str = "", image: ImageFieldFile | None = None
) -> list[object]:
    """Значение для @display(header=True) в Unfold: заголовок, подзаголовок и превью картинки."""
    initials = "".join(word[0] for word in title.split()[:2]).upper()
    picture = {"path": image.url, "width": 48, "height": 48, "squared": True} if image else None
    return [title, subtitle, initials, picture]
