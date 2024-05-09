import inspect

try:
    from PIL import Image
except ImportError as exc:
    raise ImportError(
        "Missing dependencies for computer vision:\n"
        "To install run:\n\n"
        "  pip install 'dvcx[cv]'\n"
    ) from exc

from dvcx.lib.file import File


class ImageFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._image = None

    def open(self):
        with File.open(self) as fd:
            self._image = Image.open(fd)
            self._image.load()
        return self._image

    def close(self):
        if self._image:
            self._image.close()

    def get_value(
        self,
        mode="RGB",
        size=None,
        transform=None,
        unsqueeze=True,
        open_clip_model=None,
    ):
        if self._image is None:
            self.open()

        img = self._image

        if mode:
            img = img.convert(mode)
        if size:
            img = img.resize(size)
        if transform:
            img = transform(img)
            if unsqueeze:
                img = img.unsqueeze(0)
        if open_clip_model:
            method_name = "encode_image"
            if not (
                hasattr(open_clip_model, method_name)
                and inspect.ismethod(getattr(open_clip_model, method_name))
            ):
                raise ValueError(
                    f"Unable to render Image: 'open_clip_model' doesn't support"
                    f" '{method_name}()'"
                )
            img = open_clip_model.encode_image(img)
        return img
