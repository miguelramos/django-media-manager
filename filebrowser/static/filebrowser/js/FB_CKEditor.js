function ProtectPath(path) {
    path = path.replace( /\\/g,'\\\\');
    path = path.replace( /'/g,'\\\'');
    return path ;
}

function gup( name ) {
  var url = encodeURI(window.location.href);
  url = url.replace(/&amp;/g, '&');
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(url);
  if(results == null)
    return "";
  else
    return results[1];
}

function OpenFile(fileUrl) {
    var CKEditorFuncNum = gup('CKEditorFuncNum');
    window.top.opener.CKEDITOR.tools.callFunction(CKEditorFuncNum,encodeURI(fileUrl).replace('#','%23'));
    window.top.close();
    window.top.opener.focus();
}

if (CKEDITOR) {
    CKEDITOR.config.filebrowserBrowseUrl = '/admin/filebrowser/browse?pop=3';
}

