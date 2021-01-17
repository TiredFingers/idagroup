from django.shortcuts import render, reverse, redirect
from .models import ImgModel
from .forms import NewImageForm, ResizeImgForm
from io import BytesIO
from .utils import download_img
from django.core.files.base import ContentFile
from django.conf import settings
import os
from PIL import Image
from django.contrib import messages


def index(req):
    images = ImgModel.objects.all()

    return render(req, 'imageshaper/index.html', {'images': images})


def add_img(req):
    if req.method == 'POST':

        form = NewImageForm(req.POST, req.FILES)

        if form.is_valid():
            url = form.cleaned_data.get('url', '')
            img_file = form.cleaned_data.get('img_file', '')

            if len(url) > 0:

                img = None

                try:
                    img, imgname = download_img(url)
                except Exception:
                    messages.add_message(req, messages.ERROR, 'Не удалось загрузить изображение')
                    return render(req, 'imageshaper/add_img.html', {'form': form})
                else:
                    imgrow = ImgModel()

                    if img:
                        imgio = BytesIO()
                        img.save(imgio, img.format)
                        imgrow.fs_path.save(name=imgname, content=ContentFile(imgio.getvalue()), save=False)
                        imgrow.width = img.width
                        imgrow.height = img.height
                        imgrow.save()

                        return redirect(reverse('resize_view', args=([imgrow.pk])))
                    else:
                        messages.add_message(req, messages.ERROR, 'Не удалось загрузить изображение')
                        return render(req, 'imageshaper/add_img.html', {'form': form})
                finally:
                    if img:
                        img.close()

            else:
                imgrow = ImgModel.objects.create(fs_path=img_file)
                imgrow.save()

                return redirect(reverse('resize_view', args=([imgrow.pk])))

        else:
            form.full_clean()
            return render(req, 'imageshaper/add_img.html', {'form': form})

    form = NewImageForm()

    return render(req, 'imageshaper/add_img.html', {'form': form})


def do_resize(req):
    if req.method == 'POST':

        form = ResizeImgForm(req.POST)

        if form.is_valid():
            newsize = (form.cleaned_data.get('width', 0), form.cleaned_data.get('height', 0))
            img = ImgModel.objects.get(pk=int(form.cleaned_data.get('img_id')))

            if img:

                infile = os.path.join(settings.MEDIA_ROOT, str(img.fs_path))

                with Image.open(infile) as infileimg:

                    if newsize[0] == infileimg.width and newsize[1] == infileimg.height:
                        return redirect(reverse('resize_view', args=([img.pk])))

                    if newsize[0] != infileimg.width:
                        wf = newsize[0] / infileimg.width
                        newwidth = newsize[0]
                        newheight = infileimg.height * wf

                    elif newsize[1] != infileimg.height:
                        hf = newsize[1] / infileimg.height
                        newwidth = hf * infileimg.width
                        newheight = newsize[1]

                    resized = infileimg.resize((newwidth, newheight))

                    imgrow = ImgModel()
                    imgio = BytesIO()
                    resized.save(imgio, infileimg.format)

                    imgname = infileimg.filename.split('/')[-1]

                    imgrow.fs_path.save(name=imgname, content=ContentFile(imgio.getvalue()), save=False)
                    imgrow.width = resized.width
                    imgrow.height = resized.height
                    imgrow.save()
                    return redirect(reverse('resize_view', args=([imgrow.pk])))

            else:
                messages.add_message(req, messages.ERROR, 'Изображение не существует')
                return render(req, 'imageshaper/resize_img.html', {'form': form})

        else:
            return render(req, 'imageshaper/resize_img.html', {'form': form})


def resize_view(req, img_id=None):

    from PIL import Image

    if img_id is None:
        return redirect(reverse('add_img'))

    img = ImgModel.objects.get(pk=img_id)

    if img:

        with Image.open(os.path.join(settings.MEDIA_ROOT, str(img.fs_path))) as pilimg:
            form = ResizeImgForm({'width': pilimg.width, 'height': pilimg.height, 'img_id': img.pk})

        return render(req, 'imageshaper/resize_img.html', {'form': form, 'img': img})
    else:
        form = ResizeImgForm()
        return render(req, 'imageshaper/resize_img.html', {'form': form})
