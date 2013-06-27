/**
 *
 *    $$\      $$\$$$$$$$$\$$$$$$$\  $$$$$$\ $$\   $$\$$$$$$$\ $$\      $$$$$$\$$\      $$\$$$$$$$$\
 *    $$ | $\  $$ $$  _____$$  __$$\$$  __$$\$$ |  $$ $$  __$$\$$ |     \_$$  _$$$\    $$$ $$  _____|
 *    $$ |$$$\ $$ $$ |     $$ |  $$ $$ /  \__$$ |  $$ $$ |  $$ $$ |       $$ | $$$$\  $$$$ $$ |
 *    $$ $$ $$\$$ $$$$$\   $$$$$$$\ \$$$$$$\ $$ |  $$ $$$$$$$\ $$ |       $$ | $$\$$\$$ $$ $$$$$\
 *    $$$$  _$$$$ $$  __|  $$  __$$\ \____$$\$$ |  $$ $$  __$$\$$ |       $$ | $$ \$$$  $$ $$  __|
 *    $$$  / \$$$ $$ |     $$ |  $$ $$\   $$ $$ |  $$ $$ |  $$ $$ |       $$ | $$ |\$  /$$ $$ |
 *    $$  /   \$$ $$$$$$$$\$$$$$$$  \$$$$$$  \$$$$$$  $$$$$$$  $$$$$$$$\$$$$$$\$$ | \_/ $$ $$$$$$$$\
 *    \__/     \__\________\_______/ \______/ \______/\_______/\________\______\__|     \__\________|
 *
 *
 *    -----------------------------------------------------------------------------------------------
 *
 *    @author: websublime.com
 *    @version: 1.0
 *    @description: Redactor suit editor.
 */
if (typeof RedactorPlugins === 'undefined') var RedactorPlugins = {};

RedactorPlugins.filebrowser = {
    init: function()
    {
        console.log(this);

        this.addBtn('browser', 'File Browser', $.proxy(this.activeBrowser, this));
    },
    activeBrowser: function(){
        FileBrowser.show(this.$el.attr('id'), '/admin/filebrowser/browse?pop=4&Redactor='+this.$el.attr('id'),
            $.proxy(this.observerPop, this));
    },
    observerPop: function(ev){
        var tag;

        if(this.$el.attr('type') == "Image"){
            tag = '<img src="'+this.$el.attr('file')+'">';
            this.insertHtml(tag);
        } else {
            tag = '<a href="'+this.$el.attr('file')+'">'+this.$el.attr('type')+'</a>';
            this.insertHtml(tag);
        }
    }
};

function SuitSubmit(FileURL, ThumbURL, FileType) {
    var data = {
        'file': FileURL,
        'thumb': ThumbURL,
        'type': FileType
    };

    var id = "#"+GetURLParameter('Redactor');

    $(id, opener.window.document).attr('file', FileURL);
    $(id, opener.window.document).attr('thumb', ThumbURL);
    $(id, opener.window.document).attr('type', FileType);
    //window.opener.$(id).attr('file', FileURL);
    //window.opener.RedactorPlugins.filebrowser.data = data;
    this.close();
}

function GetURLParameter(sParam){
    var sPageURL = window.location.search.substring(1);

    var sURLVariables = sPageURL.split('&');

    var parameter;

    for (var i = 0; i < sURLVariables.length; i++){
        var sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] == sParam){
            parameter = sParameterName[1];
            break;
        }
    }

    return parameter;
}
