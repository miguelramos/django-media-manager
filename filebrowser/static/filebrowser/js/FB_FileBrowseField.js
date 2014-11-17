function FileSubmit(FileURL, ThumbURL, FileType) {
    
    // var input_id=window.name.split("___").join(".");
    var input_id=window.name.replace(/____/g,'-').split("___").join(".");
    var preview_id = 'preview_' + input_id;
    var previewimage_id = 'previewimage_' + input_id;
    var link_id = 'previewlink_' + input_id;
    var errorList;
    // ignore help
    // var help_id = 'help_' + input_id;
    console.log('input_id: ' + input_id);
    input = opener.document.getElementById(input_id);
    preview = opener.document.getElementById(preview_id);
    previewImage = opener.document.getElementById(previewimage_id);
    link = opener.document.getElementById(link_id);
    // help = opener.document.getElementById(help_id);
    // set new value for input field
    input.value = FileURL;
    
    if (ThumbURL && FileType != "") {
        // selected file is an image and thumbnail is available:
        // display the preview-image (thumbnail)
        // link the preview-image to the original image
        if (link) {
            link.setAttribute("href", FileURL);
            link.setAttribute("target", "_blank");
        }
        if (preview) {
            preview.style.display = 'block';
        }
        if (previewImage) {
            previewImage.setAttribute("src", ThumbURL);
        }
        // clear out any errors.
        errorList = preview.parentNode.querySelector('.errorlist');
        if (errorList) {
            errorList.style.display = 'none';
        }
        // help.setAttribute("style", "display:block");
    } else {
        // hide preview elements
        if (link) {
            link.setAttribute("href", "");
            link.setAttribute("target", "");
        }
        if (preview) {
            preview.style.display = 'none';
        }
        if (previewImage) {
            previewImage.setAttribute("src", "");
        }
        // help.setAttribute("style", "display:none");
    }
    this.close();
}

