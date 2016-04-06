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
if (typeof RedactorObject === 'undefined') var RedactorObject = {};

RedactorPlugins.filebrowser = {
    init: function()
    {
        this.addBtn('browser', 'File Browser', $.proxy(this.activeBrowser, this));
    },
    activeBrowser: function(){
        var win = window.open(
            '/admin/filebrowser/browse/?pop=4&Redactor='+this.$el.attr('id'),
            'File Browser',
            'height=600,width=960,resizable=yes,scrollbars=yes'
        );

        RedactorObject = this;
    }
};

if(window.opener){
    window.onload = function() {

        $('button[name="redactor-select"]').on('click', $.proxy(function(e){

            var target = $(e.target);
            var tag;

            if(target.data('type')){
                if(target.data('type') == 'Image'){
                    tag = '<img src="'+target.data('file')+'">';
                    this.insertHtml(tag);
                    window.close();
                } else if(target.data('type') == 'Document'){
                    tag = '<a href="'+target.data('File')+'">'+target.data('type')+'</a>';
                    this.insertHtml(tag);
                    window.close();
                }
            }
        }, window.opener.RedactorObject));

    };
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
